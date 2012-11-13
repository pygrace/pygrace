from base import GraceObject 

DRAWTEXT_JUSTIFICATIONS = {"l":0,
                           "r":1,
                           "c":2,
##                            "XXXX":3,
                           "ll":4,
                           "lr":5,
                           "lc":6,
##                            "XXXX":7,
                           "ul":8,
                           "ur":9,
                           "uc":10,
##                            "XXXX":11,
                           "ml":12,
                           "mr":13,
                           "mc":14,
                           }

class DrawingObject(GraceObject):
    _staticType = 'DrawingObject'
    def __init__(self, parent, attrs, *args, **kwargs):
        GraceObject.__init__(self, parent, attrs, *args, **kwargs)

        # these are needed for the parent checking by drawing objects, but
        # should not be imported everything else has been (to avoid a cycle
        # in the dependency graph)
        import graph
        import grace

        # if the drawing object is added by a Graph, then record the index of
        # the graph.  Otherwise the parent of the drawing object is the grace.
        # The case in which self.parent = None occurs when Base.copy_format
        # is used with a DrawingObject subclass.  In this case, since there
        # is no instance to associate with a graph (or not), then the drawing
        # object is linked to the grace (not any particular graph)
        if isinstance(self.parent, grace.Grace):
            self._linked_graph = None
        elif isinstance(self.parent, graph.Graph):
            self._linked_graph = self.parent.index
        elif self.parent == None:
            self._linked_graph = None            
        else:
            message = 'parent of drawing object (%s) is not graph or grace.' %\
                      type(self.parent)
            raise TypeError(message)

    def _make_header(self, objectString):

        # create header with correct graph association
        headerList = ['@with %s' % objectString]
        if not self._linked_graph is None:
            template = '@    %s g%%s' % objectString
            headerList.append(template % self._linked_graph)
        return '\n'.join(headerList)

    def limits(self):
        """This method must be overwritten in all subclasses of
        DrawingObject for autoscale features to work properly.
        """
        pass
        
    def smallest_positive(self):
        """Find the smallest positive coordinate of each drawing
        object.
        """
        xmin,ymin,xmax,ymax = self.limits()
        if xmin>0.0:
            x = xmin
        else:
            x = None
        if ymin>0.0:
            y = ymin
        else:
            y = None
        return x,y        
        
class DrawBox(DrawingObject):
    def __init__(self, parent,
                 onoff = 'on',
                 loctype = 'view',
                 lowleft = (0, 0),
                 upright = (1, 1),
                 linestyle = 1,
                 linewidth = 2.0,
                 color = 1,
                 fill_color = 1,
                 fill_pattern = 1,
                 **kwargs
                 ):
        DrawingObject.__init__(self, parent, locals())
        self._formatting_template = {'lowleft': '%.20f, %.20f',
                                     'upright': '%.20f, %.20f'}
    def __str__(self):
        self._header = self._make_header('box')
        return \
"""%(_header)s
@    box %(onoff)s
@    box loctype %(loctype)s
@    box %(lowleft)s, %(upright)s
@    box linestyle %(linestyle)s
@    box linewidth %(linewidth)s
@    box color %(color)s
@    box fill color %(fill_color)s
@    box fill pattern %(fill_pattern)s
@box def""" % self
            
    def limits(self):
        """Find the limits of a DrawBox for autoscaling axes (among
        other things?)
        """
        x,y = zip(self.lowleft, self.upright)
        return min(x), min(y), max(x), max(y)

class DrawText(DrawingObject):
    def __init__(self, parent,
                 onoff = 'on',
                 loctype = 'view',
                 x = 0,
                 y = 0,
                 color = 1,
                 rot = 0,
                 font = 4,
                 just = 0,
                 char_size = 1.65,
                 text = 'DrawObjText',
                 **kwargs
                 ):
        DrawingObject.__init__(self, parent, locals())

    def __str__(self):
        self._header = self._make_header('string')
        return \
"""%(_header)s
@    string %(onoff)s
@    string loctype %(loctype)s
@    string %(x)s, %(y)s
@    string color %(color)s
@    string rot %(rot)s
@    string font %(font)s
@    string just %(just)s
@    string char size %(char_size)s
@string def "%(text)s" """ % self
        
    def limits(self):
        """Find the limits of a DrawBox for autoscaling axes (among
        other things?)
        """
        return self.x, self.y, self.x, self.y


class DrawLine(DrawingObject):
    def __init__(self, parent,
                 onoff = 'on',
                 loctype = 'view',
                 start = (0,0),
                 end = (1,1),
                 linestyle = 1,
                 linewidth = 2.0,
                 color = 1,
                 arrow = 0,
                 arrow_type = 0,
                 arrow_length = 1,
                 arrow_layout = (1.0,1.0),
                 **kwargs
                 ):
        DrawingObject.__init__(self, parent, locals())
        self._formatting_template = {'start': '%.20f, %.20f',
                                     'end': '%.20f, %.20f',
                                     'arrow_layout': '%.20f, %.20f'}

    def __setattr__(self, key, value):

        # check Graph specific attributes
        if key == 'start' or key == 'end':
            self._check_type(tuple, key, value)
        elif key == 'arrow':
            self._check_type(int, key, value)
            self._check_range(key, value, 0, 3)
        elif key == 'arrow_type':
            self._check_type(int, key, value)
            self._check_range(key, value, 0, 2)
        elif key == 'arrow_length':
            self._check_type((float, int), key, value)
            self._check_range(key, value, 0, None)
        elif key == 'arrow_layout':
            self._check_type(tuple, key, value)
            self._check_range(key, value[0], 0, None)
            self._check_range(key, value[1], 0, 1, includeMax=True)
            
        GraceObject.__setattr__(self, key, value)

    def __str__(self):
        self._header = self._make_header('line')
        return \
"""%(_header)s
@    line %(onoff)s
@    line loctype %(loctype)s
@    line %(start)s, %(end)s
@    line linewidth %(linewidth)s
@    line linestyle %(linestyle)s
@    line color %(color)s
@    line arrow %(arrow)s
@    line arrow type %(arrow_type)s
@    line arrow length %(arrow_length)s
@    line arrow layout %(arrow_layout)s
@line def""" % self

    def limits(self):
        """Find the limits of a DrawLine for autoscaling axes (among
        other things?)
        """
        x,y = zip(self.start, self.end)
        return min(x), min(y), max(x), max(y)

class DrawEllipse(DrawingObject):
    def __init__(self, parent,
                 onoff = 'on',
                 loctype = 'view',
                 lowleft = (0,0),
                 upright = (1,1),
                 linestyle = 1,
                 linewidth = 2.0,
                 color = 1,
                 fill_color = 1,
                 fill_pattern = 1,
                 **kwargs
                 ):
        DrawingObject.__init__(self, parent, locals())
        self._formatting_template = {'lowleft': '%.20f, %.20f',
                                     'upright': '%.20f, %.20f'}
    def __str__(self):
        self._header = self._make_header('ellipse')
        return \
"""%(_header)s
@    ellipse %(onoff)s
@    ellipse loctype %(loctype)s
@    ellipse %(lowleft)s, %(upright)s
@    ellipse linestyle %(linestyle)s
@    ellipse linewidth %(linewidth)s
@    ellipse color %(color)s
@    ellipse fill color %(fill_color)s
@    ellipse fill pattern %(fill_pattern)s
@ellipse def""" % self

    def limits(self):
        """Find the limits of a DrawEllipse for autoscaling axes (among
        other things?)
        """
        x,y = zip(self.lowleft, self.upright)
        return min(x), min(y), max(x), max(y)


class LabelledPoint(DrawingObject):
    def __init__(self, parent,
                 onoff = 'on',
                 loctype = 'view',
                 x = 0,
                 y = 0,
                 text_color = 1,
                 rot = 0,
                 font = 4,
                 just = 14,
                 char_size = 1.0,
                 text = 'DrawObjText',
                 r = 1,
                 linestyle = 1,
                 linewidth = 2.0,
                 outline_color = 1,
                 fill_color = 1,
                 fill_pattern = 1,
                 **kwargs
                 ):
        DrawingObject.__init__(self, parent, locals())

        lowleft, upright = (x-r, y-r), (x+r, y+r)
        self.ellipse = DrawEllipse(parent, onoff=onoff, loctype=loctype,
                                   lowleft=lowleft, upright=upright,
                                   linestyle=linestyle, linewidth=linewidth,
                                   color=outline_color, fill_color=fill_color,
                                   fill_pattern=fill_pattern)
        self.textObject = DrawText(parent, onoff=onoff, loctype=loctype,
                                   x=x, y=y, color=text_color, rot=rot,
                                   font=font, just=just, char_size=char_size,
                                   text=text)

    def __str__(self):
        return '\n'.join(map(str, (self.ellipse, self.textObject)))

    def limits(self):
        """Find the limits of a LabelledPoint for autoscaling axes (among
        other things?)
        """
        return self.x, self.y, self.x, self.y

class MultiLegend(DrawingObject):
    def __init__(self, parent,
                 onoff = 'on',
                 loctype = 'view',
                 x = 0,
                 y = 0,
                 text_color = 1,
                 rot = 0,
                 font = 4,
                 just = 14,
                 char_size = 1.0,
                 text = 'DrawObjText',
                 r = 1,
                 linestyle = 1,
                 linewidth = 2.0,
                 outline_color = 1,
                 fill_color = 1,
                 fill_pattern = 1,
                 **kwargs
                 ):
        DrawingObject.__init__(self, parent, locals())

        for symbol, label in data:
            pass

        lowleft, upright = (x-r, y-r), (x+r, y+r)
        self.ellipse = DrawEllipse(parent, onoff=onoff, loctype=loctype,
                                   lowleft=lowleft, upright=upright,
                                   linestyle=linestyle, linewidth=linewidth,
                                   color=outline_color, fill_color=fill_color,
                                   fill_pattern=fill_pattern)
        self.textObject = DrawText(parent, onoff=onoff, loctype=loctype,
                                   x=x, y=y, color=text_color, rot=rot,
                                   font=font, just=just, char_size=char_size,
                                   text=text)

    def __str__(self):
        return '\n'.join(map(str, (self.ellipse, self.textObject)))

    def limits(self):
        """Find the limits of a MultiLegend for autoscaling axes (among
        other things?)
        """
        return self.x, self.y, self.x, self.y

