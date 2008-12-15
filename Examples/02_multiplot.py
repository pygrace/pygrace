import sys
import user
import random
from __init__ import output_name
sys.path.append(user.pygracePackagePath)
from PyGrace.grace import Grace
from PyGrace.colors import ColorBrewerScheme
from PyGrace.drawing_objects import DrawText

# generate a bunch of data to plot
m, b, sigma = 10, 60, 12
x = [float(i) / 200 for i in range(0, 2000)]
y0 = [m * x_i + b for x_i in x]
r = [random.normalvariate(0, sigma) for i in y0]
y1 = [y_i + r_i for y_i, r_i in zip(y0, r)]
r_cdf = [(x_i, 1 - float(i) / len(r)) for i, x_i in enumerate(sorted(r))]
moving_average, window, l = [], [], 100
for x_i, r_i in zip(x, r):
    window.append((x_i, r_i))
    if len(window) >= l:
        x_bar, r_bar = map(sum, zip(*window))
        moving_average.append( (x_bar / float(l), r_bar / float(l)) )
        window.pop(0)

# create a grace in landscape mode
grace = Grace(colors=ColorBrewerScheme('Set1'))

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
noisy = graph1.add_dataset(zip(x, y1))

# these commands "manually" set the formatting for the dataset
noisy.line.type = 0
noisy.symbol.linestyle = 0
noisy.symbol.fill_color = 'Set1-8'
noisy.symbol.size = 0.25

# create another dataset in graph 1
clean = graph1.add_dataset(zip(x, y0))
clean.symbol.shape = 0

# the configure command can be used to set many attributes at once
clean.line.configure(type=1, linewidth=4, color='Set1-0')

# create a dataset for graph 2
residuals = graph2.add_dataset(zip(x, r))

# this function will copy all of the formatting attributes for this the
# 'residuals' dataset from the 'noisy' dataset.  When an object has children,
# the command is recursive.
residuals.copy_format(noisy)

moving = graph2.add_dataset(moving_average)
moving.copy_format(clean)
moving.line.color = 'Set1-2'

cdf = graph3.add_dataset(r_cdf)
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

# print the grace (.agr format) to a file
outStream = open(output_name(__file__), 'w')
print >> outStream, grace
outStream.close()

