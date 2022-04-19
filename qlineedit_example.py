#!/usr/bin/python

"""
ZetCode PySide tutorial

This example shows text which
is entered in a QtGui.QLineEdit
in a QtGui.QLabel widget.

author: Jan Bodnar
website: zetcode.com
"""

import sys
import os
os.environ['QT_MAC_WANTS_LAYER'] = '1'
#from PySide2 import QtGui, QtCore

from PySide2.QtWidgets import (
    QApplication, QVBoxLayout, QHBoxLayout,
    QComboBox, QPlainTextEdit, QFormLayout, QGridLayout,
    QPushButton, QCheckBox, QListWidget, QFrame,
    QWidget, QMainWindow, QLineEdit, QLabel
)

class Example(QWidget):

    def __init__(self):
        super(Example, self).__init__()

        self.initUI()

    def initUI(self):
        self.lbl = QLabel(self)
        qle = QLineEdit(self)

        qle.move(60, 100)
        self.lbl.move(60, 40)

        qle.textChanged[str].connect(self.onChanged)

        self.setGeometry(300, 300, 280, 170)
        self.setWindowTitle('QtGui.QLineEdit')
        self.show()

    def onChanged(self, text):
        self.lbl.setText(text)
        self.lbl.adjustSize()


def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()