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
from visualization import YtView
from console import QIPythonWidget
from manipulation import LocationWidget
import matplotlib


class ViewYt(QWidget):

    def __init__(self):
        super(ViewYt, self).__init__()
        self.acquisitionWidget = AcquisitionMasterW()

        self.viewWidget = QMainWindow()

        self.subWidget = QLabel("Welcome to ViewYT!")
        self.subWidget.resize(512, 512)
        self.viewWidget.setCentralWidget(self.subWidget)

        self.ipythonWidget = QIPythonWidget()

        tempWidget = QWidget()
        tempLayout = QVBoxLayout()
        tempLayout.addWidget(self.viewWidget)
        tempLayout.addWidget(self.ipythonWidget)
        tempWidget.setLayout(tempLayout)

        self.acquisitionWidget.activeW.passToViewButton.clicked.connect(
            self.pass_to_view)

        self.hideAcquisitionB = QPushButton('<<')
        self.hideAcquisitionB.setFixedSize(20, self.size().height())
        self.hideAcquisitionB.clicked.connect(self.hide_acquisition)

        self.manipulationWidget = LocationWidget()

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.acquisitionWidget)
        self.layout.addWidget(self.hideAcquisitionB)
        self.layout.addWidget(tempWidget)
        self.layout.addWidget(self.manipulationWidget)
        self.setLayout(self.layout)
        self.show()
        self.ipythonWidget.pushVariables({'ViewYT': self})

    def pass_to_view(self):
        selected_data = self.acquisitionWidget.activeW.get_active_DataObject()
        selected_data = selected_data.data
        plot = YtView(selected_data)
        plot = plot.get_plot()
        self.viewWidget.setCentralWidget(plot)
        self.viewWidget.resize(256, 256)
        self.show()

    def hide_acquisition(self):
        if not self.acquisitionWidget.isHidden():
            self.acquisitionWidget.setHidden(True)
            self.hideAcquisitionB.setText('>>')
        else:
            self.acquisitionWidget.setHidden(False)
            self.hideAcquisitionB.setText('<<')

def main():
    app = QApplication(sys.argv)
    ex = ViewYt()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
