// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/*-----------------------------------------------------------------------------
| Copyright (c) 2014-2019, PhosphorJS Contributors
|
| Distributed under the terms of the BSD 3-Clause License.
|
| The full license is in the file LICENSE, distributed with this software.
|----------------------------------------------------------------------------*/
import { expect } from 'chai';

import {
  Datastore,
  Fields,
  IServerAdapter,
  ListField,
  MapField,
  RegisterField,
  TextField
} from '@lumino/datastore';

import { MessageLoop } from '@lumino/messaging';

import { Signal } from '@lumino/signaling';

type CustomMetadata = { id: string };

type TestSchema = {
  id: string;
  fields: {
    content: TextField;
    count: RegisterField<number>;
    enabled: RegisterField<boolean>;
    tags: MapField<string>;
    links: ListField<string>;
    metadata: RegisterField<CustomMetadata>;
  };
};

let schema1: TestSchema = {
  id: 'test-schema-1',
  fields: {
    content: Fields.Text(),
    count: Fields.Number(),
    enabled: Fields.Boolean(),
    tags: Fields.Map<string>(),
    links: Fields.List<string>(),
    metadata: Fields.Register<CustomMetadata>({ value: { id: 'identifier' } })
  }
};

let schema2: TestSchema = {
  id: 'test-schema-2',
  fields: {
    content: Fields.Text(),
    count: Fields.Number(),
    enabled: Fields.Boolean(),
    tags: Fields.Map<string>(),
    links: Fields.List<string>(),
    metadata: Fields.Register<CustomMetadata>({ value: { id: 'identifier' } })
  }
};

let state = {
  [schema1.id]: [
    {
      content: 'Lorem Ipsum',
      count: 42,
      enabled: true,
      links: ['www.example.com'],
      metadata: { id: 'myidentifier' }
    }
  ],
  [schema2.id]: [
    {
      content: 'Ipsum Lorem',
      count: 33,
      enabled: false,
      links: ['www.example.com', 'https://github.com/lumino/luminojs'],
      metadata: null
    }
  ]
};

/**
 * Return a shuffled copy of an array
 */
function shuffle<T>(array: ReadonlyArray<T>): T[] {
  let ret = array.slice();
  for (let i = ret.length - 1; i > 0; i--) {
    let j = Math.floor(Math.random() * (i + 1)); // random index from 0 to i
    [ret[i], ret[j]] = [ret[j], ret[i]]; // swap elements
  }
  return ret;
}

/**
 * An in-memory implementation of a patch store.
 */
class InMemoryServerAdapter implements IServerAdapter {
  constructor() {
    this.onRemoteTransaction = null;
    this.onUndo = null;
    this.onRedo = null;
  }

  broadcast(transaction: Datastore.Transaction): void {
    this._transactions[transaction.id] = transaction;
  }

  undo(id: string): Promise<void> {
    if (this.onUndo) {
      this.onUndo(this._transactions[id]);
    }
    return Promise.resolve(undefined);
  }

  redo(id: string): Promise<void> {
    if (this.onRedo) {
      this.onRedo(this._transactions[id]);
    }
    return Promise.resolve(undefined);
  }

  onRemoteTransaction: ((transaction: Datastore.Transaction) => void) | null;

  onUndo: ((transaction: Datastore.Transaction) => void) | null;

  onRedo: ((transaction: Datastore.Transaction) => void) | null;

  get transactions(): { [id: string]: Datastore.Transaction } {
    return this._transactions;
  }

  get isDisposed(): boolean {
    return this._isDisposed;
  }

  dispose(): void {
    if (this._isDisposed) {
      return;
    }
    this._isDisposed = true;
    Signal.clearData(this);
  }

  private _isDisposed = false;
  private _transactions: { [id: string]: Datastore.Transaction } = {};
}

describe('@lumino/datastore', () => {
  describe('Datastore', () => {
    let datastore: Datastore;
    let adapter: InMemoryServerAdapter;
    const DATASTORE_ID = 1234;
    beforeEach(() => {
      adapter = new InMemoryServerAdapter();
      datastore = Datastore.create({
        id: DATASTORE_ID,
        schemas: [schema1, schema2],
        adapter
      });
    });

    afterEach(() => {
      datastore.dispose();
      adapter.dispose();
    });

    describe('create()', () => {
      it('should create a new datastore', () => {
        let datastore = Datastore.create({ id: 1, schemas: [schema1] });
        expect(datastore).to.be.instanceof(Datastore);
      });

      it('should throw an error for an invalid schema', () => {
        let invalid1 = {
          id: 'invalid-schema',
          fields: {
            '@content': Fields.Text()
          }
        };
        expect(() => {
          Datastore.create({ id: 1, schemas: [invalid1] });
        }).to.throw(/validation failed/);
        let invalid2 = {
          id: 'invalid-schema',
          fields: {
            $content: Fields.Text()
          }
        };
        expect(() => {
          Datastore.create({ id: 1, schemas: [invalid2] });
        }).to.throw(/validation failed/);
      });

      it('should restore valid state', () => {
        let datastore = Datastore.create({
          id: 1,
          schemas: [schema1, schema2],
          restoreState: JSON.stringify(state)
        });

        let reexport = datastore.toString();
        expect(JSON.parse(reexport)).to.eql(state);
      });

      it('should restore partial state', () => {
        let partialState = { [schema1.id]: state[schema1.id] };
        let datastore = Datastore.create({
          id: 1,
          schemas: [schema1, schema2],
          restoreState: JSON.stringify(partialState)
        });

        let reexport = datastore.toString();
        expect(JSON.parse(reexport)).to.eql({
          ...partialState,
          [schema2.id]: []
        });
      });
    });

    describe('dispose()', () => {
      it('should dispose of the resources held by the datastore', () => {
        expect(datastore.adapter).to.not.be.null;
        datastore.dispose();
        expect(datastore.adapter).to.be.null;
      });

      it('should be safe to call more than once', () => {
        datastore.dispose();
        datastore.dispose();
      });
    });

    describe('isDisposed()', () => {
      it('should indicate whether the datastore is disposed', () => {
        expect(datastore.isDisposed).to.be.false;
        datastore.dispose();
        expect(datastore.isDisposed).to.be.true;
      });
    });

    describe('changed', () => {
      it('should should emit upon changes to the datastore', () => {
        let called = false;
        let id = '';
        datastore.changed.connect((_, change) => {
          called = true;
          expect(change.type).to.equal('transaction');
          expect(change.transactionId).to.equal(id);
          expect(change.storeId).to.equal(DATASTORE_ID);
          expect(change.change['test-schema-1']).to.not.be.undefined;
          expect(change.change['test-schema-2']).to.be.undefined;
        });
        let t1 = datastore.get(schema1);
        id = datastore.beginTransaction();
        t1.update({ 'my-record': { enabled: true } });
        datastore.endTransaction();
        expect(called).to.be.true;
      });
    });

    describe('id', () => {
      it('should return the unique store id', () => {
        expect(datastore.id).to.equal(DATASTORE_ID);
      });
    });

    describe('inTransaction', () => {
      it('should indicate whether the datastore is in a transaction', () => {
        expect(datastore.inTransaction).to.be.false;
        datastore.beginTransaction();
        expect(datastore.inTransaction).to.be.true;
        datastore.endTransaction();
        expect(datastore.inTransaction).to.be.false;
      });
    });

    describe('adapter', () => {
      it('should be the adapter for the datastore', () => {
        expect(datastore.adapter).to.equal(adapter);
      });

      it('should recieve transactions from the datastore', () => {
        let t2 = datastore.get(schema2);
        datastore.beginTransaction();
        t2.update({ 'my-record': { enabled: true } });
        expect(Object.keys(adapter.transactions).length).to.equal(0);
        datastore.endTransaction();
        expect(Object.keys(adapter.transactions).length).to.equal(1);
      });
    });

    describe('version', () => {
      it('should increase with each transaction', () => {
        let version = datastore.version;
        let t1 = datastore.get(schema1);
        let t2 = datastore.get(schema2);

        datastore.beginTransaction();
        t2.update({ 'my-record': { enabled: true } });
        datastore.endTransaction();

        expect(datastore.version).to.be.above(version);
        version = datastore.version;

        datastore.beginTransaction();
        t1.update({ 'my-record': { enabled: true } });
        datastore.endTransaction();

        expect(datastore.version).to.be.above(version);
      });
    });

    describe('iter()', () => {
      it('should return an iterator over the tables of the datastore', () => {
        let iterator = datastore.iter();
        let t1 = iterator.next();
        let t2 = iterator.next();
        expect(t1!.schema).to.equal(schema1);
        expect(t2!.schema).to.equal(schema2);
        expect(iterator.next()).to.be.undefined;
      });
    });

    describe('get()', () => {
      it('should return a table for a schema', () => {
        let t1 = datastore.get(schema1);
        let t2 = datastore.get(schema2);
        expect(t1.schema).to.equal(schema1);
        expect(t2.schema).to.equal(schema2);
      });

      it('should throw an error for a nonexistent schema', () => {
        let schema3 = { ...schema2, id: 'new-schema' };
        expect(() => {
          datastore.get(schema3);
        }).to.throw(/No table found/);
      });
    });

    describe('beginTransaction()', () => {
      it('should allow for mutations on the datastore', () => {
        let t1 = datastore.get(schema1);
        expect(datastore.inTransaction).to.be.false;
        expect(() => {
          t1.update({ 'my-record': { enabled: true } });
        }).to.throw(/A table can only be updated/);
        datastore.beginTransaction();
        t1.update({ 'my-record': { enabled: true } });
        expect(datastore.inTransaction).to.be.true;
        datastore.endTransaction();
        expect(datastore.inTransaction).to.be.false;
      });

      it('should return a transaction id', () => {
        expect(datastore.beginTransaction()).to.not.equal('');
        datastore.endTransaction();
      });

      it('should throw if called multiple times', () => {
        datastore.beginTransaction();
        expect(() => datastore.beginTransaction()).to.throw(/Already/);
        datastore.endTransaction();
      });

      it('should queue additional transactions for processing later', async () => {
        // First, generate a transaction to apply later.
        let id = datastore.beginTransaction();
        let t2 = datastore.get(schema2);
        t2.update({
          'my-record': {
            content: { index: 0, remove: 0, text: 'hello, world' }
          }
        });
        datastore.endTransaction();
        // Create a new datastore
        let adapter2 = new InMemoryServerAdapter();
        let datastore2 = Datastore.create({
          id: 5678,
          schemas: [schema1, schema2],
          adapter: adapter2
        });
        // Begin a transaction in the new datastore
        datastore2.beginTransaction();
        t2 = datastore2.get(schema2);
        t2.update({
          'my-record': {
            enabled: true
          }
        });
        // Trigger a remote transaction. It should be queued.
        adapter2.onRemoteTransaction!(adapter.transactions[id]);
        datastore2.endTransaction();
        expect(t2.get('my-record')!.enabled).to.be.true;
        expect(t2.get('my-record')!.content).to.equal('');
        // Flush the message loop to trigger processing of the queue.
        MessageLoop.flush();
        expect(t2.get('my-record')!.enabled).to.be.true;
        expect(t2.get('my-record')!.content).to.equal('hello, world');

        datastore2.dispose();
        adapter2.dispose();
      });

      it('should automatically close a transaction later', async () => {
        datastore.beginTransaction();
        expect(datastore.inTransaction).to.be.true;
        // Flush the message loop to trigger processing of the queue.
        MessageLoop.flush();
        expect(datastore.inTransaction).to.be.false;
      });
    });

    describe('endTransaction()', () => {
      it('should emit a changed signal with the user-facing changes', () => {
        let called = false;
        let id = '';
        datastore.changed.connect((_, change) => {
          called = true;
          expect(change.type).to.equal('transaction');
          expect(change.transactionId).to.equal(id);
          expect(change.storeId).to.equal(DATASTORE_ID);
          expect(change.change['test-schema-2']).to.not.be.undefined;
          expect(change.change['test-schema-1']).to.be.undefined;
        });
        let t2 = datastore.get(schema2);
        id = datastore.beginTransaction();
        t2.update({ 'my-record': { enabled: true } });
        datastore.endTransaction();
        expect(called).to.be.true;
      });

      it('should broadcast the transaction to the server adapter', () => {
        let t2 = datastore.get(schema2);
        datastore.beginTransaction();
        t2.update({ 'my-record': { enabled: true } });
        expect(Object.keys(adapter.transactions).length).to.equal(0);
        datastore.endTransaction();
        expect(Object.keys(adapter.transactions).length).to.equal(1);
      });

      it('should throw if there is not a transaction begun', () => {
        expect(() => datastore.endTransaction()).to.throw(/No transaction/);
      });
    });

    describe('undo()', () => {
      it('should be throw without a patch server', async () => {
        let datastore = Datastore.create({
          id: DATASTORE_ID,
          schemas: [schema1, schema2]
        });
        let thrown = false;
        try {
          await datastore.undo('');
        } catch {
          thrown = true;
        } finally {
          expect(thrown).to.be.true;
          datastore.dispose();
        }
      });

      it('should throw if invoked during a transaction', async () => {
        let thrown = false;
        try {
          datastore.beginTransaction();
          await datastore.undo('');
        } catch {
          thrown = true;
        } finally {
          datastore.endTransaction();
          expect(thrown).to.be.true;
        }
      });

      it('should unapply a transaction by id', async () => {
        let t2 = datastore.get(schema2);
        let id = datastore.beginTransaction();
        t2.update({ 'my-record': { enabled: true } });
        datastore.endTransaction();
        let record = t2.get('my-record')!;
        expect(record.enabled).to.be.true;
        await datastore.undo(id);
        record = t2.get('my-record')!;
        expect(record.enabled).to.be.false;
      });

      it('should allow for multiple undos', async () => {
        let t2 = datastore.get(schema2);
        let id = datastore.beginTransaction();
        t2.update({ 'my-record': { enabled: true } });
        datastore.endTransaction();
        await datastore.undo(id);
        await datastore.undo(id);
        await datastore.undo(id);
        let record = t2.get('my-record')!;
        expect(record.enabled).to.be.false;
      });

      it('should allow for concurrent undos', async () => {
        // Create a transaction.
        let t2 = datastore.get(schema2);
        let id = datastore.beginTransaction();
        t2.update({
          'my-record': {
            enabled: true,
            content: { index: 0, remove: 0, text: 'hello, world' }
          }
        });
        datastore.endTransaction();
        let transaction = adapter.transactions[id];
        // Create a new datastore and undo the transaction before it's applied.
        let datastore2 = Datastore.create({
          id: 5678,
          schemas: [schema1, schema2],
          adapter
        });
        t2 = datastore2.get(schema2);
        // No change for concurrently undone transaction.
        adapter.onUndo!(transaction);
        let record = t2.get('my-record');
        expect(record).to.be.undefined;
        // Now apply the transaction, it should be undone still
        adapter.onRemoteTransaction!(transaction);
        record = t2.get('my-record')!;
        expect(record).to.be.undefined;
        // Now redo the transaction, it should appear.
        adapter.onRedo!(transaction);
        record = t2.get('my-record')!;
        expect(record.enabled).to.be.true;
        expect(record.content).to.equal('hello, world');
      });

      it('should emit a changed signal when undoing a change', async () => {
        let t2 = datastore.get(schema2);
        let id = datastore.beginTransaction();
        t2.update({ 'my-record': { enabled: true } });
        datastore.endTransaction();
        let record = t2.get('my-record')!;
        expect(record.enabled).to.be.true;

        let called = false;
        datastore.changed.connect((sender, args) => {
          expect(args.type).to.equal('undo');
          expect(args.transactionId).to.equal(id);
          called = true;
        });
        await datastore.undo(id);
        expect(called).to.be.true;
      });

      it('should not emit a changed signal when there is nothing to undo', async () => {
        let t2 = datastore.get(schema2);
        let id = datastore.beginTransaction();
        t2.update({ 'my-record': { enabled: true } });
        datastore.endTransaction();
        let record = t2.get('my-record')!;
        expect(record.enabled).to.be.true;
        await datastore.undo(id);

        let called = false;
        datastore.changed.connect((sender, args) => {
          called = true;
        });
        // Already undone, so no signal should be emitted.
        await datastore.undo(id);
        expect(called).to.be.false;
      });
    });

    describe('redo()', () => {
      it('should be throw without a patch server', async () => {
        let datastore = Datastore.create({
          id: DATASTORE_ID,
          schemas: [schema1, schema2]
        });
        let thrown = false;
        try {
          await datastore.redo('');
        } catch {
          thrown = true;
        } finally {
          expect(thrown).to.be.true;
          datastore.dispose();
        }
      });

      it('should throw if invoked during a transaction', async () => {
        let thrown = false;
        try {
          datastore.beginTransaction();
          await datastore.redo('');
        } catch {
          thrown = true;
        } finally {
          datastore.endTransaction();
          expect(thrown).to.be.true;
        }
      });

      it('should reapply a transaction by id', async () => {
        let t2 = datastore.get(schema2);
        let id = datastore.beginTransaction();
        t2.update({
          'my-record': {
            enabled: true,
            content: { index: 0, remove: 0, text: 'hello, world' }
          }
        });
        datastore.endTransaction();
        let record = t2.get('my-record')!;
        expect(record.enabled).to.be.true;
        expect(record.content).to.equal('hello, world');
        await datastore.undo(id);
        record = t2.get('my-record')!;
        expect(record.enabled).to.be.false;
        expect(record.content).to.equal('');
        await datastore.redo(id);
        record = t2.get('my-record')!;
        expect(record.enabled).to.be.true;
        expect(record.content).to.equal('hello, world');
      });

      it('should have redos winning in a tie', async () => {
        let t2 = datastore.get(schema2);
        let id = datastore.beginTransaction();
        t2.update({
          'my-record': {
            enabled: true,
            content: { index: 0, remove: 0, text: 'hello, world' }
          }
        });
        datastore.endTransaction();
        let record = t2.get('my-record')!;
        expect(record.enabled).to.be.true;
        expect(record.content).to.equal('hello, world');
        await datastore.undo(id);
        await datastore.undo(id);
        await datastore.undo(id);
        record = t2.get('my-record')!;
        expect(record.enabled).to.be.false;
        expect(record.content).to.equal('');
        await datastore.redo(id);
        await datastore.redo(id);
        await datastore.redo(id);
        record = t2.get('my-record')!;
        expect(record.enabled).to.be.true;
        expect(record.content).to.equal('hello, world');
      });

      it('should be safe to call extra times', async () => {
        let t2 = datastore.get(schema2);
        let id = datastore.beginTransaction();
        t2.update({
          'my-record': {
            enabled: true,
            content: { index: 0, remove: 0, text: 'hello, world' }
          }
        });
        datastore.endTransaction();
        let record = t2.get('my-record')!;
        expect(record.enabled).to.be.true;
        expect(record.content).to.equal('hello, world');
        await datastore.undo(id);
        record = t2.get('my-record')!;
        expect(record.enabled).to.be.false;
        expect(record.content).to.equal('');
        // Try to redo extra times, should not duplicate the patch.
        await datastore.redo(id);
        await datastore.redo(id);
        await datastore.redo(id);
        record = t2.get('my-record')!;
        expect(record.enabled).to.be.true;
        expect(record.content).to.equal('hello, world');
      });

      it('should emit a changed signal when redoing a change', async () => {
        let t2 = datastore.get(schema2);
        let id = datastore.beginTransaction();
        t2.update({ 'my-record': { enabled: true } });
        datastore.endTransaction();
        let record = t2.get('my-record')!;
        expect(record.enabled).to.be.true;
        await datastore.undo(id);

        let called = false;
        datastore.changed.connect((sender, args) => {
          expect(args.type).to.equal('redo');
          expect(args.transactionId).to.equal(id);
          called = true;
        });
        await datastore.redo(id);
        expect(called).to.be.true;
      });

      it('should not emit a changed signal when there is nothing to redo', async () => {
        let t2 = datastore.get(schema2);
        let id = datastore.beginTransaction();
        t2.update({ 'my-record': { enabled: true } });
        datastore.endTransaction();
        let record = t2.get('my-record')!;
        expect(record.enabled).to.be.true;
        await datastore.undo(id);
        await datastore.redo(id);

        let called = false;
        datastore.changed.connect((sender, args) => {
          called = true;
        });
        // Already redone, so no signal should be emitted.
        await datastore.redo(id);
        expect(called).to.be.false;
      });

      it('should be insensitive to causality', async () => {
        // Generate transactions that add then delete a value in a map.
        let t2 = datastore.get(schema2);
        let id1 = datastore.beginTransaction();
        t2.update({ record: { tags: { value: 'tagged' } } });
        datastore.endTransaction();
        expect(t2.get('record')!.tags.value).to.equal('tagged');
        let id2 = datastore.beginTransaction();
        t2.update({ record: { tags: { value: null } } });
        datastore.endTransaction();
        expect(t2.get('record')!.tags.value).to.be.undefined;
        let transaction1 = adapter.transactions[id1];
        let transaction2 = adapter.transactions[id2];

        // Design a set of undo and redo operations, after which
        // transaction1 should be showing, and transaction 2 should not.
        let operations = ['t1', 't2', 'u1', 'r1', 'u2', 'u1', 'r1', 'u2', 'r2'];
        // Shuffle the operations many times so that we don't accidentally
        // get the right answer.
        for (let i = 0; i < 20; i++) {
          let ops = shuffle(operations);
          // Create a new datastore
          let adapt = new InMemoryServerAdapter();
          let store = Datastore.create({
            id: 5678,
            schemas: [schema1, schema2],
            adapter: adapt
          });
          let table = store.get(schema2);
          for (let op of ops) {
            switch (op) {
              case 't1':
                adapt.onRemoteTransaction!(transaction1);
                break;
              case 't2':
                adapt.onRemoteTransaction!(transaction2);
                break;
              case 'u1':
                adapt.onUndo!(transaction1);
                break;
              case 'u2':
                adapt.onUndo!(transaction2);
                break;
              case 'r1':
                adapt.onRedo!(transaction1);
                break;
              case 'r2':
                adapt.onRedo!(transaction2);
                break;
              default:
                throw 'Unreachable';
                break;
            }
          }
          expect(table.get('record')!.tags.value).to.equal('tagged');
          adapt.dispose();
          store.dispose();
        }
      });
    });
  });
});
