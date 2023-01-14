#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @uqfoundation)
# Author: Daniel Stouffer (daniel @stoufferlab.org)
# Copyright (c) 2013 Daniel Stouffer.
# Copyright (c) 2023 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/uqfoundation/pygrace/blob/master/LICENSE
#
from pygrace.project import Project
from pygrace.colors import ColorBrewerScheme
from pygrace.dataset import SYMBOLS, LINESTYLES

# data0, data1, and data2 are all lists of (x, y) points.
import example_tools
data0, data1, data2 = example_tools.dataset_features()

grace = Project(colors=ColorBrewerScheme('Set1'))

graph = grace.add_graph()
graph.xaxis.label.text = 'x'
graph.yaxis.label.text = 'y'

# add data sets
dataset0 = graph.add_dataset(data0)
dataset1 = graph.add_dataset(data1)
dataset2 = graph.add_dataset(data2)

# autoscale the axes
graph.autoscale()

# set symbol sizes
for dataset in graph.datasets:
    dataset.symbol.size = 0.75
    dataset.symbol.linewidth = 2.0

# these methods emulate some functions in xmgrace that automatically
# set the symbols, colors, and linestyles to be different for each
# dataset in a graph.
graph.set_different_colors()
graph.set_different_symbols()
graph.set_different_linestyles()
graph.set_different_linewidths()

# the Graph.set_different* methods also allow you to specify a 'skip'
# increment, like this
graph.set_different_symbols(skip=2)

# you can also specify each attribute using their name or index.  By
# default, set_different_colors expects a name and the other
# set_different* methods expect an index.  If you specify a
# non-default type, just use the 'attr' keyword argument to specify
# either 'index' or 'name'.
#
# Now, suppose that you just can not stand black circles.  Ewwwww...
graph.set_different_colors(exclude=("White","Black"))
graph.set_different_symbols(attr='name',exclude=("None","Circle"))

# this does exactly the same thing 
graph.set_different_colors(attr='index',exclude=(0,1))
graph.set_different_symbols(exclude=(SYMBOLS["None"],SYMBOLS["Circle"]))

# another neat feature of the Graph.set_different* methods is that you
# can specify the particular order of the attributes that you want.
# For example, suppose you want to order the attributes like this:
colorsList = ["Set1-2","Set1-1", "Set1-4"]
symbolsList = [SYMBOLS["X"],SYMBOLS["Diamond"],SYMBOLS["Triangle up"]]
linestylesList = [LINESTYLES["--"],LINESTYLES["-- -- "],
                  LINESTYLES[". - . - "]]
linewidthsList = [0.5*i+1.0 for i in range(3)]

# then you would do this:
graph.set_different_colors(colorsList=colorsList)
graph.set_different_symbols(symbolsList=symbolsList)
graph.set_different_linestyles(linestylesList=linestylesList)
graph.set_different_linewidths(linewidthsList=linewidthsList)

# You can also move datasets forward/backward or to the top or bottom
# like this:
graph.move_dataset_backward(dataset2)
graph.move_dataset_to_front(dataset0)

# now they are ordered [dataset2,dataset1,dataset0].  To move them
# back, you can specify the order of all data sets like this:
graph.set_dataset_order([dataset0,dataset1,dataset2])

# now if you want the data sets in the back to have thicker lines, you
# can do this:
linewidthsList = [3,2,1]
graph.set_different_linewidths(linewidthsList=linewidthsList)

#xxxx this clearly is not working yet

# print out the Project
grace.saveall('10_dataset_features.agr')

