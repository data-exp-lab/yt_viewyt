import yt
from PyQt4 import QtGui
from acquisition_sub_widgets import CartAxisW, MasterFieldSelectionW, \
    WidthW, FieldParametersW, DataSourceW, FieldSelectorW
yt.toggle_interactivity()


class PlotObjectW(QtGui.QWidget):

    def __init__(self, parent, plot_ref):
        super(PlotObjectW, self).__init__()
        self.parent = parent
        self.plot_ref = plot_ref

        self.setWindowTitle('Plot Generator')

        label = QtGui.QLabel('Plot Type:')

        self.plt_optns = QtGui.QComboBox()
        self.plt_optns.addItems(['',
                                 'Axis Aligned Slice Plot',
                                 'Axis Aligned Projection Plot'])
        self.plt_optns.activated.connect(self.show_plot_widget)

        plt_optns_combo = QtGui.QWidget()

        plt_optns_combo_layout = QtGui.QHBoxLayout()
        plt_optns_combo_layout.addWidget(label)
        plt_optns_combo_layout.addWidget(self.plt_optns)

        plt_optns_combo.setLayout(plt_optns_combo_layout)

        self.layout = QtGui.QVBoxLayout()
        self.layout.addWidget(plt_optns_combo)

        self.setLayout(self.layout)
        self.show()

    def show_plot_widget(self):
        selection = self.plt_optns.currentText()

        if selection == 'Axis Aligned Slice Plot':
            AxisSlicePltW(self.parent, self, self.plot_ref)
        if selection == 'Axis Aligned Projection Plot':
            AxisProjectionPltW(self.parent, self, self.plot_ref)


class AxisSlicePltW(QtGui.QWidget):

    def __init__(self, parent, parent_widget, plot_ref):
        super(AxisSlicePltW, self).__init__()

        self.plot_ref = plot_ref

        self.parent = parent

        self.parent_widget = parent_widget

        self.plot_axis = CartAxisW('Axis to Slice Along:')

        self.plot_fields = MasterFieldSelectionW(
            self.parent.active_data_object)

        center_label = QtGui.QLabel("Plot Center Parameter:")
        self.center_w = QtGui.QLineEdit()

        combo_center = QtGui.QWidget()
        combo_center_layout = QtGui.QHBoxLayout()
        combo_center_layout.addWidget(center_label)
        combo_center_layout.addWidget(self.center_w)
        combo_center.setLayout(combo_center_layout)

        self.width = WidthW()

        self.field_parameters = FieldParametersW()

        label = QtGui.QLabel('Font Size:')

        self.font_size = QtGui.QSpinBox()
        self.font_size.setMinimum(1)

        font_w = QtGui.QWidget()
        font_w_layout = QtGui.QHBoxLayout()
        font_w_layout.addWidget(label)
        font_w_layout.addWidget(self.font_size)
        font_w.setLayout(font_w_layout)

        self.data_source = DataSourceW(self.parent)

        self.generate_btn = QtGui.QPushButton("Generate Plot")
        self.generate_btn.clicked.connect(self.generate_plot)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.plot_axis)
        layout.addWidget(self.plot_fields)
        layout.addWidget(combo_center)
        layout.addWidget(self.width)
        layout.addWidget(font_w)
        layout.addWidget(self.field_parameters)
        layout.addWidget(self.data_source)
        layout.addWidget(self.generate_btn)
        layout.setSpacing(0)

        self.setLayout(layout)

        self.parent_widget.layout.addWidget(self)
        self.parent_widget.show()

    def generate_plot(self, boolean):
        source = self.parent.active_data_object.data
        axis = self.plot_axis.get_axis()
        fields = self.plot_fields.get_fields()
        c = self.center_w.text()
        w = self.width.get_width()

        if c not in ['m', 'c', '', 'max', 'min']:
            self.center_w.setText("CHANGE IT. THE DEVELOPER OCCUPIED")
            c = None

        fs = self.font_size.value()

        field_params = self.field_parameters.get_field_parameters()

        dsource = self.data_source.get_data_source()

        if field_params == "None":
            plot = yt.SlicePlot(source, axis, fields, width=w,
                                fontsize=fs,
                                data_source=dsource)
            plot.show()


class AxisProjectionPltW(QtGui.QWidget):

    def __init__(self, parent, parent_widget, plot_ref):
        super(AxisProjectionPltW, self).__init__()

        self.parent = parent

        self.parent_widget = parent_widget

        self.plot_ref = plot_ref

        self.axis = CartAxisW('Axis to Project Along:')

        self.fields = MasterFieldSelectionW(
            self.parent.active_data_object)

        self.width = WidthW()

        self.weight_field = FieldSelectorW(self.parent.active_data_object,
                                           'Weighting Field:')

        self.weight_field.top_selector.addItem("None")

        self.weight_field.field_dict['None'] = []

        self.weight_field.top_selector.currentIndexChanged.connect(self.hide_selector2)

        label = QtGui.QLabel('Font Size:')

        self.font_size = QtGui.QSpinBox()
        self.font_size.setMinimum(1)
        self.font_size.setValue(18)

        font_w = QtGui.QWidget()
        font_w_layout = QtGui.QHBoxLayout()
        font_w_layout.addWidget(label)
        font_w_layout.addWidget(self.font_size)
        font_w.setLayout(font_w_layout)

        weight_label = QtGui.QLabel("Weighting Method:")
        self.weight_method = QtGui.QComboBox()
        self.weight_method.addItems(['integrate', 'mip', 'sum'])
        weight_w = QtGui.QWidget()
        weight_layout = QtGui.QHBoxLayout()
        weight_layout.addWidget(weight_label)
        weight_layout.addWidget(self.weight_method)
        weight_w.setLayout(weight_layout)

        self.field_parameters = FieldParametersW()

        self.data_source = DataSourceW(self.parent)

        self.generate_btn = QtGui.QPushButton("Generate Plot")
        self.generate_btn.clicked.connect(self.generate_plot)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.axis)
        layout.addWidget(self.fields)
        layout.addWidget(self.width)
        layout.addWidget(self.weight_field)
        layout.addWidget(weight_w)
        layout.addWidget(self.field_parameters)
        layout.addWidget(self.data_source)
        layout.addWidget(font_w)
        layout.addWidget(self.generate_btn)
        layout.setSpacing(0)

        self.setLayout(layout)

        self.parent_widget.layout.addWidget(self)
        self.parent_widget.show()

    def hide_selector2(self, index):
        if self.weight_field.top_selector.currentText() == 'None':
            self.weight_field.selector2.setHidden(True)
        else:
            self.weight_field.selector2.setHidden(False)

    def generate_plot(self, boolean):
        source = self.parent.active_data_object.data
        axis = self.axis.get_axis()
        fields = self.fields.get_fields()
        w = self.width.get_width()
        weight_field = self.weight_field.get_field()
        if weight_field[0] == 'None':
            weight_field = None
        fs = self.font_size.value()
        field_params = self.field_parameters.get_field_parameters()
        ds = self.data_source.get_data_source()
        mthd = self.weight_method.currentText()

        if field_params == 'None':
            plt = yt.ProjectionPlot(source, axis, fields, width=w,
                                    weight_field=weight_field, fontsize=fs,
                                    data_source=ds, method=mthd)
            plt.save('ProjectionsDone.png')
