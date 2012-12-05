from PyGrace.Extensions.panel import Panel, MultiPanelGrace
from PyGrace.Styles.el import ElCircleDataSet
from PyGrace.Styles.journals import NaturePanelLabel

import example_tools
dataList = example_tools.panels()

# This example illustrates some features that exist for multigraphs,
# including methods which hide redundant labels on axes.  This also
# illustrates the use of panels which automatically come with a panel
# label.

# make an instance of the Grace class
grace = MultiPanelGrace()

# add a Graph as a "child" of the grace instance
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

# Grace.autoscale_same can be used to autoscale all graphs to have the
# same bounds.  Convenient, eh?
grace.autoscale_same()

# hide all of the interior labels to make this look v. nice
grace.hide_redundant_labels()

# add axis labels to matrix of figures
grace.set_row_xaxislabel(2,"x")
grace.set_col_yaxislabel(0,"y")

# Whoa there partner, those are some rather large ticks and labels you
# have there.  You can scale them down to look more appropriate with
# the GraceObject.scale_suffix method
grace.scale_suffix(0.5,"major_size")
grace.scale_suffix(0.5,"minor_size")
grace.scale_suffix(0.5,"char_size")

# print the grace (.agr format) to a file
grace.write_file('07_panels.agr')
