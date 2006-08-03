#!/usr/bin/env python
"""
Amaral Group
Northwestern University
6/26/2006

This module holds the Legend class that is used in the grace.py module.

"""

import sys
from colors import DEFAULT_COLORS
from fonts import DEFAULT_FONTS
from xmg_exceptions import SetItemError, AttrError



# ================= Legend class =================================

class Legend:

    """
    Legend class
    """
    def __init__(self,colors,fonts,
                 onoroff = 'on',      #must be 'on' or 'off'
                 loctype = 'view',    #must be 'view' or 'world'
                 loc = (0.85,0.75),   #coordinates by upper left corner
                 box_color = 1,
                 box_pattern =  1,
                 box_linewidth = 1.0,
                 box_linestyle = 1,
                 box_fill_color = 0,
                 box_fill_pattern = 1,
                 font = "Helvetica",
                 char_size = 1.00,
                 color = 1,
                 length = 3,
                 vgap = 1,
                 hgap = 1,
                 invert = 'false'):
        self._colors = colors     # local copy of global colors dictionary
        self._fonts = fonts       # local copy of global fonts dictionary
        self['onoroff'] = onoroff
        self['loctype'] = loctype
        self['loc'] = loc
        self['box_color'] = box_color
        self['box_pattern'] = box_pattern
        self['box_linewidth'] = box_linewidth
        self['box_linestyle'] = box_linestyle
        self['box_fill_color'] = box_fill_color
        self['box_fill_pattern'] = box_fill_pattern
        self['font'] = font
        self['char_size'] = char_size
        self['color'] = color
        self['length'] = length
        self['vgap'] = vgap
        self['hgap'] = hgap
        self['invert'] = invert
      
    # access class attributes like a dictionary
    def __getitem__(self, name): return getattr(self, name)

    ##----------------------------------##
    def __setitem__(self, name, value):

        if type(value) == str:
            value = value.replace('"','')

        if name == 'onoroff': #legend on or off
            try:
                if not (value == 'on' or value == 'off'):
                    raise
                else:
                    self.onoroff = value
            except: SetItemError(self.__class__,name,value)

        elif name == 'loctype': #location type
            try:
                if not (value == 'view' or value == 'world'):
                    raise
                else:
                    self.loctype = value
            except: SetItemError(self.__class__,name,value)
                
        elif name == 'loc': #location coordinates
            try: self.loc = (float(value[0]),float(value[-1]))
            except: SetItemError(self.__class__,name,value)

        elif name == 'box_color': #box color
            try:
                if self._colors.has_key(value):
                    self.box_color = value
                else:
                    intRepr = int(value)
                    if intRepr >= len(self._colors.keys()):
                        sys.stderr.write("---------------->  " + str((self._colors.keys()))+'\n')
                        raise
                    else:
                        self.box_color = int(value)
            except:
               SetItemError(self.__class__,name, value)
                
        elif name == 'box_pattern': #box pattern
            try: self.box_pattern = int(value)
            except: SetItemError(self.__class__,name, value)

        elif name == 'box_linewidth': #box line width
            try: self.box_linewidth = float(value)
            except: SetItemError(self.__class__,name, value)

        elif name == 'box_linestyle': #box line style
            try: self.box_linestyle = int(value)
            except: SetItemError(self.__class__,name, value)
            
        elif name == 'box_fill_color': #box fill color
            try:
                if self._colors.has_key(value):
                    self.box_fill_color = value
                else:
                    intRepr = int(value)
                    if intRepr >= len(self._colors.keys()):
                        raise
                    else:
                        self.box_fill_color = intRepr
            except:
                SetItemError(self.__class__,name, value)
                
        elif name == 'box_fill_pattern': #box fill pattern
            try: self.box_fill_pattern = int(value)
            except: SetItemError(self.__class__,name, value)
            
        elif name == 'font': #font
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

        elif name == 'char_size': #char size
            try: self.char_size = float(value)
            except: SetItemError(self.__class__,name, value)
            
        elif name == 'color': #color
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
                
        elif name == 'length': #length
            try: self.length = int(value);
            except: SetItemError(self.__class__,name, value)
            
        elif name=="vgap": #vgap
            try: self.vgap = int(value);
            except: SetItemError(self.__class__,name, value)
            
        elif name == 'hgap':  #hgap
            try: self.hgap = int(value);
            except: SetItemError(self.__class__,name, value)
            
        elif name=="invert": #inverted?
            try:
                if not (value == "true" or value == "false"):
                    raise
                else:
                    self.invert = value;
            except: SetItemError(self.__class__,name, value)
        else:
            AttrError(self.__class__,name)
            
    ##-------------------------------------##

    # print
    def __repr__(self):
	lines = []

        #color and font names need quotes around name (if not represented by int index):
        #and/or syntax used here works like: type(str)? "val" : val
        

        lines.append('@    legend %s' % self.onoroff)
        lines.append('@    legend loctype %s' % self.loctype)
        lines.append('@    legend %.8f, %.8f' % (self.loc[0],self.loc[1]))
        lines.append('@    legend box color %s' %             
                     (type(self.box_color)==str and ("\"%s\"" % self.box_color) or self.box_color))
        lines.append('@    legend box linewidth %s' % self.box_linewidth)
        lines.append('@    legend box linestyle %s' % self.box_linestyle)
        lines.append('@    legend box fill color %s' %
                     (type(self.box_fill_color)==str and ("\"%s\"" % self.box_fill_color) or self.box_fill_color))
        lines.append('@    legend box fill pattern %s' % self.box_fill_pattern)
        lines.append('@    legend font  %s' % 
                     (type(self.font)==str and ("\"%s\"" % self.font) or self.font))
        lines.append('@    legend char size  %.8f' % self.char_size)
        lines.append('@    legend color %s' %  
                     (type(self.color)==str and ("\"%s\"" % self.color) or self.color))
        lines.append('@    legend length %s' % self.length)
        lines.append('@    legend vgap %s' % self.vgap)
        lines.append('@    legend hgap %s' %  self.hgap)
        lines.append('@    legend invert %s' % self.invert)
        
	return '\n'.join(lines)

# =============================================================== Test function
if __name__ == '__main__':
    
    print Legend(DEFAULT_COLORS,DEFAULT_FONTS)                                                                                                   
