import numpy as np
import sys
import os
import pandas as pd
import seaborn as sns

import progressbar_QThread

os.environ['QT_MAC_WANTS_LAYER'] = '1'

from PySide2 import QtCore
from PySide2.QtGui import QPixmap

from PySide2.QtWidgets import (
    QApplication, QVBoxLayout, QHBoxLayout,
    QComboBox, QPlainTextEdit, QFormLayout, QGridLayout,
    QPushButton, QSplitter, QCheckBox, QListWidget, QFrame,
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
        self.btn_1_dummy = QPushButton("Dummy button 1")
        self.btn_2_dummy = QPushButton("Dummy button 2")

        # Fill the layout with the buttons...
        self.btn_layout.addWidget(self.btn_show_anomalies_frame)
        self.btn_layout.addWidget(self.btn_1_dummy)
        self.btn_layout.addWidget(self.btn_2_dummy)

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
        #self.frame_splitter_layout = QHBoxLayout()

        #self.frame_frame_output = QFrame()
        #self.frame_frame_output.setFrameStyle(QFrame.Panel | QFrame.Sunken)

        #self.frame_calculation_output = QFrame()
        #self.frame_calculation_output.setFrameStyle(QFrame.Panel | QFrame.Sunken)

        #self.frame_output_terminal = QFrame()
        #self.frame_output_terminal.setFrameStyle(QFrame.Panel | QFrame.Sunken)

        #self.splitter1 = QSplitter(QtCore.Qt.Horizontal)
        #self.splitter1.addWidget(self.frame_frame_output)
        #self.splitter1.addWidget(self.frame_calculation_output)
        #self.splitter1.addWidget(self.frame_output_terminal)

        #self.frame_splitter_layout.addWidget(self.splitter1)


        # Define the widgets.. QFrame and QPlainTextEdit... (twice)
        #self.frame_for_anomalies = QFrame()
        self.frame_for_anomalies.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.calculation_terminal = QPlainTextEdit()
        self.output_terminal = QPlainTextEdit()

        # Fill the layout with the widgets...
        # self.qframe_qplaintextedit_layout.addWidget(self.frame_for_anomalies)
        # self.qframe_qplaintextedit_layout.addWidget(self.calculation_terminal)
        # self.qframe_qplaintextedit_layout.addWidget(self.output_terminal)

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
        #self.complete_layout.addLayout(self.frame_splitter_layout)

        #self.complete_layout.addLayout(self.frame_qplaintextedit_layout)
        #self.complete_layout.addStretch()

        # Set the hand-made complete layout in a superordinate QWidget called dummy_widget
        dummy_widget = QWidget()

        dummy_widget.setLayout(self.complete_layout)
        self.setCentralWidget(dummy_widget)


        # #############################################
        #  End of definition of the layout
        # #############################################

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WindowFeatureUpload(200, 150, 800)
    window.show()
    sys.exit(app.exec_())