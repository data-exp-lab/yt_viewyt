import yt
from PyQt4 import QtCore
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
        A north vector defining what direction is up for off axis slices.
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

    def __init__(self, ds, sa="x", nv=None, d=0.5):
        r"""Initializes an frb view that defaults to slicing through the x
        axis at the center of the dataset."""
        self.ds = ds
        self.sa = sa
        self.nv = nv
        self.d = d

        if type(self.sa) == str:
            if self.sa == 'x':
                self.s = ds.r[0.5, :, :]
        self.frb = self.s.to_frb(1.0, 1024)
        field = self.frb["density"].ndarray_view()
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.imshow(field)
        self.plot = FigureCanvas(self.fig)
        self.plot.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.plot.setFocus()
        self.plot.mpl_connect('key_press_event', self.canvas_zoom)

    def get_plot(self):
        r"""return the view plot"""
        return self.plot

    def canvas_zoom(self, event):
        if event.button != 1:
            return
        print "signal fired"
        x, y = event.xdata, event.ydata
        self.ax.set_xlim(x - 0.1, x + 0.1)
        self.ax.set_ylim(y - 0.1, y + 0.1)
        self.fig.canvas.draw()
        self.plot = FigureCanvas(self.fig)
        self.plot.show()


