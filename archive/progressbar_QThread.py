from PyQt5.QtWidgets import QApplication, QLabel, QDialog, QProgressBar, QVBoxLayout, QPushButton
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
            time.sleep(2)
            self.change_value.emit(cnt)

    def run(self) -> None:
        print('into run function!')
        cnt = 0
        while cnt < 10:
            cnt += 1
            time.sleep(2)
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
        self.clicked_value = 0
        self.InitUI()

    def InitUI(self):
        # General layout
        vbox = QVBoxLayout()

        # Progressbar...
        self.progressbar = QProgressBar()
        self.progressbar.adjustSize()
        self.progressbar.setStyleSheet("QProgressBar::chunk {background-color: #2196F3; width: 10px; margin: 0.5px;}")
        # self.progressbar.setStyleSheet("QProgressBar::chunk {background-color: green; width: 10px; margin: 0.5px;}")
        # Button...
        self.button = QPushButton("Run Progressbar")
        self.button.clicked.connect(self.startProgressBar)

        # QLabel...
        self.clicksLabel = QLabel("Counting: 0 clicks", self)
        self.clicksLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        # Button for clicking...
        self.countBtn = QPushButton("Klick mich!", self)
        self.countBtn.clicked.connect(self.countClicks)


        # Add the widgets to the layout!
        vbox.addWidget(self.progressbar)
        vbox.addWidget(self.button)
        vbox.addWidget(self.clicksLabel)
        vbox.addWidget(self.countBtn)

        self.setLayout(vbox)

    def startProgressBar(self):
        self.thread = MyThread()
        self.thread.change_value.connect(self.setProgressVal)
        self.thread.start()

    def setProgressVal(self, val):
        self.progressbar.setValue(val)

    def countClicks(self):
        self.clicked_value +=1
        self.clicksLabel.setText(f"Counting: {self.clicked_value} clicks")
        print('Klick mich clicked!')


if __name__ == '__main__':
    
    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec_())