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
from pygrace.graph import Graph
from pygrace.dataset import DataSet
from pygrace.extensions.network import Network

# Define a couple of node sets, a xysize set and a regular xy set
nodeset1_xysize = {
    'a1' : (0.1, 0.1, 3),
    'a2' : (0.8, 0.1, 2),
    'a3' : (0.1, 0.8, 4),
    'a4' : (0.8, 0.8, 6),
    }
nodeset2_xy = {
    'B' : (0.5, 0.5),
    'C' : (0.6, 0.2),
    }


# Define a couple of link sets
links1 = [
    ('B', 'a1'),
    ('a2', 'a4'),
    ]
links2 = [
    ('B', 'a2'),
    ('B', 'a3'),
    ('B', 'a4'),
    ]

# Create the grace instance
grace = Project()

# Create the network graph instance
network = grace.add_graph(Network)

# Add the node sets
network.add_node_set(nodeset1_xysize, type='xysize', color=3)
network.add_node_set(nodeset2_xy, size=6, color=13, line_width=6, line_color=12)

# Add the link sets
linkSet = network.add_link_set(links1, size=0.5, color=2)
linkSet.line.linestyle = 3  # dashed links
network.add_link_set(links2, size=5, color=9)

# Add a single node and a single link
network.add_node('alone', (.3, .4, 5), type='xycolor')
network.add_link(('alone', 'B'))

# Print out the grace
grace.saveall('11_network.agr')
