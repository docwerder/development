import sys

from PyQt6.QtCore import QSize
from PySide6.QtWidgets import \
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QLabel
from PySide6.QtGui import QPixmap, QImage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("First Layout Window")
        self.setMinimumSize(400, 300)

        vert_1_layout = QVBoxLayout()
        vert_2_layout = QVBoxLayout()
        vert_3_layout = QVBoxLayout()

        hor_0_layout = QHBoxLayout()
        hor_1_layout = QHBoxLayout()
        hor_2_layout = QHBoxLayout()
        hor_3_layout = QHBoxLayout()

        lbl_pdw = QLabel("PDW Version 0.6")
        lbl_logo = QLabel("Logo label")
        img = QImage("werderuser_logo.jpg")
        pixmap = QPixmap(img.scaledToWidth(180))
        lbl_logo = QLabel(self)
        #lbl_logo.setPixmap(pixmap)

        #lbl_logo.setPixmap(QPixmap("werderuser_logo.jpg"))
        #pixmap = QPixmap(lbl_logo.scaledToWidth(50))
        btn_feature_overview = QPushButton('Feature overview')
        btn_feature_upload = QPushButton('Feature upload')
        btn_feature_upload.setGeometry(110,110,100,70)

        hor_0_layout.addWidget(lbl_pdw)
        hor_0_layout.addWidget(lbl_logo)

        hor_1_layout.addWidget(btn_feature_overview)
        hor_1_layout.addWidget(btn_feature_upload)

        hor_2_layout.addWidget(QPushButton('Show feature'))
        hor_2_layout.addWidget(QPushButton('Scanning dirs'))

        hor_3_layout.addWidget(QPushButton('Button 5'))
        hor_3_layout.addWidget(QPushButton('Button 6'))

        vert_1_layout.addStretch()
        vert_1_layout.addLayout(hor_0_layout)
        #vert_1_layout.addStretch()
        vert_1_layout.addLayout(hor_1_layout)
        vert_1_layout.addStretch()
        vert_1_layout.addLayout(hor_2_layout)
        vert_1_layout.addStretch()
        vert_1_layout.addLayout(hor_3_layout)
        vert_1_layout.addStretch()

        main_widget = QWidget()
        main_widget.setLayout(vert_1_layout)
        self.setCentralWidget(main_widget)

if __name__== '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())