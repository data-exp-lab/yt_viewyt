import numpy as np
from PyQt4 import QtGui, QtCore
from matplotlib.backends.backend_qt4agg \
    import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class MplCanvas(FigureCanvas):

    def __init__(self):
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111, xlim=(0, 1024), ylim=(0, 1024))

        FigureCanvas.__init__(self, self.fig)

        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.setFocus()


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
        field = np.log10(self.frb[self.current_field].ndarray_view())
        self.ax.imshow(field)
        self.show()

    def get_plot(self):
        r"""return the view plot"""
        return self

    def pan_down(self, event):
        a = self.ax.get_ylim()
        dy = (a[1] - a[0]) / 2.0
        self.ax.set_ylim(a[0] - dy, a[1] - dy)
        self.draw()

    def pan_up(self, event):
        a = self.ax.get_ylim()
        dy = (a[1] - a[0]) / 2.0
        self.ax.set_ylim(a[0] + dy, a[1] + dy)
        self.draw()

    def pan_left(self, event):
        a = self.ax.get_xlim()
        dx = (a[1] - a[0]) / 2.0
        self.ax.set_xlim(a[0] - dx, a[1] - dx)
        self.draw()

    def pan_right(self, event):
        a = self.ax.get_xlim()
        dx = (a[1] - a[0]) / 2.0
        self.ax.set_xlim(a[0] + dx, a[1] + dx)
        self.draw()

    def zoom_in(self, event):
        a = self.ax.get_xlim()
        b = self.ax.get_ylim()
        center_x = (a[0] + a[1])/2.0
        width_x = (a[1] - a[0])
        center_y = (b[0] + b[1])/2.0
        width_y = (b[1] - b[0])
        self.ax.set_xlim(center_x - width_x/4.0, center_x + width_x/4.0)
        self.ax.set_ylim(center_y - width_y/4.0, center_y + width_y/4.0)
        self.draw()

    def zoom_out(self, event):
        a = self.ax.get_xlim()
        b = self.ax.get_ylim()
        center_x = (a[0] + a[1])/2.0
        width_x = (a[1] - a[0])
        center_y = (b[0] + b[1])/2.0
        width_y = (b[1] - b[0])
        self.ax.set_xlim(center_x - width_x*2.0, center_x + width_x*2.0)
        self.ax.set_ylim(center_y - width_y*2.0, center_y + width_y*2.0)
        self.draw()

    def upgrade(self, event):

        if event.key == "u":
            a = self.ax.get_xlim()
            b = self.ax.get_ylim()
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

            self.frb = self.s.to_frb(1.0, 1024, periodic=True)

            field = self.frb[self.current_field].ndarray_view()

            self.ax.clear()
            self.ax.imshow(field)
            self.ax.set_xlim(0, 1024)
            self.ax.set_ylim(0, 1024)

            self.draw()
