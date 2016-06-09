import yt
from PyQt4 import QtGui
from PyQt4 import QtCore
import matplotlib
from matplotlib.backends import qt_compat
#from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
#method of displaying yt plots without saving to disk is taken from
#http://matplotlib.org/examples/user_interfaces/embedding_in_qt4.html

class YtPlot(object):

    def __init__(self, data_source):
        super(YtPlot, self).__init__()
        self.source = data_source
        self.plot = yt.SlicePlot(data_source, "x", 'density', center = [0.5, 0.5, 0.5])
        self.plot = self.plot.plots[('gas', 'density')]
        self.plot = self.plot._repr_widget_()
    def get_plot(self):
        return self.plot


#class ViewWindowW(FigureCanvas):
#
#    def __init__(self, plot_object):
#        self  = FigureCanvas.__init__(self, plot_object)
