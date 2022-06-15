import sys
from PySide2.QtGui import QPixmap

from PySide2.QtWidgets import QApplication, QGridLayout, QMainWindow, QWidget, QPushButton, QLabel

# Important: the next two lines have to be imported after the Pyside2 imports.
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas  # noqa: F401
import matplotlib.pyplot as plt  # noqa: F401

# seaborn has to be imported after the matplotlib modules


# Module import
# Scanning directories
from emat_mfl_combined.applications.pdw_upload.pdw.pdw_manual_edition \
    import scan_directories_manually as window_scan_directories

# Feature overview
from emat_mfl_combined.applications.pdw_upload.pdw.pdw_manual_edition \
    import feature_overview_manually as window_feature_overview

# Feature upload
from emat_mfl_combined.applications.pdw_upload.pdw.pdw_manual_edition \
    import feature_upload_manually as window_feature_upload

# Ongoing code!
# Feature signals
from emat_mfl_combined.applications.pdw_upload.pdw.pdw_manual_edition \
    import my_show_feature_signals_manually as window_feature_signals


# import seaborn as sns
# import pandas as pd

sys.path.append(r'C:\Users\JWingbermuehle\Repos\EmatMflCombined')


class Main_PDW_GUI(QMainWindow):
    def __init__(self, x_pos_main_pdw_gui, y_pos_main_pdw_gui, width_main_gui, height_main_gui, parent=None):
        super(Main_PDW_GUI, self).__init__(parent)

        self.setWindowTitle('PDW Main GUI V0.8 - Manual edition!')
        self.x_pos_main_pdw_gui = x_pos_main_pdw_gui
        self.y_pos_main_pdw_gui = y_pos_main_pdw_gui
        self.width_main_gui = width_main_gui
        self.height_main_gui = height_main_gui

        # For control
        # print('x_pos_main_pdw_gui_init: ', self.x_pos_main_pdw_gui)
        # print('y_pos_main_pdw_gui_init: ', self.y_pos_main_pdw_gui)

        self.move(self.x_pos_main_pdw_gui, self.y_pos_main_pdw_gui)
        # print('width: ', self.width_main_gui)
        # print('height: ', self.height_main_gui)

        # Define the main layout with buttons
        # Define 'headline' consisting of header and logo ...
        lbl_pdw = QLabel('PDW GUI 0.5 - Manual edition !')
        lbl_pdw.setStyleSheet("font-size: 16px;" "color: green")
        lbl_logo = QLabel("Rosen_logo")
        lbl_logo.setPixmap(QPixmap("rosen_logo.png"))
        lbl_logo.setScaledContents(False)

        # Define Grid of pushbuttons... and their actions...
        self.btn_scanning_dirs = QPushButton('Scanning directories')
        self.scanning_dirs_window = None
        self.btn_scanning_dirs.clicked.connect(self.show_scanning_dirs_window)

        self.btn_feature_overview = QPushButton('Feature overview')
        self.window_feature_overview = None
        self.btn_feature_overview.clicked.connect(self.show_feature_overview)

        self.btn_feature_upload = QPushButton('Feature upload')
        self.window_feature_upload = None
        self.btn_feature_upload.clicked.connect(self.show_feature_upload)

        self.btn_show_feature_signals = QPushButton('Show feature signals')
        self.window_show_feature_signals = None
        self.btn_show_feature_signals.clicked.connect(self.show_feature_signals)

        # Now: Define the Alignment of the buttons and labels via qgridlayout.
        # Define the layout-form, in which the widgets should be aligned...
        # and add the widgets
        layout = QGridLayout()
        layout.addWidget(lbl_pdw, 0, 0)
        layout.addWidget(lbl_logo, 0, 1)
        layout.addWidget(self.btn_scanning_dirs, 1, 0)
        layout.addWidget(self.btn_feature_overview, 1, 1)
        layout.addWidget(self.btn_feature_upload, 2, 0)
        layout.addWidget(self.btn_show_feature_signals, 2, 1)

        # Define the scretching of the rows...
        # Dont how exactly how it works...
        # layout.setRowStretch(0, 0)
        # layout.setRowStretch(1, 6)
        # layout.setRowStretch(2, 6)

        # Showing all the widgets via the "logic" of the qwidget
        dummy_widget = QWidget()
        dummy_widget.setLayout(layout)
        self.setCentralWidget(dummy_widget)

        # Dont know, how this value is about 639?
        # width_dw = dummy_widget.frameGeometry().width()
        # print('width_dw ', width_dw)

    # Define the functions, which should be executed, when the buttons are clicked
    def show_scanning_dirs_window(self):
        if self.scanning_dirs_window is None:
            self.scanning_dirs_window = window_scan_directories.WindowScanDir(
                self.x(), self.y() + self.height() + 30, self.width()
            )
            self.scanning_dirs_window.show()
        else:
            self.scanning_dirs_window = None
        # self.scanning_window = scanning_window.WindowScanDir()
        # self.scanning_window.show()

    def show_feature_overview(self):
        if self.window_feature_overview is None:
            self.window_feature_overview = window_feature_overview.WindowShowFeatureOverview(
                self.x(), self.y(), self.width()
            )
            self.window_feature_overview.show()
        else:
            self.window_feature_overview = None

    def show_feature_upload(self):
        if self.window_feature_upload is None:
            self.window_feature_upload = window_feature_upload.WindowFeatureUpload(
                self.x(), self.y(), self.width()
            )
            self.window_feature_upload.show()
        else:
            self.window_feature_upload = None

    def show_feature_signals(self):
        if self.window_show_feature_signals is None:
            self.window_show_feature_signals = window_feature_signals.WindowShowFeatureSignals(
                150, 150, 100
            )
            self.window_show_feature_signals.show()
        else:
            self.window_show_feature_signals = None


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = Main_PDW_GUI(200, 150, 250, 150)

    # For example: Get the width of the window, BUT its problematic...
    width_main_window = window.width()
    print('width_mw: ', width_main_window)

    window.show()

    sys.exit(app.exec_())
