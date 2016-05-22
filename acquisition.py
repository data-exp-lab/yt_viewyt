import os
from PySide import QtCore
from PySide import QtGui


class directoryObject(object):

    def __init__(self, path = None):
        if path is None:
            self.location = os.getcwd()
            self.directoryTree = self.make_directory_tree()
            self.source = "Local Machine"

    def make_directory_tree(self):
        storageList = []
        startOfTree = self.location.split('/')
        startOfTree = '/' + '/'.join(startOfTree[0:len(startOfTree) - 1])
        for root, dirs, files in os.walk(self.location):
            root = root.split('/')
            dirName = root[-1]
            dirRepresentation = [dirName, dirs, files]
            storageList.append(dirRepresentation)
            for x in range(len(storageList) - 1, -1, -1):
                for y in range(len(storageList[x][1])):
                    dirName = c[x][1][y]
                    for z in range(len[storageList] - 1, -1, -1):
                        rootName = storageList[z][0]
                        if dirName == rootName:
                            c[x][1][y] = c[z]
                            del c[z]
        return c

    def get_location(self):
        return self.location

    def get_sub_directories(self):
        tipOfLocation = self.location.split('/')
        tipOfLocation = tipOfLocation[-1]
        cwdContentList = [value for value in
                          self.directoryTree[1] == tipOfLocation]
        cwdContentList = cwdContentList[0]
        subDirectoryList = []
        for x in cwdContentList[1]:
            subDirectoryList.append(x[0])
        return subDirectoryList

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
