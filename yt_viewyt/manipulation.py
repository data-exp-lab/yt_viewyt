import sys
from PyQt4.QtGui import *
from yt.units import dimensions
from yt.units.unit_lookup_table import default_unit_symbol_lut as unitTable

class CoordinateWidget(QWidget):

    def __init__(self, axis):

        super(CoordinateWidget, self).__init__()

        self.axisLabel = QLabel(axis)

        self.axisDialog = QLineEdit()

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.axisLabel)
        self.layout.addWidget(self.axisDialog)

        self.setLayout(self.layout)

class UnitWidget(QWidget):

    def __init__(self, dimension):
        super(UnitWidget, self).__init__()

        self.unitComboBox = QComboBox()
        self.label = QLabel("Units:")

        for x in unitTable:
            if unitTable[x][1] == dimension:
                self.unitComboBox.addItem(x)

        layout = QHBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.unitComboBox)
        self.setLayout(layout)

        self.show()




class LocationWidget(QWidget):

    def __init__(self):
        super(LocationWidget, self).__init__()

        layout = QVBoxLayout()

        lengthWidget = UnitWidget(dimensions.length)

        layout.addWidget(lengthWidget)

        for c in ['X:', 'Y:', 'Z:']:
            layout.addWidget(CoordinateWidget(c))

        self.setLayout(layout)

        self.show()

def main():
    app = QApplication(sys.argv)
    ex = LocationWidget()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()



