from PyQt5.QtWidgets import QApplication, QWidget, QDialog, QProgressBar, QVBoxLayout, QPushButton
import sys
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import time

class MyThread(QThread):
    change_value = pyqtSignal(int)

    def gehe_los(self):
        cnt = 0
        while cnt < 100:
            cnt += 1
            time.sleep(0.5)
            self.change_value.emit(cnt)

    def run(self):
        cnt = 0
        while cnt < 100:
            cnt += 1
            time.sleep(0.1)
            self.change_value.emit(cnt)

class Window(QDialog):
    def __init__(self):
        super().__init__()

        self.title = "PyQt5 Window"
        self.left = 500
        self.top = 200
        self.width = 200
        self.height = 200
        self.iconName = "home.png"
        self.setWindowTitle(self.title)
        self.setWindowIcon(QtGui.QIcon(self.iconName))
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()
        self.InitUI()

    def InitUI(self):
        vbox = QVBoxLayout()
        self.progressbar = QProgressBar()
        self.progressbar.adjustSize()
        vbox.addWidget(self.progressbar)

        self.button = QPushButton("Run Progressbar")
        self.button.clicked.connect(self.startProgressBar)
        vbox.addWidget(self.button)
        self.setLayout(vbox)

    def startProgressBar(self):
        self.thread = MyThread()
        self.thread.change_value.connect(self.setProgressVal)
        self.thread.start()

    def setProgressVal(self, val):
        self.progressbar.setValue(val)



App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())