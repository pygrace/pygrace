#!/usr/bin/env python
"""
Amaral Group
Northwestern University

Generic xmgrace string class that only has 4 attributes:

-label
-font
-color
-size
-type  (this is used to discern between title or label type string, important for some outputs)

can be used as a whole or inherited from
"""
import sys

from xmg_exceptions import SetItemError,AttrError

class XMG_String:
    """

    """
    def __init__(self, colors, fonts,label='',font='Helvetica',
                 color='black',size=1.0,type='title'):
        self._colors = colors
        self._fonts = fonts
        self['font']=font
        self['color']=color
        self['size']=size
        self['label']=label
        self['type']=type

    def __getitem__(self, name): return getattr(self, name)

    #--------------------------------#
    def __setitem__(self, name, value):

        if type(value) == str and not name == 'label':
            value = value.replace('"','')

        if name == 'font':
            try:
                if self._fonts.has_key(value):
                    self.font = value
                else:
                    intRepr = int(value)
                    if intRepr >= len(self._fonts.keys()):
                        raise
                    else:
                        self.font = intRepr
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
                SetItemError(self.__class__,name,value)
        elif name == 'size':
            try: self.size = float(value)
            except: SetItemError(self.__class__,name,value)
        elif name == 'label':
            try: self.label = value
            except: SetItemError(self.__class__,name,value)
                
        elif name == 'type':
            try: self.type = value
            except: SetItemError(self.__class__,name,value)
        else:
            AttrError(self.__class__,name)
        

    #--------------------------------#  
    def contents(self,prefix):
        lines = []

        lines.append(prefix + ' "'+ str(self.label)+'"')
        lines.append(prefix + ' color %s' %
                     (type(self.color)==str and ("\"%s\"" % self.color) or self.color))
        if(self.type == 'title'):
            lines.append(prefix + ' size ' + str(self.size))

        if(self.type == 'label'):
            lines.append(prefix + ' char size ' + str(self.size))
        
        lines.append(prefix + ' font %s' %
                     (type(self.font)==str and ("\"%s\"" % self.font) or self.font))

        return '\n'.join(lines)




    """
    Strictly speaking, the __repr__ function should not be used from this class
    It is there for testing purposes but because of the variety of strings used
    In XMGrace, this class is merely an over-hyped dictionary for storing values
    """
    def __repr__(self):
        lines = []

        lines.append(str(self.label));
        lines.append('color ' + str(self.color));
        lines.append('size ' + str(self.size));
        lines.append('font ' + str(self.font));
	return '\n'.join(lines)
        
# =============================================================== Test function
if __name__ == '__main__':
    print XMG_String()


