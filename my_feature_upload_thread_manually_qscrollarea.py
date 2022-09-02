#import numpy as np
import sys
import os
#import pandas as pd
#import seaborn as sns


import progressbar_QThread

os.environ['QT_MAC_WANTS_LAYER'] = '1'

from typing import Optional, List, Dict
from PySide2 import QtCore
from PySide2.QtGui import QPixmap
from PySide2.QtCore import Qt

from PySide2.QtWidgets import (
    QApplication, QVBoxLayout, QHBoxLayout, QCheckBox,
    QComboBox, QPlainTextEdit, QProgressBar, QFormLayout, QGridLayout,
    QPushButton, QSplitter, QCheckBox, QListWidget, QFrame, QScrollArea,
    QWidget, QMainWindow, QLineEdit, QLabel
)

from PySide2.QtGui import QFontMetrics


class QHLine(QFrame):
    def __init__(self):
        super(QHLine, self).__init__()
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)


class QVLine(QFrame):
    def __init__(self):
        super(QVLine, self).__init__()
        self.setFrameShape(QFrame.VLine)
        self.setFrameShadow(QFrame.Sunken)


class WindowFeatureUpload(QMainWindow):
    def __init__(self, x_pos_parent_window, y_pos_parent_window, width_parent_window):
        super().__init__()
        #dummy_widget = QWidget()
        self.x_pos_parent_window = x_pos_parent_window
        self.y_pos_parent_window = y_pos_parent_window
        self.width_pos_parent_window = width_parent_window
        #self.setFixedWidth(600)
        self.setWindowTitle("My Layout of feature upload ")

        # #############################################
        #  Define the layout
        # #############################################

        # Create the complete layout
        self.complete_layout = QVBoxLayout()

        # Layout for label and Rosen_logo
        self.label_pic_layout = QHBoxLayout()

        # Define label for header and Rosen_logo
        self.lbl_feature_overview = QLabel("Feature upload")
        self.lbl_feature_overview.setStyleSheet("font-size: 18px;" "color: rgb(44, 44, 126);")
        self.lbl_rosen_logo = QLabel("Rosen logo")
        # self.lbl_rosen_logo.setPixmap(QPixmap("rosen_logo.png"))
        self.pixmap = QPixmap("rosen_logo.png")
        print('size of picturew: ', self.lbl_rosen_logo.size() / 2)
        scaled = self.pixmap.scaled(self.lbl_rosen_logo.size() / 4, QtCore.Qt.KeepAspectRatio)
        self.lbl_rosen_logo.setPixmap(scaled)
        self.lbl_rosen_logo.setScaledContents(False)

        # Fill the label_pic_layout
        self.label_pic_layout.addWidget(self.lbl_feature_overview)
        self.label_pic_layout.addStretch()
        self.label_pic_layout.addWidget(self.lbl_rosen_logo)

        # Define layout for horizontal line
        self.hor_line_1_layout = QHBoxLayout()
        self.hor_line_1_layout.addWidget(QHLine())

        # Define layout for PDW-server and chosing_box.
        self.pdw_server_layout = QHBoxLayout()
        #self.groups.setAlignment(Qt.AlignTop)
        self.pdw_server_layout.setAlignment(QtCore.Qt.AlignLeft)
        # Define label for pdw_server and drop-down box
        self.lbl_pdw_server = QLabel("PDW-Server: ")
        self.lbl_pdw_server.setStyleSheet("font-size: 14px;" "color: rgb(44, 44, 126);")
        self.chose_pdw_server = QComboBox()
        #self.chose_pdw_server.
        for cnts in ['http://pdw-lin.roseninspection.net/pdw-emat', 'http://pdw-lin.roseninspection.net/pdw-sandbox']:
            self.chose_pdw_server.addItem(cnts)

        # Fill the layout with the widgets
        # IMPORTANT! With stretch we can controll the ratio between the widgets in one layout!!
        self.pdw_server_layout.addWidget(self.lbl_pdw_server, stretch=1)
        self.pdw_server_layout.addWidget(self.chose_pdw_server, stretch=4)

        # Define layout for horizontal line
        self.hor_line_2_layout = QHBoxLayout()
        self.hor_line_2_layout.addWidget(QHLine())

        # Define layout for load_btn
        self.load_xarray_btn_layout = QHBoxLayout()

        # Define widgets
        self.btn_load_anomalies_dir = QPushButton("Load xarray-dir...")
        self.lbl_anomalies_dir = QLineEdit("...")

        # Fill the layout with the widgets
        self.load_xarray_btn_layout.addWidget(self.btn_load_anomalies_dir)
        self.load_xarray_btn_layout.addWidget(self.lbl_anomalies_dir)

        # Define layout for horizontal line
        self.hor_line_3_layout = QHBoxLayout()
        self.hor_line_3_layout.addWidget(QHLine())

        # Layout for buttons - now it's a QHbox.
        self.btn_layout = QHBoxLayout()

        # Define buttons..
        self.btn_show_anomalies_frame = QPushButton("Show anomalies of chosen line")
        self.btn_show_scrollarea = QPushButton("Show scrollarea")
        self.btn_show_qframe = QPushButton("Show Qframe alone")

        # Fill the layout with the buttons...
        self.btn_layout.addWidget(self.btn_show_anomalies_frame)
        self.btn_layout.addWidget(self.btn_show_scrollarea)
        self.btn_layout.addWidget(self.btn_show_qframe)

        # Define layout for horizontal line
        self.hor_line_4_layout = QHBoxLayout()
        self.hor_line_4_layout.addWidget(QHLine())

        # Define the label for chosen anomaly_dir:
        self.lbl_chosen_anomaly_dir_layout = QHBoxLayout()

        # Define the widgets within layout
        lineshort_name = "30305306"
        self.lbl_chosen_anomaly_dir = QLabel("Available anomalies within the line: " + lineshort_name)
        self.lbl_chosen_anomaly_dir.setStyleSheet("font-size: 16px;" "color: rgb(44, 44, 126);")
        # Fill the layout with the widget
        self.lbl_chosen_anomaly_dir_layout.addWidget(self.lbl_chosen_anomaly_dir)

        # Define layout for horizontal line
        self.hor_line_5_layout = QHBoxLayout()
        self.hor_line_5_layout.addWidget(QHLine())

        # NOW. New widget types: QFrame and QPlainTextEdit...
        # Trying to handle wth qsplitter.
        # Link: https://zetcode.com/gui/pysidetutorial/widgets2/
        # First: Define the layout
        # self.frame_splitter_layout = QHBoxLayout()
        #
        # self.frame_frame_output = QFrame()
        # self.frame_frame_output.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        #
        # self.frame_calculation_output = QFrame()
        # self.frame_calculation_output.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        #
        # self.frame_output_terminal = QFrame()
        # self.frame_output_terminal.setFrameStyle(QFrame.Panel | QFrame.Sunken)


        # New version: First: Only QPlainTextEdit-Widgets....
        # Additional try: With scroll-Area!

        self.layout_for_frame = QHBoxLayout()
        self.frame_for_scrollarea = None

        self.scrolling_area = QScrollArea()
        self.scrolling_area.setWidgetResizable(True)

        self.layout_for_frame.addWidget(self.scrolling_area)


        self.calculation_terminal = QPlainTextEdit()
        self.output_terminal = QPlainTextEdit()



        #self.scrollframe.setStyleSheet('background-color: green;')
        #self.scrollframe.show()

        ### self.scroll_area = QScrollArea()
        ### self.scroll_area_widget = QWidget()
        ### self.vbox_in_scroll_area_widget = QVBoxLayout()

        #for i in range(1,50):
        #    object = QLabel("Label Test Scroll Area!")
        #    self.vbox_in_scroll_area_widget.addWidget(object)

        ### self.scroll_area_widget.setLayout(self.vbox_in_scroll_area_widget)

        # Scroll Area Properties
        ### self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        ### self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        ### self.scroll_area.setWidgetResizable(True)
        ### self.scroll_area.setWidget(self.scroll_area_widget)


        # Define layout and fill this three QPlainTextEdit-Widgets..
        self.qplainedittext_layout = QHBoxLayout()

        ### self.qplainedittext_layout.addWidget(self.scroll_area, stretch=1)
        self.qplainedittext_layout.addLayout(self.layout_for_frame, stretch=1)
        self.qplainedittext_layout.addWidget(self.calculation_terminal, stretch=1)
        self.qplainedittext_layout.addWidget(self.output_terminal, stretch=1)

        # Define layout for horizontal line
        self.hor_line_6_layout = QHBoxLayout()
        self.hor_line_6_layout.addWidget(QHLine())

        # Define the Upload summary labels.

        self.lbl_upload_layout = QHBoxLayout()

        # Define the labels.
        self.lbl_upload_summary = QLabel("Upload summary:")
        self.lbl_upload_summary.setStyleSheet("font-size: 16px;" "color: rgb(44, 44, 126);")
        self.lbl_upload_progress = QLabel("Upload progress:")
        self.lbl_upload_progress.setStyleSheet("font-size: 16px;" "color: rgb(44, 44, 126);")

        # Fill the layout
        self.lbl_upload_layout.addWidget(self.lbl_upload_summary)
        self.lbl_upload_layout.addWidget(self.lbl_upload_progress)

        # Define summary and progress status
        self.summary_and_progress_layout = QHBoxLayout()

        # Define the widgets
        self.upload_summary = QLabel('Detailed information about the upload...')
        self.upload_progress = QProgressBar()
        self.upload_progress.setGeometry(30, 40, 200, 25)
        self.upload_progress.adjustSize()
        #self.upload_progress.setStyleSheet("QProgressBar::chunk {background-color: #2196F3; height: 30px; width: 20px; margin: 1.5px;}")
        # Fill the layout..
        self.summary_and_progress_layout.addWidget(self.upload_summary)
        self.summary_and_progress_layout.addWidget(self.upload_progress)


        # Fill the complete_layout
        self.complete_layout.addLayout(self.label_pic_layout)
        self.complete_layout.addLayout(self.hor_line_1_layout)
        #self.complete_layout.addStretch()
        self.complete_layout.addLayout(self.pdw_server_layout)
        self.complete_layout.addLayout(self.hor_line_2_layout)
        self.complete_layout.addLayout(self.load_xarray_btn_layout)
        self.complete_layout.addLayout(self.hor_line_3_layout)
        self.complete_layout.addLayout(self.btn_layout)
        self.complete_layout.addLayout(self.hor_line_4_layout)
        self.complete_layout.addLayout(self.lbl_chosen_anomaly_dir_layout)
        self.complete_layout.addLayout(self.hor_line_5_layout)
        self.complete_layout.addLayout(self.qplainedittext_layout)
        self.complete_layout.addLayout(self.hor_line_6_layout)
        self.complete_layout.addLayout(self.lbl_upload_layout)
        self.complete_layout.addLayout(self.summary_and_progress_layout)

        #self.complete_layout.addLayout(self.frame_qplaintextedit_layout)
        #self.complete_layout.addStretch()

        # Set the hand-made complete layout in a superordinate QWidget called dummy_widget
        dummy_widget = QWidget()

        dummy_widget.setLayout(self.complete_layout)
        self.setCentralWidget(dummy_widget)


        # #############################################
        #  End of definition of the layout
        # #############################################

        # Define signals and slots
        #self.frame_scrollarea = None
        self.btn_show_scrollarea.clicked.connect(self.show_scrollarea)
        self.qframe_alone = None
        self.btn_show_qframe.clicked.connect(self.show_qframe_alone)

        self.btn_show_anomalies_frame.clicked.connect(self.show_qframe_and_scrollarea)

    def show_scrollarea(self):

        # Define the QFrame class and paste it at the right place...

        if self.frame_for_scrollarea is None:
            self.frame_for_scrollarea = FrameScrollArea()
            self.create_btn_layout()
            #self.vbox = QVBoxLayout() # Define QHBoxLayout() for containing multiple subwidgets.. here QLabels
            #self.vbox = self.frame_for_scrollarea.vbox # normally right?
            self.frame_total = self.frame_for_scrollarea.frame_total

            # for i in range(1, 50):
            #     object = QCheckBox("TextLabel for scrolling")
            #     self.vbox.addWidget(object)

            # self.frame_for_scrollarea.setLayout(self.vbox)  # normally right??
            self.frame_for_scrollarea.setLayout(self.frame_total)
            self.scrolling_area.setWidget(self.frame_for_scrollarea)

        else:
            self.frame_for_scrollarea.hide()
            self.frame_for_scrollarea = None

            # Scroll Area & Properties
            # self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
            # self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            # self.scroll.setWidgetResizable(True)

            # IMPORTANT: Fill the scrollarea-widget with the generic-QWidget-Object,
            # which contains the vboxlayout and the qlabels...
            # self.scroll.setWidget(self.widget)

            # below code is the important one!
            # self.scrolling_area.setWidget(self.scroll)
            #self.frame_scrollarea = FrameScrollArea(parent=self)
            #self.frame_scrollarea.setStyleSheet("background-color: rgba(0, 155, 255, 80);")
            #self.frame_scrollarea.move(self.frame_left.x(), self.frame_left.y())
            #self.frame_scrollarea.resize(self.frame_left.width(), self.frame_left.height())

            #self.scroll.setWidget(self.frame_scrollarea)
            #self.scroll.setWidget(self.frame_left)


            #self.frame_scrollarea.addWidget(self.scroll)
            #self.scroll.setWidget(self.widget)
            #self.scroll.show()
            #self.frame_scrollarea.
    def create_btn_layout(self):
        print('additional function output...')
        self.frame_btn_layout = QHBoxLayout()
        self.evaluate_button = QPushButton("Evaluate ...")
        self.write_button = QPushButton("Write ...")
        self.cancel_button = QPushButton("Cancel ...")
        self.frame_btn_layout.addWidget(self.evaluate_button)
        self.frame_btn_layout.addWidget(self.write_button)
        self.frame_btn_layout.addWidget(self.cancel_button)
        self.qplainedittext_layout.addLayout(self.frame_btn_layout, stretch=1)

    def show_qframe_alone(self):

        print('QFrame is none')
        if self.qframe_alone is None:
            self.qframe_alone = QFrame(parent=self)
            self.qframe_alone.setStyleSheet("background-color: rgba(0, 155, 255, 80);")

            self.qframe_alone.move(self.calculation_terminal.x(), self.calculation_terminal.y())
            self.qframe_alone.resize(self.calculation_terminal.width(), self.calculation_terminal.height())
            self.qframe_alone.show()
        else:
            self.qframe_alone.hide()
            self.qframe_alone = None

    def show_qframe_and_scrollarea(self):
        print('going into summary function...')
        self.scroll_1 = QScrollArea()
        self.widget_1 = QWidget()
        self.frame_1 = QFrame()
        self.vbox_1 = QVBoxLayout()  # Define QHBoxLayout() for containing multiple subwidgets.. here QLabels

        for i in range(1, 50):
            object_1 = QCheckBox("TextLabel for scrolling")
            self.vbox_1.addWidget(object_1)
        self.widget_1.setLayout(self.vbox_1)

        self.frame_1.addWidget(self.widget_1)

        # Scroll Area & Properties
        self.scroll_1.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll_1.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_1.setWidgetResizable(True)

        self.scroll_1.setWidget(self.widget_1)
        self.scrolling_area.setWidget(self.scroll_1)



class FrameScrollArea(QFrame):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)

        style = """FrameScrollArea {
            border: 1px solid;
            background-color: rgba(0, 155, 155, 80);
            }
            """
        self.setStyleSheet(style)


        # Define the layout for adding the buttons to the scrollarea
        self.vbox = QVBoxLayout()
        self.frame_total = QVBoxLayout()

        #self.frame_btn_layout = QHBoxLayout()

        # Define the buttons.
        #self.evaluate_button = QPushButton("Evaluate ...")
        #self.write_button = QPushButton("Write ...")
        #self.cancel_button = QPushButton("Cancel ...")

        # Fill the btn_layout
        #self.frame_btn_layout.addWidget(self.evaluate_button)
        #self.frame_btn_layout.addWidget(self.write_button)
        #self.frame_btn_layout.addWidget(self.cancel_button)

        self.frame_total.addLayout(self.vbox)
        #self.frame_btn_layout = None
        #self.frame_total.addLayout(self.frame_btn_layout)


        for i in range(1, 50):
            object = QCheckBox("Label inside Class")
            self.frame_total.addWidget(object)


#
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WindowFeatureUpload(200, 500, 1000)
    #window2 = WindowFeatureUpload_qframe()
    window.show()
    sys.exit(app.exec_())