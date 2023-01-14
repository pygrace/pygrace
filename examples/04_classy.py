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
from pygrace.styles.el import *

# the purpose of this example is to illustrate how to use different
# grace styles rather than manipulating the standard grace styles all
# the time

# instantiate a grace object
grace = Project()

# add a graph
graph = grace.add_graph(ElEmptySquareGraph)

# add some data sets
dx = 0.01
data = [(i*dx,i*dx*i*dx+1) for i in range(int(-1/dx),int(1/dx)+1)]
dataset = graph.add_dataset(data,ElShadedDataSet,7)
dataset.line.configure(color=1,linewidth=2.0,linestyle=1)

data = [(i*dx,2*i*dx*i*dx) for i in range(int(-1/dx),int(1/dx)+1)]
dataset = graph.add_dataset(data,ElShadedDataSet,0)
dataset.line.configure(color=1,linewidth=2.0,linestyle=1)

data = [(-0.5,1.75),(0.5,1.75)]
dataset = graph.add_dataset(data,ElCircleDataSet,7)
dataset.symbol.size = 3.0
dataset.symbol.linestyle = 0

data = [(-0.48,1.71),(0.48,1.71)]
dataset = graph.add_dataset(data,ElCircleDataSet,4)
dataset.symbol.size = 1.0
dataset.symbol.linestyle = 0

graph.autoscale()

# print the Project (.agr format) to a file
grace.saveall('04_classy.agr')
