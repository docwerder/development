import sys
from PyQt5.QtWidgets import QStyleFactory
print(QStyleFactory.keys())

from PyQt5.QtWidgets import *
#print(PyQt5.QtWidgets.QStyleFactory.keys())
app = QApplication(sys.argv)
app.setStyle('Windows')