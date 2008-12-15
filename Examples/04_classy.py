
# the purpose of this example is to illustrate how to use different
# grace styles rather than manipulating the standard grace styles all
# the time

import sys
import user
from __init__ import output_name
sys.path.append(user.pygracePackagePath)
from PyGrace.grace import Grace
from PyGrace.Styles.el import *

# instantiate a grace object
grace = Grace()

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

# print the grace (.agr format) to a file
outStream = open(output_name(__file__), 'w')
print >> outStream, grace
outStream.close()
