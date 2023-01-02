import sys
import os
os.environ['QT_MAC_WANTS_LAYER'] = '1'
from PySide2 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    wid = QtWidgets.QWidget()
    wid.resize(450, 150)
    grid = QtWidgets.QGridLayout(wid)
    fig = Figure(figsize=(7, 5), dpi=65, facecolor=(1, 1, 1), edgecolor=(0, 0, 0))
    canvas = FigureCanvas(fig)
    grid.addWidget(canvas, 0, 0)
    wid.show()
    sys.exit(app.exec_())