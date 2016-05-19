import os
from PySide import QtCore
from PySide import QtGui

class directoryObject(object):

    def __init__(self):
        self.location = os.getcwd()
        self.directoryTree = "Undefined"
        self.source = "Local Machine"

    def getLocation(self):
        return self.location

    def getSubDirectories(self):

    def __pathFormer(listVar):
        out = '/'
        for x in range(1, len(listVar)):
            out = out + listVar[x] + '/'


class acquisitionSourceW(QtGui.QWidget):

    def __init__(self):
        super(acquisitionSourceW, self).__init__()
        self.directoryObjs = []
        self.availableSourcesW = QtGui.QWidget()
        self.addButton = QtGui.QPushButton()
        self.removeButton = QtGui.QPushButton()
        self.rArrow = QtGui.QPushButton()
        self.lArrow = QtGui.QPushButton()
        self.leftClickMenuBar = QtGui.QMenuBar()
        self.aspectRatio = 5

class acquisitionMasterW(QtGui.QWidget):

    def __init__(self, ratio1, ratio2, ratio3):
        super(acquisitionMasterW, self).__init__()
        self.sourceW = acquisitionSourceW()
        self.activeW = acquisitionActiveW()
        self.hider = QtGui.QPushButton()
        self.aspectRatio2MainWidget = ratio1
        self.aspectRatioSourceW = ratio2
        self.aspectRatioActiveW = ratio 3

    def resizer(self):

    def main():
