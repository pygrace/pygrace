from PyGrace.grace import Grace
from PyGrace.colors import ColorBrewerScheme
from PyGrace.axis import LINEAR_SCALE, LOGARITHMIC_SCALE
from PyGrace.drawing_objects import DrawText
from PyGrace.Styles.el import ElSquareGraph, ElCircleDataSet

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
grace = Grace(colors=colors)

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

# print out the grace
grace.write_file('06_logautoscale.agr')
