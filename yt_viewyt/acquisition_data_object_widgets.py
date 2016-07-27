import types
from PyQt4 import QtGui
from yt import YTArray
from acquisition_objects import YtDataObject
from acquisition_sub_widgets import NameW, FieldParametersW, DataSourceW, \
     CoordinateUnitsW, CoordinateW, CartCoordinateComboW
from acquisition_plot_widgets import PlotObjectW


class PointW(QtGui.QWidget):

    def __init__(self, parent, parent_widget):
        super(PointW, self).__init__()
        self.parent = parent
        self.parent_widget = parent_widget

        self.coordinate_unit_w = CoordinateUnitsW()

        # Assuming Cartesian, terrible I know, but deal with it.
        self.coord_combo_w = CartCoordinateComboW()

        # Currently, inputting values here will do nothing.
        self.field_parametersw = FieldParametersW()

        self.data_sourcew = DataSourceW(self.parent)

        self.object_name = NameW(self.parent.active_data_object.name +
                                 '_point')

        self.generate_object_btn = QtGui.QPushButton('Generate Object')
        self.generate_object_btn.clicked.connect(self.generate_object)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.coordinate_unit_w)
        layout.addWidget(self.coord_combo_w)
        layout.addWidget(self.field_parametersw)
        layout.addWidget(self.data_sourcew)
        layout.addWidget(self.object_name)
        layout.addWidget(self.generate_object_btn)

        self.setLayout(layout)

        self.parent_widget.layout.addWidget(self)
        self.parent_widget.show()

    def generate_object(self):
        unit = self.coordinate_unit_w.get_unit()
        coord = self.coord_combo_w.get_coordinates()

        if unit is not None:
            coord = YTArray(coord, unit)

        name = self.object_name.get_name()

        source = self.parent.active_data_object.data

        if self.field_parametersw.get_field_parameters() == 'None':
            if self.data_sourcew.get_data_source() is None:
                point = source.point(coord)
                new_object = YtDataObject(point, name)

            else:
                dsource = self.data_source.get_data_source()
                point = source.point(coord, data_source=dsource)
                new_object = YtDataObject(point, name)

            self.parent.add_data_object(new_object)


class AxisRayW(QtGui.QWidget):
    axis_dict = {'x': 0, 'y': 1, 'z': 2}

    def __init__(self, parent, parent_widget):
        super(AxisRayW, self).__init__()

        self.parent = parent
        self.parent_widget = parent_widget

        axis_label = QtGui.QLabel('Axis of Alignment:')
        self.axisw = QtGui.QComboBox()
        self.axisw.addItems(list(self.axis_dict.keys()))

        axis_super_w = QtGui.QWidget()
        axis_layout = QtGui.QHBoxLayout()
        axis_layout.addWidget(axis_label)
        axis_layout.addWidget(self.axisw)
        axis_super_w.setLayout(axis_layout)

        self.coord_units_w = CoordinateUnitsW()

        coord_label = QtGui.QLabel('Coordinate Ray Intersects:')

        self.set_coord_widgets(None)

        coord_super_w = QtGui.QWidget()
        coord_layout = QtGui.QHBoxLayout()
        coord_layout.addWidget(coord_label)
        coord_layout.addWidget(self.coord1_w)
        coord_layout.addWidget(self.coord2_w)
        coord_super_w.setLayout(coord_layout)

        self.axisw.activated.connect(self.set_coord_widgets)

        self.data_source = DataSourceW(self.parent)

        self.field_parameters = FieldParametersW()

        self.object_name = NameW(self.parent.active_data_object.name +
                                 ' axis aligned ray')

        self.generate_object_btn = QtGui.QPushButton('Generate Object')
        self.generate_object_btn.clicked.connect(self.generate_object)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(axis_super_w)
        layout.addWidget(self.coord_units_w)
        layout.addWidget(coord_super_w)
        layout.addWidget(self.field_parameters)
        layout.addWidget(self.data_source)
        layout.addWidget(self.object_name)
        layout.addWidget(self.generate_object_btn)
        self.setLayout(layout)

        self.parent_widget.layout.addWidget(self)
        self.parent_widget.show()

    def generate_object(self):
        axis = self.axis_dict[self.axisw.currentText()]

        units = self.coord_units_w.get_unit()
        coord1 = self.coord1_w.get_coordinate()
        coord2 = self.coord1_w.get_coordinate()

        source = self.parent.active_data_object.data

        name = self.object_name.get_name()

        if units is not None:
            coord = YTArray([coord1, coord2], units)
            coord = source.arr(coord).in_units('code_length')
        else:
            coord = [coord1, coord2]

        if self.field_parameters.get_field_parameters() == 'None':
            if self.data_source.get_data_source() is None:
                ray = source.ortho_ray(axis, coord)

            else:
                dsource = self.data_source.get_data_source()
                ray = source.ortho_ray(axis, coord, data_source=dsource)

            new_object = YtDataObject(ray, name)
            self.parent.add_data_object(new_object)

    def set_coord_widgets(self, index):
        if index is None:
            axis = self.axis_dict[self.axisw.currentText()]
        else:
            axis = index
        plane_axes = [key for key in list(self.axis_dict.keys())
                      if self.axis_dict[key] != axis]
        if hasattr(self, 'coord1_w') and hasattr(self, 'coord2_w'):
            self.coord1_w.set_label(plane_axes[0])
            self.coord2_w.set_label(plane_axes[1])
        else:
            self.coord1_w = CoordinateW(plane_axes[0])
            self.coord2_w = CoordinateW(plane_axes[1])


class OffAxisRayW(QtGui.QWidget):

    def __init__(self, parent, parent_widget):
        super(OffAxisRayW, self).__init__()

        self.parent = parent
        self.parent_widget = parent_widget

        self.coordinate_units_w = CoordinateUnitsW()

        start_coord_label = QtGui.QLabel("Ray Starting Coordinate:")

        self.start_coord_w = CartCoordinateComboW()

        start_coordc = QtGui.QWidget()
        start_coordc_layout = QtGui.QHBoxLayout()
        start_coordc_layout.addWidget(start_coord_label)
        start_coordc_layout.addWidget(self.start_coord_w)
        start_coordc.setLayout(start_coordc_layout)

        end_coord_label = QtGui.QLabel("Ray Ending Coordinate:")

        self.end_coord_w = CartCoordinateComboW()

        end_coordc = QtGui.QWidget()
        end_coordc_layout = QtGui.QHBoxLayout()
        end_coordc_layout.addWidget(end_coord_label)
        end_coordc_layout.addWidget(self.end_coord_w)
        end_coordc.setLayout(end_coordc_layout)

        self.field_parameters_w = FieldParametersW()

        self.data_source_w = DataSourceW(self.parent)

        self.object_name = NameW(self.parent.active_data_object.name +
                                 '_arbitrary_ray')

        self.generate_object_btn = QtGui.QPushButton('Generate Object')
        self.generate_object_btn.clicked.connect(self.generate_object)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.coordinate_units_w)
        layout.addWidget(start_coordc)
        layout.addWidget(end_coordc)
        layout.addWidget(self.field_parameters_w)
        layout.addWidget(self.data_source_w)
        layout.addWidget(self.object_name)
        layout.addWidget(self.generate_object_btn)
        self.setLayout(layout)

        self.parent_widget.layout.addWidget(self)
        self.parent_widget.show()

    def generate_object(self):
        source = self.parent.active_data_object.data

        unit = self.coordinate_units_w.get_unit()

        sp = self.start_coord_w.get_coordinates()
        ep = self.end_coord_w.get_coordinates()

        name = self.object_name.get_name()

        if unit is not None:
            sp = YTArray(sp, unit)
            ep = YTArray(ep, unit)
            sp = source.arr(sp).in_units('code_length')
            ep = source.arr(ep).in_units('code_length')

        fp = self.field_parameters_w.get_field_parameters()

        ds = self.data_source_w.get_data_source()

        if fp == 'None':
            if ds is None:
                ray = source.ray(sp, ep)
            else:
                ray = source.ray(sp, ep, data_source=ds)

        new_object = YtDataObject(ray, name)
        self.parent.add_data_object(new_object)


class AxisSliceW(QtGui.QWidget):
    axis_dict = {"x": 0, "y": 1, "z": 2}

    def __init__(self, parent, parent_widget):
        super(AxisSliceW, self).__init__()

        self.parent = parent
        self.parent_widget = parent_widget

        axis_label = QtGui.QLabel('Axis Along Which To Slice:')

        self.axisw = QtGui.QComboBox()
        self.axisw.addItems(list(self.axis_dict.keys()))
        self.axisw.activated.connect(self.set_new_center_coord)

        axiscw = QtGui.QWidget()
        axiscw_layout = QtGui.QHBoxLayout()
        axiscw_layout.addWidget(axis_label)
        axiscw_layout.addWidget(self.axisw)
        axiscw.setLayout(axiscw_layout)

        self.slice_point_unit_w = CoordinateUnitsW()
        self.slice_point_unit_w.label.setText('Units of Slice Point' +
                                              'Coordinate:')

        self.coordinate_w = CoordinateW('Point of Slice on Axis:')

        center_label = QtGui.QLabel("Center of Slice:")
        self.center_toggle_w = QtGui.QComboBox()
        self.center_toggle_w.addItems(['None', 'Custom'])
        self.center_toggle_w.currentIndexChanged.connect(self.add_coord_widget)

        center_t_w = QtGui.QWidget()
        center_t_w_layout = QtGui.QHBoxLayout()
        center_t_w_layout.addWidget(center_label)
        center_t_w_layout.addWidget(self.center_toggle_w)
        center_t_w.setLayout(center_t_w_layout)

        self.sec_unit_w = CoordinateUnitsW()
        self.sec_unit_w.label.setText('Units of Center Coordinates:')

        self.center_coord1_w = CoordinateW('y')
        self.center_coord2_w = CoordinateW('z')

        center_coord_combo_w = QtGui.QWidget()
        center_coord_combo_layout = QtGui.QHBoxLayout()
        center_coord_combo_layout.addWidget(self.center_coord1_w)
        center_coord_combo_layout.addWidget(self.center_coord2_w)
        center_coord_combo_w.setLayout(center_coord_combo_layout)

        self.center_coord_cw = QtGui.QWidget()
        center_coord_layout = QtGui.QVBoxLayout()
        center_coord_layout.addWidget(self.sec_unit_w)
        center_coord_layout.addWidget(center_coord_combo_w)
        self.center_coord_cw.setLayout(center_coord_layout)

        self.center_coord_cw.hide()

        self.field_parameters_w = FieldParametersW()

        self.data_source_w = DataSourceW(self.parent)

        self.name_w = NameW(self.parent.active_data_object.name +
                            self.axisw.currentText() + '_axis_slice')

        self.generate_object_btn = QtGui.QPushButton('Generate Object')

        self.generate_object_btn.clicked.connect(self.generate_object)

        layout = QtGui.QVBoxLayout()

        layout.addWidget(axiscw)
        layout.addWidget(self.slice_point_unit_w)
        layout.addWidget(self.coordinate_w)
        layout.addWidget(center_t_w)
        layout.addWidget(self.center_coord_cw)
        layout.addWidget(self.field_parameters_w)
        layout.addWidget(self.data_source_w)
        layout.addWidget(self.name_w)
        layout.addWidget(self.generate_object_btn)

        self.setLayout(layout)

        self.parent_widget.layout.addWidget(self)

        self.parent_widget.show()

    def add_coord_widget(self, index):
        if self.center_toggle_w.currentText() == 'Custom':
            self.center_coord_cw.show()
        else:
            self.center_coord_cw.hide()

    def set_new_center_coord(self, index):
        new_axes = [key for key in list(self.axis_dict.keys())
                    if key != self.axisw.itemText(index)]
        self.center_coord1_w.set_label(new_axes[0])
        self.center_coord2_w.set_label(new_axes[1])

    def generate_object(self):
        axis = self.axis_dict[self.axisw.currentText()]

        coord_unit = self.slice_point_unit_w.get_unit()
        coord = self.coordinate_w.get_coordinate()

        source = self.parent.active_data_object.get_data()

        name = self.name_w.get_name()

        field_params = self.field_parameters_w.get_field_parameters()

        dsource = self.data_source_w.get_data_source()

        if coord_unit is not None:
            coord = YTArray([coord], coord_unit)
            coord = source.arr(coord).in_units('code_length').item(0)

        if self.center_toggle_w.currentText() == 'Custom':
            c_coord = [self.center_coord1_w.get_coordinate(),
                       self.center_coord2_w.get_coordinate()]
            c_coord_unit = self.sec_unit_w.get_unit()
            if c_coord_unit is not None:
                c_coord = YTArray(c_coord, c_coord_unit)
        else:
            c_coord = None

        if field_params == 'None':
            new_slice = source.slice(axis, coord, center=c_coord,
                                     field_parameters=None,
                                     data_source=dsource)
        new_object = YtDataObject(new_slice, name)

        self.parent.add_data_object(new_object)


class SphereW(QtGui.QWidget):

    def __init__(self, parent, parent_widget):
        super(SphereW, self).__init__()
        self.parent = parent
        self.parent_widget = parent_widget

        self.center_units = CoordinateUnitsW()
        self.center_units.label.setText("Center Coordinate Units:")

        self.center = CartCoordinateComboW()
        self.center.coord1.set_label('Center X:')
        self.center.coord2.set_label('Center Y:')
        self.center.coord3.set_label('Center Z:')

        self.radius_units = CoordinateUnitsW()
        self.radius_units.label.setText("Radius Length Units:")
        self.radius = CoordinateW('Radius:')

        self.field_parameters = FieldParametersW()

        self.data_source = DataSourceW(self.parent)

        self.name = NameW(self.parent.active_data_object.name + "_sphere")

        self.generate_btn = QtGui.QPushButton('Generate Object')
        self.generate_btn.clicked.connect(self.generate_object)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.center_units)
        layout.addWidget(self.center)
        layout.addWidget(self.radius_units)
        layout.addWidget(self.radius)
        layout.addWidget(self.field_parameters)
        layout.addWidget(self.data_source)
        layout.addWidget(self.name)
        layout.addWidget(self.generate_btn)

        self.setLayout(layout)
        self.parent_widget.layout.addWidget(self)
        self.parent_widget.show()

    def generate_object(self):
        source = self.parent.active_data_object.data
        center = self.center.get_coordinates()
        center_units = self.center_units.get_unit()
        radius = self.radius.get_coordinate()
        radius_units = self.radius_units.get_unit()
        field_params = self.field_parameters.get_field_parameters()
        dsource = self.data_source.get_data_source()
        name = self.name.get_name()

        if center_units is not None:
            center = YTArray(center, center_units)
        if radius_units is not None:
            radius = YTArray(radius, radius_units)

        if field_params == 'None':
            sphere = source.sphere(center, radius, data_source=dsource)
            new_object = YtDataObject(sphere, name)
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


class OneDW(QtGui.QComboBox):

    def __init__(self, parent, parent_widget):
        super(OneDW, self).__init__()
        self.parent = parent
        self.parent_widget = parent_widget
        self.addItems(['Choose An Object', 'Axis Aligned Ray',
                       'Arbitrarily Aligned Ray'])
        self.activated.connect(self.show_ray_widget)
        self.parent_widget.layout.addWidget(self)
        self.parent_widget.show()

    def show_ray_widget(self):
        if self.currentText() == 'Axis Aligned Ray':
            AxisRayW(self.parent, self.parent_widget)

        elif self.currentText() == 'Arbitrarily Aligned Ray':
            OffAxisRayW(self.parent, self.parent_widget)


class TwoDW(QtGui.QComboBox):

    def __init__(self, parent, parent_widget):
        super(TwoDW, self).__init__()
        self.parent = parent
        self.parent_widget = parent_widget
        self.addItems(['Choose An Object', 'Axis Aligned Slice',
                       'Arbitrarily Aligned Slice'])
        self.activated.connect(self.show_slice_widget)

        self.parent_widget.layout.addWidget(self)
        self.parent_widget.show()

    def show_slice_widget(self):
        if self.currentText() == 'Axis Aligned Slice':
            AxisSliceW(self.parent, self.parent_widget)
        elif self.currentText() == 'Arbitrarily Aligned Slice':
            pass


class ThreeDW(QtGui.QComboBox):

    def __init__(self, parent, parent_widget):
        super(ThreeDW, self).__init__()
        self.parent = parent
        self.parent_widget = parent_widget
        self.addItems(['All Data', 'Box Region', 'Cylinder', 'Ellipsoid',
                       'Sphere'])
        self.activated.connect(self.show_shape_widget)

        self.parent_widget.layout.addWidget(self)
        self.parent_widget.show()

    def show_shape_widget(self):
        if self.currentText() == "Sphere":
            SphereW(self.parent, self.parent_widget)


class GeometricObjectW(QtGui.QComboBox):

    def __init__(self, parent, parent_widget):
        super(GeometricObjectW, self).__init__()
        self.parent = parent
        self.parent_widget = parent_widget

        self.addItems(['Choose Object Dimension', '0D', '1D', '2D', '3D'])
        self.activated.connect(self.show_dimension_widget)

        self.parent_widget.layout.addWidget(self)

        self.parent_widget.show()

    def show_dimension_widget(self, index):
        if self.currentText() == '0D':
            ZeroDW(self.parent, self.parent_widget)
        if self.currentText() == '1D':
            OneDW(self.parent, self.parent_widget)
        if self.currentText() == '2D':
            TwoDW(self.parent, self.parent_widget)
        if self.currentText() == '3D':
            ThreeDW(self.parent, self.parent_widget)


class DataObjectW(QtGui.QWidget):

    def __init__(self, parent):
        super(DataObjectW, self).__init__()
        self.parent = parent
        self.data_object_options = QtGui.QComboBox()
        self.data_object_options.addItems(['Choose An Object Type',
                                           'Geometric Object',
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
            GeometricObjectW(self.parent, self)


class ActiveObjectMenu(QtGui.QMenu):

    def __init__(self, aParent, plot_ref):
        super(ActiveObjectMenu, self).__init__()
        self.parent = aParent
        self.plot_ref = plot_ref
        self.addAction("New Data Object", self.get_data_objectw)
        self.addAction("New Plot", self.get_plotw)
        self.addAction("Remove", self.remove)

    def remove(self):
        item = self.parent.data_object_list_widget.currentItem()
        index = self.parent.data_object_list_widget.indexOfTopLevelItem(item)
        trash = self.parent.data_object_list_widget.takeTopLevelItem(index)
        del trash
        del index
        print item.text(0)
        self.parent.data_objects = [x for x in self.parent.data_objects if
                                    x.name != item.text(0)]
        if self.parent.active_data_object is not None:
            if self.parent.active_data_object.name == item.text(0):
                self.parent.active_data_object = None

    def get_plotw(self):
        def closeEvent(self, event):
            self.deleteLater()
        plot_dialog = PlotObjectW(self.parent, self.plot_ref)
        plot_dialog.closeEvent = types.MethodType(closeEvent,
                                                  plot_dialog,
                                                  QtGui.QCloseEvent)
        plot_dialog.show()

    def get_data_objectw(self):
        def closeEvent(self, event):
            self.deleteLater()

        data_objectw = DataObjectW(self.parent)
        data_objectw.setWindowTitle('Data Object Generator')
        data_objectw.closeEvent = types.MethodType(closeEvent, data_objectw,
                                                   QtGui.QCloseEvent)
        data_objectw.show()
