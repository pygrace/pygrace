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

# make an instance of the Project class
grace = Project()

# add a Graph as a "child" of the Project instance
graph = grace.add_graph()
graph.title.text = 'Hello, world!'

# add a simple DataSet as a "child" of the graph instance.  A list of data is
# always the required first argument to add_dataset.
data = [(0, 0), (0.5, 0.75), (1, 1)]
dataset = graph.add_dataset(data)

# print the Project to a file (.agr format)
grace.saveall('00_helloworld.agr')
