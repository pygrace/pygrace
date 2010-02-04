import sys
sys.path.append('../../')
sys.path.append('../')

from PyGrace.grace import Grace
from PyGrace.graph import Graph
from PyGrace.dataset import DataSet
from PyGrace.Extensions.network import Network

# Define a couple of node sets, a xysize set and a regular xy set
# The sizes will be the radii of the nodes in world coordinates.
nodeset1_xysize = {
    'a1' : (0.1, 0.1, 0.03),
    'a2' : (0.8, 0.1, 0.02),
    'a3' : (0.1, 0.8, 0.04),
    'a4' : (0.8, 0.8, 0.06),
    'a5' : (0.865, 0.865, 0.02),
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
grace = Grace()

# Create the network graph instance
network = grace.add_graph(Network)

# Up to here, the setup is the same as undirected networks

# ------------
# Add the node sets
 
# To use link options like avoiding going under nodes, or having
# arrowheads appear right where the target node starts, the nodes
# need to be CircleNodes, and those are added one by one.
for id, data in nodeset1_xysize.items():
    network.add_circle_node(id, data, color=3, outline_color=1)

for id, (x,y) in nodeset2_xy.items():
    # you don't need to define a size, but I'll make them big
    # to demonstrate curving of links to avoid node obstacles
    bigradius = .08
    data = (x,y, bigradius)
    network.add_circle_node(id, data, color=11, line_width=6, line_color=12)

# You don't have to define a size, CircleNode can attach a
# default size if your data is of type xy only.
for id, data in nodeset3_xy.items():
    network.add_circle_node(id, data, color=1)

# This still works, but cannot use mentioned options 
network.add_node_set(nodeset4_xy, size=2, color=13, line_width=6, line_color=12)
# -------

# ------------
# Add the link sets

# For directed link sets, layout options and their default values are:
# avoid_crossing_nodes = True  (curve around -if you can- other nodes.
#                               also, if target and source are close and
#                               big, so that almost all the link is under
#                               them, try to curve away to show yourself)
# put_arrows = True            (put arrows -Drawing objects-)
# arrow_position = 0.75        (where to put the arrow. 1.0 means at the 
#                               farthest visible point, 0.0 means at
#                               nearest visible point from the origin.)
# curvature = .6               (how much each link curves by default)  
dirlinkSet = network.add_directed_link_set(links1, size=0.5,
                                           color=2,
                                           curvature = .2,
                                           arrow_position = 1.0)
dirlinkSet.line.linestyle = 3  # dashed links

# these links include links between a4 and a5, these will automatically
# curve more to show themselves (part of avoid_crossing_nodes)
network.add_directed_link_set(links2, size=5, color=9)

# Can still add a single node and a single undirected link
network.add_node('alone', (.3, .4, 5), type='xycolor')
network.add_link(('alone', 'B'))

# or a directed one
network.add_directed_link(('d', 'e'), curvature= -1.5,
                          size=3, color = 6,
                          put_arrows = False)

network.add_directed_link(('k', 'l'), curvature=0,
                          size=3, color = 3,
                          arrow_position=0.5)


# ------

# Make sure the view and the world are squares
network.set_view(0,0,1,1)
network.set_world(0,0,1,1)

# Print out the grace
grace.write_file('13_directed_network.agr')

