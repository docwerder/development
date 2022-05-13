import sys
import os
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


class WindowShowFeatureSignals(QMainWindow):
    def __init__(self, x_pos_parent_window, y_pos_parent_window, width_parent_window):
        super().__init__()
        self.x_pos_parent_window = x_pos_parent_window
        self.y_pos_parent_window = y_pos_parent_window
        self.width_pos_parent_window = width_parent_window
        #self.setFixedWidth(600)
        self.setWindowTitle("My Layout of Show feature signals manual edition!")
        self.move(150, 100)
        self.resize(2000, 1200)


        # #############################################
        #  Define the layout
        # #############################################

        # Create the complete layout
        self.complete_layout = QVBoxLayout()

        # Layout for label and Rosen_logo
        self.label_pic_layout = QHBoxLayout()

        # Define label for header and Rosen_logo
        self.lbl_feature_overview = QLabel("Show Feature Signals - Manual edition!")
        self.lbl_feature_overview.setStyleSheet("font-size: 18px;" "color: rgb(44, 44, 126);")
        self.lbl_rosen_logo = QLabel("Rosen logo")
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

        # Define layout for load_btn
        self.load_xarray_btn_layout = QHBoxLayout()

        # Define widgets
        self.btn_load_anomalies_dir = QPushButton("Load xarray") # change the function. temporarly!
        self.lbl_anomalies_dir = QLineEdit("...")

        # Fill the layout with the widgets
        self.load_xarray_btn_layout.addWidget(self.btn_load_anomalies_dir)
        self.load_xarray_btn_layout.addWidget(self.lbl_anomalies_dir)

        # Define layout for horizontal line
        self.hor_line_2_layout = QHBoxLayout()
        self.hor_line_2_layout.addWidget(QHLine())

        # Define the label for chosen anomaly_dir:
        self.lbl_chosen_anomaly_dir_layout = QHBoxLayout()

        # Define the widgets within layout
        lineshort_name = "30305306" # TODO: Define the correct variable for lineshort_name
        self.lbl_chosen_anomaly_dir = QLabel("Available anomalies within the line: " + lineshort_name)
        self.lbl_chosen_anomaly_dir.setStyleSheet("font-size: 16px;" "color: rgb(44, 44, 126);")
        # Fill the layout with the widget
        self.lbl_chosen_anomaly_dir_layout.addWidget(self.lbl_chosen_anomaly_dir)

        # Define layout for horizontal line
        self.hor_line_3_layout = QHBoxLayout()
        self.hor_line_3_layout.addWidget(QHLine())


        self.general_vbox_layout = QVBoxLayout()
        # Define the layout, in which teh QFrame, nc-display and feature_signal are located
        self.qframe_nc_signals_display_layout = QHBoxLayout()



        self.layout_frame_left = QVBoxLayout()
        self.btn_show_anom_types = QPushButton("Show anomalies...")
        self.layout_left = QHBoxLayout()

        # Define layout for apply and cancel buttons
        self.btn_bar_layout = QHBoxLayout()
        self.apply_button = QPushButton("Apply...")
        self.cancel_button = QPushButton("Cancel...")

        # Fill the layout
        self.btn_bar_layout.addWidget(self.apply_button)
        self.btn_bar_layout.addWidget(self.cancel_button)




        self.layout_frame_right = QVBoxLayout()
        self.btn_show_all_features = QPushButton("Window of ALL feature signals")
        self.lbl_all_features_of_line = QLabel("Features of line: ")
        self.qplainedit_text = QPlainTextEdit()

        self.layout_right = QHBoxLayout()

        # Locate the QFrame and nc_display into the left layout
        #self.qframe = QFrame()
        self.frame_for_scrollarea = None
        self.frame_for_scrollarea_left = MyFrame()
        self.frame_total_left = self.frame_for_scrollarea_left.vbox
        self.frame_for_scrollarea_left.setLayout(self.frame_total_left)

        self.scrolling_area_left = QScrollArea()
        self.scrolling_area_left.setWidgetResizable(True)
        #self.layout_left.addWidget(self.scrolling_area_left)

        # Define the right site
        #self.frame_for_scrollarea_right = MyFrame()
        #self.frame_total_right = self.frame_for_scrollarea_right.vbox
        #self.frame_for_scrollarea_right.setLayout(self.frame_total_right)
        #self.scrolling_area_right = QScrollArea()
        #self.scrolling_area_right.setWidgetResizable(True)

        self.frame_for_scrollarea_right = QFrame()
        self.frame_for_scrollarea_right.setStyleSheet('background-color: grey;')
        #elf.frame_for_scrollarea_right.setWidgetResizable(True)

        #self.frame_for_scrollarea_right.setFrameShadow(QFrame.Sunken)

        self.layout_frame_left.addWidget(self.btn_show_anom_types)
        self.layout_frame_left.addWidget(self.scrolling_area_left, stretch=1)
        self.layout_frame_left.addLayout(self.btn_bar_layout)

        self.layout_frame_right.addWidget(self.btn_show_all_features)
        self.layout_frame_right.addWidget(self.lbl_all_features_of_line)
        self.layout_frame_right.addWidget(self.qplainedit_text)

        self.layout_right.addWidget(self.frame_for_scrollarea_right, stretch=1)
        #self.layout_right.addWidget(self.scrolling_area_right)


        self.btn_show_anom_types.clicked.connect(self.show_frame_left)


        self.qframe_nc_signals_display_layout.addLayout(self.layout_frame_left, stretch=20)
        self.qframe_nc_signals_display_layout.addLayout(self.layout_frame_right, stretch=20)
        self.qframe_nc_signals_display_layout.addLayout(self.layout_right, stretch=100)


        # Locate the QFrame and nc_display into the left layout
        self.nc_display = QPlainTextEdit()


        # Fill the complete_layout
        self.complete_layout.addLayout(self.label_pic_layout)
        self.complete_layout.addLayout(self.hor_line_1_layout)
        self.complete_layout.addLayout(self.load_xarray_btn_layout)
        self.complete_layout.addLayout(self.hor_line_2_layout)
        self.complete_layout.addLayout(self.lbl_chosen_anomaly_dir_layout)
        self.complete_layout.addLayout(self.hor_line_3_layout)
        self.complete_layout.addLayout(self.qframe_nc_signals_display_layout)
        # Define the overall layout in which the nc-files and signals are pasted..
        # As part of the vbox layout....

        # Set the hand-made complete layout in a superordinate QWidget called dummy_widget
        dummy_widget = QWidget()

        dummy_widget.setLayout(self.complete_layout)
        self.setCentralWidget(dummy_widget)

    def show_frame_left(self):

        if self.frame_for_scrollarea is None:
            self.frame_for_scrollarea = MyFrame()
            self.frame_total = self.frame_for_scrollarea.vbox

            self.frame_for_scrollarea.setLayout(self.frame_total)
            self.scrolling_area_left.setWidget(self.frame_for_scrollarea)
        else:
            self.frame_for_scrollarea.hide()
            self.frame_for_scrollarea = None



class MyFrame(QFrame):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)

        style = """MyFrame {
            border: 1px solid;
            background-color: white;
            }
            """
        self.setStyleSheet(style)
        self.vbox = QVBoxLayout()
        #self.frame_total = QVBoxLayout()
        #self.frame_total.addLayout(self.vbox)
        for i in range(1, 50):
            object = QCheckBox("Label inside Class")
            self.vbox.addWidget(object)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WindowShowFeatureSignals(200, 500, 1000)
    #window2 = WindowFeatureUpload_qframe()
    window.show()
    sys.exit(app.exec_())