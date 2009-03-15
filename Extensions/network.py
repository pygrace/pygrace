from PyGrace.grace import Grace
from PyGrace.graph import Graph
from PyGrace.dataset import DataSet

class NodeSet(DataSet):
    """A dataset containing network nodes.

    Nodes in the same dataset can be treated as any dataset in Grace,
    which means that color, size, and so on can be changed
    simultaneously for all nodes in the set. In general, a NodeSet can
    take advantage of any of the properties of regular DataSets. For
    example, a type='xysize' NodeSet has nodes with different sizes,
    and a type='xycolor' dataset contains nodes with different colors.

    -data (see DataSet definition) needs to be a dictionary indexed by
    the nodes' labels, and whose values are the (x,y) coordinates of
    the nodes (or (x,y,size), (x,y,color), and so on if the type is
    'xysize', 'xycolor', and so on).
    """
    def __init__(self, size=1, color=1, line_width=1, line_color=1,
                 *args, **kwargs):
        DataSet.__init__(self, *args, **kwargs)
        for aNode in self.data:
            self.parent.node_xy[aNode] = self.data[aNode][0:2]
        try:
            self.data = self.data.values()
        except:
            raise TypeError, 'data for a NodeSet must be a dictionary'
        self.symbol.configure(size=size,
                              fill_color=color,
                              linewidth=line_width,
                              color=line_color)
        self.line.linestyle = 0

class LinkSet(DataSet):
    """A dataset containing network links.

    Link in the same dataset can be treated as any dataset in Grace,
    which means that color, width, and so on can be changed
    simultaneously for all links in the set. In general, a LinkSet can
    take advantage of any of the properties of regular DataSets.

    data for the creation of a link needs to be a list of node pairs.
    """
    def __init__(self, size=1, color=1,
                 *args, **kwargs):
        DataSet.__init__(self, *args, **kwargs)
        theData = []
        try:
            for n1, n2, in self.data:
                x1, y1 = self.parent.node_xy[n1]
                x2, y2 = self.parent.node_xy[n2]
                theData.append((x1, y1))
                theData.append((x2, y2))
            self.data = theData
        except KeyError:
            raise KeyError, 'nodes should be in the network before adding links'
        except:
            raise TypeError, 'data must be a list of node pairs'
        self.symbol.shape = 0
        self.line.configure(type=4,
                            linestyle=1,
                            linewidth=size,
                            color=color)

class Network(Graph):
    """A graph to display networks.
    """
    def __init__(self, bounding_box=False, *args, **kwargs):
        Graph.__init__(self, *args, **kwargs)

        self.node_xy = {}  # stores node coordinates
        self.xaxis.onoff='off'
        self.yaxis.onoff='off'
        if not bounding_box:
            self.frame.linestyle = 0
        self.view.configure(xmin = 0.01 * self.parent.max_canvas_width,
                            xmax = 0.99 * self.parent.max_canvas_width,
                            ymin = 0.01 * self.parent.max_canvas_height,
                            ymax = 0.99 * self.parent.max_canvas_height)

    def add_node_set(self, node_data,
                     size=1, color=1, line_width=1, line_color=1,
                     *args, **kwargs):
        """Add a bunch of nodes to the graph.

        Nodes will be added to the Network graph as a NodeSet.

        -node_data needs to be a dictionary indexed by the nodes'
        labels, and whose values are the (x,y) coordinates of the
        nodes (or (x,y,size), (x,y,color), and so on if the type is
        'xysize', 'xycolor', and so on).
        """
        return self.add_dataset(node_data,
                                NodeSet,
                                size=size, color=color,
                                line_width=line_width, line_color=line_color,
                                *args, **kwargs)

    def add_node(self, label, node_data,
                 size=1, color=1, line_width=1, line_color=1,
                 *args, **kwargs):
        """Add a single node to the graph.

        The node will be added to the Network graph as a NodeSet.

        -label contains the label of the node.

        -node_data needs to be the (x,y) coordinates of the node (or
        (x,y,size), (x,y,color), and so on if the type is 'xysize',
        'xycolor', and so on).
        """
        return self.add_dataset({label : node_data},
                                NodeSet,
                                size=size, color=color,
                                line_width=line_width, line_color=line_color,
                                *args, **kwargs)

    def add_link_set(self, node_pairs, size=1, color=1, *args, **kwargs):
        """Add a bunch of links to the graph.

        Links will be added to the Network graph as a LinkSet.

        -node_pairs needs to be a list of pairs of nodes (label1,
        label2), and the corresponding nodes need to exist in the
        network already.
        """
        linkSet = self.add_dataset(node_pairs,
                                   LinkSet,
                                   size=size, color=color,
                                   *args, **kwargs)
        self.move_dataset_to_back(linkSet)
        return linkSet

    def add_link(self, node_pair, size=1, color=1, *args, **kwargs):
        """Add a single link to the graph.

        The link will be added to the Network graph as a LinkSet.

        -node_pair needs to be a pair of nodes (label1, label2), and
        the corresponding nodes need to exist in the network already.
        """
        linkSet = self.add_dataset([node_pair],
                                   LinkSet,
                                   size=size, color=color,
                                   *args, **kwargs)
        self.move_dataset_to_back(linkSet)
        return linkSet
