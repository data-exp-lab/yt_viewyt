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

        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.setFocus()

        self.fig.canvas.mpl_connect('key_press_event', self.zoom)

    def zoom(self, event):

        if event.key == "i":
            a = self.ax.get_xlim()
            b = self.ax.get_ylim()
            self.ax.set_xlim(0.25 * a[0], 0.25 * a[1])
            self.ax.set_ylim(0.25 * b[0], 0.25 * b[1])
            self.draw()

        if event.key == 'o':
            a = self.ax.get_xlim()
            b = self.ax.get_ylim()
            self.ax.set_xlim(4 * a[0], 4 * a[1])
            self.ax.set_ylim(4 * b[0], 4 * b[1])
            self.draw()


class FrbView(MplCanvas):
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

        super(FrbView, self).__init__()
        self.fig.canvas.mpl_connect('key_press_event', self.pan)
        self.fig.canvas.mpl_connect('key_press_event', self.upgrade)

        if nv is not None:
            self.s = ds.cutting(nv, c)
        if type(sa) == str:
            if sa == 'x':
                self.s = ds.r[0.5, :, :]
            if sa == 'y':
                self.s = ds.r[:, 0.5, :]
            if sa == 'z':
                self.s = ds.r[:, 0.5, :]

        self.current_field = field
        self.frb = self.s.to_frb(1.0, 1024, periodic=True)
        field = self.frb[self.current_field].ndarray_view()
        self.ax.imshow(field)

    def get_plot(self):
        r"""return the view plot"""
        return self

    def pan(self, event):

        if event.key == "j":
            a = self.ax.get_ylim()
            dy = (a[1] - a[0]) / 2.0
            self.ax.set_ylim(a[0] - dy, a[1] - dy)
            self.draw()

        if event.key == "k":
            a = self.ax.get_ylim()
            dy = (a[1] - a[0]) / 2.0
            self.ax.set_ylim(a[0] + dy, a[1] + dy)
            self.draw()

        if event.key == "h":
            a = self.ax.get_xlim()
            dx = (a[1] - a[0]) / 2.0
            self.ax.set_xlim(a[0] - dx, a[1] - dx)
            self.draw()

        if event.key == "l":
            a = self.ax.get_xlim()
            dx = (a[1] - a[0]) / 2.0
            self.ax.set_xlim(a[0] + dx, a[1] + dx)
            self.draw()

    def upgrade(self, event):

        if event.key == "u":
            a = self.ax.get_ylim()
            b = self.ax.get_xlim()
            xmin = (1.0 / self.frb.convert_distance_x(1.0)) * a[0]
            xmax = (1.0 / self.frb.convert_distance_x(1.0)) * a[1]
            ymin = (1.0 / self.frb.convert_distance_y(1.0)) * b[0]
            ymax = (1.0 / self.frb.convert_distance_y(1.0)) * b[1]

            ds = self.s.ds

            axis = self.s.axis

            coord = self.s.coord

            if axis == 0:
                self.s = ds.r[coord, xmin:xmax, ymin:ymax]

            if axis == 1:
                self.s = ds.r[xmin:xmax, coord, ymin:ymax]

            if axis == 2:
                self.s = ds.r[xmin:xmax, ymin:ymax, coord]

            self.frb = self.s.to_frb(xmax - xmin, 1024, periodic=True)

            field = self.frb[self.current_field].ndarray_view()

            self.ax.cla()
            self.ax.imshow(field)
            self.ax.set_xlim(0, 1024)
            self.ax.set_ylim(0, 1024)

            self.show()
