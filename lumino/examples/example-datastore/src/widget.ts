// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/*-----------------------------------------------------------------------------
| Copyright (c) 2019, PhosphorJS Contributors
|
| Distributed under the terms of the BSD 3-Clause License.
|
| The full license is in the file LICENSE, distributed with this software.
|----------------------------------------------------------------------------*/
import { JSONExt, JSONObject } from '@lumino/coreutils';

import { Datastore, Fields, RegisterField, TextField } from '@lumino/datastore';

import { DisposableDelegate, IDisposable } from '@lumino/disposable';

import { Panel, Widget } from '@lumino/widgets';

import * as CodeMirror from 'codemirror';

import {
  COLLABORATOR_COLOR,
  COLLABORATOR_ID,
  COLLABORATOR_NAME
} from './collaborator';

/**
 * The time that a collaborator name hover persists.
 */
const HOVER_TIMEOUT = 1000;

/**
 * A schema for an editor model. Currently contains two fields, the current
 * value and whether the model is read only. Other fields could include
 * language, mimetype, and collaborator cursors.
 */
export const EDITOR_SCHEMA = {
  id: 'editor',
  fields: {
    readOnly: Fields.Boolean(),
    text: Fields.Text(),
    collaborators: Fields.Map<ICollaboratorState>()
  }
};

/**
 * An interface representing a location in an editor.
 */
export interface IPosition extends JSONObject {
  /**
   * The cursor line number.
   */
  readonly line: number;

  /**
   * The cursor column number.
   */
  readonly column: number;
}

/**
 * An interface representing a user selection.
 */
export interface ITextSelection extends JSONObject {
  /**
   * The start of the selection.
   */
  readonly start: IPosition;

  /**
   * The end of the selection.
   */
  readonly end: IPosition;
}

/**
 * An interface representing collaborator cursor state.
 */
export interface ICollaboratorState extends JSONObject {
  /**
   * The current cursor selections.
   */
  selections: ITextSelection[];

  /**
   * A display name for the collaborator.
   */
  name: string;

  /**
   * A display color for the collaborator.
   */
  color: string;
}

/**
 * A widget which hosts a collaborative CodeMirror text editor.
 */
export class CodeMirrorEditor extends Panel {
  /**
   * Create a new editor widget.
   *
   * @param datastore: a datastore which holds an editor table using `EDITOR_SCHEMA`.
   *
   * @param record: the record to watch in the editor table.
   */
  constructor(datastore: Datastore, record: string) {
    super();
    this.addClass('content');
    this._store = datastore;
    this._record = record;

    // Get initial values for the editor
    let editorTable = this._store.get(EDITOR_SCHEMA);
    let initialValue = editorTable.get(record)!.text;
    let readOnly = editorTable.get(record)!.readOnly;

    // Set up the DOM structure
    this._editorWidget = new Widget();
    this._checkWidget = new Widget();
    this._checkWidget.node.style.height = `${this._toolbarHeight}px`;
    this._checkWidget.addClass('read-only-check');
    this._checkWidget.node.textContent = 'Read Only';
    this._check = document.createElement('input');
    this._check.type = 'checkbox';
    this._check.checked = readOnly;
    this._checkWidget.node.appendChild(this._check);

    this.addWidget(this._checkWidget);
    this.addWidget(this._editorWidget);

    // Listen to changes in the checkbox.
    this._check.onchange = this._onChecked.bind(this);

    // Create the editor instance.
    this._editor = CodeMirror(this._editorWidget.node, {
      value: initialValue,
      lineNumbers: true,
      readOnly
    });

    // Listen for changes on the editor model.
    CodeMirror.on(
      this._editor.getDoc(),
      'beforeChange',
      this._onEditorChange.bind(this)
    );

    // Listen for changes to the editor cursors.
    CodeMirror.on(
      this._editor,
      'cursorActivity',
      this._onCursorActivity.bind(this)
    );

    // Listen for changes on the datastore.
    datastore.changed.connect(this._onDatastoreChange, this);
  }

  /**
   * Undo the last user action.
   */
  undo(): void {
    let id = this._undo.pop();
    if (id) {
      this._redo.push(id);
      void this._store.undo(id);
    }
  }

  /**
   * Redo the last user action.
   */
  redo(): void {
    let id = this._redo.pop();
    if (id) {
      this._undo.push(id);
      void this._store.redo(id);
    }
  }

  /**
   * Whether the editor is currently focused.
   */
  hasFocus(): boolean {
    return this.node.contains(document.activeElement);
  }

  /**
   * Handle the DOM events for the editor.
   *
   * @param event - The DOM event sent to the editor.
   *
   * #### Notes
   * This method implements the DOM `EventListener` interface and is
   * called in response to events on the editor's DOM node. It should
   * not be called directly by user code.
   */
  handleEvent(event: Event): void {
    switch (event.type) {
      case 'scroll':
        this._clearHover();
        break;
      default:
        break;
    }
  }

  /**
   * A message handler invoked on a `'resize'` message.
   *
   * @param msg - the resize message.
   */
  protected onResize(msg: Widget.ResizeMessage): void {
    if (msg.width >= 0 && msg.height >= 0) {
      this._editor.setSize(msg.width, msg.height - this._toolbarHeight);
    } else if (this.isVisible) {
      this._editor.setSize(null, null);
    }
    this._editor.refresh();
    this._clearHover();
  }

  /**
   * Handle a `after-show` message for the editor.
   */
  protected onAfterShow() {
    this._editor.refresh();
  }

  /**
   * Handle a `after-attach` message for the editor.
   */
  protected onAfterAttach() {
    this.node.addEventListener('scroll', this, true);
  }

  /**
   * Handle a `before-detach` message for the editor.
   */
  protected onBeforeDetach() {
    this.node.removeEventListener('scroll', this, true);
  }

  /**
   * Handle a local check event.
   */
  private _onChecked(): void {
    // If this was a remote change, we are done.
    if (this._changeGuard) {
      return;
    }
    // Update the readonly state
    this._editor.setOption('readOnly', this._check.checked);
    // Update the table to broadcast the change.
    let editorTable = this._store.get(EDITOR_SCHEMA);
    let id = this._store.beginTransaction();
    editorTable.update({
      [this._record]: {
        readOnly: this._check.checked
      }
    });
    this._store.endTransaction();
    // Update the undo/redo stack.
    this._undo.push(id);
    this._redo.length = 0;
  }

  /**
   * Handle a local editor change.
   *
   * @param doc - the CodeMirror doc which changed.
   *
   * @param change - the CodeMirror change payload.
   */
  private _onEditorChange(
    doc: CodeMirror.Doc,
    change: CodeMirror.EditorChange
  ): void {
    // If this was a remote change, we are done.
    if (this._changeGuard) {
      return;
    }
    let editorTable = this._store.get(EDITOR_SCHEMA);
    let start = doc.indexFromPos(change.from);
    let end = doc.indexFromPos(change.to);
    let text = change.text.join('\n');
    // If this was a local change, update the table.
    let id = this._store.beginTransaction();
    editorTable.update({
      [this._record]: {
        text: {
          index: start,
          remove: end - start,
          text: text
        }
      }
    });
    this._store.endTransaction();
    // Update the undo/redo stack.
    this._undo.push(id);
    this._redo.length = 0;
  }

  /**
   * Respond to a change in the editor cursors.
   */
  private _onCursorActivity(): void {
    // Only add selections inf the editor has focus. This avoids unwanted
    // triggering of cursor activity due to other collaborator actions.
    if (this._editor.hasFocus()) {
      let selections = Private.getSelections(this._editor.getDoc());
      let name = COLLABORATOR_NAME;
      let color = COLLABORATOR_COLOR;
      let editorTable = this._store.get(EDITOR_SCHEMA);
      this._store.beginTransaction();
      editorTable.update({
        [this._record]: {
          collaborators: {
            [COLLABORATOR_ID]: { name, color, selections }
          }
        }
      });
      this._store.endTransaction();
    }
  }

  /**
   * Respond to a change on the datastore.
   *
   * @param store - the datastore which changed.
   *
   * @param change - the change content.
   */
  private _onDatastoreChange(
    store: Datastore,
    change: Datastore.IChangedArgs
  ): void {
    // Ignore changes that have already been applied locally.
    if (change.type === 'transaction' && change.storeId === store.id) {
      return;
    }
    let doc = this._editor.getDoc();
    // Apply text field changes to the editor.
    let c = change.change['editor'];
    if (c && c[this._record] && c[this._record].text) {
      let textChanges = c[this._record].text as TextField.Change;
      textChanges.forEach(tc => {
        // Convert the change data to codemirror range and inserted text.
        let from = doc.posFromIndex(tc.index);
        let to = doc.posFromIndex(tc.index + tc.removed.length);
        let replacement = tc.inserted;

        // Apply the operation, setting the change guard so we can ignore
        // the change signals from codemirror.
        this._changeGuard = true;
        doc.replaceRange(replacement, from, to, '+input');
        this._changeGuard = false;
      });
    }

    // If the readonly state has changed, update the check box, setting the
    // change guard so we can ignore it in the onchange event.
    if (c && c[this._record] && c[this._record].readOnly) {
      this._changeGuard = true;
      let checkChange = c[this._record].readOnly as RegisterField.Change<
        boolean
      >;
      this._check.checked = checkChange.current;
      // Update the readonly state
      this._editor.setOption('readOnly', this._check.checked);
      this._changeGuard = false;
    }

    // If the collaborator state has changed, rerender any selections.
    if (c && c[this._record] && c[this._record].collaborators) {
      let record = store.get(EDITOR_SCHEMA).get(this._record)!;
      let { collaborators } = record;
      this._clearAllSelections();
      let ids = Object.keys(collaborators);
      for (let id of ids) {
        if (id !== COLLABORATOR_ID) {
          this._markSelections(id, collaborators[id]!);
        }
      }
    }
  }

  /**
   * Clean currently shown selections for the editor.
   */
  private _clearAllSelections() {
    this._clearHover();
    let ids = Object.keys(this._selectionMarkers);
    for (let id of ids) {
      this._clearSelections(id);
    }
  }

  /**
   * Clean currently shown selections for a given collaborator.
   */
  private _clearSelections(id: string) {
    let ids = Object.keys(this._selectionMarkers);
    if (this._hoverId === id) {
      this._clearHover();
    }
    for (let id of ids) {
      let markers = this._selectionMarkers[id]!;
      markers.forEach(marker => {
        marker.clear();
      });
      delete this._selectionMarkers[id];
    }
  }

  /**
   * Marks selections.
   */
  private _markSelections(uuid: string, collaborator: ICollaboratorState) {
    let markers: CodeMirror.TextMarker[] = [];
    let doc = this._editor.getDoc();

    // Style each selection for the uuid.
    collaborator.selections.forEach(selection => {
      // Only render selections if the start is not equal to the end.
      // In that case, we don't need to render the cursor.
      if (!JSONExt.deepEqual(selection.start, selection.end)) {
        // Selections only appear to render correctly if the anchor
        // is before the head in the document. That is, reverse selections
        // do not appear as intended.
        let forward: boolean =
          selection.start.line < selection.end.line ||
          (selection.start.line === selection.end.line &&
            selection.start.column <= selection.end.column);
        let anchor = Private.toCodeMirrorPosition(
          forward ? selection.start : selection.end
        );
        let head = Private.toCodeMirrorPosition(
          forward ? selection.end : selection.start
        );
        let markerOptions = Private.toTextMarkerOptions(collaborator);
        markers.push(doc.markText(anchor, head, markerOptions));
      } else {
        let caret = this._getCaret(uuid, collaborator);
        markers.push(
          doc.setBookmark(Private.toCodeMirrorPosition(selection.end), {
            widget: caret
          })
        );
      }
    });
    this._selectionMarkers[uuid] = markers;
    // Set a timer to auto-dispose of these markers, cleaning up after
    // collaborators who might have left. We choose a random time between one
    // and two minutes to avoid racing between active collaborators.
    if (this._timers[uuid]) {
      window.clearTimeout(this._timers[uuid]);
    }
    this._timers[uuid] = window.setTimeout(() => {
      this._clearSelections(uuid);
      delete this._timers[uuid];
    }, 60 * 1000 * (1 + Math.random()));
  }

  /**
   * Construct a caret element representing the position
   * of a collaborator's cursor.
   */
  private _getCaret(
    uuid: string,
    collaborator: ICollaboratorState
  ): HTMLElement {
    let { name, color } = collaborator;
    let hoverTimeout: number;
    let caret: HTMLElement = document.createElement('span');
    caret.className = 'collaborator-cursor';
    caret.style.borderBottomColor = color;
    caret.onmouseenter = () => {
      this._clearHover();
      let rect = caret.getBoundingClientRect();
      // Construct and place the hover box.
      let hover = document.createElement('div');
      hover.className = 'collaborator-cursor-hover';
      hover.style.left = String(rect.left) + 'px';
      hover.style.top = String(rect.bottom) + 'px';
      hover.textContent = name;
      hover.style.backgroundColor = color;

      // If the user mouses over the hover, take over the timer.
      hover.onmouseenter = () => {
        window.clearTimeout(hoverTimeout);
      };
      hover.onmouseleave = () => {
        hoverTimeout = window.setTimeout(() => {
          this._clearHover();
        }, HOVER_TIMEOUT);
      };
      document.body.appendChild(hover);
      this._hoverId = uuid;
      this._hover = new DisposableDelegate(() => {
        window.clearTimeout(hoverTimeout);
        document.body.removeChild(hover);
      });
    };
    caret.onmouseleave = () => {
      hoverTimeout = window.setTimeout(() => {
        this._clearHover();
      }, HOVER_TIMEOUT);
    };
    return caret;
  }

  /**
   * If there is currently a hover box of a collaborator name, clear it.
   */
  private _clearHover(): void {
    this._hoverId = '';
    if (this._hover) {
      this._hover.dispose();
      this._hover = null;
    }
  }

  /**
   * Converts an editor selection to a code mirror selection.
   */
  private _changeGuard: boolean = false;
  private _check: HTMLInputElement;
  private _checkWidget: Widget;
  private _editor: CodeMirror.Editor;
  private _editorWidget: Widget;
  private _hover: IDisposable | null = null;
  private _hoverId: string = '';
  private _record: string;
  private _selectionMarkers: {
    [key: string]: CodeMirror.TextMarker[] | undefined;
  } = {};
  private _store: Datastore;
  private _timers: { [key: string]: number } = {};
  private _toolbarHeight = 24;
  private _undo: string[] = [];
  private _redo: string[] = [];
}

/**
 * A namespace for module-private functionality.
 */
namespace Private {
  /**
   * Create CodeMirror text marker options for a collaborator.
   */
  export function toTextMarkerOptions(
    collaborator: ICollaboratorState
  ): CodeMirror.TextMarkerOptions {
    let r = parseInt(collaborator.color.slice(1, 3), 16);
    let g = parseInt(collaborator.color.slice(3, 5), 16);
    let b = parseInt(collaborator.color.slice(5, 7), 16);
    let css = `background-color: rgba( ${r}, ${g}, ${b}, 0.15)`;
    return {
      title: collaborator.name,
      css
    };
  }

  /**
   * Convert an editor position to a code mirror position.
   */
  export function toCodeMirrorPosition(position: IPosition) {
    return {
      line: position.line,
      ch: position.column
    };
  }

  /**
   * Converts a code mirror selection to an editor selection.
   */
  export function toSelection(selection: {
    anchor: CodeMirror.Position;
    head: CodeMirror.Position;
  }): ITextSelection {
    return {
      start: toPosition(selection.anchor),
      end: toPosition(selection.head)
    };
  }

  /**
   * Convert a code mirror position to an editor position.
   */
  export function toPosition(position: CodeMirror.Position): IPosition {
    return {
      line: position.line,
      column: position.ch
    };
  }

  /**
   * Gets the selections for all the cursors, never `null` or empty.
   */
  export function getSelections(doc: CodeMirror.Doc): ITextSelection[] {
    let selections = doc.listSelections();
    if (selections.length > 0) {
      return selections.map(selection => Private.toSelection(selection));
    }
    let cursor = doc.getCursor();
    let selection = Private.toSelection({ anchor: cursor, head: cursor });
    return [selection];
  }
}
