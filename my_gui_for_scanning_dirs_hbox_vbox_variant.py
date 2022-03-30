import sys
import os
os.environ['QT_MAC_WANTS_LAYER'] = '1'
from PySide2.QtGui import QPixmap

from PySide2.QtWidgets import (
    QApplication, QVBoxLayout,
    QHBoxLayout, QFormLayout,
    QPushButton, QCheckBox, QListWidget,
    QWidget, QMainWindow, QLineEdit, QLabel
)
class WindowScanDir(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("First layout test of scanning dir - hbox/vbox")

        # TODO: Define the position of the window via x_pos_parent_window etc...

        # Create the full  layout
        full_layout = QVBoxLayout()

        # Layout for label and picture
        label_pic_layout = QHBoxLayout()
        lbl_scan_pdw = QLabel('Scan directories manually !')
        lbl_scan_pdw.setStyleSheet("font-size: 22px;" "color: green")
        lbl_logo = QLabel("Rosen_logo")
        lbl_logo.setPixmap(QPixmap("rosen_logo.png"))
        lbl_logo.setScaledContents(False)

        label_pic_layout.addWidget(lbl_scan_pdw)
        label_pic_layout.addStretch()
        label_pic_layout.addWidget(lbl_logo)

        # Temp-layout for buttons and listwidgets area
        btn_and_listwidget_layout = QHBoxLayout()

        # Buttons should be arranged vertically
        btn_layout = QVBoxLayout()
        btn_add_anomaly_dir = QPushButton('Add ...')
        btn_create_df = QPushButton('Create ...')
        btn_save_anomaly_list = QPushButton('Save anomaly...')
        btn_chose_csv_file = QPushButton('Save csv ...')
        btn_write_anomaly_dirs_to_csv = QPushButton('Write ...')
        # btn_layout.addSpacing(-1)
        btn_layout.addWidget(btn_add_anomaly_dir)
        # btn_layout.insertSpacing(0, -10)
        btn_layout.addStretch(1)
        btn_layout.addWidget(btn_create_df)
        btn_layout.addStretch(1)
        btn_layout.addWidget(btn_save_anomaly_list)
        btn_layout.addStretch(1)
        btn_layout.addWidget(btn_chose_csv_file)
        btn_layout.addStretch(1)
        btn_layout.addWidget(btn_write_anomaly_dirs_to_csv)
        btn_layout.setContentsMargins(-10, 0, 10, +10)
        # Listwidgets should be arranged vertically
        list_widget_layout = QVBoxLayout()

        text_anomaly_dirs = QListWidget()
        text_anomaly_dirs.addItem("anomaly 1")
        text_anomaly_dirs.addItem("anomaly 2")

        list_info = QListWidget()
        list_info.addItem("list info 1")
        list_info.addItem("list info 2")

        list_widget_layout.addWidget(text_anomaly_dirs)
        list_widget_layout.addStretch()
        list_widget_layout.addWidget(list_info)


        # Arange the different layout in the desired manner

        btn_and_listwidget_layout.addLayout(btn_layout)
        btn_and_listwidget_layout.addLayout(list_widget_layout)

        full_layout.addLayout(label_pic_layout)
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