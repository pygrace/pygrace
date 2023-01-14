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
from pygrace.axis import LINEAR_SCALE, LOGARITHMIC_SCALE
from pygrace.drawing_objects import DrawText
from pygrace.styles.el import ElSquareGraph, ElCircleDataSet

import example_tools
data = example_tools.logautoscale()

# Demonstrate how the autoscaling works for logarithmic axes.  In
# particular demonstrate how to get ride of drawing objects that are
# outside of bounds of graph

#------------------------------------------------------------------------------
# make a nice figure
#------------------------------------------------------------------------------
# instantiate a sweet figgy fig
colors = ColorBrewerScheme("Set1")
grace = Project(colors=colors)

# to add some data to graph, just add the DrawBox to the 'world'
# coordinates.  this ensures that all of the autoscaling will work
# properly.
graph = grace.add_graph(ElSquareGraph)
dataset = graph.add_dataset(data,ElCircleDataSet,3)

# add some drawing objects to graph
graph.add_drawing_object(DrawText,loctype="world",
                         x=0.001,y=0.001,text="Now you see me",
                         color=2)
graph.add_drawing_object(DrawText,loctype="world",
                         x=0,y=0,text="Now you don't",
                         color=2)

# autoscale the axes.  autoscale behavior is such that on logarithmic
# axes it scales the axes to be great than zero
graph.logxy()
graph.autoscale()

# get rid of text that is off axis
graph.remove_extraworld_drawing_objects()

# label axes
graph.xaxis.label.text = "Negative X's are hidden"
graph.yaxis.label.text = "Negative Y's are hidden"

# print out the Project
grace.saveall('06_logautoscale.agr')
