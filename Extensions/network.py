import sys

from PyGrace.grace import Grace
from PyGrace.graph import Graph
from PyGrace.dataset import DataSet
from PyGrace.drawing_objects import DrawLine, DrawText
from datastat import frange
from math import sqrt, sin, cos

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
    def __init__(self, size=1, color=1, line_width=1, line_color=1, shape=1,
                 labels=False, *args, **kwargs):
        if size > 10:
            print >> sys.stderr, 'WARNING: Node size > 10: ' + \
                  'will be set to 10'
        DataSet.__init__(self, *args, **kwargs)
        for aNode in self.data:
            self.parent.node_xy[aNode] = self.data[aNode][0:2]
            if self.type == 'xysize':
                if aNode not in self.parent.node_sz:
                    self.parent.node_sz[aNode] = self.data[aNode][2]                
            else:
                if aNode not in self.parent.node_sz:
                    self.parent.node_sz[aNode] = size
        try:
            if labels:
                self.data = [values + (label, )
                             for label, values  in self.data.iteritems()]
            else:
                self.data = [values for label,values in self.data.iteritems()]
        except:
            raise TypeError, 'data for a NodeSet must be a dictionary'
        self.symbol.configure(size=size,
                              fill_color=color,
                              linewidth=line_width,
                              color=line_color,
                              shape=shape)
        self.line.linestyle = 0
        if labels:
            self.avalue.onoff='on'


class SolidCircle(DataSet):
    """A dataset that shows up as a solid circle.

    data for the creating of the SolidCircle must be the
    center of the circle and a radius.
    """
    def __init__(self, color=1, outline_color = None, *args, **kwargs):
        DataSet.__init__(self, *args, **kwargs)
        if len(self.data) != 3 and len(self.data.values()[0]) != 3:
            raise TypeError, 'Data for SolidCircle MUST contain 3 items (x,y & radius)'
        if type(self.data) in (tuple, list):
            # data is (x,y,r)
            x0 = self.x0 = self.data[0]
            y0 = self.y0 = self.data[1]
            r  = self.r  = self.data[2]
        elif type(self.data) == dict:
            # data is {label: (x,y,r)}
            val = self.data.values()[0]
            x0 = self.x0 = val[0]
            y0 = self.y0 = val[1]
            r  = self.r  = val[2]
            self.labeleddata = {}
            for key,val in self.data.items():
                self.labeleddata[key] = val
        def circle(t):
            x = x0 + r*cos(t)
            y = y0 + r*sin(t)
            return x,y
        self.data = [circle(t) for t in frange(0, 6.3, .1)]
        self.symbol.configure(shape=0)
        if outline_color is None:
            self.line.configure(linewidth=0, color=color)
        else:
            self.line.configure(linewidth=2, color=outline_color)
        self.fill.configure(type=1, rule=0, color=color)



class CircleNode(SolidCircle):
    """ A special nodeset for one node, using a SolidCircle dataset to
    represent the node.

    The advantage of CircleNode over a normal nodeset is that the area
    occupied by the node is set in world coordinates. A symbol keeps
    its size and shape when zoomed in or when axis limits are
    changed. This is good in many cases, but it makes it very
    difficult to find out if something is in the area the node
    covers. CircleNode has the method in_circle, that finds out if
    that's the case. The disadvantage of using world coordinates is
    that if the x- and y- sides of the View are scaled differently
    (which is default behavior in grace), the circle turns into an
    ellipse. They have to be scaled in the same way, i.e. xmin=ymin,
    xmax=ymax for view coordinates. In other words, the View must be a
    square.  This is usually the case when working with coordinates
    anyway, to avoid disproportions in placements of items.
    """
    def __init__(self, color=2, outline_color=None, labels=False, *args, **kwargs):
        data = kwargs['data']
        for key in data.keys():
            if len(data[key]) == 2:
                xmin,ymin,xmax,ymax = kwargs['parent'].get_world()
                default_size = 0.03 * abs(xmax - xmin)
                x,y = data[key]
                data[key] = (x , y, default_size)
        SolidCircle.__init__(self, color=color, outline_color=outline_color,
                             *args, **kwargs)
        # self.data is changed at this moment. It is a list of points
        # defining the circle.
        for aNode in self.labeleddata:
            # to reach all the beautiful methods of CircleNode (in_circle),
            # we want to keep the whole node instance in the memory as well :)
            self.parent.nodes[aNode] = self
            # and now the regular xy and size stuff as well
            self.parent.node_xy[aNode] = (self.x0, self.y0)
            if aNode not in self.parent.node_sz:
                self.parent.node_sz[aNode] = self.r      
        if labels:
            self.avalue.onoff='on'
        
    def in_circle(self,x,y):
        x0 = self.x0
        y0 = self.y0
        r  = self.r
        if (x-x0)**2+(y-y0)**2 < r**2:
            return True
        return False




class LinkSet(DataSet):
    """A dataset containing network links.

    Link in the same dataset can be treated as any dataset in Grace,
    which means that color, width, and so on can be changed
    simultaneously for all links in the set. In general, a LinkSet can
    take advantage of any of the properties of regular DataSets.

    data for the creation of a link needs to be a list of node pairs.

    Nodes with the right labels need to have been added to the network
    before their links can be added. Otherwise, a ValueError is raised
    (unless the keyword ignore_missing is set to True, in which case
    the link is ignored and there is only a warning sent to stderr).
    """
    def __init__(self, size=1, color=1, ignore_missing=False, 
                 *args, **kwargs):
        DataSet.__init__(self, *args, **kwargs)
        theData = []
        try:
            for n1, n2, in self.data:
                try:
                    x1, y1 = self.parent.node_xy[n1]
                    x2, y2 = self.parent.node_xy[n2]
                    theData.append((x1, y1))
                    theData.append((x2, y2))
                except KeyError:
                    if ignore_missing:
                        print >> sys.stderr, 'WARNING: ignoring link %s-%s' % (
                            n1, n2
                            )
                    else:
                        raise KeyError, \
                              'nodes should be added to the network first'
            self.data = theData
        except:
            raise TypeError, 'data must be a list of node pairs'
        self.symbol.shape = 0
        self.line.configure(type=4,
                            linestyle=1,
                            linewidth=size,
                            color=color)



class Bezier:
    """Quadratic Bezier curve"""
    def __init__(self, x0,y0,x1,y1, curvature=0):
        # Middle point of the curve
        # positive curvature: curve right
        # negative curvature: curve left
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        # Also adding self.xc, self.yc, self.curvature
        self.change_curvature(curvature)
        
    def change_curvature(self, new_curvature):
        self.curvature = new_curvature
        # the point in the middle of the straight line
        xm, ym = (self.x0+self.x1)/2. , (self.y0+self.y1)/2.
        # point of curvature ('Bezier middle point', 'the third point')
        # [on the line perpendicular to the
        # straight line between x0,y0 and x1,y1]
        self.xc = xm + self.curvature * (self.y1-self.y0)/2.
        self.yc = ym - self.curvature * (self.x1-self.x0)/2.
        
    def change_middle_point(self, new_xc, new_yc):
        self.xc = new_xc
        self.yc = new_yc
        xm, ym = (self.x0+self.x1)/2. , (self.y0+self.y1)/2.
        curvature_x = 2. * (new_xc - xm) / (self.y1-self.y0)/2.
        curvature_y = 2. * (new_xc - xm) / (self.x1-self.x0)/2.
        self.curvature = max(curvature_x, curvature_y)

    def curve_function(self, t):
        """a function that returns a point on the curve.
        t is between [0,1]. At t=0, the curve is at x0,y0 
        At t=1, the curve is at x1,y1
        """
        x = self.x0*((1-t)**2) + self.xc*2*(1-t)*t + self.x1*(t**2)
        y = self.y0*((1-t)**2) + self.yc*2*(1-t)*t + self.y1*(t**2)
        return x,y

    def points(self, n):
        """ returns n points as a list of tuples:
        [(x0,y0), (xa,ya), (xb,yb), ... , (xk,yk), (x1,y1)]
        """
        Pts = [ (0.0, 0.0) ] * n
        for i in range(n):
            t = i / (n-1.)
            Pts[i] = self.curve_function(t)
        return Pts


    
class DirectedLinkSet(LinkSet):
    """Also a dataset containing network links.

    The links are directed. They can have arrows, they can curve
    around nodes on their path and they can be given a default
    curvature to be able to show both forward and backward connections
    between two nodes (the default is slightly to the right). Other
    than that, they are the same as LinkSet.
    """
    def __init__(self, size=1, color=1, 
                 avoid_crossing_nodes=True, put_arrows=True,
                 curvature = .6,
                 arrow_position = 0.75,
                 *args, **kwargs):
            DataSet.__init__(self, *args, **kwargs)
            if arrow_position > 1.0:
                arrow_position = 1.0
            elif arrow_position < 0.0:
                arrow_position = 0.0

            newData = []

            for n1, n2, in self.data:
                curveData = []

                xi, yi = self.parent.node_xy[n1]
                xf, yf = self.parent.node_xy[n2]
                try:
                    source = self.parent.nodes[n1]
                    target = self.parent.nodes[n2]
                except KeyError:
                    # nodes are not stored in self.parent.nodes
                    # the following option won't work, turn them off
                    avoid_crossing_nodes = False
                    source, target = None, None

                # Quadratic Bezier curve
                curve = Bezier(xi,yi,xf,yf, curvature=curvature)

                #######################################################
                # Now check in the curve is under any other node      #
                # but the source and the target. You can only do      #
                # this if the nodes are CircleNode, of course.
                # If they are, change curvature, check again.
                if avoid_crossing_nodes:
                    while True:
                        giveup = False
                        recheck = False
                        increment = .3
                        for x,y in curve.points(1000)[1:-1]:
                            for n in self.parent.nodes:
                                node = self.parent.nodes[n]
                                if not hasattr(node, 'in_circle') or n in (n1, n2):
                                    continue
                                if node.in_circle(x,y):
                                    recheck = True
                                    if 0 < curve.curvature < 10:
                                        curve.change_curvature(curve.curvature + increment)
                                    elif curve.curvature > 10:
                                        curve.change_curvature(-.4)
                                    elif -10 < curve.curvature <= 0:
                                        curve.change_curvature(curve.curvature - increment)
                                    elif curve.curvature < -10:
                                        curve.change_curvature(5)
                                        giveup = True
                                    #print n1,n2, 'under', n, '-> new curvature', curve.curvature
                                    break # the loop over nodes to check coverage
                            if recheck or giveup:
                                break # the loop over points of link
                        if recheck and not giveup:
                            continue # the while loop (check coverage again)
                        else:
                            #end of cheking without breaks. Passed the test.
                            break # the while loop
                        
                    # Check if all the curve is under source and target nodes
                    # If so, curve it away and back in (give it a high curvature)
                    while True:
                        covered = 0
                        for x,y in curve.points(40)[1:-1]:
                            for node in (source, target):
                                if not hasattr(node, 'in_circle'): break
                                if node.in_circle(x,y):
                                    covered += 1
                        if covered/(2*38.) > 0.29:
                            if 0 < curve.curvature <= 5:
                                curve.change_curvature(curve.curvature + .4)
                            elif curve.curvature > 5:
                                curve.change_curvature(-1.4)
                            elif 0 >= curve.curvature > -15:
                                curve.change_curvature(curve.curvature - .4)
                            elif curve.curvature < -15:
                                break # give up
                            #print n1,n2, 'cover %.1f %%' % (100*covered/(2*38.)), ' -> new curvature', curve.curvature
                        else:                                        #
                            break                                    #
                ######################################################

                # This is a linkset, so every point except the
                # first and the last ones must appear twice
                # (one segment is plotted, the next ignored)
                curveData.append((xi, yi))
                for x,y in curve.points(120)[1:-1]:
                    curveData.append((x, y))
                    curveData.append((x, y))
                curveData.append((xf, yf))

                if put_arrows:
                    # Find the position of the arrow
                    # the range of visible points
                    def visible_points(node1, node2):
                        # scan all points on the curve starting from
                        # center of second node, going back, stop when
                        # you found the fist point NOT under the node.
                        # (the edge of it). node1 and node2 are instances
                        # of start & end nodes. If these are not CircleNode,
                        # the position is just the end.
                        domain = []
                        # If not CircleNodes, assume everything's visible
                        if (not hasattr(node1, 'in_circle')) or \
                                (not hasattr(node2, 'in_circle')):
                            domain.append(curveData[0])
                            for i in range (1, len(curveData)-1, 2):
                                domain.append(CurveData[i])
                            domain.append(curveData[-1])
                            return domain
                        # Otherwise, scan for when we get out
                        # from under node 1:
                        node_1_out = len(curveData)-2
                        for i in range(1, len(curveData)-1, 2):
                            x,y = curveData[i]
                            if not node1.in_circle(x,y):
                                # We broke out from under node 1.
                                # Check if we are already under node 2.
                                node_1_out = i
                                break
                        # If we are already under node 2, nothing is
                        # visible go backwards, say the visible
                        # part is the intersection of nodes!
                        if node2.in_circle(x,y):
                            for i in range(node_1_out, 1, -2):
                                domain.insert(0, curveData[i])
                                x,y = curveData[i]
                                if not node2.in_circle(x,y):
                                    if len(domain) == 1: domain.insert(0, curveData[i-1])
                                    return domain
                            # end of for, we are back at start
                            return domain
                        # But if we are not there yet, scan forwards until you find it
                        node_2_out = len(curveData)-2
                        for i in range(node_1_out, len(curveData)-1, 2):
                            x,y = curveData[i]
                            if node2.in_circle(x,y):
                                node_2_out = i
                                if len(domain) == 1: domain.append(cureveData[i+1])
                                return domain
                            else:
                                domain.append(curveData[i])
                        # In case we couldn't fill domain, there aren't any visibles left,
                        # say all is visible
                        if domain == []:
                            domain.append(curveData[0])
                            for i in range (1, len(curveData)-1, 2):
                                domain.append(CurveData[i])
                            domain.append(curveData[-1])
                        # you found it, return it
                        return domain

                    # Find your arrow position
                    domain = visible_points(source, target)
                    domain.reverse()
                    i = int(arrow_position * len(domain)) -1
                    if i < 1: i = 1
                    start, end = domain[i-1], domain[i]
                    self.parent.add_drawing_object(DrawLine,
                                                   loctype="world",
                                                   onoff="on",
                                                   start=start,
                                                   end=end,
                                                   linestyle=1,
                                                   linewidth=size,
                                                   color=color,
                                                   arrow=2,
                                                   arrow_type=1,
                                                   arrow_length = 1.5,
                                                   arrow_layout=(0.8,0.8))
                    ###############
#                     #Write the i j of links (for debugging)
#                     self.parent.add_drawing_object(DrawText,
#                                                    char_size = .8,
#                                                    text = '%s %s' % (n1,n2),
#                                                    loctype="world",
#                                                    onoff="on",
#                                                    x = start[0],
#                                                    y=start[1],
#                                                    color=color)
                    #################

                # put the calculated link into the collective data for the linkset.
                newData.extend(curveData)

            # Configure the whole linkset
            self.data = newData
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
        self.node_sz = {}  # stores node sizes
        self.nodes = {}    # stores node instances (if needed)
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

    def add_circle_node(self, label, node_data,
                                  *args, **kwargs):
        """Add a single circle node to the graph.

        The node will be added to the Network graph as a CircleNode.

        -label contains the label of the node.

        -node_data needs to be the (x,y,r) coordinates of the node and the radius (size)
        """
        return self.add_dataset({label: node_data},
                                CircleNode,
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

    def add_directed_link_set(self, node_pairs, size=1, color=1,
                              *args, **kwargs):
        """Add a bunch of directed links to the graph.

        Links will be added to the Network graph as a DirectedLinkSet.

        -node_pairs needs to be a pair of nodes (label1, label2), and
        the corresponding nodes need to exist in the network already.
        """
        dirlinkSet = self.add_dataset(node_pairs,
                                   DirectedLinkSet,
                                   size=size, color=color,
                                   *args, **kwargs)
        self.move_dataset_to_back(dirlinkSet)
        return dirlinkSet

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

    def add_directed_link(self, node_pair, *args, **kwargs):
        """Add a single directed link to the graph.

        The link will be added to the Network graph as a DirectedLinkSet.

        -node_pair needs to be a pair of nodes (label1, label2), and
        the corresponding nodes need to exist in the network already.
        """
        dirlinkSet = self.add_dataset([node_pair],
                                   DirectedLinkSet,
                                   *args, **kwargs)
        self.move_dataset_to_back(dirlinkSet)
        return dirlinkSet

