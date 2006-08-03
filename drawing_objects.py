#!/usr/bin/env python
"""
Amaral Group
Northwestern University

All classes and data structures required for the dataset class.

"""

import sys
from xmg_exceptions import SetItemError,AttrError
from fonts import DEFAULT_FONTS
from colors import DEFAULT_COLORS

#-------------- Box Class ------------------#

class Box:

    def __init__(self, colors=DEFAULT_COLORS, fonts=DEFAULT_FONTS,
                 onoff = 'on',
                 loctype = 'view',
                 lowleft = (0,0),
                 upright = (1,1),
                 linestyle = 1,
                 linewidth = 2.0,
                 color = 1,
                 fill_color = 1,
                 fill_pattern = 1):
        self._colors = colors
        self._fonts = fonts
        self['onoff'] = onoff
        self['loctype'] = loctype
        self['lowleft'] = lowleft
        self['upright'] = upright
        self['linestyle'] = linestyle
        self['linewidth'] = linewidth
        self['color'] = color
        self['fill_color'] = fill_color
        self['fill_pattern'] = fill_pattern

    def __getitem__(self, name): return getattr(self, name)
    def __setitem__(self, name, value):

        if type(value) == str:
            value = value.replace('"','')

        if name == 'onoff':
            try: self.onoff = value
            except: SetItemError(self.__class__, name, value)
            
        elif name == 'loctype':
            try: self.loctype = value
            except: SetItemError(self.__class__, name, value)

        elif name == 'linestyle':
            try: self.linestyle = int(value)
            except: SetItemError(self.__class__, name, value)

        elif name == 'lowleft':
            try:
                if not type(value) == tuple:
                    raise
                else:
                    self.lowleft = value
            except: SetItemError(self.__class__, name, value)
                
        elif name == 'upright':
            try:
                if not type(value) == tuple:
                    raise
                else:
                    self.upright = value
            except: SetItemError(self.__class__, name, value)
            
        elif name == 'linewidth':
            try: self.linewidth = float(value)
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
                        self.color = int(value)
            except:
                SetItemError(self.__class__,name, value)
               
        elif name == 'fill_color': 
            try:
                if self._colors.has_key(value):
                    self.fill_color = value
                else:
                    intRepr = int(value)
                    if intRepr >= len(self._colors.keys()):
                        raise
                    else:
                        self.fill_color = intRepr
            except:
                SetItemError(self.__class__,name, value)
                
        elif name == 'fill_pattern': 
            try: self.fill_pattern = int(value)
            except: SetItemError(self.__class__,name, value)

        else:
            AttrError(self.__class__, name)

    def __repr__(self):
        
        lines = []

        lines.append('@with box')
        lines.append('@    box %s' % self.onoff)
        lines.append('@    box loctype %s' % self.loctype)
        lines.append('@    box %.8f, %.8f, %.8f, %.8f' % (self.lowleft[0],self.lowleft[1],
                                                          self.upright[0],self.upright[1]))
        lines.append('@    box linestyle %s' % self.linestyle)
        lines.append('@    box linewidth %s' % self.linewidth)
        lines.append('@    box color %s' %             
                     (type(self.color)==str and ("\"%s\"" % self.color) or self.color))
        lines.append('@    box fill color %s' %             
                     (type(self.fill_color)==str and ("\"%s\"" % self.fill_color) or self.fill_color))
        lines.append('@    box fill pattern %s' % self.fill_pattern)
        lines.append('@box def')

        return '\n'.join(lines)
            
            
#-------------- String Class ------------------#

class Text:

    def __init__(self, colors=DEFAULT_COLORS, fonts=DEFAULT_FONTS,
                 onoff = 'on',
                 loctype = 'view',
                 x = 0,
                 y = 0,
                 color = 1,
                 rot = 0,
                 font = 1,
                 just = 10, #?
                 char_size = 1.0,
                 text = ""):
        self._colors = colors
        self._fonts = fonts
        self['onoff'] = onoff
        self['loctype'] = loctype
        self['x'] = x
        self['y'] = y 
        self['color'] = color
        self['rot'] = rot
        self['font'] = font 
        self['just'] = just
        self['char_size'] = char_size
        self['text'] = text

    def __getitem__(self, name): return getattr(self, name)
    def __setitem__(self, name, value):

        if type(value) == str and not name == 'text':
            value = value.replace('"','')
            
        if name == 'onoff':
            try: self.onoff = value
            except: SetItemError(self.__class__, name, value)
            
        elif name == 'loctype':
            try: self.loctype = value
            except: SetItemError(self.__class__, name, value)

        elif name == 'x':
            try: self.x = float(value)
            except: SetItemError(self.__class__, name, value)
            
        elif name == 'y':
            try: self.y = float(value)
            except: SetItemError(self.__class__, name, value)

        elif name == 'color':
            try:
                if self._colors.has_key(value):
                    self.color = value
                else:
                    intRepr = int(value)
                    if intRepr >= len(self._colors.keys()):
                        raise
                    else:
                        self.color = int(value)
            except:
               SetItemError(self.__class__,name, value)

        elif name == 'rot':
            try: self.rot = int(value)
            except: SetItemError(self.__class__, name, value)

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

        elif name == 'just':
           try: self.just = int(value)
           except: SetItemError(self.__class__, name, value)

        elif name == 'char_size':
            try: self.char_size = float(value)
            except: SetItemError(self.__class__, name, value)

        elif name == 'text':
            try: self.text = value
            except: SetItemError(self.__class__, name, value)
        else:
            AttrError(self.__class__,name)

    def __repr__(self):
        
        lines = []

        lines.append('@with string')
        lines.append('@    string %s' % self.onoff)
        lines.append('@    string loctype %s' % self.loctype)
        lines.append('@    string %.8f, %.8f' % (self.x,self.y))
        lines.append('@    string color %s' %             
                     (type(self.color)==str and ("\"%s\"" % self.color) or self.color))
        lines.append('@    string rot %s' % self.rot)
        lines.append('@    string font %s' %
                     (type(self.font)==str and ("\"%s\"" % self.font) or self.font))
        lines.append('@    string rot %s' % self.rot)
        lines.append('@    string just %s' % self.just)
        lines.append('@    string char size %s' % self.char_size)
        lines.append('@    string def "%s"' % self.text)

        return '\n'.join(lines)
        
#-------------- Line Class ------------------#

class Line:
    def __init__(self, colors=DEFAULT_COLORS, fonts=DEFAULT_FONTS,
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
                 arrow_layout = (1.0,1.0)):
        self._colors = colors
        self._fonts = fonts
        self['onoff'] = onoff
        self['loctype'] = loctype
        self['start'] = start
        self['end'] = end
        self['linestyle'] = linestyle
        self['linewidth'] = linewidth
        self['color'] = color
        self['arrow'] = arrow
        self['arrow_type'] = arrow_type 
        self['arrow_length'] = arrow_length
        self['arrow_layout'] = arrow_layout
        

    def __getitem__(self, name): return getattr(self, name)
    def __setitem__(self, name, value):
        
        if type(value) == str:
            value = value.replace('"','')
            
        if name == 'onoff':
            try: self.onoff = value
            except: SetItemError(self.__class__, name, value)
                
        elif name == 'loctype':
            try: self.loctype = value
            except: SetItemError(self.__class__, name, value)

        elif name == 'linestyle':
            try: self.linestyle = int(value)
            except: SetItemError(self.__class__, name, value)

        elif name == 'start':
            try:
                if not type(value) == tuple:
                    raise
                else:
                    self.start = value
            except: SetItemError(self.__class__, name, value)
                
        elif name == 'end':
            try:
                if not type(value) == tuple:
                    raise
                else:
                    self.end = value
            except: SetItemError(self.__class__, name, value)
            
        elif name == 'linewidth':
            try: self.linewidth = float(value)
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
                        self.color = int(value)
            except:
                SetItemError(self.__class__,name, value)
               
        elif name == 'arrow':
            try: self.arrow = int(value)
            except: SetItemError(self.__class__, name, value)
            
        elif name == 'arrow_type':
            try: self.arrow_type = int(value)
            except: SetItemError(self.__class__, name, value)

        elif name == 'arrow_length':
            try: self.arrow_length = float(value)
            except: SetItemError(self.__class__, name, value)

        elif name == 'arrow_layout':
            try:
                if not type(value) == tuple:
                    raise
                else:
                    self.arrow_layout = value
            except: SetItemError(self.__class__, name, value)
            
        else:
            AttrError(self.__class__, name)

    def __repr__(self):
        
        lines = []

        lines.append('@with line')
        lines.append('@    line %s' % self.onoff)
        lines.append('@    line loctype %s' % self.loctype)
        lines.append('@    line %.8f, %.8f, %.8f, %.8f' % (self.start[0],self.start[1],
                                                          self.end[0],self.end[1]))
        lines.append('@    line linestyle %s' % self.linestyle)
        lines.append('@    line linewidth %s' % self.linewidth)
        lines.append('@    line color %s' %             
                     (type(self.color)==str and ("\"%s\"" % self.color) or self.color))
        lines.append('@    line arrow %s' % self.arrow)
        lines.append('@    line arrow type %s' % self.arrow_type)
        lines.append('@    line arrow length %s' % self.arrow_length)
        
        lines.append('@    line arrow layout %.8f, %.8f' % (self.arrow_layout[0], self.arrow_layout[1]))
        lines.append('@line def')

        return '\n'.join(lines)



#-------------- Ellipse Class ------------------#

#NOT IMPLEMENTED

class Ellipse:
    pass
