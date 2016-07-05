import os
os.environ["QT_API"] = 'pyqt'
import sip
sip.setapi("QString", 2)
sip.setapi("QVariant", 2)
import sys
import StringIO
from PyQt4 import QtGui, QtCore
from acquisition import AcquisitionMasterW
from visualization import FrbView
from console import QIPythonWidget


class ViewYt(QtGui.QWidget):

    def __init__(self):
        super(ViewYt, self).__init__()
        self.acquisitionWidget = AcquisitionMasterW()

        self.viewWidget = QtGui.QMdiArea()
        self.viewWidget.tileSubWindows()
        self.viewWidget.addSubWindow(QtGui.QLabel("Welcome to ViewYT"))
        self.viewWidget.resize(512, 512)

        self.ipythonWidget = QIPythonWidget()

        comboWidget = QtGui.QWidget()
        comboLayout = QtGui.QVBoxLayout()
        comboLayout.addWidget(self.viewWidget)
        comboLayout.addWidget(self.ipythonWidget)
        comboWidget.setLayout(comboLayout)

        self.acquisitionWidget.activeW.passToViewButton.clicked.connect(
            self.pass_to_view)

        self.hideAcquisitionB = QtGui.QPushButton('<<')
        self.hideAcquisitionB.setFixedSize(20, self.size().height())
        self.hideAcquisitionB.clicked.connect(self.hide_acquisition)

        self.layout = QtGui.QHBoxLayout()
        self.layout.addWidget(self.acquisitionWidget)
        self.layout.addWidget(self.hideAcquisitionB)
        self.layout.addWidget(comboWidget)
        self.setLayout(self.layout)

        self.show()

        self.ipythonWidget.pushVariables({'ViewYT': self})

    def pass_to_view(self):
        selected_data = self.acquisitionWidget.activeW.get_active_DataObject()
        selected_data = selected_data.data
        plot = FrbView(selected_data)
        plotW = plot.get_plot()
        plotW.setSizePolicy(QtGui.QSizePolicy.Expanding,
                            QtGui.QSizePolicy.Expanding)
        plotW.setContentsMargins(0, 0, 0, 0)
        plotW.updateGeometry()
        self.viewWidget.addSubWindow(plotW)
        for x in self.viewWidget.subWindowList():
            x.show()
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
