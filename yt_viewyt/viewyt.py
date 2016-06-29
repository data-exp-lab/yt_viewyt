import os
os.environ['QT_API'] = 'pyqt'
import sip
sip.setapi("QString", 2)
sip.setapi("QVariant", 2)
import sys
import StringIO
from PyQt4 import QtGui, QtCore
from acquisition import AcquisitionMasterW
from visualization import FrbView
from console import QIPythonWidget
from manipulation import LocationWidget
import matplotlib


class ViewYt(QtGui.QWidget):

    def __init__(self):
        super(ViewYt, self).__init__()
        self.acquisitionWidget = AcquisitionMasterW()

        self.viewWidget = QtGui.QMainWindow()

        self.subWidget = QtGui.QLabel("Welcome to ViewYT!")
        self.subWidget.resize(512, 512)
        self.viewWidget.setCentralWidget(self.subWidget)

        self.ipythonWidget = QIPythonWidget()

        tempWidget = QtGui.QWidget()
        tempLayout = QtGui.QVBoxLayout()
        tempLayout.addWidget(self.viewWidget)
        tempLayout.addWidget(self.ipythonWidget)
        tempWidget.setLayout(tempLayout)

        self.acquisitionWidget.activeW.passToViewButton.clicked.connect(
            self.pass_to_view)

        self.hideAcquisitionB = QtGui.QPushButton('<<')
        self.hideAcquisitionB.setFixedSize(20, self.size().height())
        self.hideAcquisitionB.clicked.connect(self.hide_acquisition)

        self.layout = QtGui.QHBoxLayout()
        self.layout.addWidget(self.acquisitionWidget)
        self.layout.addWidget(self.hideAcquisitionB)
        self.layout.addWidget(tempWidget)
        self.setLayout(self.layout)

        self.show()

        self.ipythonWidget.pushVariables({'ViewYT': self})

    def pass_to_view(self):
        selected_data = self.acquisitionWidget.activeW.get_active_DataObject()
        selected_data = selected_data.data
        plot = FrbView(selected_data)
        plot = plot.get_plot()
        self.viewWidget.setCentralWidget(plot)
        self.viewWidget.resize(512, 512)
        self.show()

    def hide_acquisition(self):
        if not self.acquisitionWidget.isHidden():
            self.acquisitionWidget.setHidden(True)
            self.hideAcquisitionB.setText('>>')
        else:
            self.acquisitionWidget.setHidden(False)
            self.hideAcquisitionB.setText('<<')


def main():
    app = QtGui.QApplication(sys.argv)
    ViewYt()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
