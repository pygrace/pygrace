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

# data1 and data2 are both lists of (x, y) points.
import example_tools
data1, data2 = example_tools.singleplot()

grace = Project(colors=ColorBrewerScheme('Paired'))

graph = grace.add_graph()
graph.xaxis.label.text = 'Fake X'
graph.yaxis.label.text = 'Fake Y'

dataset1 = graph.add_dataset(data1, legend='Set 1')
dataset1.symbol.fill_color = 'Paired-0'

dataset2 = graph.add_dataset(data2, legend='Set 2')
dataset2.symbol.fill_color = 'Paired-1'

graph.set_world_to_limits()
graph.logxy()

grace.saveall('01_singleplot.agr')

