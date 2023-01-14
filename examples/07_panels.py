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
from pygrace.extensions.panel import Panel, MultiPanelProject
from pygrace.styles.el import ElCircleDataSet
from pygrace.styles.journals import NaturePanelLabel

import example_tools
dataList = example_tools.panels()

# This example illustrates some features that exist for multigraphs,
# including methods which hide redundant labels on axes.  This also
# illustrates the use of panels which automatically come with a panel
# label.

# make an instance of the Project class
grace = MultiPanelProject()

# add a Panel as a "child" of the Project instance
for data in dataList:
    graph = grace.add_graph(Panel)

    # configure placement of panel label
    graph.panel_label.copy_format(NaturePanelLabel)

    # configure placement of panel label
    graph.panel_label.configure(placement="our",dx=0.01,dy=0.01)

    # add a simple DataSet as a "child" of the graph instance.  A list
    # of data is always the required first argument to add_dataset.
    dataset = graph.add_dataset(data,ElCircleDataSet,1)

    # ticklabels
    graph.xaxis.ticklabel.configure(format="decimal",prec=1)
    graph.yaxis.ticklabel.configure(format="decimal",prec=1)

# automatically space multi graph and automatically format figures.
# width_to_height_ratio specifies the frame dimensions, hgap and vgap
# specify the horizontal and vertical gap between frames, hoffset
# specifies the offset from the left and right side, and voffset
# specifies the offset from the top and bottom.  
grace.automulti(width_to_height_ratio=1.0,hgap=0.05,vgap=0.05,
                hoffset=(0.1,0.05),voffset=(0.05,0.1))

# autoscale all graphs to have the same bounds.
grace.autoscale_same()

# hide all of the interior labels
grace.hide_redundant_labels()

# add axis labels to matrix of figures
grace.set_row_xaxislabel(2,"x")
grace.set_col_yaxislabel(0,"y")

# scale down the large ticks and labels
grace.scale_suffix(0.5,"major_size")
grace.scale_suffix(0.5,"minor_size")
grace.scale_suffix(0.5,"char_size")

# print the Project (.agr format) to a file
grace.saveall('07_panels.agr')
