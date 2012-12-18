from PyGrace.graph import Graph
from PyGrace.drawing_objects import DrawText, DRAWTEXT_JUSTIFICATIONS
from PyGrace.Extensions.multi_grace import MultiGrace
from PyGrace.Extensions.network import Network
from PyGrace.Extensions.tree import Tree

class PanelLabel(DrawText):
    """This class is useful for adding panel labels to figures.  Note that
    dx and dy are automatically adjusted to correctly space the 

    index = index of labelling scheme

    dx,dy = Spatial offset from Panel corner.  Direction of dx changes
        depending on placement specification.
    placement = 'iur' (inside upper right), 'our' (outside upper right),
         'ilr' (inside lowr right), etc.
    """

    def __init__(self,parent,index=None,dx=0.05,dy=0.05,
                 placement="iur",label_scheme=None,
                 *args,**kwargs):
        DrawText.__init__(self,parent,*args,**kwargs)

        # add panel keyword arguments to local name space.  This
        # allows you to (i) say things like "graph.panel_label.dx=0.1"
        # and (ii) use copy format to copy the attribute values of the
        # panel label.
        self._set_kwargs_attributes(locals())

        # panel label always lives in view coordinates to prevent it
        # from being marked as out of bounds in the event that
        # Graph.remove_extraworld_drawing_objects is called.
        if self.loctype!="view":
            message = """
PanelLabel always lives in 'view' coordinates to prevent it from being
marked as out of bounds in the event that
Graph.remove_extraworld_drawing_objects is called.
"""
            raise TypeError, message

        # specify formats for panel labels
        self.set_text()

        # place the panel label.  This method is also called at draw
        # time in the event that a user changes the location of the
        # PanelLabel
        #
        # Checking for None, which is necessary for copy_format to work.
        if self.parent is not None: 
            self.place_label()

    def set_text(self,label_scheme=None,index=None):
        """Set the text of the panel label at draw time based on the
        label_scheme and the index.
        """
        
        # nothing has been specified
        if ((self.label_scheme is None and label_scheme is None) or
            (self.index is None and index is None)):
            self.text = ''
            return
        
        # make sure label_scheme is legal
        if label_scheme is None:
            label_scheme = self.label_scheme
        elif not self.root.label_schemes.has_key(label_scheme):
            message = """
Label scheme '%s' is not allowed.  Try one of these instead:
%s
"""%(str(label_scheme),
     '\n'.join(self.root.label_schemes.keys()))
            raise TypeError,message
        self.label_scheme = label_scheme

        # make sure index is legal
        if index is None:
            index = self.index
        elif index<0 or index>=len(self.root.label_schemes[label_scheme]):
            message = """
Label index '%s' is not allowed for label scheme '%s'.
For label scheme '%s', label index must be between 0 and %d.
"""%(str(index),
     label_scheme,
     label_scheme,
     len(self.root.label_schemes[label_scheme]))
            raise TypeError,message
        self.index = index

        # set the text of the label
        self.text = self.root.label_schemes[self.label_scheme][self.index]

    def place_label(self,placement=None,dx=None,dy=None,just=None):
        """Place the PanelLabel near with format placement and position dx and
        dy, which are measured as the fraction of the length of the
        longest side of the frame of the Panel (its parent).  This
        method requires no arguments, but you can specify placement,
        dx, and dy optionally.  You can also additionally optionally
        specify the justification with 'just', which will override the
        default behavior of a PanelLabel which automatically justifies
        this feature.

        This method is called at draw time to correctly place the label.
        """

        # find the position of the frame
        xmin,ymin,xmax,ymax = self.parent.get_view()

        # variables for the placement of the label
        xys = {"ul": (xmin,ymax),
               "uc": (0.5*(xmin+xmax),ymax),
               "ur": (xmax,ymax),
               "ml": (xmin,0.5*(ymin+ymax)),
               "mc": (0.5*(xmin+xmax),0.5*(ymin+ymax)),
               "mr": (xmax,0.5*(ymin+ymax)),
               "ll": (xmin,ymin),
               "lc": (0.5*(xmin+xmax),ymin),
               "lr": (xmax,ymin),
               }
        outward_direction = {"ul": (-1.0,1.0),
                             "uc": (0.0,1.0),
                             "ur": (1.0,1.0),
                             "ml": (-1.0,0.0),
                             "mc": (0.0,0.0),
                             "mr": (1.0,0.0),
                             "ll": (-1.0,-1.0),
                             "lc": (0.0,-1.0),
                             "lr": (1.0,-1.0),
                             }
        opposite_just = {"ul": "lr",
                         "uc": "lc",
                         "ur": "ll",
                         "ml": "mr",
                         "mc": "mc",
                         "mr": "ml",
                         "ll": "ur",
                         "lc": "uc",
                         "lr": "ul",
                         }

        # set the placement variables as necessary
        if placement is not None:
            self.placement = placement
        if dx is not None: 
            self.dx = dx
        if dy is not None:
            self.dy = dy

        # make sure placement is legal
        if self.placement not in xys.keys():
            i = lambda s: "'i" + s + "',"
            o = lambda s: "'o" + s + "',"
            keys = xys.keys()
            keys.sort()
            message ="""
Unknown placement.  Placement should be one of 
%s
%s
"""%(' '.join(map(i,keys)),' '.join(map(o,keys)))
            
        # deal with the justification of the text
        if just is not None:
            self.just = just
        else:
            if self.placement[0]=='i':
                self.just = DRAWTEXT_JUSTIFICATIONS[self.placement[1:]]
            else:
                self.just = DRAWTEXT_JUSTIFICATIONS[opposite_just[self.placement[1:]]]
        
        # place the friggin' label
        key = self.placement[1:]
        if self.placement[0]=='i':
            sign = -1.0
        else:
            sign = 1.0
        self.x = xys[key][0] + sign*outward_direction[key][0]*self.dx
        self.y = xys[key][1] + sign*outward_direction[key][1]*self.dy

    def __str__(self):
        """Override the __str__ functionality to draw the PanelLabel at
        draw time.
        """
        self.set_text()
        self.place_label()
        return DrawText.__str__(self)

class Panel(Graph):
    """A Panel is a Graph that has a panel label.

    """

    def __init__(self,panel_index=None,
                 *args,**kwargs):
        Graph.__init__(self,*args,**kwargs)

        # find a default index for this graph
        if panel_index is None:
            if self.index is None:
                panel_index = 0
            else:
                panel_index = self.index

        # specify the default justification for the label
        self.panel_label = self.add_drawing_object(PanelLabel,panel_index)

class MultiPanelGrace(MultiGrace):
    """Grace object to hold panel schemes.
    """

    def __init__(self,label_scheme="LATIN",*args,**kwargs):
        MultiGrace.__init__(self,*args,**kwargs)

        # dummy variables
        latin_alphabet = "abcdefghijklmnopqrstuvwxyz"
        roman_numerals = ["i","ii","iii","iv","v","vi","vii","viii","ix","x"]

        # add default label schemes
        self.label_schemes = {}
        self.add_label_scheme('',['']*100)
        self.add_label_scheme("latin",[c.lower() for c in latin_alphabet])
        self.add_label_scheme("LATIN",[c.upper() for c in latin_alphabet])
        self.add_label_scheme("roman",[n.lower() for n in roman_numerals])
        self.add_label_scheme("ROMAN",[n.upper() for n in roman_numerals])

        # specify the label scheme
        self.set_label_scheme(label_scheme)

    def add_label_scheme(self,label_scheme,labels):
        """Add a label scheme to this Grace.
        """

        if (self.label_schemes.has_key(label_scheme) and 
            self.label_schemes[label_scheme]!=tuple(labels)):
            message = """Label scheme '%s' already exists.
"""%(label_scheme)
            raise KeyError,message

        self.label_schemes[label_scheme] = tuple(labels)

    def set_label_scheme(self,label_scheme):
        """Specify the label scheme for the grace and all panels
        in the grace.
        """

        if not self.label_schemes.has_key(label_scheme):
            l = self.label_schemes.keys()
            l.sort()
            possible_label_schemes = ''
            for a_scheme in l[:-1]:
                possible_label_schemes += '\'' + a_scheme + "', "
            possible_label_schemes += "or '" + l[-1]
            message = """Label scheme '%s' does not exist.  
Only labels schemes %s are possible.
"""%(label_scheme,possible_label_schemes)
            raise KeyError,message

        self.label_scheme = label_scheme
        for graph in self.graphs:
            if isinstance(graph,Panel):
                graph.panel_label.label_scheme = label_scheme

    def place_labels(self,placement=None,dx=None,dy=None,just=None):
        """Place all labels in grace at the same time.
        """
        for graph in self.graphs:
            if isinstance(graph,Panel):
                    graph.panel_label.place_label(placement=placement,
                                                  dx=dx,dy=dy,just=just)

    def add_graph(self, cls=Panel, *args, **kwargs):
        """Overwrite the add_graph of Grace base so that the default
        argument is a panel
        """
        graph = MultiGrace.add_graph(self,cls,*args,**kwargs)
        if isinstance(graph,Panel):
            graph.panel_label.configure(label_scheme=self.label_scheme)
        return graph

class NetworkPanel(Panel,Network):
    """A panel to display networks.
    """
    def __init__(self, *args, **kwargs):
        Panel.__init__(self,*args,**kwargs)
        drawing_objects = self.drawing_objects
        Network.__init__(self,*args,**kwargs)
        self.drawing_objects.extend(drawing_objects)

class TreePanel(Panel,Tree):
    """A panel to display trees.
    """
    def __init__(self, *args, **kwargs):
        Panel.__init__(self,*args,**kwargs)
        drawing_objects = self.drawing_objects
        Tree.__init__(self,*args,**kwargs)
        self.drawing_objects.extend(drawing_objects)
