import sys
import random

from random import normalvariate as nv

# add the root directory of the PyGrace package to the PYTHONPATH
from example_tools import PYGRACE_PATH
sys.path.append(PYGRACE_PATH)

from PyGrace.grace import Grace
from PyGrace.graph import Graph
from PyGrace.dataset import DataSet
from PyGrace.colors import ColorBrewerScheme
from PyGrace.Extensions.latex_string import LatexString
from PyGrace.drawing_objects import DrawText

from example_tools import output_name

class ScatterPoints(DataSet):
    def __init__(self, color, *args, **kwargs):
        DataSet.__init__(self, *args, **kwargs)

        # make symbols circles of uniform color (with no line)
        self.symbol.configure(shape=1, fill_color=color, color=color)
        self.line.configure(type=0, linestyle=0, color=color)

class CDFGraph(Graph):
    def __init__(self, data, *args, **kwargs):
        Graph.__init__(self, *args, **kwargs)
        self.dataset = self.add_dataset(data)
        self.dataset.line.configure(type=2, linestyle=2)
        self.autoscalex()
        self.yaxis.ticklabel.configure(format="decimal",prec=1)

def calculate_cdf(data, normalized=True):

    countDict = {}
    for item in data:
        try:
            countDict[item] += 1
        except KeyError:
            countDict[item]  = 1

    countX = countDict.items()
    countX.sort()

    unnormalized = []
    n_greater_or_equal = len(data)
    for (x, count) in countX:
        unnormalized.append( (x, n_greater_or_equal) )
        n_greater_or_equal -= count

    normalized_result = []
    for (x, n_greater_or_equal) in unnormalized:
        fraction_greater_or_equal = float(n_greater_or_equal) / len(data)
        normalized_result.append( (x, fraction_greater_or_equal) )

    if normalized:
        return normalized_result
    else:
        return unnormalized

# generate a bunch of data (xy scatter plots in this case)
nPoints = 10
data = [random.randint(1, 9) for i in range(nPoints)]
data.sort()
#print >> sys.stderr, data
cdf = calculate_cdf(data, normalized=True)

# make the plot
grace = Grace(colors=ColorBrewerScheme('Set1'))
graph = grace.add_graph(CDFGraph, cdf)
xLabel = LatexString(r'$\langle$ \xb\f{}\sj\N $\rangle$')
graph.set_labels(xLabel, 'CDF*')
#graph.format_for_print(6)
description = grace.add_drawing_object(DrawText)
description.text = r'* This is actually an \5estimate\f{} of the complementary cumulative distribution function'
description.char_size = 0.75
#print grace
# print the grace (.agr format) to a file
grace.write_file(output_name(__file__))
