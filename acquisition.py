import os
from PySide import QtCore
from PySide import QtGui



r"""The initial component for an object that provides a backend for navigating
folders on a system.

This class provides immediate access to a users location in the system
directory, any sub-directories the user can move into, and any files
in the current user location. It also has the ability to move around
in the directory system.

Parameters
----------
location:String
    String that contains the current working directory.
directoryTree:List
    List that contains the path-name of the current directory,
    the list of sub-directories in the current directory, and
    a list of files in the current directory.
source:String
    a string denoting where the current directoryObject is from.
    A future goal of this application is the ability to support
    data from multiple sources via ssh.
"""

class DirectoryObject(object):

    r"""Initializes all object parameters."""
    def __init__(self, path = None, source = "Local Machine"):
        if path is None:
            self.location = os.getcwd()
            self.directoryTree = self.make_directory_tree()
            self.source = source
        if path is not None:
            self.location = path
            self.location = self.make_directory_tree()
            self.source = source

    r"""Provides a list of information about the current working directory"""
    def make_directory_tree(self):
        storageList = []
        for root, dirs, files in os.walk(self.location):
            root = root.split('/')
            dirName = root[-1]
            dirRepresentation = [dirName, dirs, files]
            storageList.append(dirRepresentation)
        return storageList[0]

    r"""gets your location"""
    def get_location(self):
        return self.location

    r"""gets the subdirectories present at your location."""
    def get_sub_directories(self):
        return self.directoryTree[1]

    r"""gets teh files at your location."""
    def get_files(self):
        return self.directoryTree[2]

    r"""changes directory in manner dependent on inputs.

    based on the value of direction, the method moves the object up or down
    in the system's directory hierarchy. If the desire is to move down, a
    subdirectory name must be provided.

    parameters
    ----------
    direction : int
        Dictates if changing to a subdirectory or super directory,
        based on sign of int.
    path : {None, string}, optional
        if not None, it is expected that the object is moving to an immediate
        subdirectory whose name is the value of path.
    """
    def change_directory(self, direction = {-1, 1}, path = None):
        if direction == 1:
            os.chdir(self.location + "/" + path)
            self.location = os.getcwd()
            self.directoryTree = self.make_directory_tree()
        if direction == -1:
            newPath = self.location.split('/')
            newPath = '/' + '/'.join(newPath[1:len(newPath)-1])
            os.chdir(newPath)
            self.location = os.getcwd()
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
