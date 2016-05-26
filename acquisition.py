import sys
import os
import yt
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
        tmp = self.directoryTree[1]
        out = []
        for x in tmp:
            if x[0] != '.':
                out.append(x)
        return out

    r"""gets the files at your location."""
    def get_files(self):
        tmp = self.directoryTree[2]
        out = []
        for x in tmp:
            if x[0] != '~' and x[0] != '.':
                out.append(x)
        return out

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

This widget is meant to enable file navigation from multiple sources (read devices) so that remote as well as local data can be accessed. It then calls for a ytObject to be instantiated utilizing the name and location of selected files.

Parameters
----------
directoryObjs : list
    A list of all available directory objs, both local and remote.
activeDirectoryObj : DirectoryObject
    The directory object whose files and folders are currently displayed by
    the widget.
fileTreeWidget : QTreeWidget
    The widget that displays the ``activeDirectoryObj`` files and folders.
    It also responds to user input to enable navigation on the ``activeDirectoryObj``.
lButton : QPushButton
    One of two buttons used to cycle through the list of available directoryObjs.
    Currently has no functionality.
rButton : QPushButton
    The other button used to cycle through the list of avialable directories.
    Currently has no functionality.
sourceLabel : QLabel
    A Widget whose text displays the current activeDirectoryObj.
sourceBarLayout : QHBoxLayout
    The layout of the widget containing lButton, rButton, and
    sourceLabel.
sourceBarWidget : QWidget
    The widget containing lButton, rButton, and sourceLabel
loadButtton : QPushButton
    The button that is supposed to function as the call
    to load a file for users. Subject to change.
layout : QVBoxLayout
    The Layout of this widget.
Notes
------
This is going to be something that will be continuously modified so long as
someone is working on the app as a whole. Potential improvements include:
-shortening __init__
    accomplished by making functions that take care of setting up layouts.
-creating a widget menu
    making a widget that appears when users left click on files to load
    them. This menu would have the ability to load straight to a view, load the
    files as a dataset series, move the files, etc.
-acceptable file highlighting
    create a way to identify files that can be loaded by yt or loaded into a
    view. have these files and their parent directories have a standard
    appearance. Other files and directories would have a lower contrast
    or whatever terminology describes the demphasis exhibited by other
    folder navigation systems (finder *cough cough*).
-ability to have remote sources
    enable remote data access. This will mean placing an add and subract
    button somewhere. Beyond that, I currently have no idea how to go about this.
-Whatever a bulk number of users request
    this is made for users by users, so if we all want something, make every
    effort to make it happen.
"""
class AcquisitionSourceW(QtGui.QWidget):

    def __init__(self):
        super(AcquisitionSourceW, self).__init__()

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

        self.loadButton = QtGui.QPushButton("Load")

        self.layout = QtGui.QVBoxLayout()
        self.layout.addWidget(self.sourceBarWidget)
        self.layout.addWidget(self.fileTreeWidget)
        self.layout.addWidget(self.loadButton)

        self.setLayout(self.layout)
        self.show()

    r"""Initializes a local DirectoryObject."""
    def make_initial_DirectoryObjects(self):
        a = DirectoryObject()
        self.directoryObjs.append(a)

    r"""Lists everything in the current directory as a tree.

        This takes every file and directory in the current
        directory and constructs a Tree widget with
        icons."""
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
            childItem.setIcon(0, self.style().standardIcon(
                QtGui.QStyle.SP_FileIcon))
        for x in self.activeDirectoryObj.get_sub_directories():
            childItem = QtGui.QTreeWidgetItem(directory)
            childItem.setText(0, x)
            childItem.setIcon(0, self.style().standardIcon(
                QtGui.QStyle.SP_DirIcon))
        self.fileTreeWidget.addTopLevelItem(directory)
        directory.setExpanded(True)

    r"""Function called by collapsing the current directory representation
        on screen.

        This function clears the fileTreeWidget, moves the activeDirectoryObj to
        the directory above the current working directory, and reconstructs the
        fileTreeWidget based on the new location."""
    def move_up(self):
        self.fileTreeWidget.clear()
        self.activeDirectoryObj.change_directory(direction = -1)
        self.set_file_tree_widget()

    r"""Function called by clicking on an entry in the fileTreeWidget that is
        also a sub-directory of the current working directory. Moves the
        activeDirectoryObj to the sub-directory, clears the fileTreeWidget,
        and then constructs the fileTreeWidget according to the new location.
    """
    def move_down(self):
        if self.fileTreeWidget.currentItem().text(0) in self.activeDirectoryObj.get_sub_directories():
            nextDir = self.fileTreeWidget.currentItem().text(0)
            self.fileTreeWidget.clear()
            self.activeDirectoryObj.change_directory(direction = 1, path = nextDir)
            self.set_file_tree_widget()

class YtObject(object):

    def __init__(self, fileName):
        super(YtObject, self).__init__()

        if isinstance(fileName, list):
            self.data = yt.load(fileName)
            self.dataType = "data set series"
            self.name = "Needs Work"
        else:
            self.data = yt.load(fileName)
            self.dataType = "dataset"
            self.name = fileName

class AcquisitionActiveW(QtGui.QWidget):

    def __init__(self):
        super(AcquisitionActiveW, self).__init__()
        self.dataObjects = []
        self.activeDataObject = None

        self.label = QtGui.QLabel("Active Data Objects")

        self.dataObjectListWidget = QtGui.QListWidget()
        self.set_ObjectListWidget()

        self.layout = QtGui.QVBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.dataObjectListWidget)
        self.setLayout(self.layout)

        self.show()

    def add_data_object(self, dataObject):
        self.dataObjects.append(dataObject)
        self.set_ObjectListWidget()

    def add_data_object_from_file(self, filename):
        self.dataObjects.append(YtObject(filename))
        self.set_ObjectListWidget()


    #def set_active_DataObject(self):

    def set_ObjectListWidget(self):
        self.dataObjectListWidget.clear()
        for x in self.dataObjects:
            listWidgetItem = QtGui.QListWidgetItem()
            listWidgetItem.setText(x.name)
            listWidgetItem.setIcon(QtGui.QIcon("icons/yt_icon.png"))
            self.dataObjectListWidget.addItem(listWidgetItem)

class AcquisitionMasterW(QtGui.QWidget):

    def __init__(self):
        super(AcquisitionMasterW, self).__init__()
        self.sourceW = AcquisitionSourceW()
        self.activeW = AcquisitionActiveW()

        self.sourceW.loadButton.clicked.connect(self.load_to_activeW)

        self.layout = QtGui.QVBoxLayout()
        self.layout.addWidget(self.activeW)
        self.layout.addWidget(self.sourceW)
        self.setLayout(self.layout)
        self.show()

    def load_to_activeW(self):
        selectedFile = self.sourceW.fileTreeWidget.currentItem().text(0)
        self.activeW.add_data_object_from_file(selectedFile)



def main():
    app = QtGui.QApplication(sys.argv)
    ex = AcquisitionMasterW()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
