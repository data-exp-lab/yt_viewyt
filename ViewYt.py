import sys
from PySide import QtGui, QtCore
from acquisition import AcquisitionMasterW
from visualization import YtPlot
import matplotlib
matplotlib.rcParams['backend.qt4'] = 'PySide'
from matplotlib.backends import qt_compat
#from matpotlib.backends.backend_qt4agg import FigureCanvasQtAgg as FigureCanvas

#method of displaying yt plots without saving to disk is taken from
#http://matplotlib.org/examples/user_interfaces/embedding_in_qt4.html

class ViewYt(QtGui.QWidget):

    def __init__(self):
        super(ViewYt, self).__init__()
        self.acquisitionWidget = AcquisitionMasterW()

        self.viewWidget = None

        self.subWidget = QtGui.QWidget()

        self.acquisitionWidget.activeW.passToViewButton.clicked.connect(
            self.pass_to_view)
        self.show_from_conditions()

    def pass_to_view(self):
        selected_data = self.acquisitionWidget.activeW.get_active_DataObject()
        selected_data = selected_data.data
        plot = YtPlot(selected_data)
        self.viewWidget = plot
        self.show_from_conditions()

    def show_from_conditions(self):
        layout = QtGui.QHBoxLayout()
        layout.addWidget(self.acquisitionWidget)
        if self.viewWidget is not None:
            layout.addWidget(self.viewWidget)
        self.setLayout(layout)
        self.show()


def main():
    app = QtGui.QApplication(sys.argv)
    ex = ViewYt()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
