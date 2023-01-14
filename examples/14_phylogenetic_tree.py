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
from pygrace.extensions.tree import Tree

# data is a string of a newick tree
import example_tools
data = example_tools.tree()

# make an instance of the grace Project class
grace = Project(colors=ColorBrewerScheme('Set1'))

# add a Tree graph as a "child" of the Project instance
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

# print out the Project
grace.saveall('14_phylogenetic_tree.agr')

