import sys

from PyGrace.grace import Grace
from PyGrace.graph import Graph
from PyGrace.dataset import DataSet
from PyGrace.drawing_objects import DrawLine, DrawText
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
        
            # -- Preferences (Fixed manual tweaks - not arguments) -----

            # radius buffer percentage for determining where the circle
            # of a node ends. To avoid links curving around but still
            # touching the nodes
            node_border_buffer_percentage = 0.08

            # The threshold percentage of points in a link that are under the target
            # and the source. If this much or more are covered, the links try to bend
            # themselves, so that more of them are visible.
            bad_cover_percentage = 0.29

            # ----------------------

            DataSet.__init__(self, *args, **kwargs)
            if arrow_position > 1.0:
                arrow_position = 1.0
            elif arrow_position < 0.0:
                arrow_position = 0.0

            newData = []

            # -- loop over each link -- #
            for n1, n2, in self.data:
                curveData = []

                xi, yi = self.parent.node_xy[n1]
                xf, yf = self.parent.node_xy[n2]

                source = n1
                target = n2

                # Quadratic Bezier curve
                curve = Bezier(xi,yi,xf,yf, curvature=curvature)

                wxmin,wymin,wxmax,wymax = kwargs['parent'].get_world()
                vxmin,vymin,vxmax,vymax = kwargs['parent'].get_view()

                # compute the scaling factor between items in the world space and in the view space
                # asuming that one uses circular node symbols
                # if the view space is not square, there are potential issues
                ratio = min((wxmax - wxmin)/(vxmax - vxmin),(wymax - wymin)/(vymax - vymin))

                def point_under_node(x,y,node, buffer_perc=0.00):
                    """given a point and a node label,
                    checks if point is under the node symbol"""
                    # get node info
                    x0, y0 = self.parent.node_xy[node]
                    r = (self.parent.node_sz[node]/100.) * ratio * (1 + buffer_perc)
                    # check if point is under the node (within the circle)
                    if (x-x0)**2+(y-y0)**2 <= r**2:
                        return True
                    else:
                        return False


                if avoid_crossing_nodes:
                ####################################################################
                # Now check if the curve is under any other node                   #
                # but the source and the target. If it is, change curvature,       #
                # check again:                                                     #
                # CURVE AROUND NODES IN YOUR WAY
                #
                    while True:
                        giveup = False
                        recheck = False
                        increment = 0.3
                        for x,y in curve.points(1000)[1:-1]:
                            for n in self.parent.node_xy:
                                if n in (source, target):
                                    # we won't try to curve around these 
                                    continue
                                # check if point is under the node (within the circle)
                                if point_under_node(x,y,n, buffer_perc = node_border_buffer_percentage):
                                    # point is indeed under it. curve away and recheck.
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
                #                                                                  #
                #                                                                  #
                ######------------                                    -------#######
                #     Check if all the curve is under source and target nodes      #
                #     If so, curve it away and back in (give it a high curvature): #
                #     FLARE OUT IF SOURCE AND TARGET COVER YOU
                #
                    while True:
                        covered = 0
                        for x,y in curve.points(40)[1:-1]:
                            for n in (source, target):
                                # check if point (x,y) is in the node
                                if point_under_node(x,y,n):
                                    covered += 1
                        if covered/(2*38.) >= bad_cover_percentage:
                            # bad_cover_percentage or more is covered
                            # bend a little to show more of yourself
                            # do this again and again until either
                            # the coverage is less than the threshold
                            # or you curved a lot but still couldn't get away
                            # ( threshold to give up: |curvature| = 15  )
                            if 0 < curve.curvature <= 5:
                                curve.change_curvature(curve.curvature + .4)
                            elif curve.curvature > 5:
                                curve.change_curvature(-1.4)
                            elif 0 >= curve.curvature > -15:
                                curve.change_curvature(curve.curvature - .4)
                            elif curve.curvature < -15:
                                break # give up
                            #print n1,n2, 'cover %.1f %%' % (100*covered/(2*38.)), ' -> new curvature', curve.curvature
                        else:                                                    #
                            break                                                #
                #                                                                #
                ##################################################################

                # This is a linkset, so every point except the
                # first and the last ones must appear twice
                # (one segment is plotted, the next ignored)
                curveData.append((xi, yi))
                for x,y in curve.points(120)[1:-1]:
                    curveData.append((x, y))
                    curveData.append((x, y))
                curveData.append((xf, yf))


                if put_arrows:
                ##################################################################
                # PUT AN ARROWHEAD ON THE LINK                                   #
                #                                                                
                #
                    # Find the position of the arrow
                    # the range of visible points
                    def visible_points(node1, node2):
                        # scan all points on the curve starting from
                        # center of second node, going back, stop when
                        # you found the fist point NOT under the node.
                        # (the edge of it). node1 and node2 are instances
                        # of start & end nodes. 
                        domain = []
                        # Otherwise, scan for when we get out
                        # from under node 1:
                        node_1_out = len(curveData)-2
                        for i in range(1, len(curveData)-1, 2):
                            x,y = curveData[i]
                            if not point_under_node(x,y,node1):
                                # We broke out from under node 1.
                                # Check if we are already under node 2.
                                node_1_out = i
                                break
                        # If we are already under node 2, nothing is
                        # visible go backwards, say the visible
                        # part is the intersection of nodes!
                        if point_under_node(x,y,node2):
                            if node_1_out == 1:
                                domain=[curveData[0],curveData[1]]
                            for i in range(node_1_out, 1, -2):
                                domain.insert(0, curveData[i])
                                x,y = curveData[i]
                                if not point_under_node(x,y,node2):
                                    if len(domain) == 1: domain.insert(0, curveData[i-1])
                                    return domain
                            # end of for, we are back at start
                            return domain
                        # But if we are not there yet, scan forwards until you find it
                        node_2_out = len(curveData)-2
                        for i in range(node_1_out, len(curveData)-1, 2):
                            x,y = curveData[i]
                            if point_under_node(x,y,node2):
                                node_2_out = i
                                if len(domain) == 1: domain.append(0, curveData[i+1])
                                return domain
                            else:
                                domain.append(curveData[i])
                        # In case we couldn't fill domain, there aren't any visibles left,
                        # say all is visible
                        if domain == []:
                            domain.append(curveData[0])
                            for i in range (1, len(curveData)-1, 2):
                                domain.append(curveData[i])
                            domain.append(curveData[-1])
                        # you found it, return it
                        return domain

                    # Find your arrow position
                    domain = visible_points(source, target)
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
                                                   arrow_length = 0.85,
                                                   arrow_layout=(0.8,0.8))
                #                                                                #
                #                                                                #
                ##################################################################

                      #---------------#
#                     #Write the i j of links (for debugging)
#                     self.parent.add_drawing_object(DrawText,
#                                                    char_size = .8,
#                                                    text = '%s %s' % (n1,n2),
#                                                    loctype="world",
#                                                    onoff="on",
#                                                    x = start[0],
#                                                    y=start[1],
#                                                    color=color)
                      #---------------#

                # put the calculated link into the collective data for the linkset.
                newData.extend(curveData)

            # -- end of loop over each link -- #

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

