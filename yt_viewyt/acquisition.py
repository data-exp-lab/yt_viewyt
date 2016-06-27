"""All classes associated with acquiring data for application"""

import sys
import os
import yt
from PyQt4 import QtGui


class DirectoryObject(object):
    r"""The initial component for an object that provides a backend
    for navigating folders on a system.

    This class provides immediate access to a users location in the system
    directory, any sub-directories the user can move into, and any files
    in the current user location. It also has the ability to move around
    in the directory system.

    Parameters
    ----------
    location : String
        String that contains the current working directory.
    directoryTree : List
        List that contains the path-name of the current directory,
        the list of sub-directories in the current directory, and
        a list of files in the current directory.
    source : String
        The string denoting where the current directoryObject is from.
        A future goal of this application is the ability to support
        data from multiple sources via some mechanism.

    Notes:
    -------
    I have not investigated it deeply due to my ignorance regarding networking,
    but the following topics may provide the foundation needed to build an
    inter-device application:
    -python subprocess module
    -QtGui.QFileSystemModel
    """

    def __init__(self, path=None, source="Local Machine"):
        r"""Initializes an instance of the DirectoryObject.

        Creates a DirectoryObject based on an input path, with the initial
        assumption that the path is to a location on the local machine.

        Parameters
        ----------
        path : {None, sting}, optional
            The path that marks the initial location of the given
            instance.
        source : {'Local Machine', 'other source string'}, optional
            The source of the given path and ultimately the instance
            itself. Defaults to "Local Machine".

        Returns
        -------
        DirectoryObject
            """
        if path is None:
            self.location = os.getcwd()
            self.directoryTree = self.make_directory_tree()
            self.source = source
        else:
            self.location = path
            self.location = self.make_directory_tree()
            self.source = source

    def make_directory_tree(self):
        r"""Provides a list of information about the current
        working directory.

        Provides the current directory name, sub directories, and files
        by taking the first output of the os.walk() command.

        Returns
        -------
        List
            This output contains the current directory name, subdirectory
            names, and file names in the current directory, in that order."""
        a = os.walk(self.location).next()
        dirName = a[0].split('/')
        dirName = dirName[-1]
        return [dirName, a[1], a[2]]

    def get_location(self):
        r"""gets your location"""
        return self.location

    def get_top_dir_name(self):
        return self.directoryTree[0]

    def get_sub_directories(self):
        r"""gets the subdirectories present at your location."""
        tmp = self.directoryTree[1]
        out = []
        for x in tmp:
            if x[0] != '.':
                out.append(x)
        return out

    def get_files(self):
        r"""gets the files at your location."""
        tmp = self.directoryTree[2]
        out = []
        for x in tmp:
            if x[0] != '~' and x[0] != '.':
                out.append(x)
        return out

    def change_directory(self, direction={-1, 1}, path=None):
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
            if not None, it is expected that the object is moving to an
            immediate subdirectory whose name is the value of path.
        """
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


class AcquisitionSourceW(QtGui.QWidget):
    r"""A widget for adding sources, finding files, and passing said files to the
    load command.

    This widget is meant to enable file navigation from multiple sources
    (read devices) so that remote as well as local data can be accessed.
    It then calls for a ytObject to be instantiated utilizing the name
    and location of selected files.

    Parameters
    ----------
    directoryObjs : list
        A list of all available directory objs, both local and remote.
    activeDirectoryObj : DirectoryObject
        The directory object whose files and folders are currently displayed by
        the widget.
    fileTreeWidget : QTreeWidget
        The widget that displays the ``activeDirectoryObj`` files and folders.
        It also responds to user input to enable navigation on the
        ``activeDirectoryObj``.
    lButton : QPushButton
        One of two buttons used to cycle through the list of available
        directoryObjs. Currently has no functionality.
    rButton : QPushButton
        The other button used to cycle through the list of available
        directories. Currently has no functionality.
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
    button somewhere. Beyond that, I currently have no idea how to go
    about this.
    -Whatever a bulk number of users request
    this is made for users by users, so if we all want something, make every
    effort to make it happen.
    """

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

    def make_initial_DirectoryObjects(self):
        r"""Initializes a local DirectoryObject."""
        a = DirectoryObject()
        self.directoryObjs.append(a)

    def set_file_tree_widget(self):
        r"""Lists everything in the current directory as a tree.

        This takes every file and directory in the current
        directory and constructs a Tree widget with
        icons."""
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

    def move_up(self):
        r"""Function called by collapsing the current directory representation
        on screen.

        This function clears the fileTreeWidget, moves the activeDirectoryObj
        to the directory above the current working directory, and
        reconstructs the fileTreeWidget based on the new location."""
        self.fileTreeWidget.clear()
        self.activeDirectoryObj.change_directory(direction=-1)
        self.set_file_tree_widget()

    def move_down(self):
        r"""Function called by clicking on an entry in the fileTreeWidget that is
        also a sub-directory of the current working directory. Moves the
        activeDirectoryObj to the sub-directory, clears the fileTreeWidget,
        and then constructs the fileTreeWidget according to the new location.
        """
        if self.fileTreeWidget.currentItem().text(0) \
           in self.activeDirectoryObj.get_sub_directories():
            nextDir = self.fileTreeWidget.currentItem().text(0)
            self.fileTreeWidget.clear()
            self.activeDirectoryObj.change_directory(direction=1, path=nextDir)
            self.set_file_tree_widget()


class YtObject(object):
    r"""A basic representation of a data object loaded through yt.

    This is the object that is used to track all objects that have been
    loaded with yt or created by a method written in yt, like novel
    data objects.

    Parameters
    -----------
    data : yt.frontends object
        The actual data object referenced by yt.

    dataType : string
        This parameter references whether the data loaded into yt is a dataset
        series or a single data object. It will ultimately be used to determine
        whether widgets that manipulate the time step of a view will be
        available or not.

    name : string
        The name of the loaded object. It defaults to the name of the filename
        in the case of a single data object.

    Notes
    ------
    This is a weak class at the moment, and could utilize a lot of work.
    Some improvements that could be made:
    -Support for icons that distinguish what frontend yt is using, and if the
    object is a single data object or a data series.
    -Methods to create novel data objects from the initial file loaded, and to
    name those novel objects
    -Methods to save data objects
    """

    def __init__(self, fileName):
        r"""Initializes an instance of the YtObject.

        Specifically, this creates an instance of YtObject based on the type
        of `fileName`. If it is a list, the initialization assumes a
        data series.

        Parameters
        ----------
        fileName : string or list of string
            The name of the file from which the instance is being
            initialized.

        Returns
        -------
        self : YtObject"""
        super(YtObject, self).__init__()

        if isinstance(fileName, list):
            self.data = yt.load(fileName)
            self.dataType = "data set series"
            self.name = "Needs Work"
        else:
            self.data = yt.load(fileName)
            self.dataType = "dataset"
            self.name = fileName

    def get_data(self):
        r"""Returns the yt data object for the given instance

        Returns
        -------
        data : yt.frontend_like
        The data from the instance of the YtObject.
        """
        return self.data


class AcquisitionActiveW(QtGui.QWidget):

    def __init__(self):
        super(AcquisitionActiveW, self).__init__()
        self.dataObjects = []
        self.activeDataObject = None

        self.label = QtGui.QLabel("Active Data Objects")

        self.dataObjectListWidget = QtGui.QListWidget()
        self.set_ObjectListWidget()
        self.dataObjectListWidget.itemClicked.connect(
            self.set_active_DataObject)

        self.passToViewButton = QtGui.QPushButton("View")

        self.layout = QtGui.QVBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.dataObjectListWidget)
        self.layout.addWidget(self.passToViewButton)
        self.setLayout(self.layout)

        self.show()

    def add_data_object(self, dataObject):
        self.dataObjects.append(dataObject)
        self.set_ObjectListWidget()

    def add_data_object_from_file(self, filename):
        print filename
        tempObj = YtObject(filename)
        self.add_data_object(tempObj)

    def set_active_DataObject(self):
        for x in self.dataObjects:
            if x.name == self.dataObjectListWidget.currentItem().text():
                self.activeDataObject = x

    def get_active_DataObject(self):
        return self.activeDataObject

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
        selectedFile = str(selectedFile)
        self.activeW.add_data_object_from_file(selectedFile)


def main():
    app = QtGui.QApplication(sys.argv)
    AcquisitionMasterW()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
