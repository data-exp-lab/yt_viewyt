import yt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class YtPlot(object):

    def __init__(self, data_source):
        super(YtPlot, self).__init__()
        self.source = data_source
        self.frb = self.source.r[:, :, 0.5].to_frb(1, 1024)
        self.fieldVal = self.frb["density"].ndarray_view()
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.imshow(self.fieldVal)
        self.plot = FigureCanvas(fig)



    def get_plot(self):
        return self.plot


