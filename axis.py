import base, sys

LINEAR_SCALE = "Normal"
LOGARITHMIC_SCALE = "Logarithmic"

class AxisBar(base.GraceObject):
    _staticType = 'AxisBar'
    def __init__(self, parent,
                 onoff='on',
                 color=1,
                 linestyle=1,
                 linewidth=2,
                 ):
        base.GraceObject.__init__(self, parent, locals())

    def __str__(self):
        self.orientation = self.parent.orientation
        self.alt = self.parent.alt
        return \
"""@    %(alt)s%(orientation)saxis bar %(onoff)s
@    %(alt)s%(orientation)saxis bar color %(color)s
@    %(alt)s%(orientation)saxis bar linestyle %(linestyle)s
@    %(alt)s%(orientation)saxis bar linewidth %(linewidth)s""" % self

class AxisLabel(base.GraceObject):
    _staticType = 'AxisLabel'
    def __init__(self, parent,
                 text='',
                 font=4,
                 color=1,
                 char_size=1.75,
                 layout='para',
                 place='normal',
                 place_loc='auto',
                 place_tup=(0, 0.08),
                 ):
        base.GraceObject.__init__(self, parent, locals())
        self._formatting_template = {'place_tup': '%.20f, %.20f'}

    def __setattr__(self, key, value):

        # check type of AxisLabel specific attribute
        if key == 'place':
            self._check_type(str, key, value)
        elif key == 'layout':
            self._check_type(str, key, value)
            
        base.GraceObject.__setattr__(self, key, value)

    def __str__(self):
        self.orientation = self.parent.orientation
        self.alt = self.parent.alt
        return \
"""@    %(alt)s%(orientation)saxis label layout %(layout)s
@    %(alt)s%(orientation)saxis label place %(place)s
@    %(alt)s%(orientation)saxis label place %(place_loc)s
@    %(alt)s%(orientation)saxis label place %(place_tup)s
@    %(alt)s%(orientation)saxis label "%(text)s"
@    %(alt)s%(orientation)saxis label color %(color)s
@    %(alt)s%(orientation)saxis label char size %(char_size)s
@    %(alt)s%(orientation)saxis label font %(font)s""" % self
            
class Tick(base.GraceObject):
    _staticType = 'Tick'
    def __init__(self, parent,
                 onoff='on',
                 major=0.5,
                 minor_ticks=1,
                 default=6,
                 place_rounded='true',
                 inout='in',
                 major_size=1.65,
                 major_color=1,
                 major_linewidth=2.0,
                 major_linestyle=1,
                 major_grid='off',
                 minor_size=1.15,
                 minor_color= 1,
                 minor_linewidth=2.0,
                 minor_linestyle=1,
                 minor_grid='off',
                 place='both',
                 spec_ticks=(),
                 spec_ticklabels=(),
                 spec_ticktypes=(),
                 spec_type='none',
                 spec_typedefault='major',
                 spec_labeldefault='',
                 ):
        base.GraceObject.__init__(self, parent, locals())

    def __setattr__(self, key, value):

        # check type of AxisLabel specific attribute
        if key == 'major':
            self._check_type((float, int), key, value)
            self._check_range(key, value, 0, None, includeMin=False)
        elif key == 'minor_ticks':
            self._check_type(int, key, value)
            self._check_range(key, value, 0, None)
        elif key.endswith('grid'):
            self._check_type(str, key, value)
            self._check_membership(key, value, ('on', 'off'))
        elif key == 'default':
            self._check_type(int, key, value)
        elif key == 'place_rounded':
            self._check_type(str, key, value)
            self._check_membership(key, value, ('true', 'false'))
        elif key == 'inout':
            self._check_type(str, key, value)
            self._check_membership(key, value, ('in', 'out'))
        elif key == 'spec_ticks':
            self._check_type((tuple, list), key, value)
        elif key == 'spec_ticktypes':
            self._check_type((tuple, list), key, value)
        elif key == 'spec_ticklabels':
            self._check_type((tuple, list), key, value)
        elif key == 'spec_labeldefault':
            self._check_type(str, key, value)
        elif key == 'spec_typedefault':
            self._check_type(str, key, value)
            self._check_membership(key, value, ('major', 'minor'))
        elif key == 'spec_type':
            self._check_type(str, key, value)
            self._check_membership(key, value, ('none', 'ticks', 'both'))

        base.GraceObject.__setattr__(self, key, value)
        
    def __str__(self):

        # get orientation and alt from parent (axis)
        self.orientation = self.parent.orientation
        self.alt = self.parent.alt

        # record the number of special ticks
        self.spec_number = len(self.spec_ticks)

        # write all of the non-special attributes
        tickString = \
"""@    %(alt)s%(orientation)saxis tick %(onoff)s
@    %(alt)s%(orientation)saxis tick major %(major)s
@    %(alt)s%(orientation)saxis tick minor ticks %(minor_ticks)s
@    %(alt)s%(orientation)saxis tick default %(default)s
@    %(alt)s%(orientation)saxis tick place rounded %(place_rounded)s
@    %(alt)s%(orientation)saxis tick %(inout)s
@    %(alt)s%(orientation)saxis tick place %(place)s
@    %(alt)s%(orientation)saxis tick major size %(major_size)s
@    %(alt)s%(orientation)saxis tick major color %(major_color)s
@    %(alt)s%(orientation)saxis tick major linewidth %(major_linewidth)s
@    %(alt)s%(orientation)saxis tick major linestyle %(major_linestyle)s
@    %(alt)s%(orientation)saxis tick major grid %(major_grid)s
@    %(alt)s%(orientation)saxis tick minor color %(minor_color)s
@    %(alt)s%(orientation)saxis tick minor linewidth %(minor_linewidth)s
@    %(alt)s%(orientation)saxis tick minor linestyle %(minor_linestyle)s
@    %(alt)s%(orientation)saxis tick minor grid %(minor_grid)s
@    %(alt)s%(orientation)saxis tick minor size %(minor_size)s
@    %(alt)s%(orientation)saxis tick spec type %(spec_type)s
@    %(alt)s%(orientation)saxis tick spec %(spec_number)s""" % self

        # if there are no special ticks, just return the tick info now
        if self.spec_number == 0:
            return tickString

        # if there are ticklabels given, use them. otherwise, default is blank
        if len(self.spec_ticklabels) == len(self.spec_ticks):
            labels = self.spec_ticklabels
        else:
            labels = [self.spec_labeldefault for i in self.spec_ticks]

        # if there are ticktypes given, use them. otherwise, default is major
        if len(self.spec_ticktypes) == len(self.spec_ticks):
            types = self.spec_ticktypes
        else:
            types = [self.spec_typedefault for i in self.spec_ticks]

        # make two lines for each tick (label, and tick value)
        lines = []
        for i, (t, l, y) in enumerate(zip(self.spec_ticks, labels, types)):
            tickLine = '@    %s%saxis tick %s %i, %s' % \
                (self.alt, self.orientation, y, i, t)
            labelLine = '@    %s%saxis ticklabel %i, "%s"' % \
                (self.alt, self.orientation, i, l)
            lines.append(tickLine)
            lines.append(labelLine)

        # join all special tick lines into a string
        specialTickString = '\n'.join(lines)

        # return a string with tick information and special ticks
        return '\n'.join((tickString, specialTickString))

class TickLabel(base.GraceObject):
    _staticType = 'TickLabel'
    def __init__(self, parent,
                 onoff='on',
                 format='general',
                 prec=3,
                 formula='',
                 append='',
                 prepend='',
                 angle=0,
                 skip=0,
                 stagger=0,
                 place='normal',
                 offset_loc='auto',
                 offset_tup=(0.0, 0.0),
                 start_type='auto',
                 start = 0.0,
                 stop_type = 'auto',
                 stop = 0.0,
                 char_size = 1.65,
                 font=4,
                 color=1,
                 ):
        base.GraceObject.__init__(self, parent, locals())
        self._formatting_template = {'offset_tup': '%.20f, %.20f'}

    def __setattr__(self, key, value):

        # check type of AxisLabel specific attribute
        if key == 'angle':
            self._check_type((float, int), key, value)
            self._check_range(key, value, 0, 32, includeMax=False)
        elif key == 'stagger':
            self._check_type(int, key, value)
            self._check_range(key, value, 0, 9)
        elif key == 'start' or key == 'stop':
            self._check_type((float, int), key, value)
        elif key == 'start_type' or key == 'stop_type':
            self._check_type(str, key, value)
            self._check_membership(key, value, ('auto', 'spec'))
        elif key == 'formula':
            self._check_type(str, key, value)

        base.GraceObject.__setattr__(self, key, value)

    def __str__(self):
        self.orientation = self.parent.orientation
        self.alt = self.parent.alt
        return \
"""@    %(alt)s%(orientation)saxis ticklabel %(onoff)s
@    %(alt)s%(orientation)saxis ticklabel format %(format)s
@    %(alt)s%(orientation)saxis ticklabel prec %(prec)s
@    %(alt)s%(orientation)saxis ticklabel formula "%(formula)s"
@    %(alt)s%(orientation)saxis ticklabel append "%(append)s"
@    %(alt)s%(orientation)saxis ticklabel prepend "%(prepend)s"
@    %(alt)s%(orientation)saxis ticklabel angle %(angle)s
@    %(alt)s%(orientation)saxis ticklabel skip %(skip)s
@    %(alt)s%(orientation)saxis ticklabel stagger %(stagger)s
@    %(alt)s%(orientation)saxis ticklabel place %(place)s
@    %(alt)s%(orientation)saxis ticklabel offset %(offset_loc)s
@    %(alt)s%(orientation)saxis ticklabel offset %(offset_tup)s
@    %(alt)s%(orientation)saxis ticklabel start type %(start_type)s
@    %(alt)s%(orientation)saxis ticklabel start %(start)s
@    %(alt)s%(orientation)saxis ticklabel stop type %(stop_type)s
@    %(alt)s%(orientation)saxis ticklabel stop %(stop)s
@    %(alt)s%(orientation)saxis ticklabel char size %(char_size)s
@    %(alt)s%(orientation)saxis ticklabel font %(font)s
@    %(alt)s%(orientation)saxis ticklabel color %(color)s""" % self

class Axis(base.GraceObject):
    def __init__(self, parent,
                 orientation = 'x',
                 alt='',
                 onoff='on',
                 scale=LINEAR_SCALE,
                 invert='off',
                 type_zero = 'false',
                 offset = (0.0,0.0),
                 ):
        # for the axis object, the static type is determined by the orientation
        # and whether or not it is the alternative
        self._staticType = '%s%sAxis' % (alt, orientation)
        base.GraceObject.__init__(self, parent, locals())
        self.bar = AxisBar(self)
        self.label = AxisLabel(self)
        self.tick = Tick(self)
        self.ticklabel = TickLabel(self)
        self._formatting_template = {'offset': '%.20f, %.20f'}

    def __setattr__(self, key, value):

        # check type of AxisLabel specific attribute
        if key == 'orientation':
            self._check_type(str, key, value)
            self._check_membership(key, value, ('x', 'y'))
        elif key == 'scale':
            self._check_type(str, key, value)
            SCALE_TYPES = (LINEAR_SCALE, LOGARITHMIC_SCALE)
            self._check_membership(key, value, SCALE_TYPES)
        elif key == 'alt':
            self._check_type(str, key, value)
            self._check_membership(key, value, ('', 'alt'))
        elif key == 'type_zero':
            self._check_type(str, key, value)
            self._check_membership(key, value, ('true', 'false'))

        base.GraceObject.__setattr__(self, key, value)

    def __str__(self):

        # only print everything if axis is on
        if self.onoff == 'on':
            body = \
"""@    %(alt)s%(orientation)saxis %(onoff)s
@    %(alt)s%(orientation)saxis type zero %(type_zero)s
@    %(alt)s%(orientation)saxis offset %(offset)s
%(bar)s
%(label)s
%(tick)s
%(ticklabel)s""" % self
        else:
            body = """@    %(alt)s%(orientation)saxis %(onoff)s""" % self

        # alt axis does not have a scale specified (the alt-axis and primary
        # axis must have the same type of scale)
        if self.alt:
            return body
        else:
            header = \
"""@    %(orientation)saxes scale %(scale)s
@    %(orientation)saxes invert %(invert)s""" % self
            return '\n'.join((header, body))

    def set_log(self):
        self.scale = LOGARITHMIC_SCALE
        self.ticklabel.format = 'Power'
        self.ticklabel.prec = 0
        self.tick.major = 10
        self.tick.minor_ticks = 9

    def set_lin(self):
        self.scale = LINEAR_SCALE
        self.ticklabel.format = 'general'
        self.ticklabel.prec = 1
        self.tick.major = 0.5
        self.tick.minor_ticks = 1

    def set_scale(self,scale):
        if scale==LINEAR_SCALE:
            self.set_lin()
        elif scale==LOGARITHMIC_SCALE:
            self.set_log()
        else:
            message = """
scale must be either LINEAR_SCALE or LOGARITHMIC_SCALE.
"""
            raise TypeError,message

    def set_format(self, format, precision=1):
        self.ticklabel.format = format
        self.ticklabel.prec = precision
