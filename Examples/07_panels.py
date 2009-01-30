
# This example illustrates some features that exist for multigraphs,
# including methods which hide redundant labels on axes.  This also
# illustrates the use of panels which automatically come with a panel
# label.

import sys
from random import random

from example_tools import output_name

# add the root directory of the PyGrace package to the PYTHONPATH
from example_tools import PYGRACE_PATH
sys.path.append(PYGRACE_PATH)

from PyGrace.grace import Grace
from PyGrace.Extensions.panel import Panel
from PyGrace.Styles.el import ElCircleDataSet

# make an instance of the Grace class
grace = Grace()

# add a Graph as a "child" of the grace instance
for i in range(9):
    graph = grace.add_graph(Panel)
    graph.panel_label.configure(placement="our",dx=0.01,dy=0.01)

    # add a simple DataSet as a "child" of the graph instance.  A list
    # of data is always the required first argument to add_dataset.
    data = [(random(),random()) for i in range(100)]
    dataset = graph.add_dataset(data,ElCircleDataSet,1)

    # label axes
    graph.xaxis.label.text = 'x'
    graph.yaxis.label.text = 'y'
    
    # ticklabels
    graph.xaxis.ticklabel.configure(format="decimal",prec=1)
    graph.yaxis.ticklabel.configure(format="decimal",prec=1)

# automatically space multi graph and automatically format figures
grace.automulti(width_to_height_ratio=1.0,hgap=0.05,vgap=0.05)
grace.autoformat()

# hide all of the interior labels to make this look v. nice
grace.hide_redundant_labels()

# print the grace (.agr format) to a file
grace.write_file(output_name(__file__))

