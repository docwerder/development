import applescript
import sys
from PySide2.QtWidgets import QApplication, QGridLayout, QMainWindow, QWidget, QPushButton, QLabel, QDialog ,QDialogButtonBox, QVBoxLayout, QMessageBox



class CustomDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Connect to WERDERNAS")

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel("Something happened ...")
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)




def mnt_WERDERNAS():

    def okButtonClicked(self):
        print("Going into the button function!")
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Question")
        dlg.setText("This is a dialog")
        #button = dlg.exec_()


    applescript.run('''
        tell application "Finder"
            try
                mount volume "afp://192.168.178.48/WERDERNAS" as user name "admin" with password "pax123"
            
            on error
                display dialog "Es ist ein Fehler aufgetreten!" buttons ¬
                {" OK "} default button 1 ¬
                with icon stop
            end try
        end tell

    ''')

    print('Apple Script successfully executed!')
    okButtonClicked


def mnt_WERDERNAS2():

    applescript.run('''
        tell application "Finder"
            try
                mount volume "afp://192.168.178.48/WERDERNAS2" as user name "admin" with password "pax123"
            on error
                display dialog "Es ist ein Fehler aufgetreten!" buttons ¬
                {" OK "} default button 1 ¬
                with icon stop
            end try
        end tell
    ''')

def mnt_WERDERNASX():
    applescript.run('''
        tell application "Finder"
            try
                mount volume "afp://192.168.178.48/WERDERNASX" as user name "admin" with password "pax123"
            on error
                display dialog "Es ist ein Fehler aufgetreten!" buttons ¬
                {" OK "} default button 1 ¬
                with icon stop
            end try
        end tell
    ''')

def mnt_WERDERNAS2X():
    applescript.run('''
        tell application "Finder"
            try
                mount volume "afp://192.168.178.48/WERDERNAS2X" as user name "admin" with password "pax123"
            on error
                display dialog "Es ist ein Fehler aufgetreten!" buttons ¬
                {" OK "} default button 1 ¬
                with icon stop
            end try
        end tell
    ''')