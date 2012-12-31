from pygrace import PyGrace as Grace
from pygrace.graph import Graph
from pygrace.dataset import DataSet
from pygrace.colors import ColorBrewerScheme

class ScatterPoints(DataSet):
    def __init__(self, color, *args, **kwargs):
        DataSet.__init__(self, *args, **kwargs)

        # make symbols circles of uniform color (with no line)
        self.symbol.configure(shape=1, fill_color=color, color=color)
        self.line.configure(type=0, linestyle=0, color=color)

class ManyScatterGraph(Graph):
    def __init__(self, dataList, *args, **kwargs):
        Graph.__init__(self, *args, **kwargs)

        # make graph square
        self.view.xmax = self.view.xmin + (self.view.ymax - self.view.ymin)

        # add the datasets that are given
        for index, data in enumerate(dataList):
            self.dataset = self.add_dataset(data, ScatterPoints, index + 2)

        # autoscale the axes
        self.autoscale()

# ---------------------------------- this is the part where YOU do the analysis
# dataList is a list of lists, each one of (x, y) points
import example_tools
dataList = example_tools.simplesubclass()

# make the plot
grace = Grace(colors=ColorBrewerScheme('Set1'))
graph = grace.add_graph(ManyScatterGraph, dataList)
graph.set_labels('Snerdwump', 'Sneezle')
graph.format_for_print(6)

# print the grace (.agr format) to a file
grace.write_file('03_simplesubclass.agr')
