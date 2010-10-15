import sys

from PyGrace.grace import Grace
from PyGrace.graph import Graph
from PyGrace.dataset import DataSet

class Tree(Graph):
    """A graph to display trees (such as phylogenetic trees).
    """
    def __init__(self, parent, orientation='right', **kwargs):
        Graph.__init__(self, parent, **kwargs)
        
        self.labels = {}  # stores leaf labels
        for axis in [self.xaxis, self.yaxis]:
            axis.bar.onoff='off'
            axis.tick.onoff='off'

        # adjust axis properties based on orientation
        self.orientation = orientation
        if self.orientation in ['right','left']:
            self.xaxis.ticklabel.onoff='off'
            if self.orientation == 'right':
                self.yaxis.ticklabel.place = 'opposite'
        elif self.orientation in ['up','down']:
            self.yaxis.ticklabel.onoff='off'
            if self.orientation == 'up':
                self.xaxis.ticklabel.place = 'opposite'

        self.frame.linestyle = 0
        self.view.configure(xmin = 0.075 * self.parent.max_canvas_width,
                            xmax = 0.925 * self.parent.max_canvas_width,
                            ymin = 0.075 * self.parent.max_canvas_height,
                            ymax = 0.925 * self.parent.max_canvas_height)

    def __setattr__(self, key, value):
        # check type of AxisLabel specific attribute
        if key == 'orientation':
            self._check_type(str, key, value)
            self._check_membership(key, value, ('right','left','up','down'))
            
        Graph.__setattr__(self, key, value)

    def add_tree(self, tree_data,
                 size=1, color=1, line_width=1, line_color=1,
                 *args, **kwargs):
        """Add a tree to the graph.

        The tree is a string argument that contains the tree
        information.  The string must follow the Newick tree format
        (also known as Newick notation or New Hampshire tree format).
        See http://en.wikipedia.org/wiki/Newick_format for details.

        The tree will be added to the Tree graph as a DataSet.
        The labels will be added as special tick labels.

        """
        # parse the newick tree
        def parse_newick_tree(newick_tree):
            tree = []
            leafs = {}
            nodes = {}

            c = 0
            empty_name = 0
            leaf_x = 1
            while ")" in newick_tree:
                # find the nodes to be merged
                firstclose = newick_tree.index(")")
                lastopen = newick_tree[:firstclose].rindex("(")
                tomerge = newick_tree[lastopen:firstclose+1]

                # cut this into the components
                localnodes = tomerge.replace("(","").replace(")","").split(",")

                for node in localnodes:
                    name, length = node.split(":")

                    # if it is a leaf node
                    if '.internal.dbs.' not in name:
                        leafs[name] = [leaf_x, 1, float(length)]
                        nodes[name] = leafs[name]
                        leaf_x += 1
                    # this means that it is a previously merged node that needs to have it's dy-value updated
                    else:
                        if not name:
                            name = '.empty.dbs.' + str(empty_name)
                            empty_name += 1

                        nodes[name] = nodes[name] + [float(length)]

                    # add the data to draw the branches
                    x,y,dy = nodes[name]
                    tree.append([x,y])
                    tree.append([x,y+dy])

                # split each component into their parts, the name and the branch length
                localnodes = [i.split(':') for i in localnodes]

                # the merged node gets the average x-value of those who are merged
                x = sum([nodes[i[0]][0] for i in localnodes])/float(len(localnodes))

                # and starts from y+dy
                y = nodes[localnodes[0][0]][1] + float(localnodes[0][1])

                # add this guy to the node list
                merged_node = ''
                if ":" in newick_tree[firstclose+1:]:
                    next_colon = newick_tree[firstclose+1:].index(":")
                    merged_node = '.internal.dbs.'+newick_tree[firstclose+1:firstclose+1+next_colon]+'.'+str(c)
                    nodes[merged_node] = [x,y]

                # add the horizontal line
                for i in xrange(len(localnodes)):
                    for j in xrange(i+1,len(localnodes)):
                        tree += [[nodes[localnodes[i][0]][0],y],[nodes[localnodes[j][0]][0],y]]

                # strip out the nodes that we just merged and put a new name in their place
                newick_tree = newick_tree[:lastopen] + merged_node + newick_tree[firstclose+1+next_colon:]

                c+=1

            label_coord = [j[0] for i,j in leafs.items() if '.empty.dbs.' not in i]
            label_text = [i.replace("_"," ") for i in leafs.keys() if '.empty.dbs.' not in i]

            # adjust things according to the orientation;
            # specifically, adjust the coordinates and set the special
            # tick labels
            if self.orientation == 'right' or self.orientation == 'left':
                if self.orientation == 'right':
                    tree = [[-j,i] for i,j in tree]
                else:
                    tree = [[j,i] for i,j in tree]

                self.yaxis.tick.set_spec_ticks(label_coord, [], label_text)

                # add a buffer to the sides
                ymin, ymax = min(label_coord), max(label_coord)
                self.world.ymin = ymin - 0.05*(ymax-ymin)
                self.world.ymax = ymax + 0.05*(ymax-ymin)
            elif self.orientation == 'up' or self.orientation == 'down':
                if self.orientation == 'up':
                    tree = [[i,-j] for i,j in tree]
                elif self.orientation == 'down':
                    pass

                self.xaxis.tick.set_spec_ticks(label_coord, [], label_text)
                self.xaxis.ticklabel.configure(angle=270,)

                # add a buffer to the sides
                xmin, xmax = min(label_coord), max(label_coord)
                self.world.xmin = xmin - 0.05*(xmax-xmin)
                self.world.xmax = xmax + 0.05*(xmax-xmin)

            return tree
            
        data = self.add_dataset(parse_newick_tree(tree_data),
                                DataSet,
                                size=size, color=color,
                                line_width=line_width, line_color=line_color,
                                *args, **kwargs)

        # the tree should be just lines and is drawn as segments
        data.symbol.configure(shape=0,)
        data.line.configure(type=4,)

        return data
