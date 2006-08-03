#!/usr/bin/env python
"""
Amaral Group
Northwestern University
4/5/2006

This module contains the Timestamp class, to be used in grace.py.
"""

import time
from colors import DEFAULT_COLORS
from fonts import DEFAULT_FONTS

from xmg_exceptions import SetItemError, AttrError

# ============================================================= Timestamp class
class Timestamp:
    """Timestamp class

    This is used to output a timestamp to an xmgrace file.

    Example:

    >> a = Timestamp()
    >> a['onoroff'] = 'on'
    >> a['color'] = 'blue'
    >> a['angle'] = 15
    >> print a

    @timestamp on
    @timestamp 0.03, 0.03
    @timestamp color \"blue\"
    @timestamp rot 15
    @timestamp font \"Helvetica\"
    @timestamp char size 1.000000
    @timestamp def \"Thu Apr  6 14:38:47 2006\"
    """
    def __init__(self, colors=DEFAULT_COLORS, fonts=DEFAULT_FONTS,
                 onoroff='off',
                 x = 0.03, y = 0.03,
                 color = 'black', font = 'Helvetica',
                 angle = 0, size = 1.0
                 ):
        
	# set defaults as class attributes

        self._colors = colors
        self._fonts = fonts

	self['onoff'] = onoroff
	self['x'], self['y'] = x, y
	self['color'] = color
	self['rot'] = angle
	self['font'] = font
	self['char_size'] = size

    # access class attributes like a dictionary
    def __getitem__(self, name): return getattr(self, name)
    def __setitem__(self, name, value):

        if type(value) == str:
            value = value.replace('"','')

        if name == 'onoff':
            try: self.onoff = value
            except: SetItemError(self.__class__,name,value)
        elif name == 'x':
            try: self.x = float(value)
            except: SetItemError(self.__class__,name,value)
        elif name == 'y':
            try: self.y = float(value)
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
                        self.color = int(value)
            except:
                SetItemError(self.__class__,name, value)
        elif name == 'rot':
            try: self.rot = float(value)
            except: SetItemError(self.__class__,name,value)
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

        elif name == 'char_size':
            try: self.size = float(value)
            except: SetItemError(self.__class__,name,value)
        else:
            AttrError(self.__class__,name)
            
	
    def _string_time(self):
        """_string_time() -> str

        Return a nicely formatted string with the time.
        """
	return time.ctime()

    def __repr__(self):
	lines = []
	
	lines.append('@timestamp %s' % self.onoff)
	lines.append('@timestamp %.02f, %.02f' % (self.x, self.y))
	lines.append('@timestamp color %s' %
                     (type(self.color)==str and ("\"%s\"" % self.color) or self.color))
	lines.append('@timestamp rot %s' % self.rot)
	lines.append('@timestamp font %s' %
                     (type(self.font)==str and ("\"%s\"" % self.font) or self.font))
	lines.append('@timestamp char size %.06f' % self.size)
	lines.append('@timestamp def "%s"' % self._string_time())
	
	return '\n'.join(lines)

        
# =============================================================== Test function
if __name__ == '__main__':
    a = Timestamp()

    a['onoroff'] = 'on'
    a['color'] = 'blue'
    a['angle'] = 15

    print a

