from base import GraceObject

SYMBOLS = {"None":0,
           "Circle":1,
           "Square":2,
           "Diamond":3,
           "Triangle up":4,
           "Triangle left":5,
           "Triangle down":6,
           "Triangle right":7,
           "Plus":8,
           "X":9,
           "Star":10,
           "Char":11,
           }
INDEX2SYMBOLS = {}
for name,index in SYMBOLS.iteritems():
    INDEX2SYMBOLS[index] = name
LINETYPES = {"None":0,
             "Straight":1,
             "Left stairs":2,
             "Right stairs":3,
             "Segments":4,
             "3-Segments":5}
INDEX2LINETYPES = {}
for name,index in LINETYPES.iteritems():
    INDEX2LINETYPES[index] = name
LINESTYLES = {"None":0,
              "--":1,
              ". . ":2,
              "- - ":3,
              "-- -- ":4,
              ". - . - ":5,
              ". -- . -- ":6,
              ". . - . . - ":7,
              "- - . - - . ":8}
INDEX2LINESTYLES = {}
for name,index in LINESTYLES.iteritems():
    INDEX2LINESTYLES[index] = name

class Symbol(GraceObject):
    _staticType = 'Symbol'
    def __init__(self, parent,
                 shape = 1,
                 size = 0.5,
                 color = 1,
                 pattern = 1,
                 fill_color = 1,
                 fill_pattern = 1,
                 linewidth = 1.0,
                 linestyle = 1,
                 char = 65,
                 char_font = 0,
                 skip = 0,
                 **kwargs
                 ):
        GraceObject.__init__(self, parent, locals())

    def __setattr__(self, key, value):

        # check type of Symbol specific attribute
        if key == 'skip':
            self._check_type(int, key, value)
        elif key == 'char':
            self._check_type(int, key, value)
            self._check_range(key, value, 0, 128, includeMax=False)
        elif key == 'shape':
            self._check_type(int, key, value)
            self._check_range(key, value, 0, 12, includeMax=False)

        GraceObject.__setattr__(self, key, value)

    def __str__(self):
        self.index = self.parent.index
        return \
"""@    s%(index)s symbol %(shape)s
@    s%(index)s symbol size %(size)s
@    s%(index)s symbol color %(color)s
@    s%(index)s symbol pattern %(pattern)s
@    s%(index)s symbol fill color %(fill_color)s
@    s%(index)s symbol fill pattern %(fill_pattern)s
@    s%(index)s symbol linewidth %(linewidth)s
@    s%(index)s symbol linestyle %(linestyle)s
@    s%(index)s symbol char %(char)s
@    s%(index)s symbol char font %(char_font)s
@    s%(index)s symbol skip %(skip)s""" % self

class Line(GraceObject):
    _staticType = 'Line'
    def __init__(self, parent,
                 type = 1,
                 linestyle = 1,
                 linewidth = 2.0,
                 color = 1,
                 pattern = 1,
                 **kwargs
                 ):
        GraceObject.__init__(self, parent, locals())

    def __setattr__(self, key, value):

        # check Line specific attributes
        if key == 'type':
            self._check_type(int, key, value)
            self._check_range(key, value, 0, 6, includeMax=False)
            
        GraceObject.__setattr__(self, key, value)

    def __str__(self):
        self.index = self.parent.index
        return \
"""@    s%(index)s line type %(type)s
@    s%(index)s line linestyle %(linestyle)s
@    s%(index)s line linewidth %(linewidth)s
@    s%(index)s line color %(color)s
@    s%(index)s line pattern %(pattern)s""" % self
    
class Baseline(GraceObject):
    _staticType = 'BaseLine'
    def __init__(self, parent,
                 type = 0,
                 onoff="off",
                 **kwargs
                 ):
        GraceObject.__init__(self, parent, locals())

    def __setattr__(self, key, value):

        # check BaseLine specific attributes
        if key == 'type':
            self._check_type(int, key, value)
            self._check_range(key, value, 0, 6, includeMax=False)
            
        GraceObject.__setattr__(self, key, value)

    def __str__(self):
        self.index = self.parent.index
        return \
"""@    s%(index)s baseline type %(type)s
@    s%(index)s baseline %(onoff)s""" % self

class Fill(GraceObject):
    _staticType = 'Fill'
    def __init__(self, parent,
                 type = 0,
                 rule = 0,
                 color = 1,
                 pattern = 1,
                 **kwargs
                 ):
        GraceObject.__init__(self, parent, locals())

    def __setattr__(self, key, value):

        # check Fill specific attributes
        if key == 'type':
            self._check_type(int, key, value)
            self._check_range(key, value, 0, 2)
        elif key == 'rule':
            self._check_type(int, key, value)
            self._check_range(key, value, 0, 1)
            
        GraceObject.__setattr__(self, key, value)
        
    def __str__(self):
        self.index = self.parent.index
        return \
"""@    s%(index)s fill type %(type)s
@    s%(index)s fill rule %(rule)s
@    s%(index)s fill color %(color)s
@    s%(index)s fill pattern %(pattern)s""" % self

class AnnotatedValue(GraceObject):
    _staticType = 'AnnotatedValue'
    def __init__(self, parent,
                 onoff = "off",
                 type = 4,
                 char_size = 0.65,
                 font = 4,
                 color = 1,
                 rot = 0,
                 format = "general",
                 prec = 3,
                 prepend = '',
                 append = '',
                 offset = (0.0,0.0),
                 **kwargs
                 ):
        GraceObject.__init__(self, parent, locals())
        self._formatting_template = {'offset': '%.20f, %.20f'}

    def __setattr__(self, key, value):

        # check AnnotatedValue specific attributes
        if key == 'type':
            self._check_type(int, key, value)
            self._check_range(key, value, 0, 6, includeMax=False)
            
        GraceObject.__setattr__(self, key, value)
        
    def __str__(self):
        self.index = self.parent.index
        return \
"""@    s%(index)s avalue %(onoff)s
@    s%(index)s avalue type %(type)s
@    s%(index)s avalue char size %(char_size)s
@    s%(index)s avalue font %(font)s
@    s%(index)s avalue color %(color)s
@    s%(index)s avalue rot %(rot)s
@    s%(index)s avalue format %(format)s
@    s%(index)s avalue prec %(prec)s
@    s%(index)s avalue prepend "%(prepend)s"
@    s%(index)s avalue append "%(append)s"
@    s%(index)s avalue offset %(offset)s""" % self
               
class ErrorBar(GraceObject):
    _staticType = 'ErrorBar'
    def __init__(self, parent,
                 onoff = "on",
                 place = "both",
                 color = 1,
                 pattern = 1,
                 size = 1.0,
                 linewidth = 2.0,
                 linestyle = 1,
                 riser_linewidth = 2.0,
                 riser_linestyle = 1,
                 riser_clip = "off",
                 riser_clip_length = 0.1,
                 **kwargs
                 ):
        GraceObject.__init__(self, parent, locals())

    def __setattr__(self, key, value):

        # check type of ErrorBar specific attribute
        if key == 'riser_clip':
            self._check_type(str, key, value)
            self._check_membership(key, value, ('on', 'off'))
        elif key == 'riser_clip_length':
            self._check_type((float, int), key, value)
            self._check_range(key, value, 0, None)

        GraceObject.__setattr__(self, key, value)
        
    def __str__(self):
        self.index = self.parent.index
        return \
"""@    s%(index)s errorbar %(onoff)s
@    s%(index)s errorbar place %(place)s
@    s%(index)s errorbar color %(color)s
@    s%(index)s errorbar pattern %(pattern)s
@    s%(index)s errorbar size %(size)s
@    s%(index)s errorbar linewidth %(linewidth)s
@    s%(index)s errorbar linestyle %(linestyle)s
@    s%(index)s errorbar riser linewidth %(riser_linewidth)s
@    s%(index)s errorbar riser linestyle %(riser_linestyle)s
@    s%(index)s errorbar riser clip %(riser_clip)s
@    s%(index)s errorbar riser clip length %(riser_clip_length)s""" % self

class DataSet(GraceObject):
    _staticType = 'DataSet'
    def __init__(self, parent, data, index,
                 type='xy',
                 hidden='false',
                 dropline='off',
                 comment='',
                 legend='',
                 **kwargs
                 ):
        GraceObject.__init__(self, parent, locals())
        self.baseline = Baseline(self)
        self.symbol = Symbol(self)
        self.line = Line(self)
        self.fill = Fill(self)
        self.avalue = AnnotatedValue(self)
        self.errorbar = ErrorBar(self)

    def __setattr__(self, key, value):

        DATA_TYPES = ('xy', 'xydx', 'xydy', 'xydxdy', 'xydydy', 
                      'xydxdx', 'xydxdxdydy', 'bar', 'bardy', 'bardydy',
                      'xyhilo', 'xyz', 
#                       'xyr', # apparently unsupported
                      'xysize', 'xycolor',
#                       'xycolpat', # xmgrace does not support
                      'xyvmap', 'xyboxplot')

        # check DataSet specific attributes
        if key == 'type':
            self._check_type(str, key, value)
            self._check_membership(key, value, DATA_TYPES)
        elif key == 'dropline':
            self._check_type(str, key, value)
            self._check_membership(key, value, ('on', 'off'))
        elif key == 'comment':
            self._check_type(str, key, value)
        elif key == 'legend':
            self._check_type(str, key, value)
            
        GraceObject.__setattr__(self, key, value)

    def __str__(self):
        return \
"""@    s%(index)s hidden %(hidden)s
@    s%(index)s type %(type)s
%(symbol)s
%(line)s
%(baseline)s
@    s%(index)s dropline %(dropline)s
%(fill)s
%(avalue)s
%(errorbar)s
@    s%(index)s comment "%(comment)s"
@    s%(index)s legend "%(legend)s" """ % self

    def data_bounds(self):
        x, y = [], []
        if self.data:
            if self.type=="xy" or self.type=="bar":
                columns = zip(*self.data)
                x, y = columns[:2]
            elif self.type=="xydx":
                for datum in self.data:
                    x.extend([datum[0],
                              datum[0]-datum[2],
                              datum[0]+datum[2]])
                    y.append(datum[1])
            elif self.type=="xydy":
                for datum in self.data:
                    x.append(datum[0])
                    y.extend([datum[1],
                              datum[1]-datum[2],
                              datum[1]+datum[2]])
            elif self.type=="xydxdy":
                for datum in self.data:
                    x.extend([datum[0],
                              datum[0]-datum[2],
                              datum[0]+datum[2]])
                    y.extend([datum[1],
                              datum[1]-datum[3],
                              datum[1]+datum[3]])
            elif self.type=="xydxdx":
                for datum in self.data:
                    x.extend([datum[0],
                              datum[0]+datum[2],
                              datum[0]-datum[3]])
                    y.append(datum[1])
            elif self.type=="xydydy":
                for datum in self.data:
                    x.append(datum[0])
                    y.extend([datum[1],
                              datum[1]+datum[2],
                              datum[1]-datum[3]])
            elif self.type=="xydxdxdydy":
                for datum in self.data:
                    x.extend([datum[0],
                              datum[0]+datum[2],
                              datum[0]-datum[3]])
                    y.extend([datum[1],
                              datum[1]+datum[4],
                              datum[1]-datum[5]])
            elif self.type=="bardy":
                for datum in self.data:
                    x.append(datum[0])
                    y.extend([datum[1],
                              datum[1]+datum[2],
                              datum[1]-datum[2]])
            elif self.type=="bardydy":
                for datum in self.data:
                    x.append(datum[0])
                    y.extend([datum[1],
                              datum[1]+datum[2],
                              datum[1]-datum[3]])
            elif self.type=="xyhilo":
                columns = zip(*self.data)
                x = columns[0]
                y = columns[1] + columns[2] + columns[3] + columns[4]
            elif self.type=="xyz":
                columns = zip(*self.data)
                x, y = columns[:2]
#             elif self.type=="xyr": # xmgrace does not support
#                 for datum in self.data:
#                     x.extend([datum[0]-datum[2],
#                               datum[0]+datum[2]])
#                     y.extend([datum[1]-datum[2],
#                               datum[1]+datum[2]])
            elif self.type=="xysize":
                columns = zip(*self.data)
                x, y = columns[:2]
            elif self.type=="xycolor":
                columns = zip(*self.data)
                x, y = columns[:2]
#             elif self.type=="xycolpat": # xmgrace does not support
#                 pass
            elif self.type=="xyvmap":
                for datum in self.data:
                    x.extend([datum[0],
                              datum[0]+datum[2]])
                    y.extend([datum[1],
                              datum[1]+datum[3]])
            elif self.type=='xyboxplot':
                col = zip(*self.data)
                x = col[0]
                y = col[1] + col[2] + col[3] + col[4]
            else:
                message = """
Can not find limits of DataSet with type %s
"""%self.type
                raise TypeError, message
        return x,y

    def limits(self,only_visible=True):
        if self.data:
            if ((only_visible and self.hidden=="false") 
                or not only_visible):
                x, y = self.data_bounds()
                return min(x), min(y), max(x), max(y)
        return None,None,None,None

    def smallest_positive(self,only_visible=True):
        if self.data:
            if ((only_visible and self.hidden=="false") 
                or not only_visible):
                x, y = self.data_bounds()
                x = [i for i in x if i > 0]
                y = [i for i in y if i > 0]
                if x:
                    xMin = min(x)
                else:
                    xMin = None
                if y:
                    yMin = min(y)
                else:
                    yMin = None
                return xMin, yMin
        return None,None

    def _repr_data(self):
        if self.type[:2]=='xy' or self.type[:3] =='bar': #any xy or bar type
            l=[' '.join(map(str,self.data[i])) for i in range(len(self.data))]
        else:
            l = []
        l.append('&')
        return '\n'.join(l)

