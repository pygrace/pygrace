#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @uqfoundation)
# Author: Daniel Stouffer (daniel @stoufferlab.org)
# Copyright (c) 2013 Daniel Stouffer.
# Copyright (c) 2023 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/uqfoundation/pygrace/blob/master/LICENSE
#
# This example demonstrates how to use a color plot.
#
# One important feature of color plots is that drawing objects in
# xmgrace are plotted above the frame of a graph.  As a result, we use
# the grace.clone_graph method to copy the frame of the graph and make
# things look pretty.
#
# Another important feature of color plots is that specifying a
# particular world coordinate can automatically place drawing objects
# outside of the domain of the graph.
# graph.remove_extraworld_drawing_objects fixes this problem by
# removing all of the drawing objects that appear in the world
# coordinates and are out of bounds.
#
# It also demonstrates how to use a pygrace.style to format figures in
# a customized format

import random

from pygrace.project import Project
from pygrace.colors import ColorBrewerScheme
from pygrace.axis import LINEAR_SCALE, LOGARITHMIC_SCALE
from pygrace.drawing_objects import DrawBox

from pygrace.extensions.colorbar import SolidRectangle, ColorBar
from pygrace.styles.el import ElGraph, ElLogColorBar


#------------------------------------------------------------------------------
# make a nice figure
#------------------------------------------------------------------------------
# get the data
import example_tools
data = example_tools.colorplot()

# find bounds of pdf
x0s,y0s,x1s,y1s,pdfs = list(zip(*data))
maxpdf=max(pdfs)
minpdf = float("inf")
for pdf in pdfs:
    if pdf<minpdf and pdf>0.0:
        minpdf=pdf

# instantiate a figure
colors = ColorBrewerScheme("YlOrBr",n=253) # this is the max number of colors

# change the opacity percent of a colorscheme
# colors.change_opacity(20, exclude_black=False)

grace = Project(colors=colors)

# add a colorbar
colorbar = grace.add_graph(ElLogColorBar,domain=(minpdf,maxpdf),
                           scale=LOGARITHMIC_SCALE,autoscale=False)

# to add some data to graph, just add SolidRectangle datasets
graph = grace.add_graph()
graph.copy_format(ElGraph)
for (x0,y0,x1,y1,pdf) in data:
    if pdf > 0.0:
        color = colorbar.z2color(pdf)
        # you can change the opacity percentage of a single color, as well
        # color.change_opacity(60)
        graph.add_dataset([(x0,y0), (x1,y1)], SolidRectangle, color)

# move things around
graph.set_view(0.2,0.2,0.9,0.9)
colorbar.set_view(0.95,0.2,1.0,0.9)

# label axes
colorbar.set_label("Probability density, p(x,y)")
graph.xaxis.label.text = "Model"
graph.yaxis.label.text = "Truth"

# all of the autoscale features work, too
graph.autoscalex()
graph.autotickx()

# restrict y-axis scale to the same as the x-axis scale
xmin,ymin,xmax,ymax = graph.get_world()
graph.set_world(xmin,xmin,xmax,xmax)
graph.autoticky()

# get rid of points that are out of bounds
graph.remove_extraworld_drawing_objects()

# print out the Project
grace.saveall("05_colorplot.agr")
