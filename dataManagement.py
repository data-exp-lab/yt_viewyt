"""
Data management widget for ytView.
"""
import yt
from PySide import QtCore
from PySide import QtGui


        
class dataSourceWidget(QtCore.QObject):
    
    def __init__(self):
        super(dataSourceWidget, self).__init__()
        
        self.addButton = QtGui.QPushButton("add")
        self.addButton.setStyle(QtGui.QPlastiqueStyle)
        self.removeButton = QtGui.QPushButton("remove")
        self.removeButton.setStyle(QtGui.QPlastiqueStyle)
        layout = QtGui.QLayout(self)
        layout.addWidget(self.removeButton, 0, 0)
        layout.addWidget(self.addButton, 0, 1)
        
        self.setLayout()
        


class dataObjectWidget(QtCore.QObject):
        
        
class dataManagement(QtCore.QObject):
    
    def __init__(self):