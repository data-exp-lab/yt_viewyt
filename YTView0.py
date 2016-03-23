# -*- coding: utf-8 -*-
"""
Created on Sun Feb 14 16:41:36 2016

@author: A_Gilbert
"""
import sys
import math
import yt
import numpy as np
from PySide import QtCore
from PySide import QtGui


class YTView(QtGui.QMainWindow):
    
    def __init__(self):
        super(YTView, self).__init__()
        
        self.L = [1, 0, 0]
        self.N = [0,0,1]
        self.width = (10,'kpc')
        self.unitList = ["m","km","au","ly","pc","kpc","Mpc","Gpc"]
        
        self.ds = self.makeDataSet(sys.argv[1])
        self.makeInitialImage(self.ds)
        self.getFields(self.ds)
        
        self.size = QtCore.QSize(600,508)
        self.img = QtGui.QImageReader("initial.png")
        self.img.setScaledSize(self.size)
        
        self.pixmap = QtGui.QPixmap.fromImageReader(self.img)
        self.lbl = QtGui.QLabel(self)
        self.lbl.setPixmap(self.pixmap)
        super(YTView,self).setCentralWidget(self.lbl)
        
        self.FieldComboBox = QtGui.QComboBox()
        self.FieldValues = self.getFields(self.ds)
        self.FieldComboBox.insertItems(0, self.FieldValues)
        self.FieldComboBox.currentIndexChanged.connect(self.updateFieldImage)
        self.dockWidget1 = QtGui.QDockWidget("fieldValueBox", self)
        self.dockWidget1.setWidget(self.FieldComboBox)
        super(YTView,self).addDockWidget(QtCore.Qt.TopDockWidgetArea, self.dockWidget1)
        
        self.aziSlideWidget = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.aziSlideWidget.valueChanged.connect(self.angleSlideWidgetChanged)
        self.aziSlideWidget.setRange(0,360)
        self.aziSlideWidget.setValue(0)
        self.aziSlideWidget.setTickPosition(QtGui.QSlider.TicksBelow)
        self.aziSlideWidget.setTickInterval(10)
        
        self.polarSlideWidget = QtGui.QSlider(QtCore.Qt.Vertical)
        self.polarSlideWidget.valueChanged.connect(self.angleSlideWidgetChanged)
        self.polarSlideWidget.setRange(0,180)
        self.polarSlideWidget.setValue(90)
        self.polarSlideWidget.setTickPosition(QtGui.QSlider.TicksLeft)
        self.polarSlideWidget.setTickInterval(10)
        self.dockWidget2 = QtGui.QDockWidget("polarAngleSlider", self)
        self.dockWidget2.setWidget(self.polarSlideWidget)
        super(YTView,self).addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.dockWidget2)
        
        self.uButton = QtGui.QPushButton()
        self.uButton.setText("up")
        self.uButton.clicked.connect(self.panUp)
        
        self.dButton = QtGui.QPushButton()
        self.dButton.setText("down")
        self.dButton.clicked.connect(self.panDown)
        
        self.lButton = QtGui.QPushButton()
        self.lButton.setText("left")
        self.lButton.clicked.connect(self.panLeft)
        
        self.rButton = QtGui.QPushButton()
        self.rButton.setText("right")
        self.rButton.clicked.connect(self.panRight)
        
        self.deltaValWidget = QtGui.QSpinBox()
        
        self.deltaUnitWidget = QtGui.QComboBox()
        self.deltaUnitWidget.addItems(self.unitList)
        
        self.deltaWidgetLayout = QtGui.QGridLayout()
        self.deltaWidgetLayout.addWidget(self.deltaValWidget,0,0)
        self.deltaWidgetLayout.addWidget(self.deltaUnitWidget,0,1)
        self.deltaWidget = QtGui.QWidget()
        self.deltaWidget.setLayout(self.deltaWidgetLayout)
        
        self.panWidgetLayout = QtGui.QGridLayout()
        self.panWidgetLayout.addWidget(self.deltaWidget, 2, 2)
        self.panWidgetLayout.addWidget(self.uButton,1,2)
        self.panWidgetLayout.addWidget(self.dButton,3,2)
        self.panWidgetLayout.addWidget(self.lButton,2,1)
        self.panWidgetLayout.addWidget(self.rButton,2,3)
        
        self.panWidget = QtGui.QWidget()
        self.panWidget.setLayout(self.panWidgetLayout)
        
        self.bWidgetLayout = QtGui.QGridLayout()
        self.bWidgetLayout.addWidget(self.aziSlideWidget)
        self.bWidgetLayout.addWidget(self.panWidget,0,1)
    
        self.bWidget = QtGui.QWidget()
        self.bWidget.setLayout(self.bWidgetLayout)
        
        self.dockWidget3 = QtGui.QDockWidget()
        self.dockWidget3.setWidget(self.bWidget)
        super(YTView,self).addDockWidget(QtCore.Qt.BottomDockWidgetArea, self.dockWidget3)
        
        
        
        self.show()
     
     
    def updateFieldImage(self):
        L = self.L
        N = self.N
        w = self.width
        fieldString = self.FieldValues[self.FieldComboBox.currentIndex()]
        image = yt.OffAxisSlicePlot(self.ds, L, fieldString, width=w, north_vector=N)
        image.save("initial.png")
        self.img = QtGui.QImageReader("initial.png")
        self.img.setScaledSize(self.size)
        self.lbl.setPixmap(QtGui.QPixmap.fromImageReader(self.img))
        self.lbl.show()
        
    def makeDataSet(self,inputString):
        return yt.load(inputString)
        
    def makeInitialImage(self, ds):
        L = [1,0,0] #looking along the x-axis
        N = [0, 0, 1]
        image = yt.OffAxisSlicePlot(ds, L, 'density', width=self.width, north_vector=N)
        image.save("initial.png")
        
    def getFields(self,ds):
        flist = ds.field_list
        dflist = ds.derived_field_list
        flist = flist + dflist
        for x in range(0,len(flist)):
            a = flist[x][1]
            flist[x] = a
        return flist
        
    def angleSlideWidgetChanged(self):
        polar = math.radians(self.polarSlideWidget.value())
        azi = math.radians(self.aziSlideWidget.value())
        x = math.cos(azi)*math.sin(polar)
        y = math.sin(azi)*math.sin(polar)
        z = math.cos(polar)
        xn = math.cos(azi)*math.cos(polar)
        yn = math.sin(azi)*math.cos(polar)
        zn = -1 * math.sin(polar)
        self.L = [x,y,z]
        self.N = [xn,yn,zn]
        image = yt.OffAxisSlicePlot(self.ds, self.L, self.FieldValues[self.FieldComboBox.currentIndex()], width=self.width, north_vector=self.N)
        image.save("initial.png")
        self.img = QtGui.QImageReader("initial.png")
        self.img.setScaledSize(self.size)
        self.lbl.setPixmap(QtGui.QPixmap.fromImageReader(self.img))
        self.lbl.show()
        
    def panUp(self):
        image = yt.OffAxisSlicePlot(self.ds, self.L, self.FieldValues[self.FieldComboBox.currentIndex()], width=self.width, north_vector=self.N)
        dx = (0, self.unitList[self.deltaUnitWidget.currentIndex()])
        dy = (self.deltaValWidget.value(), self.unitList[self.deltaUnitWidget.currentIndex()])
        image.pan((dx, dy))
        image.save("initial.png")
        self.img = QtGui.QImageReader("initial.png")
        self.img.setScaledSize(self.size)
        self.lbl.setPixmap(QtGui.QPixmap.fromImageReader(self.img))
        self.lbl.show()
        
    def panDown(self):
        image = yt.OffAxisSlicePlot(self.ds, self.L, self.FieldValues[self.FieldComboBox.currentIndex()], width=self.width, north_vector=self.N)
        dx = yt.YTQuantity(0, self.deltaUnitWidget.currentText())
        dy = yt.YTQuantity(-1*self.deltaValWidget.value(), self.deltaUnitWidget.currentText())
        image.pan((dx, dy))
        image.save("initial.png")
        self.img = QtGui.QImageReader("initial.png")
        self.img.setScaledSize(self.size)
        self.lbl.setPixmap(QtGui.QPixmap.fromImageReader(self.img))
        self.lbl.show()
    
    def panRight(self):
        image = yt.OffAxisSlicePlot(self.ds, self.L, self.FieldValues[self.FieldComboBox.currentIndex()], width=self.width, north_vector=self.N)
        dx = yt.YTQuantity(self.deltaValWidget.value(), self.deltaUnitWidget.currentText())
        dy = yt.YTQuantity(0, self.deltaUnitWidget.currentText())
        image.pan((dx,dy))
        image.save("initial.png")
        self.img = QtGui.QImageReader("initial.png")
        self.img.setScaledSize(self.size)
        self.lbl.setPixmap(QtGui.QPixmap.fromImageReader(self.img))
        self.lbl.show()
    
    def panLeft(self):
        image = yt.OffAxisSlicePlot(self.ds, self.L, self.FieldValues[self.FieldComboBox.currentIndex()], width=self.width, north_vector=self.N)
        dx = yt.YTQuantity(-1*self.deltaValWidget.value(), self.deltaUnitWidget.currentText())
        dy = yt.YTQuantity(0, self.deltaUnitWidget.currentText())
        image.pan((dx,dy))
        image.save("initial.png")
        self.img = QtGui.QImageReader("initial.png")
        self.img.setScaledSize(self.size)
        self.lbl.setPixmap(QtGui.QPixmap.fromImageReader(self.img))
        self.lbl.show()
        


        
        
        
def main():
        
    app = QtGui.QApplication(sys.argv)
    ex = YTView()
    sys.exit(app.exec_())
        
        
        
        
        
if __name__ == '__main__':
    main()
