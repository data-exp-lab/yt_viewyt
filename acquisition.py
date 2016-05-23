import os
from PySide import QtCore
from PySide import QtGui


class directoryObject(object):

    def __init__(self, path = None, source = "Local Machine"):
        if path is None:
            self.location = os.getcwd()
            self.directoryTree = self.make_directory_tree()
            self.source = source
        if path is not None:
            self.location = path
            self.location = self.make_directory_tree()
            self.source = source

    def make_directory_tree(self):
        storageList = []
        for root, dirs, files in os.walk(self.location):
            root = root.split('/')
            dirName = root[-1]
            dirRepresentation = [dirName, dirs, files]
            storageList.append(dirRepresentation)
        return storageList[0]

    def get_location(self):
        return self.location

    def get_sub_directories(self):
        return self.directoryTree[1]

    def get_files(self):
        return self.directoryTree[2]

    def change_directory(self, direction, path = None,
                         source = "Local Machine"):
        if direction == 1:
            os.chdir(self.location + "/" + path)
            self.location = os.getcwd()
            self.directoryTree = self.make_directory_tree()
            self.source = source
        if direction == -1:
            newPath = self.location.split('/')
            newPath = '/' + '/'.join(newPath[1:len(newPath)-1])
            os.chdir(newPath)
            self.location = os.getcwd()
            self.source = source
            self.directoryTree = self.make_directory_tree()

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
        self.aspectRatioActiveW = ratio3
