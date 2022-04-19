import numpy as np
import sys
import os
import pandas as pd
import seaborn as sns
os.environ['QT_MAC_WANTS_LAYER'] = '1'

from PySide2 import QtCore
from PySide2.QtGui import QPixmap
from PySide2 import QtWidgets

from PySide2.QtWidgets import (
    QApplication, QVBoxLayout, QHBoxLayout,
    QFormLayout, QGridLayout,
    QPushButton, QCheckBox, QListWidget, QFrame,
    QWidget, QMainWindow, QLineEdit, QLabel
)
from PySide2.QtGui import QFontMetrics
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


def text_size(self, text):
    """ Returns the size (dx,dy) of the specified text string (using the
        current control font).
    """
    rect = QFontMetrics(self.control.font()).boundingRect(text)

    return (rect.width(), rect.height())


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


class WindowShowFeatureOverview(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My Layout of feature overview - hbox/vbox")

        # #############################################
        #  Define the layout
        # #############################################
        # Create the complete layout
        self.complete_layout = QVBoxLayout()

        # Layout for label and Rosen_logo
        self.label_pic_layout = QHBoxLayout()

        # Define label for header and Rosen_logo
        self.lbl_feature_overview = QLabel("Feature overview")
        self.lbl_feature_overview.setStyleSheet("font-size: 16px;" "color: green")
        self.lbl_rosen_logo = QLabel("Rosen logo")
       # self.lbl_rosen_logo.setPixmap(QPixmap("rosen_logo.png"))
        self.pixmap = QPixmap("rosen_logo.png")
        print('size of picturew: ', self.lbl_rosen_logo.size()/2)
        scaled = self.pixmap.scaled(self.lbl_rosen_logo.size() / 4, QtCore.Qt.KeepAspectRatio)
        self.lbl_rosen_logo.setPixmap(scaled)
        self.lbl_rosen_logo.setScaledContents(False)

        # Fill the label_pic_layout
        self.label_pic_layout.addWidget(self.lbl_feature_overview)
        self.label_pic_layout.addStretch()              # Distribute the widget equidistant
        self.label_pic_layout.addWidget(self.lbl_rosen_logo)

        # Layout for buttons - now it's a QHbox.
        self.btn_layout = QHBoxLayout()

        # Define buttons..
        self.btn_load_features_for_overview = QPushButton("Load features for overview")
        self.btn_1_dummy = QPushButton("Dummy button 1")
        self.btn_2_dummy = QPushButton("Dummy button 2")

        self.btn_layout.addWidget(self.btn_load_features_for_overview)
        self.btn_layout.addWidget(self.btn_1_dummy)
        self.btn_layout.addWidget(self.btn_2_dummy)

        # Define layout for a horizontal line...
        self.hor_lin_1_layout = QHBoxLayout()
        self.hor_lin_1_layout.addWidget(QHLine())

        # Define layout for a horizontal line...
        self.hor_lin_2_layout = QHBoxLayout()
        self.hor_lin_2_layout.addWidget(QHLine())

        self.lbl_line_layout = QVBoxLayout()

        self.lbl_line = QLabel('Available lines')
        self.list_lines = QListWidget()
        self.list_lines.setFixedWidth(140)
        # self.test_text = QLabel("hello till")
        # print('self.test_text.text: ', self.test_text.text())
        # t_metrics = self.test_text.fontMetrics()
        # print('t_metrics: ', t_metrics.width(self.test_text.text()))
        list_of_lines = ['30305306', '30TUCCAS', '28LIBASSTRTTtzztzztzzt']
        self.list_lines.addItems(['30305306', '30TUCCAS', '28LIBASSTRTTtzztzztzzt'])
        max_length_of_elements = max(list_of_lines, key=len)
        self.max_element = QLabel(max_length_of_elements)
        max_width_of_line_list = self.max_element.fontMetrics().width(max_length_of_elements)
        self.list_lines.setFixedWidth(max_width_of_line_list * 1.2)
        self.lbl_line_layout.addWidget(self.lbl_line)
        self.lbl_line_layout.addWidget(self.list_lines)




        # Define layout-place for the canvas
        self.canvas_layout = QVBoxLayout()

        self.fig = Figure(figsize=(7, 5), dpi=65, facecolor=(1, 1, 1), edgecolor=(0, 0, 0))
        # print('type: ', type(self.fig))
        # Define Canvas and plot an example sinus curve
        self.canvas_feature_overview = FigureCanvas(self.fig)
        self.figure_feature_overview = self.fig.add_subplot(111)
        self.figure_feature_overview.clear()
        self.figure_feature_overview.set_ylabel('volts')
        self.figure_feature_overview.set_title('A sine wave')
        t = np.arange(0.0, 1.0, 0.01)
        s = np.sin(2 * np.pi * t)

        line = self.figure_feature_overview.plot(t, s, lw=2)
        # With the command below, the plot will be shown
        self.canvas_layout.addWidget(self.canvas_feature_overview)

        # Define an additional Canvas below the first one, because of QVBoxLayout()
        self.fig_2 = Figure(figsize=(7, 5), dpi=65, facecolor=(1, 1, 1), edgecolor=(0, 0, 0))
        self.canvas_feature_overview_uploaded_features = FigureCanvas(self.fig_2)
        self.figure_overview_uploaded_features = self.fig_2.add_subplot(111)
        self.figure_overview_uploaded_features.clear()
        self.figure_overview_uploaded_features.set_ylabel('volts')
        self.figure_overview_uploaded_features.set_title('A cosinus wave')
        t = np.arange(0.0, 1.0, 0.01)
        c = np.cos(2 * np.pi * t)
        line = self.figure_overview_uploaded_features.plot(t, c, lw=3)
        # With the command below, the plot will be shown
        self.canvas_layout.addWidget(self.canvas_feature_overview_uploaded_features)


        # Define layout for canvas AND line display
        self.canvas_and_line_layout = QHBoxLayout()

        self.canvas_and_line_layout.addLayout(self.canvas_layout)
        self.canvas_and_line_layout.addLayout(self.lbl_line_layout)


        # Place the layout in the desired manner...
        self.complete_layout.addLayout(self.label_pic_layout)
        self.complete_layout.addLayout(self.hor_lin_1_layout)
        self.complete_layout.addLayout(self.btn_layout)
        self.complete_layout.addLayout(self.hor_lin_2_layout)
        self.complete_layout.addLayout(self.canvas_and_line_layout)


        # self.complete_layout.addLayout(self.canvas_layout)
        # Set the hand-made complete layout in a superordinate QWidget called dummy_widget
        dummy_widget = QWidget()
        dummy_widget.setLayout(self.complete_layout)
        self.setCentralWidget(dummy_widget)


        # #############################################
        #  End of definition of the layout
        # #############################################


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WindowShowFeatureOverview()
    window.show()
    sys.exit(app.exec_())

