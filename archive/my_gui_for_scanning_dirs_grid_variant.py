import sys
import os
os.environ['QT_MAC_WANTS_LAYER'] = '1'

from PySide2 import QtCore
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import (
    QApplication, QVBoxLayout,
    QHBoxLayout, QFormLayout, QGridLayout,
    QPushButton, QCheckBox, QListWidget,
    QWidget, QMainWindow, QLineEdit, QLabel
)
class WindowScanDir(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("First layout test of scanning dir - grid variant")

        # Create the full  layout
        full_layout = QVBoxLayout()

        # Layout for label and picture
        label_pic_layout = QHBoxLayout()
        lbl_scan_pdw = QLabel('Scan directories ')
        lbl_scan_pdw.setStyleSheet("font-size: 20px;" "color: green")
        lbl_logo = QLabel("Rosen_logo")
        lbl_logo.setPixmap(QPixmap("rosen_logo.png").scaledToWidth(150))
        lbl_logo.setScaledContents(False)

        label_pic_layout.addWidget(lbl_scan_pdw)
        label_pic_layout.addStretch()
        label_pic_layout.addWidget(lbl_logo)

        # Temp-layout for buttons and listwidgets area
        btn_and_listwidget_layout = QGridLayout()

        # Buttons and listwidgets should be arranged within QGridLayout
        btn_add_anomaly_dir = QPushButton('Add ...')
        btn_create_df = QPushButton('Create ...')
        btn_save_anomaly_list = QPushButton('Save anomaly...')
        btn_chose_csv_file = QPushButton('Save csv ...')
        btn_write_anomaly_dirs_to_csv = QPushButton('Write ...')

        # Define listwidgets...
        text_anomaly_dirs = QListWidget()
        text_anomaly_dirs.addItem("anomaly 1")
        text_anomaly_dirs.addItem("anomaly 2")

        list_info = QListWidget()
        list_info.addItem("list info 1a")
        list_info.addItem("list info 2")


        # Fill the QGridLayout....
        btn_and_listwidget_layout.addWidget(btn_add_anomaly_dir, 0, 0)
        btn_and_listwidget_layout.addWidget(btn_create_df, 1, 0)
        btn_and_listwidget_layout.addWidget(btn_save_anomaly_list, 2, 0)
        btn_and_listwidget_layout.addWidget(btn_chose_csv_file, 3, 0)
        btn_and_listwidget_layout.addWidget(btn_write_anomaly_dirs_to_csv, 4, 0)
        btn_and_listwidget_layout.addWidget(text_anomaly_dirs, 0, 1, 3, 1)
        btn_and_listwidget_layout.addWidget(list_info, 3, 1, 2, 1)

        # Arange the different layout in the desired manner


        full_layout.addLayout(label_pic_layout)
        full_layout.addStretch()
        full_layout.addLayout(btn_and_listwidget_layout)

        dummy_widget = QWidget()
        dummy_widget.setLayout(full_layout)
        self.setCentralWidget(dummy_widget)

        #
        #
        #
        # # Add a label and a line edit to the form layout
        # topLayout.addRow("Some Text:", QLineEdit())
        # topLayout.addRow("Some additional Text:", QLineEdit())
        #
        # # Create a layout for the checkboxes
        # optionsLayout = QVBoxLayout()
        # # Add some checkboxes to the layout
        # optionsLayout.addWidget(QCheckBox("Option one"))
        # optionsLayout.addWidget(QCheckBox("Option two"))
        # optionsLayout.addWidget(QCheckBox("Option three"))
        # # Nest the inner layouts into the outer layout
        # outerLayout.addLayout(topLayout)
        # outerLayout.addLayout(optionsLayout)
        # # Set the window's main layout
        # # self.setLayout(outerLayout)

        # widget = QWidget()
        # widget.setLayout(outerLayout)
        # self.setCentralWidget(widget)

if __name__== '__main__':
    app = QApplication(sys.argv)
    window = WindowScanDir()
    window.show()
    sys.exit(app.exec_())