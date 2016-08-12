import os
os.environ["QT_API"] = 'pyqt'
import sip
sip.setapi("QString", 2)
sip.setapi("QVariant", 2)
import sys
import StringIO
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import pyqtSlot
import matplotlib
matplotlib.use('Qt4Agg')
from acquisition import AcquisitionMasterW
from visualization import ViewWidget
from console import QIPythonWidget


class ViewYt(QtGui.QWidget):

    def __init__(self):
        super(ViewYt, self).__init__()

        self.view_widget = ViewWidget()

        self.acquisitionWidget = AcquisitionMasterW(self.view_widget)

        self.view_widget.enough_windows[bool].connect(self.show_link_button)

        self.ipythonWidget = QIPythonWidget()

        comboWidget = QtGui.QWidget()
        comboLayout = QtGui.QVBoxLayout()
        comboLayout.addWidget(self.view_widget)
        comboLayout.addWidget(self.ipythonWidget)
        comboWidget.setLayout(comboLayout)

        self.acquisitionWidget.activeW.pass_to_view_button.clicked.connect(
            self.pass_to_view)

        self.hideAcquisitionB = QtGui.QPushButton('<<')
        self.hideAcquisitionB.setFixedSize(20, self.size().height())
        self.hideAcquisitionB.clicked.connect(self.hide_acquisition)

        self.link_button = QtGui.QPushButton('link views')
        self.link_button.clicked.connect(
            self.view_widget.make_standard_frb_link)
        self.link_button.setHidden(True)

        self.layout = QtGui.QHBoxLayout()
        self.layout.addWidget(self.acquisitionWidget)
        self.layout.addWidget(self.hideAcquisitionB)
        self.layout.addWidget(comboWidget)
        self.layout.addWidget(self.link_button)
        self.setLayout(self.layout)

        self.show()

        self.ipythonWidget.pushVariables({'ViewYT': self})

    def pass_to_view(self):
        selected_data = self.acquisitionWidget.activeW.get_active_data_object()
        selected_data = selected_data.data
        self.view_widget.add_frb_view(selected_data)

    def hide_acquisition(self):
        if not self.acquisitionWidget.isHidden():
            self.acquisitionWidget.setHidden(True)
            self.hideAcquisitionB.setText('>>')
        else:
            self.acquisitionWidget.setHidden(False)
            self.hideAcquisitionB.setText('<<')

    @pyqtSlot(bool)
    def show_link_button(self, val):
        if val:
            self.link_button.setHidden(False)


def main():
    app = QtGui.QApplication(sys.argv)
    ViewYt()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
