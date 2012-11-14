import sys
sys.path.append('../../')
sys.path.append('../')

from PyGrace.colors import RandomColorScheme, MarkovChainColorScheme
from PyGrace.dataset import SYMBOLS
from PyGrace.Extensions.panel import Panel,MultiPanelGrace

# This example illustrates how to use all of the different types of
# data sets.

# all of the data set types
data_types = ['xy', 'xydx', 'xydy', 'xydxdy', 'xydydy', 
              'xydxdx', 'xydxdxdydy', 'bar', 'bardy', 'bardydy',
              'xyhilo', 'xyz', 'xysize', 'xycolor',
              'xyvmap', 'xyboxplot']
n_components = [2, 3, 3, 4, 4, 
                4, 6, 2, 3, 4, 
                5, 3, 3, 3, 
                4, 6]

from random import random, randint

# make an instance of the Grace class that uses RandomColorScheme
seed = randint(0,10000)
colors = RandomColorScheme(seed,len(data_types))
# colors = MarkovChainColorScheme(seed,len(data_types))
grace = MultiPanelGrace(colors=colors)

# specify the label scheme
grace.add_label_scheme("my_scheme",data_types)
grace.set_label_scheme("my_scheme")

# add a Graph as a "child" of the grace instance
for i in range(len(data_types)):
    graph = grace.add_graph(Panel)

    # customize the panel label scheme
    graph.panel_label.configure(dx=0.02,dy=0.02,placement="iul")

    # add a simple DataSet as a "child" of the graph instance.  A list
    # of data is always the required first argument to add_dataset.
    data = []
    for n in range(3):
        datum = [random() for j in range(n_components[i])]
        data.append(tuple(datum))
    dataset = graph.add_dataset(data,type=data_types[i])

    # customize dataset
    dataset.line.configure(type=0)
    dataset.symbol.configure(shape=SYMBOLS["Triangle up"],
                             fill_color=i+2)

# automatically space multi graph and automatically format figures.
# width_to_height_ratio specifies the frame dimensions, hgap and vgap
# specify the horizontal and vertical gap between frames, hoffset
# specifies the offset from the left and right side, and voffset
# specifies the offset from the top and bottom.  
grace.automulti(width_to_height_ratio=1.0,hgap=0.02,vgap=0.02,
                hoffset=(0.03,0.03),voffset=(0.03,0.03))
grace.autoformat()

# hide all ticklabels and ticks
for graph in grace.graphs:
    graph.xaxis.tick.onoff = 'off'
    graph.xaxis.ticklabel.onoff = 'off'
    graph.yaxis.tick.onoff = 'off'
    graph.yaxis.ticklabel.onoff = 'off'

# print the grace (.agr format) to a file
grace.write_file('09_datasets.agr')
