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
from pygrace.drawing_objects import DrawText

# all datasets are lists of (x, y) points
import example_tools
data1, data2, data3, data4, data5 = example_tools.multiplot()

# make a Project instance with the "Set1" color scheme
grace = Project(colors=ColorBrewerScheme('Set1'))

# this function returns the maximum x and y "view" values to fit in the page
xView, yView = grace.set_landscape()

# create graphs and set locations on page
graph1 = grace.add_graph()
graph1.set_view(0.10 * xView, 0.55 * yView, 0.90 * xView, 0.90 * yView)

# to illustrate the use of drawing objects, and just to make things a little
# more complicated, here is a manually added label to graph 1.
title1 = graph1.add_drawing_object(DrawText, text='(a) Regression',
                                   x=0.10*xView, y=0.91*yView, just=4)

# this will set the axis labels. it is a good idea to use raw strings (r'')
# so that backslashes (which are used to give xmgrace text formatting commands)
# are not used as escape characters.
graph1.set_labels(r'\xt\4', r'\xg\4(\xt\4)')

graph2 = grace.add_graph()
graph2.set_view(0.10 * xView, 0.10 * yView, 0.45 * xView, 0.45 * yView)
graph2.set_labels(r'\xt\4', r'\xg\4\s1\N(\xt\4)-\xg\4\s0\N(\xt\4)')
title2 = graph2.add_drawing_object(DrawText, text='(b) Residuals',
                                   x=0.10*xView, y=0.46*yView, just=4)

graph3 = grace.add_graph()
graph3.set_view(0.55 * xView, 0.10 * yView, 0.90 * xView, 0.45 * yView)
graph3.set_labels(r'\xg\4\s1\N-\xg\4\s0\N', r'CDF(\xg\4\s1\N-\xg\4\s0\N)')
title3 = graph3.add_drawing_object(DrawText, text='(c) Distribution',
                                   x=0.55*xView, y=0.46*yView, just=4)


# create a dataset for graph 1
noisy = graph1.add_dataset(data1)

# these commands "manually" set the formatting for the dataset
noisy.line.type = 0
noisy.symbol.linestyle = 0
noisy.symbol.fill_color = 'Set1-8'
noisy.symbol.size = 0.25

# create another dataset in graph 1
clean = graph1.add_dataset(data2)
clean.symbol.shape = 0

# the configure command can be used to set many attributes at once
clean.line.configure(type=1, linewidth=4, color='Set1-0')

# create a dataset for graph 2
residuals = graph2.add_dataset(data3)

# this function will copy all of the formatting attributes for this the
# 'residuals' dataset from the 'noisy' dataset.  When an object has children,
# the command is recursive.
residuals.copy_format(noisy)

moving = graph2.add_dataset(data4)
moving.copy_format(clean)
moving.line.color = 'Set1-2'

cdf = graph3.add_dataset(data5)
cdf.copy_format(clean)
cdf.line.color = 'Set1-1'

# set all attributes that end with 'char_size' to 1.15 for the grace and all
# children (and childrens children, etc...)
grace.set_suffix(1.15, 'char_size', all=True)

# for all graphs, scale the size of the ticks by a factor of 0.6
for graph in grace.graphs:
    graph.xaxis.tick.scale_suffix(0.6, 'size', all=True)
    graph.yaxis.tick.scale_suffix(0.6, 'size', all=True)
    
# autoscales all graphs in the grace
grace.autoscale()

# sets everything to Helvetica except the titles, which are Bigger and Bolder
grace.set_fonts('Helvetica')
grace.configure_group(title1, title2, title3,
                      font='Helvetica-Bold', char_size=1.25)

# print the Project (.agr format) to a file
grace.saveall('02_multiplot.agr')

