import os
os.environ['QT_API'] = 'pyqt'
import sip
sip.setapi("QString", 2)
sip.setapi("QVariant", 2)
import sys
import StringIO
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from acquisition import AcquisitionMasterW
from visualization import YtPlot
from console import QIPythonWidget
import matplotlib
#from matpotlib.backends.backend_qt4agg import FigureCanvasQtAgg as FigureCanvas

#method of displaying yt plots without saving to disk is taken from
#http://matplotlib.org/examples/user_interfaces/embedding_in_qt4.html


class ViewYt(QWidget):

    def __init__(self):
        super(ViewYt, self).__init__()
        self.acquisitionWidget = AcquisitionMasterW()

        self.viewWidget = QMainWindow()

        self.subWidget = QLabel("Welcome to ViewYT!")
        self.subWidget.resize(512, 512)
        self.viewWidget.setCentralWidget(self.subWidget)

        self.ipythonWidget = QIPythonWidget()

        executeNotebookCommand = QKeyEvent(QEvent.KeyPress, Qt.Key_Enter, Qt.NoModifier)
        tempWidget = QWidget()
        tempLayout = QVBoxLayout()
        tempLayout.addWidget(self.viewWidget)
        tempLayout.addWidget(self.ipythonWidget)
        tempWidget.setLayout(tempLayout)

        self.acquisitionWidget.activeW.passToViewButton.clicked.connect(
            self.pass_to_view)

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.acquisitionWidget)
        self.layout.addWidget(tempWidget)
        self.setLayout(self.layout)
        self.show()

    def pass_to_view(self):
        selected_data = self.acquisitionWidget.activeW.get_active_DataObject()
        selected_data = selected_data.data
        plot = YtPlot(selected_data)
        plot = plot.get_plot()
        print type(plot)
        self.viewWidget.setCentralWidget(plot)
        self.viewWidget.resize(512, 512)
        self.show()

    def show_from_conditions(self):
        layout = QHBoxLayout()
        layout.addWidget(self.acquisitionWidget)
        layout.addWidget(self.viewWidget)
        self.setLayout(layout)
        self.show()


def main():
    app = QApplication(sys.argv)
    ex = ViewYt()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
