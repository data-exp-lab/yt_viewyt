r"""This module defines all of the widgets used to generate yt plots from
loaded data objects.
"""
import yt
from PyQt4 import QtGui
from acquisition_sub_widgets import CartAxisW, MasterFieldSelectionW, \
    WidthW, FieldParametersW, DataSourceW, FieldSelectorW
from viewtypes import PlotWindowView
yt.toggle_interactivity()


class PlotObjectW(QtGui.QWidget):
    r"""A widget for selecting which type of plot to generate and then
    displaying that plot generator.

    Parameters
    ----------
    parent : AcquisitionActiveW
        The widget that is ultimately responsible for creating the widget
        instance, and that also manages all data the widget may utilize.
    plot_ref : ViewWidget
        A reference to the application plot viewing area, that allows for plots
        to be displayed in the windowed area."""

    def __init__(self, parent, plot_ref):
        super(PlotObjectW, self).__init__()
        self.parent = parent
        self.plot_ref = plot_ref

        self.setWindowTitle('Plot Generator')

        label = QtGui.QLabel('Plot Type:')

        self.plt_optns = QtGui.QComboBox()
        self.plt_optns.addItems(['',
                                 'Axis Aligned Slice Plot',
                                 'Axis Aligned Projection Plot',
                                 'Phase Plot', 'Profile Plot'])
        self.plt_optns.currentIndexChanged.connect(self.show_plot_widget)

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
        r"""Shows the correct plot generation widget based on user input."""
        selection = self.plt_optns.currentText()

        if selection == 'Axis Aligned Slice Plot':
            AxisSlicePltW(self.parent, self, self.plot_ref)
        if selection == 'Axis Aligned Projection Plot':
            AxisProjectionPltW(self.parent, self, self.plot_ref)
        if selection == 'Phase Plot':
            PhasePltW(self.parent, self, self.plot_ref)
        if selection == 'Profile Plot':
            ProfilePltW(self.parent, self, self.plot_ref)


class AxisSlicePltW(QtGui.QWidget):
    r"""A widget that displays all of the options users can make to generate
    an on axis slice plot.

    Parameters
    ----------
    parent : AcquisitionActiveW
        The widget that is ultimately responsible for this widgets creation.
        This allows the plot widget to interact with loaded data.
    parent_widget : QtGui.QWidget
        The widget which displays this widget as one of its children.
    plot_ref : ViewWidget
        A reference to the application view area allowing for the plot to
        be displayed in said area."""

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

    def generate_plot(self):
        r"""Generates an on axis slice plot from the given parameters in the
        widget. """
        source = self.parent.active_data_object.data
        axis = self.plot_axis.get_axis()
        fields = self.plot_fields.get_fields()
        c = self.center_w.text()
        w = self.width.get_width()

        if c not in ['m', 'c', '', 'max', 'min']:
            self.center_w.setText("CHANGE IT.")
            c = None

        fs = self.font_size.value()

        field_params = self.field_parameters.get_field_parameters()

        dsource = self.data_source.get_data_source()

        if field_params == "None":
            plot = yt.SlicePlot(source, axis, fields, width=w,
                                fontsize=fs,
                                data_source=dsource)
            view = PlotWindowView(plot)
            self.plot_ref.addSubWindow(view)
            view.show()


class AxisProjectionPltW(QtGui.QWidget):
    r"""A widget for getting user input needed to generate an on axis projection
    plot.

    Parameters
    ----------
    parent : AcquisitionActiveW
        The widget that contains all references to data and enabled the
        creation of the plot.
    parent_widget : QtGui.QWidget
        The widget that will display this widget as one of its children.
    plot_ref : ViewWidget
        A reference to the area where plots are displayed so that the newly
        generated plot can be put there."""

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

        self.weight_field.top_selector.currentIndexChanged.connect(
            self.hide_selector2)

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
            view = PlotWindowView(plt)
            self.plot_ref.addSubWindow(view)
            view.show()


class PhasePltW(QtGui.QWidget):

    def __init__(self, parent, parent_widget, plot_ref):
        super(PhasePltW, self).__init__()

        self.parent = parent
        self.parent_widget = parent_widget
        self.plot_ref = plot_ref

        self.x_field = FieldSelectorW(self.parent.active_data_object,
                                      'X Binning Field for Profile:')
        self.y_field = FieldSelectorW(self.parent.active_data_object,
                                      'Y Binning Field for Profile:')
        self.z_field = MasterFieldSelectionW(self.parent.active_data_object)

        self.weight_field = FieldSelectorW(self.parent.active_data_object,
                                           'Field for Calculating Weighted' +
                                           'Averages:')
        self.weight_field.top_selector.addItem('Default')
        self.weight_field.top_selector.addItem('None')

        x_bin_label = QtGui.QLabel('Number of bins for X field:')
        self.x_bins = QtGui.QSpinBox()
        self.x_bins.setMaximum(1000)
        self.x_bins.setValue(128)
        x_bin_w = QtGui.QWidget()
        x_bin_layout = QtGui.QHBoxLayout()
        x_bin_layout.addWidget(x_bin_label)
        x_bin_layout.addWidget(self.x_bins)
        x_bin_w.setLayout(x_bin_layout)

        y_bin_label = QtGui.QLabel('Number of bins for Y field:')
        self.y_bins = QtGui.QSpinBox()
        self.x_bins.setMaximum(1000)
        self.y_bins.setValue(128)
        y_bin_w = QtGui.QWidget()
        y_bin_layout = QtGui.QHBoxLayout()
        y_bin_layout.addWidget(y_bin_label)
        y_bin_layout.addWidget(self.y_bins)
        y_bin_w.setLayout(y_bin_layout)

        accumulation_label = QtGui.QLabel('Accumulation:')
        self.accumulation = QtGui.QComboBox()
        self.accumulation.addItems(['False', 'True'])
        accumulation_w = QtGui.QWidget()
        accumulation_w_layout = QtGui.QHBoxLayout()
        accumulation_w_layout.addWidget(accumulation_label)
        accumulation_w_layout.addWidget(self.accumulation)
        accumulation_w.setLayout(accumulation_w_layout)

        fractional_label = QtGui.QLabel('Fractional:')
        self.fractional = QtGui.QComboBox()
        self.fractional.addItems(['False', 'True'])
        fractional_w = QtGui.QWidget()
        fractional_w_layout = QtGui.QHBoxLayout()
        fractional_w_layout.addWidget(fractional_label)
        fractional_w_layout.addWidget(self.fractional)
        fractional_w.setLayout(fractional_w_layout)

        fontsize_label = QtGui.QLabel('Font Size:')
        self.fontsize = QtGui.QSpinBox()
        self.fontsize.setValue(18)
        font_w = QtGui.QWidget()
        font_w_layout = QtGui.QHBoxLayout()
        font_w_layout.addWidget(fontsize_label)
        font_w_layout.addWidget(self.fontsize)
        font_w.setLayout(font_w_layout)

        self.generate_btn = QtGui.QPushButton("Generate Plot")
        self.generate_btn.clicked.connect(self.generate_plot)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.x_field)
        layout.addWidget(self.y_field)
        layout.addWidget(self.z_field)
        layout.addWidget(self.weight_field)
        layout.addWidget(x_bin_w)
        layout.addWidget(y_bin_w)
        layout.addWidget(accumulation_w)
        layout.addWidget(fractional_w)
        layout.addWidget(font_w)
        layout.addWidget(self.generate_btn)

        self.setLayout(layout)

        self.parent_widget.layout.addWidget(self)
        self.parent_widget.show()

    def generate_plot(self):
        source = self.parent.active_data_object.data
        x_field = self.x_field.get_field()
        y_field = self.y_field.get_field()
        z_field = self.z_field.get_fields()
        weight_field = self.weight_field.get_field()
        if weight_field[0] == 'None':
            weight_field = None
        elif weight_field[0] == 'Default':
            weight_field = 'cell_mass'
        x_bins = self.x_bins.value()
        y_bins = self.y_bins.value()
        accumulation = self.accumulation.currentText() == 'True'
        fractional = self.fractional.currentText() == 'True'
        fontsize = self.fontsize.value()

        plot = yt.PhasePlot(source, x_field, y_field, z_field,
                            weight_field=weight_field, x_bins=x_bins,
                            y_bins=y_bins, accumulation=accumulation,
                            fractional=fractional, fontsize=fontsize)
        view = PlotWindowView(plot)
        self.plot_ref.addSubWindow(view)
        view.show()


class ProfilePltW(QtGui.QWidget):

    def __init__(self, parent, parent_widget, plot_ref):
        super(ProfilePltW, self).__init__()

        self.parent = parent
        self.parent_widget = parent_widget
        self.plot_ref = plot_ref

        self.x_field = FieldSelectorW(self.parent.active_data_object,
                                      'Binning Field:')

        self.y_field = MasterFieldSelectionW(self.parent.active_data_object)

        self.weight_field = FieldSelectorW(self.parent.active_data_object,
                                           'Weighting Field:')
        self.weight_field.field_dict['None'] = []
        self.weight_field.field_dict['Default'] = []

        n_label = QtGui.QLabel("Number of bins in profile:")
        self.n_bins = QtGui.QSpinBox()
        self.n_bins.setValue(64)
        self.n_bins.setMaximum(1000)
        n_w = QtGui.QWidget()
        n_w_layout = QtGui.QHBoxLayout()
        n_w_layout.addWidget(n_label)
        n_w_layout.addWidget(self.n_bins)
        n_w.setLayout(n_w_layout)

        accum_label = QtGui.QLabel('Accumulation:')
        self.accum = QtGui.QComboBox()
        self.accum.addItems(['True', 'False'])

        accum_w = QtGui.QWidget()
        accum_w_layout = QtGui.QHBoxLayout()
        accum_w_layout.addWidget(accum_label)
        accum_w_layout.addWidget(self.accum)
        accum_w.setLayout(accum_w_layout)

        frac_label = QtGui.QLabel("Fractional:")
        self.frac = QtGui.QComboBox()
        self.frac.addItems(['True', 'False'])
        frac_w = QtGui.QWidget()
        frac_w_layout = QtGui.QHBoxLayout()
        frac_w_layout.addWidget(frac_label)
        frac_w_layout.addWidget(self.frac)
        frac_w.setLayout(frac_w_layout)

        x_log_label = QtGui.QLabel("Logarithmic X-Axis:")
        self.x_log = QtGui.QComboBox()
        self.x_log.addItems(['True', 'False'])
        x_log_w = QtGui.QWidget()
        x_log_layout = QtGui.QHBoxLayout()
        x_log_layout.addWidget(x_log_label)
        x_log_layout.addWidget(self.x_log)
        x_log_w.setLayout(x_log_layout)

        y_log_label = QtGui.QLabel("Logarithmic Y-Axis")
        self.y_log = QtGui.QComboBox()
        self.y_log.addItems(['True', 'False'])
        y_log_w = QtGui.QWidget()
        y_log_layout = QtGui.QHBoxLayout()
        y_log_layout.addWidget(y_log_label)
        y_log_layout.addWidget(self.y_log)
        y_log_w.setLayout(y_log_layout)

        self.generate_btn = QtGui.QPushButton("Generate Plot")
        self.generate_btn.clicked.connect(self.generate_plot)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.x_field)
        layout.addWidget(self.y_field)
        layout.addWidget(self.weight_field)
        layout.addWidget(n_w)
        layout.addWidget(accum_w)
        layout.addWidget(frac_w)
        layout.addWidget(x_log_w)
        layout.addWidget(y_log_w)
        layout.addWidget(self.generate_btn)
        self.setLayout(layout)

        self.parent_widget.layout.addWidget(self)
        self.parent_widget.show()

    def generate_plot(self):
        s = self.parent.active_data_object.data
        xf = self.x_field.get_field
        yf = self.y_field.get_fields()
        wf = self.weight_field.get_field()
        if wf == 'Default':
            wf = 'cell_mass'
        if wf == 'None':
            wf = None
        nb = self.n_bins.value()
        accum = self.accum.currentText() == 'True'
        frac = self.frac.currentText() == 'True'
        xl = self.x_log.currentText() == 'True'
        yl = self.y_log.currentText() == 'True'

        plt = yt.ProfilePlot(s, xf, yf, weight_field=wf, n_bins=nb,
                             accumulation=accum, fractional=frac, x_log=xl,
                             y_log=yl)
        view = PlotWindowView(plt)
        self.plot_ref.addSubWindow(view)
        view.show()
