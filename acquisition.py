import sys
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

Notes:
-------
I have not investigated it deeply due to my ignorance regarding networking,
but the following topics may provide the foundation needed to build an inter-device
application:
-python subprocess module
-QtGui.QFileSystemModel
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
        a = os.walk(self.location).next()
        dirName = a[0].split('/')
        dirName = dirName[-1]
        return [dirName, a[1], a[2]]

    r"""gets your location"""
    def get_location(self):
        return self.location

    def get_top_dir_name(self):
        return self.directoryTree[0]

    r"""gets the subdirectories present at your location."""
    def get_sub_directories(self):
        return self.directoryTree[1]

    r"""gets the files at your location."""
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

r"""A widget for adding sources, finding files, and passing said files to the
load command.

"""
class acquisitionSourceW(QtGui.QWidget):

    def __init__(self):
        super(acquisitionSourceW, self).__init__()

        self.directoryObjs = []
        self.make_initial_DirectoryObjects()

        self.activeDirectoryObj = self.directoryObjs[0]
        self.activeSource = self.activeDirectoryObj.source

        self.fileTreeWidget = QtGui.QTreeWidget()
        self.set_file_tree_widget()
        self.fileTreeWidget.itemCollapsed.connect(self.move_up)
        self.fileTreeWidget.itemClicked.connect(self.move_down)

        self.lButton = QtGui.QPushButton("<")
        self.rButton = QtGui.QPushButton(">")
        self.sourceLabel = QtGui.QLabel("Source: " + self.activeSource)

        self.sourceBarLayout = QtGui.QHBoxLayout()
        self.sourceBarLayout.addWidget(self.lButton)
        self.sourceBarLayout.addWidget(self.sourceLabel)
        self.sourceBarLayout.addWidget(self.rButton)

        self.sourceBarWidget = QtGui.QWidget()
        self.sourceBarWidget.setLayout(self.sourceBarLayout)

        self.layout = QtGui.QVBoxLayout()
        self.layout.addWidget(self.sourceBarWidget)
        self.layout.addWidget(self.fileTreeWidget)

        self.setLayout(self.layout)
        self.show()

    def make_initial_DirectoryObjects(self):
        a = DirectoryObject()
        self.directoryObjs.append(a)

    def set_file_tree_widget(self):
        self.fileTreeWidget.setColumnCount(1)
        hiddenHeader = QtGui.QTreeWidgetItem()
        hiddenHeader.setText(0, "go away")
        self.fileTreeWidget.setHeaderItem(hiddenHeader)
        hiddenHeader.setHidden(True)
        self.fileTreeWidget.setHeaderItem(None)
        directory = QtGui.QTreeWidgetItem(self.fileTreeWidget)
        directory.setText(0, self.activeDirectoryObj.get_top_dir_name())
        for x in self.activeDirectoryObj.get_files():
            childItem = QtGui.QTreeWidgetItem(directory)
            childItem.setText(0, x)
        for x in self.activeDirectoryObj.get_sub_directories():
            childItem = QtGui.QTreeWidgetItem(directory)
            childItem.setText(0, x)
        self.fileTreeWidget.addTopLevelItem(directory)
        directory.setExpanded(True)

    def move_up(self):
        self.fileTreeWidget.clear()
        self.activeDirectoryObj.change_directory(direction = -1)
        self.set_file_tree_widget()

    def move_down(self):
        if self.fileTreeWidget.currentItem().text(0) in self.activeDirectoryObj.get_sub_directories():
            nextDir = self.fileTreeWidget.currentItem().text(0)
            self.fileTreeWidget.clear()
            self.activeDirectoryObj.change_directory(direction = 1, path = nextDir)
            self.set_file_tree_widget()

def main():
    app = QtGui.QApplication(sys.argv)
    ex = acquisitionSourceW()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
