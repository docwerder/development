import sys
import os
from PySide2.QtGui import QPixmap
from PySide2 import QtCore
from PySide2.QtCore import Qt
from PySide2.QtGui import QPixmap
from PySide2.QtCore import QThread
from PySide2.QtCore import Signal as pyqtSignal
os.environ['QT_MAC_WANTS_LAYER'] = '1'
from PySide2.QtWidgets import (
    QApplication, QVBoxLayout, QHBoxLayout, QGridLayout, QLineEdit,
    QMainWindow, QWidget, QPushButton, QComboBox, QLabel, QListWidget,
    QFileDialog, QFrame, QMessageBox
)
#from emat_mfl_combined.applications.pdw_upload.analysis_tools.path2proj import Path2ProjAnomaliesGeneral
import pathlib
import os
import pandas as pd
from tabulate import tabulate

class QHLine(QFrame):
    def __init__(self):
        super(QHLine, self).__init__()
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)

class WindowFindProperties(QMainWindow):
    def __init__(self, x_pos_parent_window, y_pos_parent_window, width_parent_window):
        super().__init__()

        self.x_pos_parent_window = x_pos_parent_window
        self.y_pos_parent_window = y_pos_parent_window
        self.width_parent_window = width_parent_window

        self.setWindowTitle("GUI Find properties V0.5 - Manual edition!")

        ###################################################
        # Define the layout !!
        ###################################################

        # Create the complete layout
        self.complete_layout = QVBoxLayout()

        # Layout for label and Rosen logo
        self.label_pic_layout = QHBoxLayout()

        # Define labels for header and Rosen_logo
        self.lbl_find_props = QLabel("Find properties")
        self.lbl_find_props.setStyleSheet("font-size: 16px;" "color: rgba(44, 44, 125, 255);")
        self.lbl_rosen_logo = QLabel("Rosen logo")
        self.pixmap = QPixmap("rosen_logo.png")
        #self.lbl_rosen_logo.setPixmap(QPixmap("rosen_logo.png"))
        self.scaled_picture = self.pixmap.scaled(self.lbl_rosen_logo.size() / 4, QtCore.Qt.KeepAspectRatio)
        self.lbl_rosen_logo.setPixmap(self.scaled_picture)
        self.lbl_rosen_logo.setScaledContents(True)

        # Fill the label_pic_layout
        self.label_pic_layout.addWidget(self.lbl_find_props)
        self.label_pic_layout.addStretch()  # Distribute the widgets equidistant
        self.label_pic_layout.addWidget(self.lbl_rosen_logo)

        # Define horizontal line
        self.hor_line_1_layout = QHBoxLayout()
        self.hor_line_1_layout.addWidget(QHLine())

        # Define label of query_string
        self.lbl_query_str_layout = QHBoxLayout()
        self.lbl_query_str = QLabel("Query string (use cases)")
        #self.lbl_query_str.setStyleSheet("background-color: green;")
        self.lbl_query_str_layout.addWidget(self.lbl_query_str)

        self.use_case_layout = QHBoxLayout()
        self.use_case_combobox = QComboBox()
        self.use_case_combobox.addItem("REF_WT_ASS ge 0")
        self.use_case_combobox.addItem("LogDist ge 0")
        self.use_case_layout.addWidget(self.use_case_combobox)

        self.btn_execute_query = QPushButton("Execute query!")
        self.use_case_layout.addWidget(self.btn_execute_query)

        # Define label for modifications
        self.lbl_modifications_layout = QHBoxLayout()
        self.lbl_modifications =QLabel('Modifications')
        self.lbl_modifications_layout.addWidget(self.lbl_modifications)

        # Define label for the modifications
        self.modifications_layout = QGridLayout()
        self.lbl_lower_limit = QLabel("Lower limit")
        self.lbl_upper_limit = QLabel("Upper limit")
        self.lower_limit_edit = QLineEdit()
        self.upper_limit_edit = QLineEdit()
        self.modifications_layout.addWidget(self.lbl_lower_limit, 0, 0)
        self.modifications_layout.addWidget(self.lower_limit_edit, 0, 1)
        self.modifications_layout.addWidget(self.lbl_upper_limit, 1, 0)
        self.modifications_layout.addWidget(self.upper_limit_edit, 1, 1)

        # Fill the complete layout
        self.complete_layout.addLayout(self.label_pic_layout)
        #self.complete_layout.addStretch(1)
        self.complete_layout.addLayout(self.hor_line_1_layout)
       # self.complete_layout.addStretch(1)
        self.complete_layout.addLayout(self.lbl_query_str_layout)
        self.complete_layout.addStretch(1)
        self.complete_layout.addLayout(self.use_case_layout)
        self.complete_layout.addStretch(1)
        self.complete_layout.addLayout(self.lbl_modifications_layout)
        self.complete_layout.addStretch(1)
        self.complete_layout.addLayout(self.modifications_layout)

        # Set the hand-made complete_layout in a superordinate QWidget called dummy_widget
        self.dummy_widget = QWidget()
        self.dummy_widget.setLayout(self.complete_layout)
        self.setCentralWidget(self.dummy_widget)

        self.use_case_combobox.currentIndexChanged.connect(self.use_case_item_changed)

        # ##
        # Define signal and slots
        # ####



    def use_case_item_changed(self):
        print('Current item: ', self.use_case_combobox.currentText())
        print('Current...: ', self.use_case_combobox.currentIndex())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WindowFindProperties(200, 330, 800)
    window.show()
    sys.exit(app.exec_())
