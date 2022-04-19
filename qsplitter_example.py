#!/usr/bin/python

"""
ZetCode PySide tutorial

This example shows
how to use QtGui.QSplitter widget.

author: Jan Bodnar
website: zetcode.com
"""

import sys
import os
os.environ['QT_MAC_WANTS_LAYER'] = '1'
from PySide2 import QtGui, QtCore

from PySide2.QtWidgets import(
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QFrame,
    QSplitter, QLabel, QStyleFactory
)

class Example(QWidget):

    def __init__(self):
        super(Example, self).__init__()

        self.initUI()

    def initUI(self):
        hbox = QHBoxLayout(self)

        topleft = QFrame(self)
        topleft.setFrameShape(QFrame.StyledPanel)

        topright = QFrame(self)
        topright.setFrameShape(QFrame.StyledPanel)

        bottom = QFrame(self)
        # bottom.setFrameShape(QFrame.StyledPanel)
        bottom.setFrameStyle(QFrame.Panel | QFrame.Sunken)

        splitter1 = QSplitter(QtCore.Qt.Horizontal)
        splitter1.addWidget(topleft)
        splitter1.addWidget(topright)

        splitter2 = QSplitter(QtCore.Qt.Vertical)
        #splitter2.addWidget(bottom)
        splitter2.addWidget(splitter1)

        label = QLabel("This is a test-label ")
        label.setFrameStyle(QFrame.Panel | QFrame.Raised)
        label.setLineWidth(2)

        hbox.addWidget(splitter2)
        hbox.addWidget(label)
        self.setLayout(hbox)
        #QApplication.setStyle(QStyleFactory.create('Cleanlooks'))

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('QtGui.QSplitter')
        self.show()

    #def onChanged(self, text):
    #    self.lbl.setText(text)
    #    self.lbl.adjustSize()


def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()