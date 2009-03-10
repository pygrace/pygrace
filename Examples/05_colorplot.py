
# This example demonstrates how to use a color plot.
#
# One important feature of color plots is that drawing objects in
# XMGrace are plotted above the frame of a graph.  As a result, we use
# the Grace.clone_graph method to copy the frame of the graph and make
# things look pretty.
#
# Another important feature of color plots is that specifying a
# particular world coordinate can automatically place drawing objects
# outside of the domain of the graph.
# Graph.remove_extraworld_drawing_objects fixes this problem by
# removing all of the drawing objects that appear in the world
# coordinates and are out of bounds.
#
# It also demonstrates how to use a PyGrace.Style to format figures in
# a customized format

import sys
import random

from PyGrace.grace import Grace
from PyGrace.Extensions.colorbar import ColorBar
from PyGrace.colors import ColorBrewerScheme
from PyGrace.axis import LINEAR_SCALE, LOGARITHMIC_SCALE
from PyGrace.drawing_objects import DrawBox

from PyGrace.Styles.el import ElGraph, ElLogTick, ElLogTickLabel, ElAxisLabel

from random import normalvariate
from math import floor,ceil

#------------------------------------------------------------------------------
# make data to plot
#------------------------------------------------------------------------------
# generate some synthetic data from eliptical Gaussian
data = []
for i in range(10000):
    x = normalvariate(0,1.0)
    y = normalvariate(-x,1.0)
    data.append((x,y))

# quick and dirty class for creating a pdf
class Bin2D:
    def __init__(self,lwrbnd,uprbnd,pdf=0.0):
        self.lwrbnd = lwrbnd
        self.uprbnd = uprbnd
        self.pdf = pdf

# create quick and dirty histogram
delta = 0.2
f = lambda zs: floor(min(zs)/delta)*delta
g = lambda zs: ceil(max(zs)/delta)*delta
xmin,ymin = map(f,zip(*data))
xmax,ymax = map(g,zip(*data))
bins = []
for i in range(int(xmin/delta),int(xmax/delta)):
    for j in range(int(ymin/delta),int(ymax/delta)):
        lwrbnd = (i*delta,j*delta)
        uprbnd = ((i+1)*delta,(j+1)*delta)
        bins.append(Bin2D(lwrbnd,uprbnd))
M = int(xmax/delta) - int(xmin/delta)
N = int(ymax/delta) - int(ymin/delta)
for datum in data:
    i = int(floor((datum[0]-xmin)/delta))
    j = int(floor((datum[1]-ymin)/delta))
    bin = bins[N*i + j]
    if not (bin.lwrbnd[0]<=datum[0] and datum[0]<bin.uprbnd[0] and
            bin.lwrbnd[1]<=datum[1] and datum[1]<bin.uprbnd[1]):
        s = "bin not correctly identified" + \
            str(bin.lwrbnd) + ' ' + str(bin.uprbnd) + ' ' + str(datum)
        raise TypeError, s
    bin.pdf += 1.0
minpdf,maxpdf = 1.0/float(len(data))/delta/delta, 0.0
for bin in bins:
    bin.pdf /= float(len(data))*(bin.uprbnd[0] - bin.lwrbnd[0])\
               *(bin.uprbnd[1] - bin.lwrbnd[1])
    if bin.pdf > maxpdf:
        maxpdf = bin.pdf

#------------------------------------------------------------------------------
# make a nice figure
#------------------------------------------------------------------------------
# instantiate a sweet figgy fig
colors = ColorBrewerScheme("YlOrBr",n=253) # this is the maximum number of colors
grace = Grace(colors=colors)

# add a colorbar
colorbar = grace.add_graph(ColorBar,domain=(minpdf,maxpdf),
                           scale=LOGARITHMIC_SCALE,autoscale=False)

# copy the format
## colorbar.copy_format(ElGraph)
colorbar.yaxis.tick.copy_format(ElLogTick)
colorbar.yaxis.ticklabel.copy_format(ElLogTickLabel)
colorbar.yaxis.ticklabel.place="opposite"
colorbar.yaxis.label.copy_format(ElAxisLabel)
colorbar.yaxis.label.place="opposite"

# to add some data to graph, just add the DrawBox to the 'world'
# coordinates.  this ensures that all of the autoscaling will work
# properly.
graph = grace.add_graph()
graph.copy_format(ElGraph)
for bin in bins:
    if bin.pdf > 0.0:
        color = colorbar.z2color(bin.pdf)
        graph.add_drawing_object(DrawBox,
                                 lowleft = tuple(bin.lwrbnd),
                                 upright = tuple(bin.uprbnd),
                                 loctype="world", 
                                 fill_color=color,
                                 color=color,
                                 linestyle=0,
                                 linewidth=0,
                                 )

# move things around
graph.set_view(0.2,0.2,0.9,0.9)
colorbar.set_view(0.95,0.2,1.0,0.9)

# label axes
colorbar.set_label("Probability density, p(x,y)")
graph.xaxis.label.text = "Mike is better than Dean"
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

# clone the graph and colorbar to place the frames above the drawing
# objects that are associated with each graph
clone_graph = grace.clone_graph(graph)
clone_colorbar = grace.clone_graph(colorbar)

# print out the grace
grace.write_file("05_colorplot.agr")
