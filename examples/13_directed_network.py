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
# The sizes will be the radii of the nodes in world coordinates.
nodeset1_xysize = {
    'a1' : (0.1, 0.1, 3),
    'a2' : (0.8, 0.1, 2),
    'a3' : (0.1, 0.8, 4),
    'a4' : (0.8, 0.8, 6),
    'a5' : (0.865, 0.865, 2),
    }
nodeset2_xy = {
    'B' : (0.5, 0.5),
    'C' : (0.6, 0.2),
    }

nodeset3_xy = {
    'k' : (0.43, 0.8),
    'l' : (0.57, 0.9),
    }

nodeset4_xy = {
    'd' : (0.1, 0.35),
    'e' : (0.1, 0.55),
    }


# Define a couple of link sets
links1 = [
    ('B', 'a1'),
    ('a2', 'a4'),
    ('a4', 'a2'),
    ]
links2 = [
    ('B', 'a2'),
    ('B', 'a3'),
    ('a4', 'B'),
    ('a5', 'a4'),
    ('a4', 'a5'),
   ]

# Create the grace instance
grace = Project()

# Create the network graph instance
network = grace.add_graph(Network)

# Make sure the view and the world are squares
# This is *essential* since the link drawing code relies 
# upon the world and view being defined BEFORE their instantiation.
#         (You want to work with squares in any case, because
#          otherwise coordinates shift, distances are misperceived)
network.set_view(0,0,1,1)
network.set_world(0,0,1,1)


# ----------------------------
# Add the node sets
# ----

# nodeset 1 ----------
network.add_node_set(nodeset1_xysize, type = 'xysize',
                     color=3, line_width=1, line_color=1)


# nodeset 2 ----------
for id, (x,y) in list(nodeset2_xy.items()):
    # you don't need to define a size, but I'll make them big
    # to demonstrate curving of links to avoid node obstacles
    # This also demonstrates add_node (it adds a single node)
    bigradius = 8
    data = (x,y, bigradius)
    network.add_node(id, data, type='xysize', color=11,
                     line_width=6, line_color=11)


# nodeset 3 ----------
# You don't have to define a size, nodes will have a
# default size if your data is of type xy only.
for id, data in list(nodeset3_xy.items()):
    network.add_node(id, data)
# Note that you don't need the for loop, this also works:
# network.add_node_set(nodeset3_xy)


# nodeset 4 ----------
# If you're adding a nodeset of type xy, you don't have to
# specifically indicate that 
network.add_node_set(nodeset4_xy, size=2, color=13, line_width=6, line_color=12)

# ---------------------------------

# ----------------------------------
# Add the link sets
# ------

# For directed link sets, layout options and their default values are:
# avoid_crossing_nodes = True  (curve around -if you can- other nodes.
#                               also, if target and source are close and
#                               big, so that almost all the link is under
#                               them, try to curve away to show yourself)
# put_arrows = True            (put arrowheads -drawing objects-)
# arrow_position = 0.75        (where to put the arrow. 1.0 means at the 
#                               farthest visible point, 0.0 means at
#                               nearest visible point from the origin.)
# curvature = .6               (how much each link curves by default. 
#                               positive curvature is to the right.)  

# links 1 ---------------
dirlinkSet = network.add_directed_link_set(links1, size=0.5,
                                           color=2,
                                           curvature = .2,
                                           arrow_position = 1.0)
dirlinkSet.line.linestyle = 3  # dashed links

# links 2 ----------------
# these links include links between a4 and a5, these will automatically
# curve more to show themselves (part of avoid_crossing_nodes)
network.add_directed_link_set(links2, size=5, color=9)

# single undirected ------
# You can still add a single node and a single undirected link ...
network.add_node('alone', (.3, .4, 5), type='xycolor')
network.add_link(('alone', 'B'))

# single directed --------
# ... or a directed one
network.add_directed_link(('d', 'e'), curvature= -1.5,
                          size=3, color = 6,
                          put_arrows = False)

network.add_directed_link(('k', 'l'), curvature=0,
                          size=3, color = 3,
                          arrow_position=0.5)

# ------------------------------------

# Print out the grace
grace.saveall('13_directed_network.agr')

