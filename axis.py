#!/usr/bin/env python
"""
Amaral Group
Northwestern University

Generic axis class.

"""
import sys

from fonts import DEFAULT_FONTS
from colors import DEFAULT_COLORS
from xmg_string import XMG_String
from xmg_exceptions import SetItemError,AttrError

#---------------------------------------------------------------------------
# useful data structures
#---------------------------------------------------------------------------
shapes = {"None":0,
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
          "Char":11};

linetypes = {"None":0,
             "Straight":1,
             "Left stairs":2,
             "Right stairs":3,
             "Segments":4,
             "3-Segments":5}

linestyles = {"--":0,
              ". . ":1,
              "- - ":2,
              "-- -- ":3,
              ". - . - ":4,
              ". -- . -- ":5,
              ". . - . . - ":6,
              "- - . - - . ":7};

#---------------------------------------------------------------------
# XMG_Bar Class
#---------------------------------------------------------------------

class XMG_Bar:

    def __init__(self,colors,
                 onoff='on',
                 color='black',
                 linestyle='. . ',
                 linewidth=1.0,
                 ):
        self._colors=colors
        self['onoff'] = onoff
        self['color'] = color
        self['linestyle'] = linestyle
        self['linewidth'] = linewidth
        
    def __getitem__(self,name): return getattr(self,name)

    def __setitem__(self, name, value):

        if type(value) == str:
            value = value.replace('"','')
        
        if name == 'onoff':
            try: self.onoff = value
            except: SetItemError(self.__class__,name, value)
        elif name == 'color':
            try:
                if self._colors.has_key(value):
                    self.color = value
                else:
                    intRepr = int(value)
                    if intRepr >= len(self._colors.keys()):
                        raise
                    else:
                        self.color = intRepr
            except:
                SetItemError(self.__class__,name,value)
        elif name == 'linestyle':
            try:
                if linestyles.has_key(value):
                    self.linestyle = linestyles[value]
                else:
                    self.linestyle = int(value)
            except: SetItemError(self.__class__, name, value)
        elif name == 'linewidth':
            try: self.linewidth = float(value)
            except: SetItemError(self.__class__,name, value)
        else:
            AttrError(self.__class__, name)


    def repr(self, orientation, alt=''):
        lines = []

        lines.append('@    ' + alt+orientation +'axis  bar '  + str(self.onoff))
        lines.append('@    ' + alt+orientation +'axis  bar color %s' %
                     (type(self.color)==str and ("\"%s\"" % self.color) or self.color));
        lines.append('@    ' + alt+orientation +'axis  bar linestyle '  + str(self.linestyle))
        lines.append('@    ' + alt+orientation +'axis  bar linewidth '  + str(self.linewidth))
        
        return lines
#---------------------------------------------------------------------
# XMG_Label Class
#---------------------------------------------------------------------

class XMG_Label:

    def __init__(self, colors, fonts,
                 label=None,
                 layout = 'para',
                 place = 'auto',
                 ):
        self._colors = colors
        self._fonts = fonts
        if label:
            self['label'] = label
        else:
            self['label'] = XMG_String(colors = self._colors, fonts=self._fonts,type='label')
        self['layout'] = layout
        self['place'] = place

        self.place_tup = None #this should be a tuple type

    def __getitem__(self,name): return getattr(self,name)

    def __setitem__(self, name, value):

        if type(value) == str:
            value = value.replace('"','')
        
        if name == 'label':
            if not value.__class__ == XMG_String:
                SetItemError(self.__class__,name,value)
            else:
                self.label = value
        elif name == 'layout':
            try: self.layout = value
            except: SetItemError(self.__class__, name, value )
        elif name == 'place':
            try: self.place = value
            except: SetItemError(self.__class__, name, value )
        elif name == 'place_tup':
            try:
                if not type(value) == tuple:
                    raise
                else:
                    self.place_tup = value
            except: SetItemError(self.__class__, name, value )  
        else:
            AttrError(self.__class__,name)


    def repr(self, orientation, alt=''):

        lines = []
        prefix = '@    ' + alt+orientation + 'axis  label'

        lines.append(prefix + ' layout ' + str(self.layout))
        lines.append(prefix + ' place ' + str(self.place))
        if self['place_tup']:
            lines.append(prefix + ' place ' + str(self['place_tup'])[1:-1])
        lines.append(self.label.contents(prefix))

        return lines
            

#---------------------------------------------------------------------
# XMG_Tick Class
#---------------------------------------------------------------------

class XMG_Tick:

    def __init__(self, colors,
                 onoff='on',
                 major=0.5,
                 minor_ticks=1,
                 default=6,
                 place_rounded='true',
                 inout='in',#or both
                 major_size=1.00,
                 major_color=1,
                 major_linewidth=1.0,
                 major_linestyle=1.0,
                 major_grid='off',
                 minor_size=.5,
                 minor_color='black',
                 minor_linewidth=1.0,
                 minor_linestyle=1,
                 minor_grid='off',
                 place='both',
                 spec=0,
                 spec_type='none',
                 ):
        self._colors = colors
        self['onoff'] = onoff
        self['major'] = major
        self['minor_ticks'] = minor_ticks
        self['default'] = default
        self['place_rounded'] = place_rounded
        self['inout'] = inout
        self['major_size'] = major_size
        self['major_color'] = major_color
        self['major_linewidth'] = major_linewidth
        self['major_linestyle'] = major_linestyle
        self['major_grid']=major_grid
        self['minor_size'] = minor_size
        self['minor_color'] = major_color
        self['minor_linewidth'] = minor_linewidth
        self['minor_linestyle'] = minor_linestyle
        self['minor_grid']=minor_grid
        self['place'] = place
        self.spec_ticks = []
        self['spec'] = len(self.spec_ticks)
        self['spec_type'] = spec_type

    def __getitem__(self,name): return getattr(self,name)

    def __setitem__(self,name,value):

        if type(value) == str:
            value = value.replace('"','')

        if name == 'onoff':
            try: self.onoff = value
            except: SetItemError(self.__class__,name, value)
        elif name == 'major':
            try: self.major = float(value)
            except: SetItemError(self.__class__,name, value)
        elif name == 'minor_ticks':
            try: self.minor_ticks = float(value)#float or int?
            except: SetItemError(self.__class__,name, value)
        elif name == 'default':
            try: self.default = int(value)#float or int?
            except: SetItemError(self.__class__,name, value)
        elif name == 'place_rounded':
            try: self.place_rounded = value
            except: SetItemError(self.__class__,name, value)
        elif name == 'inout':
            try: self.inout = value
            except: SetItemError(self.__class__,name, value)
        elif name == 'major_size':
            try: self.major_size = float(value)
            except: SetItemError(self.__class__,name, value)
        elif name == 'major_color':
            try:
                if self._colors.has_key(value):
                    self.major_color = value
                else:
                    intRepr = int(value)
                    if intRepr >= len(self._colors.keys()):
                        raise
                    else:
                        self.major_color = intRepr
            except:
                SetItemError(self.__class__,name,value)
        elif name == 'major_linewidth':
            try: self.major_linewidth = float(value)
            except: SetItemError(self.__class__,name, value)
        elif name == 'major_linestyle':
            try:
                if linestyles.has_key(value):
                    self.major_linestyle = linestyles[value]
                else:
                    self.major_linestyle = int(value)
            except: SetItemError(self.__class__, name, value)
        elif name == 'major_grid':
            try: self.major_grid = value
            except: SetItemError(self.__class__,name, value)
        elif name == 'minor_size':
            try: self.minor_size = float(value)
            except: SetItemError(self.__class__,name, value)
        elif name == 'minor_grid':
            try: self.minor_grid = value
            except: SetItemError(self.__class__,name, value)
        elif name == 'minor_color':
            try:
                if self._colors.has_key(value):
                    self.minor_color = value
                else:
                    intRepr = int(value)
                    if intRepr >= len(self._colors.keys()):
                        raise
                    else:
                        self.minor_color = intRepr
            except:
                SetItemError(self.__class__,name,value)
        elif name == 'minor_linewidth':
            try: self.minor_linewidth = float(value)
            except: SetItemError(self.__class__,name, value)
        elif name == 'minor_linestyle':
            try:
                if linestyles.has_key(value):
                    self.minor_linestyle = linestyles[value]
                else:
                    self.minor_linestyle = int(value)
            except: SetItemError(self.__class__, name, value)
        elif name == 'place':
            try: self.place = value
            except: SetItemError(self.__class__, name, value)
        elif name == 'spec':
            try: self.spec = int(value)
            except: SetItemError(self.__class__, name, value)    
        elif name == 'spec_type':
            try: self.spec_type = value
            except: SetItemError(self.__class__, name, value)
        else:
            AttrError(self.__class__, name)

    def add_spec(self,attr): #add a special tick (special ticklabels are included here as well
        try:                 #not in the ticklabel class 
            if not attr[0] in ['ticklabel','major','minor']:
                raise
            attr[1] = int(attr[1])
            if not attr[0] == 'ticklabel':
                attr[2] = float(attr[2])
            self.spec_ticks.append(attr)
            self.spec += 1
        except:
            SetItemError(self.__class__,'spec_ticks',attr)

    # Add a special ticklabel and its tick
    def add_spec_ticklabel(self, position, ticklabel=''):
        self.spec_ticks.append(('major', self.spec, position))
        self.spec_ticks.append(('ticklabel', self.spec, ticklabel))
        self.spec += 1
        
    def repr(self, orientation, alt=''):
        lines = []

        lines.append('@    ' + alt+orientation +'axis  tick '  + str(self.onoff))
        lines.append('@    ' + alt+orientation +'axis  tick major '  + str(self.major))
        lines.append('@    ' + alt+orientation +'axis  tick minor ticks '  + str(self.minor_ticks))
        lines.append('@    ' + alt+orientation +'axis  tick default '  + str(self.default))
        lines.append('@    ' + alt+orientation +'axis  tick place rounded '  + str(self.place_rounded))
        lines.append('@    ' + alt+orientation +'axis  tick '  + str(self.inout))
        lines.append('@    ' + alt+orientation +'axis  tick major size '  + str(self.major_size))
        lines.append('@    ' + alt+orientation +'axis  tick major color %s' % 
                     (type(self.major_color)==str and ("\"%s\"" % self.major_color) or self.major_color));
        lines.append('@    ' + alt+orientation +'axis  tick major linewidth '  + str(self.major_linewidth))
        lines.append('@    ' + alt+orientation +'axis  tick major linestyle '  + str(self.major_linestyle))
        lines.append('@    ' + alt+orientation +'axis  tick major grid '  + str(self.major_grid))
        lines.append('@    ' + alt+orientation +'axis  tick minor color %s' % 
                     (type(self.minor_color)==str and ("\"%s\"" % self.minor_color) or self.minor_color));
        lines.append('@    ' + alt+orientation +'axis  tick minor linewidth '  + str(self.minor_linewidth))
        lines.append('@    ' + alt+orientation +'axis  tick minor linestyle '  + str(self.minor_linestyle))
        lines.append('@    ' + alt+orientation +'axis  tick minor grid '  + str(self.minor_grid))
        lines.append('@    ' + alt+orientation +'axis  tick minor size '  + str(self.minor_size))
        
        return lines
#---------------------------------------------------------------------
# XMG_Ticklabel Class
#---------------------------------------------------------------------

class XMG_Ticklabel:

    def __init__(self,colors,fonts,
                 onoff='on',
                 format='general',
                 prec=5,
                 formula='',
                 append='',
                 prepend='',
                 angle=0,
                 skip=0,
                 stagger=0,
                 place='normal',
                 offset1='auto', #offset type?
                 offset2=(0.0,0.0), #the tuple
                 start_type='auto',
                 start = 0.00000,
                 stop_type = 'auto',
                 stop = 0.00000,
                 char_size = 1.00000,
                 font=0,
                 color=1,
                 ):
        self._colors = colors
        self._fonts = fonts
        self['onoff'] = onoff
        self['format'] = format
        self['prec'] = prec
        self['formula'] = formula
        self['append'] = append
        self['prepend'] = prepend
        self['angle'] = angle
        self['skip'] = skip
        self['stagger'] = stagger
        self['place'] = place
        self['offset1'] = offset1
        self['offset2'] = offset2
        self['start_type'] = start_type
        self['start'] = start
        self['stop_type'] = stop_type
        self['stop'] = stop
        self['char_size'] = char_size
        self['font'] = font
        self['color'] = color
    
    def __getitem__(self,name): return getattr(self,name)
    
    def __setitem__(self,name,value):

        if type(value) == str:
            value = value.replace('"','')
    
        if name == 'onoff':
            try: self.onoff = value
            except: SetItemError(self.__class__,name, value)
        elif name == 'format':
            try: self.format = value
            except: SetItemError(self.__class__,name, value)
        elif name == 'prec':
            try: self.prec = int(value)
            except: SetItemError(self.__class__,name, value)
        elif name == 'formula':
            try: self.formula = value
            except: SetItemError(self.__class__,name, value)
        elif name == 'append':
            try: self.append = value
            except: SetItemError(self.__class__,name, value)
        elif name == 'prepend':
            try: self.prepend = value
            except: SetItemError(self.__class__,name, value)
        elif name == 'angle':
            try: self.angle = int(value)
            except: SetItemError(self.__class__,name, value)
        elif name == 'skip':
            try: self.skip = int(value)
            except: SetItemError(self.__class__,name, value)
        elif name == 'stagger':
            try: self.stagger = int(value)
            except: SetItemError(self.__class__,name, value)
        elif name == 'place':
            try: self.place = value
            except: SetItemError(self.__class__,name, value)
        elif name == 'offset1':
            try: self.offset1 = value
            except: SetItemError(self.__class__,name, value)
        elif name == 'offset2':
            try:
                if not type(value) == tuple:
                    raise
                else:
                    self.offset2 = value
            except: SetItemError(self.__class__,name, value)
        elif name == 'start_type':
            try: self.start_type = value
            except: SetItemError(self.__class__,name, value)
        elif name == 'start':
            try: self.start = float(value)
            except: SetItemError(self.__class__,name, value)
        elif name == 'stop_type':
            try: self.stop_type = value
            except: SetItemError(self.__class__,name, value)
        elif name == 'stop':
            try: self.stop = float(value)
            except: SetItemError(self.__class__,name, value)
        elif name == 'char_size':
            try: self.char_size = float(value)
            except: SetItemError(self.__class__,name, value)
        elif name == 'font':
            try:
                if self._fonts.has_key(value):
                    self.font = value
                else:
                    intRepr = int(value)
                    if intRepr >= len(self._fonts.keys()):
                        raise
                    else:
                        self.font = intRepr
            except: SetItemError(self.__class__,name, value)
        elif name == 'color':
            try:
                if self._colors.has_key(value):
                    self.color = value
                else:
                    intRepr = int(value)
                    if intRepr >= len(self._colors.keys()):
                        raise
                    else:
                        self.color = intRepr
            except:
                SetItemError(self.__class__,name,value)
        else:
            AttrError(self.__class__,name)

    def repr(self, orientation, alt=''):
        lines = []

        lines.append('@    ' + alt+orientation +'axis  ticklabel '  + str(self.onoff))
        lines.append('@    ' + alt+orientation +'axis  ticklabel format '  + str(self.format))
        lines.append('@    ' + alt+orientation +'axis  ticklabel prec '  + str(self.prec))
        lines.append('@    ' + alt+orientation +'axis  ticklabel formula "%s"'  % self.formula)
        lines.append('@    ' + alt+orientation +'axis  ticklabel append "%s"' % self.append)
        lines.append('@    ' + alt+orientation +'axis  ticklabel prepend "%s"' % self.prepend)
        lines.append('@    ' + alt+orientation +'axis  ticklabel angle '  + str(self.angle))
        lines.append('@    ' + alt+orientation +'axis  ticklabel skip '  + str(self.skip))
        lines.append('@    ' + alt+orientation +'axis  ticklabel stagger '  + str(self.stagger))
        lines.append('@    ' + alt+orientation +'axis  ticklabel place '  + str(self.place))
        lines.append('@    ' + alt+orientation +'axis  ticklabel offset '  + str(self.offset1))
        lines.append('@    ' + alt+orientation +'axis  ticklabel offset '  + str(self.offset2)[1:-1])
        lines.append('@    ' + alt+orientation +'axis  ticklabel start type '  + str(self.start_type))
        lines.append('@    ' + alt+orientation +'axis  ticklabel start '  + str(self.start))
        lines.append('@    ' + alt+orientation +'axis  ticklabel stop type '  + str(self.stop_type))
        lines.append('@    ' + alt+orientation +'axis  ticklabel stop '  + str(self.stop))
        lines.append('@    ' + alt+orientation +'axis  ticklabel char size '  + str(self.char_size))
        lines.append('@    ' + alt+orientation +'axis  ticklabel font %s' % 
                     (type(self.font)==str and ("\"%s\"" % self.font) or self.font));
        lines.append('@    ' + alt+orientation +'axis  ticklabel color %s' % 
                     (type(self.color)==str and ("\"%s\"" % self.color) or self.color));
        return lines
            
#---------------------------------------------------------------------
# Axis Class
#---------------------------------------------------------------------

class Axis:

    def __init__(self, colors, fonts,
                 scale='Normal',
                 invert='off',
                 onoff='on',
                 type_zero = 'false',
                 offset = (0.0,0.0),
                 bar = None,
                 label = None,
                 tick = None,
                 ticklabel = None,
                 orientation = 'x',
                 alt=None):

        self._colors = colors
        self._fonts = fonts
        self['scale'] = scale
        self['invert'] = invert
        self['onoff'] = onoff
        self['type_zero']=type_zero
        self['offset']=offset
        if alt:
            self['alt'] = 'alt'
            self['onoff'] = 'off'
        else:
            self['alt'] = ''
        if bar:
            self['bar'] = bar
        else:
            self['bar'] = XMG_Bar(self._colors) 
        if label:
            self['label']=label
        else:
            self['label']=XMG_Label(self._colors, self._fonts, XMG_String(self._colors, self._fonts,type='label'),layout='para',place='auto')
        if tick:
            self['tick'] = tick
        else:
            self['tick'] = XMG_Tick(self._colors)
        if ticklabel:
            self['ticklabel'] = ticklabel
        else:
            self['ticklabel'] = XMG_Ticklabel(self._colors,self._fonts)

        self['orientation']=orientation

    def __getitem__(self, name): return getattr(self, name)
    def __setitem__(self, name, value):

        if type(value) == str:
            value = value.replace('"','')

        if name == 'onoff':
            try: self.onoff = value
            except: SetItemError(self.__class__,name,value)
        elif name == 'scale':
            try: self.scale = value
            except: SetItemError(self.__class__,name,value)
        elif name == 'invert':
            try: self.invert = value
            except: SetItemError(self.__class__,name,value)
        elif name == 'type_zero':
            try: self.type_zero = value
            except: SetItemError(self.__class__,name,value)
        elif name == 'offset':
            try:
                if not type(value) == tuple:
                    raise
                else:
                    self.offset = value
            except: SetItemError(self.__class__,name,value)
        elif name =='bar':
            if not value.__class__ == XMG_Bar:
                SetItemError(self.__class__,name,value)
            else:
                self.bar = value
        elif name =='alt':
            self.alt = value
        elif name == 'label':
            if not value.__class__ == XMG_Label:
                SetItemError(self.__class__,name,value)
            else:
                self.label = value
        elif name == 'tick':
            if not value.__class__ == XMG_Tick:
                SetItemError(self.__class__,name,value)
            else:
                self.tick = value
        elif name == 'ticklabel':
            if not value.__class__ == XMG_Ticklabel:
                SetItemError(self.__class__,name,value)
            else:
                self.ticklabel = value
        elif name == 'orientation':
            #print value
            try: self.orientation = value
            except: SetItemError(self.__class__,name,value)
        else:
            AttrError(self.__class__,name)


    def __repr__(self):

        # count the number of special ticks
        spec = 0
        for spec_tick in self.tick.spec_ticks:
            if spec_tick[0]!="ticklabel":
                spec += 1

        alt=self.alt
        lines = []
        lines.append('@    '+self.orientation+'axes  scale ' + str(self['scale']))
        lines.append('@    '+self.orientation+'axes  invert ' + str(self['invert']))
        lines.append('@    '+alt+self.orientation+'axis  ' + str(self['onoff']))
        lines.append('@    '+alt+self.orientation+'axis  type zero ' + str(self['type_zero']))
        lines.append('@    '+alt+self.orientation+'axis  offset ' + str(self.offset)[1:-1])
        lines.extend(self.bar.repr(self.orientation, alt))
        lines.extend(self.label.repr(self.orientation, alt))
        lines.extend(self.tick.repr(self.orientation, alt))
        lines.extend(self.ticklabel.repr(self.orientation, alt))
        lines.append('@    '+alt+self.orientation+'axis  tick place ' + str(self.tick['place']))
        lines.append('@    '+alt+self.orientation+'axis  tick spec type ' + str(self.tick['spec_type']))
        lines.append('@    '+alt+self.orientation+'axis  tick spec ' + str(self.tick.spec))

        #-----special ticks-------#
        for item in self.tick.spec_ticks:
            if item[0] == 'ticklabel':
                lines.append('@    '+alt+self.orientation+'axis  ticklabel ' + str(item[1]) + ', "' + str(item[2]) +'"')
            else:
                lines.append('@    '+alt+self.orientation+'axis  tick ' + str(item[0]) + ' ' + str(item[1]) + ',' + str(item[2]))
        #-------------------------#

        
	return '\n'.join(lines)
        
# =============================================================== Test function
if __name__ == '__main__':
    print Axis(DEFAULT_COLORS,DEFAULT_FONTS)


