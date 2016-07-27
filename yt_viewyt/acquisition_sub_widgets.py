from PyQt4 import QtGui
from yt.units import dimensions
from yt.units.unit_lookup_table import default_unit_symbol_lut as ulut, \
    prefixable_units, \
    unit_prefixes
from acquisition_objects import YtDataObject
from yt.data_objects.static_output import FieldNameContainer as Container


class NameW(QtGui.QWidget):

    def __init__(self, start_text):
        super(NameW, self).__init__()

        label = QtGui.QLabel('Object Name:')

        self.name_w = QtGui.QLineEdit()
        self.name_w.setText(start_text)

        layout = QtGui.QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.name_w)

        self.setLayout(layout)

    def get_name(self):
        return self.name_w.text()


class FieldParametersW(QtGui.QWidget):

    def __init__(self):
        super(FieldParametersW, self).__init__()
        self.field_parameters_label = QtGui.QLabel('Field Parameters')
        self.field_parameters = QtGui.QComboBox()
        self.field_parameters.addItem('None')

        field_parameters_layout = QtGui.QHBoxLayout()
        field_parameters_layout.addWidget(self.field_parameters_label)
        field_parameters_layout.addWidget(self.field_parameters)

        self.setLayout(field_parameters_layout)

    def get_field_parameters(self):
        return self.field_parameters.currentText()


class DataSourceW(QtGui.QWidget):

    def __init__(self, parent):
        super(DataSourceW, self).__init__()
        self.parent = parent

        self.data_sourcel = QtGui.QLabel('data_source')
        self.data_source = QtGui.QComboBox()
        self.data_source.addItem('None')

        data_source_layout = QtGui.QHBoxLayout()
        data_source_layout.addWidget(self.data_sourcel)
        data_source_layout.addWidget(self.data_source)

        self.setLayout(data_source_layout)

        # this object's parent is an AcquisitionActiveW
        self.data_source.addItems([x.name for x in
                                  self.parent.data_objects if type(x) ==
                                   YtDataObject])

    def get_data_source(self):
        name = self.data_source.currentText()
        out = [x for x in self.parent.data_objects if x.name == name]
        if len(out) == 1:
            out = out[0].data
        else:
            out = None
        return out


class CartAxisW(QtGui.QWidget):

    def __init__(self, label):
        super(CartAxisW, self).__init__()
        label = QtGui.QLabel(label)

        self.options = QtGui.QComboBox()
        self.options.addItems(['x', 'y', 'z'])

        layout = QtGui.QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.options)

        self.setLayout(layout)

    def get_axis(self):
        return self.options.currentText()


class CoordinateUnitsW(QtGui.QWidget):

    def __init__(self):
        super(CoordinateUnitsW, self).__init__()

        self.label = QtGui.QLabel("Coordinate Units:")
        self.unit_list = QtGui.QComboBox()
        self.unit_list.addItems([x for x in ulut.keys() if
                                 ulut[x][1] == dimensions.length])
        self.unit_list.addItem('Code Length')
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
            out = self.unit_list.currentText()
            if out == 'Code Length':
                out = None
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
        self.value.setMaximum(1000)
        layout = QtGui.QHBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.value)
        self.setLayout(layout)

    def get_coordinate(self):
        return self.value.value()

    def set_label(self, new_coord):
        self.label.setText(new_coord)
        self.show()


class CartCoordinateComboW(QtGui.QWidget):

    def __init__(self):
        super(CartCoordinateComboW, self).__init__()
        self.coord1 = CoordinateW('x')
        self.coord2 = CoordinateW('y')
        self.coord3 = CoordinateW('z')

        layout = QtGui.QHBoxLayout()
        layout.addWidget(self.coord1)
        layout.addWidget(self.coord2)
        layout.addWidget(self.coord3)

        self.setLayout(layout)

    def get_coordinates(self):
        return [self.coord1.get_coordinate(),
                self.coord2.get_coordinate(),
                self.coord3.get_coordinate()]


class Var2CoordinateComboW(QtGui.QWidget):

    def __init__(self, label1, label2):
        super(Var2CoordinateComboW, self).__init__()
        self.coordinate1 = CoordinateW(label1)
        self.coordinate2 = CoordinateW(label2)

        layout = QtGui.QHBoxLayout()

        layout.addWidget(self.coordinate1)
        layout.addWidget(self.coordinate2)

        self.setLayout(layout)

    def get_coordinates(self):
        return [self.coordinate1.get_coordinate(),
                self.coordinate2.get_coordinate()]


class WidthW(QtGui.QWidget):

    def __init__(self):
        super(WidthW, self).__init__()

        opt1 = QtGui.QCheckBox('Square Plot')
        opt2 = QtGui.QCheckBox('Rectangle Plot')

        opt1.setChecked(True)

        self.buttons = QtGui.QButtonGroup()
        self.buttons.addButton(opt1)
        self.buttons.addButton(opt2)

        buttonw = QtGui.QGroupBox("Plot Shape:")
        buttonw_layout = QtGui.QHBoxLayout()
        buttonw_layout.addWidget(opt1)
        buttonw_layout.addWidget(opt2)

        buttonw.setLayout(buttonw_layout)

        self.units = CoordinateUnitsW()
        self.units.label.setText('Units of Plot Region Dimension:')

        self.width = Var2CoordinateComboW('Plot Region Side Length:',
                                          'Plot Region Height:')
        self.width.coordinate2.setHidden(True)

        self.buttons.buttonClicked.connect(self.set_plot_params)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(buttonw)
        layout.addWidget(self.units)
        layout.addWidget(self.width)
        self.setLayout(layout)

    def set_plot_params(self):
        case = self.buttons.checkedButton().text()[0]

        if case == 'S':
            self.units.label.setText('Units of Plot Region Dimension:')
            self.width.coordinate2.setHidden(True)
        else:
            self.units.label.setText("Units of Plot Region Dimensions:")
            self.width.coordinate1.setLabel('Plot Region Width:')
            self.width.coordinate2.setHidden(False)

    def get_width(self):
        case = self.buttons.checkedButton().text()[0]

        if case == 'S':
            coord = self.width.coordinate1.get_coordinate()
            unit = self.units.get_unit()
            if unit is not None:
                return (coord, unit)
            else:
                return coord
        else:
            coord = self.width.get_coordinates
            unit = self.units.get_unit()
            if unit is not None:
                return ((coord[0], unit), (coord[1], unit))
            else:
                return (coord[0], coord[1])


class FieldSelectorW(QtGui.QWidget):

    def __init__(self, data_object, a_label):
        super(FieldSelectorW, self).__init__()
        label = QtGui.QLabel(a_label)

        if hasattr(data_object.data, 'ds'):
            source = data_object.data.ds
        else:
            source = data_object.data

        self.field_dict = {}
        self.field_dict = self.recursive_dict('fields', source,
                                              self.field_dict)

        self.top_selector = QtGui.QComboBox()
        self.top_selector.addItems(self.field_dict['fields'])
        self.top_selector.currentIndexChanged.connect(
            self.set_selector2)

        self.selector2 = QtGui.QComboBox()
        self.selector2.addItems(self.field_dict[
            self.top_selector.currentText()])
        self.selector2.setEditable(True)

        layout = QtGui.QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.top_selector)
        layout.addWidget(self.selector2)

        self.setLayout(layout)

    def recursive_dict(self, name, source, field_dict):
        field_dict[name] = []
        for x in dir(getattr(source, name)):
            field_dict[name].append(x)
            if type(getattr(getattr(source, name), x)) == Container:
                field_dict = self.recursive_dict(x, getattr(source, name),
                                                 field_dict)
        return field_dict

    def set_selector2(self, index):
        ref = self.top_selector.currentText()
        self.selector2.clear()
        self.selector2.addItems(self.field_dict[ref])

    def get_field(self):
        return (self.top_selector.currentText(), self.selector2.currentText())


class VarFieldSelectorsW(QtGui.QWidget):

    def __init__(self, data_object, num):
        super(VarFieldSelectorsW, self).__init__()
        self.source = data_object
        self.widget_list = []

        self.layout = QtGui.QVBoxLayout()

        self.set_field_selectors(num)

        for x in self.widget_list:
            self.layout.addWidget(x)

        self.setLayout(self.layout)

    def set_field_selectors(self, num):
        if len(self.widget_list) < num:
            while len(self.widget_list) < num:
                i = len(self.widget_list)
                label = "Field %s:" % i
                self.widget_list.append(FieldSelectorW(self.source, label))
                self.layout.addWidget(self.widget_list[-1])
        else:
            while len(self.widget_list) > num:
                trash = self.widget_list.pop()
                self.layout.removeWidget(trash)
                del trash

    def get_fields(self):
        fields = []
        for x in self.widget_list:
            fields.append(x.get_field())
        return fields


class MasterFieldSelectionW(QtGui.QWidget):

    def __init__(self, data_object):
        super(MasterFieldSelectionW, self).__init__()

        self.source = data_object

        num_label = QtGui.QLabel('Number of Fields to Plot:')

        self.num_selector = QtGui.QSpinBox()
        self.num_selector.setMinimum(1)
        self.num_selector.setValue(1)

        num_w = QtGui.QWidget()
        num_w_layout = QtGui.QHBoxLayout()
        num_w_layout.addWidget(num_label)
        num_w_layout.addWidget(self.num_selector)
        num_w.setLayout(num_w_layout)

        self.field_list = VarFieldSelectorsW(self.source, 1)

        self.num_selector.valueChanged.connect(
            self.field_list.set_field_selectors)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(num_w)
        layout.addWidget(self.field_list)

        self.setLayout(layout)

    def get_fields(self):
        return self.field_list.get_fields()
