from PyQt4 import QtGui, QtCore
from matplotlib.backends.backend_qt4agg \
    import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class YtView(object):
    r"""The base type of visual for viewYt.

    This is class is the super class of every type of view displayed in the
    application.

    Parameters
    ----------
    source : yt.data_objects.api.Dataset
        The dataset from which all information will be gathered."""

    def __init__(self, data_source):
        super(YtView, self).__init__()
        self.source = data_source
        self.frb = self.source.r[:, :, 0.5].to_frb(1, 1)

    def get_plot(self):
        return self.plot


class MplCanvas(FigureCanvas):

    def __init__(self):
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111, xlim=(0, 1024), ylim=(0, 1024))

        FigureCanvas.__init__(self, self.fig)
        FigureCanvas.setSizePolicy(self, QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        self.fig.canvas.mpl_connect('button_press_event', self.zoom)
        self.fig.canvas.mpl_connect('key_press_event', self.on_press)

    def zoom(self, event):
        if event.button != 1:
            return
        x, y = event.xdata, event.ydata
        self.ax.set_xlim(x - 128, x + 128)
        self.ax.set_ylim(y - 128, y + 128)
        self.draw()

    def on_press(self, event):
        print event.key


class FrbView(object):
    r""""The view displaying data as an FRB.

    This is the first view to be loaded when a data object is called to view,
    due to its speed and effective ability to navigate slices of data.
    It defaults to loading on axis slices of data, but off axis slices can
    be created. Note that off axis slices can be very expensive to create.

    Parameters
    ----------
    sa : array_like, string
        Slice axis; the Cartesian vector orthogonal to the slice plane.
    nv : array_like, optional
        A normal vector defining what plane is being sliced for off axis
        slices.
    d : float
        A depth marking how far along `sa` the slice is being taken. Assumed to
        be in code units. For on axis slices, this is the distance from the
        left edge of the `sa`.
    s
        The data slice
    frb
        The frb
    field : string, string tuple
        The field being displayed by the current frb.

    plot : mplObject"""

    def __init__(self, ds, sa="x", nv=None, d=0.5, c=[0, 0, 0],
                 field="density"):
        r"""Initializes an frb view that defaults to slicing through the x
        axis at the center of the dataset."""

        if nv is not None:
            self.s = ds.cutting(nv, c)
        if type(sa) == str:
            if sa == 'x':
                self.s = ds.r[0.5, :, :]
            if sa == 'y':
                self.s = ds.r[:, 0.5, :]
            if sa == 'z':
                self.s = ds.r[:, 0.5, :]

        self.frb = self.s.to_frb(1.0, 1024)
        field = self.frb[field].ndarray_view()
        self.plot = MplCanvas()
        self.plot.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.plot.setFocus()
        self.plot.ax.imshow(field)

    def get_plot(self):
        r"""return the view plot"""
        return self.plot
