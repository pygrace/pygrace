from PyGrace.graph import Graph
from PyGrace.drawing_objects import DrawText, DRAWTEXT_JUSTIFICATIONS

class Panel(Graph):
    """A Panel is a Graph that has a panel label.

    """

    def __init__(self,parent,index,panel_index=None,
                 *args,**kwargs):
        Graph.__init__(self,parent,index)

        # find a default index for this graph
        if panel_index is None and not index is None:
            panel_index = index
        elif index is None:
            panel_index = 0

        # specify the default justification for the label
        self.panel_label = self.add_drawing_object(PanelLabel,index)

class PanelLabel(DrawText):
    """This class is useful for adding panel labels to figures.  Note that
    dx and dy are automatically adjusted to correctly space the 

    label_index = index of labelling scheme

    dx,dy = Spatial offset from Panel corner.  Direction of dx changes
        depending on placement specification.
    placement = 'iur' (inside upper right), 'our' (outside upper right),
         'ilr' (inside lowr right), etc.
    """

    def __init__(self,parent,label_index,dx=0.05,dy=0.05,
                 placement="iur",label_scheme="LATIN",
                 *args,**kwargs):
        DrawText.__init__(self,parent,*args,**kwargs)

        # add panel keyword arguments to local name space.  This
        # allows you to (i) say things like "graph.panel_label.dx=0.1"
        # and (ii) use copy format to copy the attribute values of the
        # panel label.
        self._set_kwargs_attributes(locals())

        # make sure parent is a graph
        if not isinstance(parent,Graph):
            message = """
PanelLabel's expect to have parents that are Graph's.
"""
            
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

        # specify automatically available label schemes
        latin_alphabet = "abcdefghijklmnopqrstuvwxyz"
        roman_numerals = ["i","ii","iii","iv","v","vi","vii","viii","ix","x"]
        self.label_schemes = {"LATIN":[c.upper() for c in latin_alphabet],
                              "latin":[c.lower() for c in latin_alphabet],
                              "ROMAN":[n.upper() for n in roman_numerals],
                              "roman":[n.lower() for n in roman_numerals],
                              }

        # specify formats for panel labels
        self.label_scheme = label_scheme
        self.label_index = 0
        self.set_text(label_scheme,label_index)

        # place the panel label.  This method is also called at draw
        # time in the event that a user changes the location of the
        # PanelLabel
        self.place_label()

    def add_scheme(self,scheme_name,scheme_labels):
        """This gives the user the ability to customize their label
        scheme however they damn well please.
        """
        if self.label_schemes.has_key(scheme_name):
            message = """Label scheme '%s' already exists!
"""%scheme_name
            raise TypeError,message
        self.label_schemes[scheme_name] = scheme_labels

    def set_text(self,label_scheme=None,label_index=None):
        """Set the text of the panel label at draw time based on the
        label_scheme and the label_index.
        """

        # make sure label_scheme is legal
        if label_scheme is None:
            label_scheme = self.label_scheme
        elif not self.label_schemes.has_key(label_scheme):
            message = """
Label scheme '%s' is not allowed.  Try one of these instead:
%s
"""%(str(label_scheme),
     '\n'.join(label_sheme.keys()))
            raise TypeError,message
        self.label_scheme = label_scheme

        # make sure label_index is legal
        if label_index is None:
            label_index = self.label_index
        elif label_index<0 or label_index>=len(self.label_schemes[label_scheme]):
            message = """
Label index '%s' is not allowed for label scheme '%s'.
For label scheme '%s', label index must be between 0 and %d.
"""%(str(label_index),
     label_scheme,
     label_scheme,
     len(self.label_schemes[label_scheme]))
            raise TypeError,message
        self.label_index = label_index

        # set the text of the label
        self.text = self.label_schemes[self.label_scheme][self.label_index]

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
