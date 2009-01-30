import sys

from random import normalvariate as nv

# add the root directory of the PyGrace package to the PYTHONPATH
from example_tools import PYGRACE_PATH
sys.path.append(PYGRACE_PATH)

from PyGrace.grace import Grace
from PyGrace.graph import Graph
from PyGrace.dataset import DataSet
from PyGrace.colors import ColorBrewerScheme
from example_tools import output_name

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

# generate a bunch of data (xy scatter plots in this case)
nSets, nPoints = 9, 200
dataList = [[(nv(mx, 1), nv(my, 1)) for i in range(nPoints)] \
            for mx, my in [(nv(0,3), nv(0, 3)) for i in range(nSets)]]

# make the plot
grace = Grace(colors=ColorBrewerScheme('Set1'))
graph = grace.add_graph(ManyScatterGraph, dataList)
graph.set_labels('Snerdwump', 'Sneezle')
graph.format_for_print(6)

# print the grace (.agr format) to a file
grace.write_file(output_name(__file__))
