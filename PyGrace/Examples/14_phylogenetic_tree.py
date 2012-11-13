import sys
sys.path.append('../../')
sys.path.append('../')

from PyGrace.grace import Grace
from PyGrace.colors import ColorBrewerScheme
from PyGrace.dataset import SYMBOLS, LINESTYLES
from PyGrace.Extensions.tree import Tree

# ---------------------------------- this is the part where YOU do the analysis
# data is a string of a newick tree
import example_tools
data = example_tools.tree()

# make an instance of the Grace class
grace = Grace(colors=ColorBrewerScheme('Set1'))

# add a Tree Graph as a "child" of the grace instance
graph = grace.add_graph(Tree,orientation='down')

# load the data
tree = graph.add_tree(data,)

# change the x-axis ticklabel's angle
# by default (since names tend to be long) the labels are rotated
# but in this example we just use letters so there is no need to rotate
graph.xaxis.ticklabel.configure(angle=0,)

# autoscale the axes
graph.autoscale()
#graph.autoformat()

# print out the grace
grace.write_file('14_phylogenetic_tree.agr')

