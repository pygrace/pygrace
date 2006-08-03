#!/usr/bin/env python
"""
Amaral Group
Northwestern University
4/11/2006

This module holds the Frame class that is used in the grace.py module.

"""

from fonts import DEFAULT_FONTS
from colors import DEFAULT_COLORS
from xmg_exceptions import SetItemError, AttrError

# ================= Frame class =================================
class Frame:
    
    """
    Frame class

    """
    def __init__(self,colors,fonts,
                 type = 0,
                 linestyle = 1,
                 linewidth = 1.0,
                 color = 'black',
                 pattern = 1,
                 background_color = 0,
                 background_pattern = 0
                 ):
        self._colors = colors
        self._fonts = fonts
        self['type'] = type
        self['linestyle'] = linestyle
        self['linewidth'] = linewidth
        self['color'] = color
        self['pattern'] = pattern
        self['background_color'] = background_color
        self['background_pattern'] = background_pattern

    # access class attributes like a dictionary
    def __getitem__(self, name): return getattr(self, name)


    #-----------------------------------#
    def __setitem__(self, name, value): 

        if type(value) == str:
            value = value.replace('"','')

        if name == 'type':
            try: self.type = int(value)  #what are the restrictions on this attr?      
            except: SetItemError(self.__class__,name,value)
        elif name == 'linestyle':
            try: self.linestyle = int(value)
            except: SetItemError(self.__class__,name,value)
        elif name == 'linewidth':
            try: self.linewidth = float(value)
            except: SetItemError(self.__class__,name,value)
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
                SetItemError(self.__class__,name, value)
        elif name == 'pattern':
            try: self.pattern = int(value)
            except: SetItemError(self.__class__,name,value)
        elif name == 'background_color':
            try:
                if self._colors.has_key(value):
                    self.background_color = value
                else:
                    intRepr = int(value)
                    if intRepr >= len(self._colors.keys()):
                        raise
                    else:
                        self.background_color = intRepr
            except:
                SetItemError(self.__class__,name, value)
        elif name == 'background_pattern':
            try: self.background_pattern = int(value)
            except: SetItemError(self.__class__,name,value)
        else:
            AttrError(self.__class__, name)


    #-----------------------------------#

    # print
    def __repr__(self):
	lines = []

        #color names need quotes around name (if not represented by int index):
        #and/or syntax used here works like: type(str)? "val" : val

        lines.append('@    frame type %s' % self.type)
        lines.append('@    frame linestyle %s' % self.linestyle)
        lines.append('@    frame linewidth %.01f' % self.linewidth)
        lines.append('@    frame color %s' %
                     (type(self.color)==str and ("\"%s\"" % self.color) or self.color))
        lines.append('@    frame pattern %s' % self.pattern)
        lines.append('@    frame background color %s' %
                     (type(self.background_color)==str and ("\"%s\"" % self.background_color) or self.background_color))
        lines.append('@    frame background pattern %s' %
                     self.background_pattern)
        
	return '\n'.join(lines)


# =============================================================== Test function
if __name__ == '__main__':
    print Frame(DEFAULT_COLORS,DEFAULT_FONTS)
