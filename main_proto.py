#!/usr/bin/env python
import sys
import os
os.environ['QT_MAC_WANTS_LAYER'] = '1'
from PySide2.QtCore import QCoreApplication
from PySide2.QtGui import QFontMetrics
from PySide2.QtWidgets import (QApplication, QStyle, QWidget, QMainWindow, QTableWidget, QTableWidgetItem)


# import platform
# platform.platform()
# >>> platform.system()
# 'Windows'
# platform.release()
# 'XP'
# platform.version()
# '5.1.2600'

class MyApp(QApplication):
    def __init__(self, cmdLine):
        super(MyApp, self).__init__(cmdLine)
        self.upperTape = self.style().pixelMetric(QStyle.PM_TitleBarHeight)
        self.edge = self.style().pixelMetric(QStyle.PM_MdiSubWindowFrameWidth)
        self.myRectangle = self.getMarginalWindowSize(0.025)

    def getMarginalWindowSize(self, marginRatio):
        rectangle = self.desktop().availableGeometry()
        margin = int(rectangle.height() * marginRatio)
        rectangle.adjust(margin + self.edge, self.upperTape,
                         -(margin + self.edge), -self.edge)
        return rectangle


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle('Basic Drawing')
        self.app = QCoreApplication.instance()
        self.setGeometry(self.app.myRectangle)
        st = self.app.style()
        self.params = (('ButtonMargin', st.pixelMetric(QStyle.PM_ButtonMargin)),
                       ('DockWidgetTitleBarButtonMargin', st.pixelMetric(QStyle.PM_DockWidgetTitleBarButtonMargin)),
                       ('ButtonDefaultIndicator', st.pixelMetric(QStyle.PM_ButtonDefaultIndicator)),
                       ('MenuButtonIndicator', st.pixelMetric(QStyle.PM_MenuButtonIndicator)),
                       ('ButtonShiftHorizontal', st.pixelMetric(QStyle.PM_ButtonShiftHorizontal)),
                       ('ButtonShiftVertical', st.pixelMetric(QStyle.PM_ButtonShiftVertical)),
                       ('DefaultFrameWidth', st.pixelMetric(QStyle.PM_DefaultFrameWidth)),
                       ('SpinBoxFrameWidth', st.pixelMetric(QStyle.PM_SpinBoxFrameWidth)),
                       ('ComboBoxFrameWidth', st.pixelMetric(QStyle.PM_ComboBoxFrameWidth)),
                       ('MdiSubWindowFrameWidth', st.pixelMetric(QStyle.PM_MdiSubWindowFrameWidth)),
                       ('MdiSubWindowMinimizedWidth', st.pixelMetric(QStyle.PM_MdiSubWindowMinimizedWidth)),
                       ('LayoutLeftMargin', st.pixelMetric(QStyle.PM_LayoutLeftMargin)),
                       ('LayoutTopMargin', st.pixelMetric(QStyle.PM_LayoutTopMargin)),
                       ('LayoutRightMargin', st.pixelMetric(QStyle.PM_LayoutRightMargin)),
                       ('LayoutBottomMargin', st.pixelMetric(QStyle.PM_LayoutBottomMargin)),
                       ('LayoutHorizontalSpacing', st.pixelMetric(QStyle.PM_LayoutHorizontalSpacing)),
                       ('LayoutVerticalSpacing', st.pixelMetric(QStyle.PM_LayoutVerticalSpacing)),
                       ('MaximumDragDistance', st.pixelMetric(QStyle.PM_MaximumDragDistance)),
                       ('ScrollBarExtent', st.pixelMetric(QStyle.PM_ScrollBarExtent)),
                       ('ScrollBarSliderMin', st.pixelMetric(QStyle.PM_ScrollBarSliderMin)),
                       ('SliderThickness', st.pixelMetric(QStyle.PM_SliderThickness)),
                       ('SliderControlThickness', st.pixelMetric(QStyle.PM_SliderControlThickness)),
                       ('SliderLength', st.pixelMetric(QStyle.PM_SliderLength)),
                       ('SliderTickmarkOffset', st.pixelMetric(QStyle.PM_SliderTickmarkOffset)),
                       ('SliderSpaceAvailable', st.pixelMetric(QStyle.PM_SliderSpaceAvailable)),
                       ('DockWidgetSeparatorExtent', st.pixelMetric(QStyle.PM_DockWidgetSeparatorExtent)),
                       ('DockWidgetHandleExtent', st.pixelMetric(QStyle.PM_DockWidgetHandleExtent)),
                       ('DockWidgetFrameWidth', st.pixelMetric(QStyle.PM_DockWidgetFrameWidth)),
                       ('DockWidgetTitleMargin', st.pixelMetric(QStyle.PM_DockWidgetTitleMargin)),
                       ('MenuBarPanelWidth', st.pixelMetric(QStyle.PM_MenuBarPanelWidth)),
                       ('MenuBarItemSpacing', st.pixelMetric(QStyle.PM_MenuBarItemSpacing)),
                       ('MenuBarHMargin', st.pixelMetric(QStyle.PM_MenuBarHMargin)),
                       ('MenuBarVMargin', st.pixelMetric(QStyle.PM_MenuBarVMargin)),
                       ('ToolBarFrameWidth', st.pixelMetric(QStyle.PM_ToolBarFrameWidth)),
                       ('ToolBarHandleExtent', st.pixelMetric(QStyle.PM_ToolBarHandleExtent)),
                       ('ToolBarItemMargin', st.pixelMetric(QStyle.PM_ToolBarItemMargin)),
                       ('ToolBarItemSpacing', st.pixelMetric(QStyle.PM_ToolBarItemSpacing)),
                       ('ToolBarSeparatorExtent', st.pixelMetric(QStyle.PM_ToolBarSeparatorExtent)),
                       ('ToolBarExtensionExtent', st.pixelMetric(QStyle.PM_ToolBarExtensionExtent)),
                       ('TabBarTabOverlap', st.pixelMetric(QStyle.PM_TabBarTabOverlap)),
                       ('TabBarTabHSpace', st.pixelMetric(QStyle.PM_TabBarTabHSpace)),
                       ('TabBarTabVSpace', st.pixelMetric(QStyle.PM_TabBarTabVSpace)),
                       ('TabBarBaseHeight', st.pixelMetric(QStyle.PM_TabBarBaseHeight)),
                       ('TabBarBaseOverlap', st.pixelMetric(QStyle.PM_TabBarBaseOverlap)),
                       ('TabBarScrollButtonWidth', st.pixelMetric(QStyle.PM_TabBarScrollButtonWidth)),
                       ('TabBarTabShiftHorizontal', st.pixelMetric(QStyle.PM_TabBarTabShiftHorizontal)),
                       ('TabBarTabShiftVertical', st.pixelMetric(QStyle.PM_TabBarTabShiftVertical)),
                       ('ProgressBarChunkWidth', st.pixelMetric(QStyle.PM_ProgressBarChunkWidth)),
                       ('SplitterWidth', st.pixelMetric(QStyle.PM_SplitterWidth)),
                       ('TitleBarHeight', st.pixelMetric(QStyle.PM_TitleBarHeight)),
                       ('IndicatorWidth', st.pixelMetric(QStyle.PM_IndicatorWidth)),
                       ('IndicatorHeight', st.pixelMetric(QStyle.PM_IndicatorHeight)),
                       ('ExclusiveIndicatorWidth', st.pixelMetric(QStyle.PM_ExclusiveIndicatorWidth)),
                       ('ExclusiveIndicatorHeight', st.pixelMetric(QStyle.PM_ExclusiveIndicatorHeight)),
                       ('MenuPanelWidth', st.pixelMetric(QStyle.PM_MenuPanelWidth)),
                       ('MenuHMargin', st.pixelMetric(QStyle.PM_MenuHMargin)),
                       ('MenuVMargin', st.pixelMetric(QStyle.PM_MenuVMargin)),
                       ('MenuScrollerHeight', st.pixelMetric(QStyle.PM_MenuScrollerHeight)),
                       ('MenuTearoffHeight', st.pixelMetric(QStyle.PM_MenuTearoffHeight)),
                       ('MenuDesktopFrameWidth', st.pixelMetric(QStyle.PM_MenuDesktopFrameWidth)),
                       #('CheckListButtonSize', st.pixelMetric(QStyle.PM_CheckListButtonSize)),
                       #('CheckListControllerSize', st.pixelMetric(QStyle.PM_CheckListControllerSize)),
                       ('HeaderMarkSize', st.pixelMetric(QStyle.PM_HeaderMarkSize)),
                       ('HeaderGripMargin', st.pixelMetric(QStyle.PM_HeaderGripMargin)),
                       ('HeaderMargin', st.pixelMetric(QStyle.PM_HeaderMargin)),
                       ('SpinBoxSliderHeight', st.pixelMetric(QStyle.PM_SpinBoxSliderHeight)),
                       ('ToolBarIconSize', st.pixelMetric(QStyle.PM_ToolBarIconSize)),
                       ('SmallIconSize', st.pixelMetric(QStyle.PM_SmallIconSize)),
                       ('LargeIconSize', st.pixelMetric(QStyle.PM_LargeIconSize)),
                       ('FocusFrameHMargin', st.pixelMetric(QStyle.PM_FocusFrameHMargin)),
                       ('FocusFrameVMargin', st.pixelMetric(QStyle.PM_FocusFrameVMargin)),
                       ('IconViewIconSize', st.pixelMetric(QStyle.PM_IconViewIconSize)),
                       ('ListViewIconSize', st.pixelMetric(QStyle.PM_ListViewIconSize)),
                       ('ToolTipLabelFrameWidth', st.pixelMetric(QStyle.PM_ToolTipLabelFrameWidth)),
                       ('CheckBoxLabelSpacing', st.pixelMetric(QStyle.PM_CheckBoxLabelSpacing)),
                       ('RadioButtonLabelSpacing', st.pixelMetric(QStyle.PM_RadioButtonLabelSpacing)),
                       ('TabBarIconSize', st.pixelMetric(QStyle.PM_TabBarIconSize)),
                       ('SizeGripSize', st.pixelMetric(QStyle.PM_SizeGripSize)),
                       ('MessageBoxIconSize', st.pixelMetric(QStyle.PM_MessageBoxIconSize)),
                       ('ButtonIconSize', st.pixelMetric(QStyle.PM_ButtonIconSize)),
                       ('TextCursorWidth', st.pixelMetric(QStyle.PM_TextCursorWidth)),
                       ('TabBar_ScrollButtonOverlap', st.pixelMetric(QStyle.PM_TabBar_ScrollButtonOverlap)),
                       ('TabCloseIndicatorWidth', st.pixelMetric(QStyle.PM_TabCloseIndicatorWidth)),
                       ('TabCloseIndicatorHeight', st.pixelMetric(QStyle.PM_TabCloseIndicatorHeight)),
                       ('CustomBase', st.pixelMetric(QStyle.PM_CustomBase))
                       )

        self.tw = QTableWidget(len(self.params), 2)
        length = 0
        strin = ''
        for i in range(len(self.params)):
            item1 = QTableWidgetItem(self.params[i][0])
            item2 = QTableWidgetItem(str(self.params[i][1]))
            self.tw.setItem(i, 0, item1)
            self.tw.setItem(i, 1, item2)
        self.setCentralWidget(self.tw)

        # fm = QFontMetrics(self.tw.font())
        fm = QFontMetrics(self.tw.item(1, 1).font())
        # fm = self.tw.fontMetrics()
        for param in self.params:
            l = fm.size(1, self.tr(param[0])).width()
            if l > length:
                length = l
                strin = self.tr(param[0])
        print
        'MaxWidth: {0}, for string: {1}'.format(length, strin)
        self.tw.setColumnWidth(0, length)

        appFont = self.app.font()
        cellFont = self.tw.item(1, 1).font()
        tableFont = self.tw.font()
        print
        appFont
        print
        cellFont
        print
        tableFont
        print
        fm
        # print 'TitleBarHeight: {0}'.format(app.upperTape)
        # print 'MdiSubWindowFrameWidth: {0}'.format(app.edge)


app = MyApp(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec_())