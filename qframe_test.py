import sys
import os
os.environ['QT_MAC_WANTS_LAYER'] = '1'
from PySide2.QtWidgets import (
    QApplication, QWidget, QFrame
)



if __name__ == '__main__':

    app = QApplication(sys.argv)

    window = QWidget()
    window.resize(250, 150)
    window.move(300, 300)
    window.setWindowTitle('Sample')

    window.frame = QFrame(window)
    window.frame.setLineWidth(15)
    window.frame.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
    # window.frame.setStyleSheet("background-color: rgb(200, 255, 255);"
    #                            "border-width: 1;"
    #                            "border-radius: 3;"
    #                            "border-style: solid;"
    #                            "border-color: rgb(10, 10, 10)"
    #                            )
    app.setStyle("fusion")
    window.frame.move(120, 20)
    window.show()

    sys.exit(app.exec_())