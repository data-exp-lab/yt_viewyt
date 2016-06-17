import yt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas

class YtPlot(object):

    def __init__(self, data_source):
        super(YtPlot, self).__init__()
        self.source = data_source
        self.plot = yt.ProjectionPlot(data_source, "x", 'density', center = [0.5, 0.5, 0.5])
        self.plot = self.plot.plots[('gas', 'density')]
        self.plot = FigureCanvas(self.plot.figure)

    def get_plot(self):
        return self.plot


