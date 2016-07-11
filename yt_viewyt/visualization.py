from viewtypes import FrbView
from links import StandardFrbLink
from PyQt4 import QtGui
from PyQt4.QtCore import pyqtSignal


class ViewWidget(QtGui.QMdiArea):

    enough_windows = pyqtSignal(bool)

    def __init__(self):
        super(ViewWidget, self).__init__()
        self.tileSubWindows()
        self.resize(512, 512)
        self.num_sub_windows = len(self.subWindowList())
        self.links = []

    def add_frb_view(self, data):
        plot = FrbView(data)
        window = QtGui.QMdiSubWindow()
        window.setWidget(plot.canvas)
        self.addSubWindow(window)
        self.links.append(StandardFrbLink([plot]))
        for x in self.subWindowList():
            x.show()
        self.num_sub_windows += 1
        self.signal_enough_windows()

    def signal_enough_windows(self):
        if self.num_sub_windows > 1:
            self.enough_windows.emit(True)

    def make_standard_frb_link(self):
        frb_list = []
        for x in self.subWindowList():
            frb_list.append(x.widget())
        self.links.append(StandardFrbLink(frb_list))
