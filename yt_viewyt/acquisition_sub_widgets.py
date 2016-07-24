import types
from PyQt4 import QtGui
from yt.units import dimensions
from yt.units.unit_lookup_table import default_unit_symbol_lut as ulut, \
    prefixable_units, \
    unit_prefixes
from yt import YTArray
from acquisition_objects import YtDataObject


class CoordinateUnitsW(QtGui.QWidget):

    def __init__(self):
        super(CoordinateUnitsW, self).__init__()
        self.unit = None

        self.label = QtGui.QLabel("Unit:")
        self.unit_list = QtGui.QComboBox()
        self.unit_list.addItems([x for x in ulut.keys() if
                                 ulut[x][1] == dimensions.length])
        self.unit_list.currentIndexChanged.connect(self.check_prefix)

        self.prefix_widget = QtGui.QComboBox()
        self.prefix_widget.addItems(list(unit_prefixes.keys()))
        self.prefix_widget.addItem('None')
        self.prefix_widget.setHidden(True)

        self.layout = QtGui.QHBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.prefix_widget)
        self.layout.addWidget(self.unit_list)
        self.setLayout(self.layout)

    def check_prefix(self, index):
        unit = self.unit_list.itemText(index)
        if unit in prefixable_units:
            self.prefix_widget.setHidden(False)
        else:
            self.prefix_widget.setHidden(True)

    def get_unit(self):
        if self.prefix_widget.isHidden():
            return self.unit_list.currentText()
        else:
            unit = self.unit_list.currentText()
            prefix = self.prefix_widget.currentText()
            if prefix != 'None':
                out = prefix + unit
            else:
                out = unit
            return out


class CoordinateW(QtGui.QWidget):

    def __init__(self, coord):
        super(CoordinateW, self).__init__()
        self.label = QtGui.QLabel(coord)
        self.value = QtGui.QDoubleSpinBox()
        layout = QtGui.QHBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.value)
        self.setLayout(layout)

    def get_coordinate(self):
        return self.value.value()


class PointW(QtGui.QWidget):

    def __init__(self, parent, parent_widget):
        super(PointW, self).__init__()
        self.parent = parent
        self.parent_widget = parent_widget

        self.coordinate_unit_w = CoordinateUnitsW()

        # Assuming Cartesian, terrible I know, but deal with it.
        self.coord1 = CoordinateW('x')
        self.coord2 = CoordinateW('y')
        self.coord3 = CoordinateW('z')

        coord_combo_widget = QtGui.QWidget()
        coord_layout = QtGui.QHBoxLayout()
        coord_layout.addWidget(self.coord1)
        coord_layout.addWidget(self.coord2)
        coord_layout.addWidget(self.coord3)
        coord_combo_widget.setLayout(coord_layout)

        # Currently, inputting values here will do nothing.
        self.field_parametersw = QtGui.QWidget()
        self.field_parameters_label = QtGui.QLabel('Field Parameters')
        self.field_parameters = QtGui.QComboBox()
        self.field_parameters.addItem('None')

        field_parameters_layout = QtGui.QHBoxLayout()
        field_parameters_layout.addWidget(self.field_parameters_label)
        field_parameters_layout.addWidget(self.field_parameters)

        self.field_parametersw.setLayout(field_parameters_layout)

        self.data_sourcew = QtGui.QWidget()

        self.data_sourcel = QtGui.QLabel('data_source')
        self.data_source = QtGui.QComboBox()
        self.data_source.addItem('None')

        data_source_layout = QtGui.QHBoxLayout()
        data_source_layout.addWidget(self.data_sourcel)
        data_source_layout.addWidget(self.data_source)

        self.data_sourcew.setLayout(data_source_layout)

        # this object's parent is an AcquisitionActiveW
        self.data_source.addItems([x.name for x in
                                  self.parent.data_objects if type(x) ==
                                   YtDataObject])

        self.object_name = QtGui.QLineEdit()
        self.object_name.setText(self.parent.active_data_object.
                                 name + '_point')

        self.generate_object_btn = QtGui.QPushButton('Generate Object')
        self.generate_object_btn.clicked.connect(self.generate_object)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.coordinate_unit_w)
        layout.addWidget(coord_combo_widget)
        layout.addWidget(self.field_parametersw)
        layout.addWidget(self.data_sourcew)
        layout.addWidget(self.object_name)
        layout.addWidget(self.generate_object_btn)

        self.setLayout(layout)

        self.parent_widget.layout.addWidget(self)
        self.parent_widget.show()

    def generate_object(self):
        unit = self.coordinate_unit_w.get_unit()
        coord_unit1 = (self.coord1.get_coordinate())
        coord_unit2 = (self.coord2.get_coordinate())
        coord_unit3 = (self.coord2.get_coordinate())
        coord = [coord_unit1, coord_unit2, coord_unit3]
        coord = YTArray(coord, unit)

        name = self.object_name.text()

        source = self.parent.active_data_object.data

        if self.field_parameters.currentText() == 'None':
            if self.data_source.currentText() == 'None':
                point = source.point(coord)
                new_object = YtDataObject(point, name)

            else:
                dsource = [x for x in self.parent.data_objects
                           if x.name == self.data_source.currentText()]
                point = source.point(coord, data_source=dsource)
                new_object = YtDataObject(point, name)

            self.parent.add_data_object(new_object)


class ZeroDW(QtGui.QComboBox):

    def __init__(self, parent, parent_widget):
        super(ZeroDW, self).__init__()
        self.parent = parent
        self.parent_widget = parent_widget
        self.addItem('Point')
        self.parent_widget.layout.addWidget(self)
        self.parent_widget.show()

        PointW(self.parent, self.parent_widget)


class GeometricObjectW(QtGui.QComboBox):

    def __init__(self, parent, parent_widget):
        super(GeometricObjectW, self).__init__()
        self.parent = parent
        self.parent_widget = parent_widget

        self.addItems(['0D', '1D', '2D', '3D'])
        self.activated.connect(self.show_dimension_widget)

        self.parent_widget.layout.addWidget(self)

        self.parent_widget.show()

    def show_dimension_widget(self, index):
        if self.currentText() == '0D':
            ZeroDW(self.parent, self.parent_widget)


class DataObjectW(QtGui.QWidget):

    def __init__(self, parent):
        super(DataObjectW, self).__init__()
        self.parent = parent
        self.data_object_options = QtGui.QComboBox()
        self.data_object_options.addItems(['Geometric Object',
                                           'Filtering Object',
                                           'Collection Object',
                                           'Construction Object'])
        self.data_object_options.activated.connect(
            self.show_object_widget)

        self.layout = QtGui.QVBoxLayout()
        self.layout.addWidget(self.data_object_options)
        self.setLayout(self.layout)

    def show_object_widget(self, index):
        if self.data_object_options.currentText() == 'Geometric Object':
            geometric_obj_w = GeometricObjectW(self.parent, self)
            self.layout.addWidget(geometric_obj_w)
            self.show()


class ActiveObjectMenu(QtGui.QMenu):

    def __init__(self, aParent):
        super(ActiveObjectMenu, self).__init__()
        self.parent = aParent
        self.addAction("New Data Object", self.get_data_objectw)
        self.addAction("New Plot", self.get_plotw)
        self.addAction("Remove", self.remove)

    def remove(self):
        item = self.parent.data_object_list_widget.currentItem()
        index = self.parent.data_object_list_widget.indexOfTopLevelItem(item)
        trash = self.parent.data_object_list_widget.takeTopLevelItem(index)
        del trash
        del index
        self.parent.dataObjects = [x for x in self.parent.data_objects if
                                   x.name != item.text(0)]
        if self.parent.active_data_object is not None:
            if self.parent.active_data_object.name == item.text(0):
                self.parent.active_data_object = None

    def get_plotw(self):
        def closeEvent(self, event):
            self.deleteLater()
            del(self.parent.plot_dialog)
        self.plot_dialog = QtGui.QWidget()
        self.plot_dialog.closeEvent = types.MethodType(closeEvent,
                                                       self.plot_dialog,
                                                       QtGui.QCloseEvent)
        self.plot_dialog.parent = self
        self.plot_dialog.show()

    def get_data_objectw(self):
        def closeEvent(self, event):
            self.deleteLater()

        data_objectw = DataObjectW(self.parent)
        data_objectw.closeEvent = types.MethodType(closeEvent, data_objectw,
                                                   QtGui.QCloseEvent)
        data_objectw.show()
