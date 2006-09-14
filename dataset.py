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

#---------------------------------------------------------------------------
# Symbol class
#---------------------------------------------------------------------------
class XMG_Symbol:
    """Symbol class for xmgrace dataset
    """

    # constructor
    def __init__(self, colors, fonts,
                 shape = 'None',
                 size = 1.0,
                 color = 3,
                 pattern = 1,
                 fill_color = 1,
                 fill_pattern = 0,
                 linewidth = 1.0,
                 linestyle = 1,
                 char = 65,
                 char_font = 0,
                 skip = 0):
        self._colors = colors
        self._fonts = fonts
        self['shape'] = shape;
        self['size'] = size;
        self['color'] = color;
        self['pattern'] = pattern;
        self['fill_color'] = fill_color;
        self['fill_pattern'] = fill_pattern;
        self['linewidth'] = linewidth;
        self['linestyle'] = linestyle;
        self['char'] = char;
        self['char_font'] = char_font;
        self['skip'] = skip;

    def __getitem__(self, name): return getattr(self, name)
    def __setitem__(self, name, value):

        if type(value) == str:
            value = value.replace('"','')
        
        if name == 'shape':
            try:
                if shapes.has_key(value):
                    self.shape = shapes[value]
                else:
                    self.shape = int(value)
            except: SetItemError(self.__class__, name, value)
            
        elif name == 'size':
            try: self.size = float(value)
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
                        self.color = intRepr
            except:
                SetItemError(self.__class__,name,value)

        elif name == 'pattern':
            try: self.pattern = int(value)
            except: SetItemError(self.__class__,name,value)

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
                SetItemError(self.__class__,name,value)

        elif name == 'fill_pattern':
            try: self.fill_pattern = int(value)
            except: SetItemError(self.__class__,name,value)

        elif name == 'linewidth':
            try: self.linewidth = float(value)
            except: SetItemError(self.__class__,name, value)

        elif name == 'linestyle':
            try:
                if linestyles.has_key(value):
                    self.linestyle = linestyles[value]
                else:
                    self.linestyle = int(value)
            except: SetItemError(self.__class__, name, value)
            
        elif name == 'char':
            try: self.char = int(value)
            except: SetItemError(self.__class__,name, value)
            
        elif name == 'char_font':
            try:
                if self._fonts.has_key(value):
                    self.char_font = value
                else:
                    intRepr = int(value)
                    if intRepr >= len(self._fonts.keys()):
                        raise
                    else:
                        self.char_font = intRepr
            except: SetItemError(self.__class__,name, value)
            
        elif name == 'skip':
            try: self.skip = int(value)
            except: SetItemError(self.__class__,name, value)

        else:
            AttrError(self.__class__, name)

    def repr(self, id):

        lines = []

        lines.append('@    s' + str(id) + ' symbol ' + str(self.shape));
        lines.append('@    s' + str(id) + ' symbol size ' + str(self.size));
        lines.append('@    s' + str(id) + ' symbol color %s' %
                     (type(self.color)==str and ("\"%s\"" % self.color) or self.color));
        lines.append('@    s' + str(id) + ' symbol pattern ' + str(self.pattern));
        lines.append('@    s' + str(id) + ' symbol fill color ' + str(self.fill_color));
        lines.append('@    s' + str(id) + ' symbol fill pattern ' + str(self.fill_pattern));
        lines.append('@    s' + str(id) + ' symbol linewidth ' + str(self.linewidth));
        lines.append('@    s' + str(id) + ' symbol linestyle ' + str(self.linestyle));
        lines.append('@    s' + str(id) + ' symbol char ' + str(self.char));
        lines.append('@    s' + str(id) + ' symbol char font %s' %
                     (type(self.char_font)==str and ("\"%s\"" % self.char_font) or self.char_font))
        lines.append('@    s' + str(id) + ' symbol skip ' + str(self.skip));
        return lines
#---------------------------------------------------------------------------
# Line class
#---------------------------------------------------------------------------
class XMG_Line:
    """Line class for xmgrace dataset
    """

    # constructor
    def __init__(self,colors, type = 1,
                 style = 1,
                 width = 1.0,
                 color = 1,
                 pattern = 1):
        self._colors = colors
        self['type'] = type;
        self['linestyle'] = style;
        self['linewidth'] = width;
        self['color'] = color;
        self['pattern'] = pattern;
        
    def __getitem__(self, name): return getattr(self, name)
    def __setitem__(self, name, value):

        if type(value) == str:
            value = value.replace('"','')
        
        if name == 'type':
            try:
                if linestyles.has_key(value):
                    self.type = linestyles[value]
                else:
                    self.type = int(value)
            except: SetItemError(self.__class__, name, value)

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
                
        elif name == 'pattern':
            try: self.pattern = int(value)
            except: SetItemError(self.__class__,name, value)
        else:
            AttrError(self.__class__, name)

    def repr(self,id):
        lines = []

        lines.append('@    s' + str(id) + ' line type ' + str(self.type));
        lines.append('@    s' + str(id) + ' line linestyle ' + str(self.linestyle));
        lines.append('@    s' + str(id) + ' line linewidth ' + str(self.linewidth));
        lines.append('@    s' + str(id) + ' line color %s' %
                     (type(self.color)==str and ("\"%s\"" % self.color) or self.color));
        lines.append('@    s' + str(id) + ' line pattern ' + str(self.pattern));
        return lines
    
#---------------------------------------------------------------------------
# baseline class
#---------------------------------------------------------------------------
class XMG_Baseline:
    """Baseline class for xmgrace dataset.
    """

    # constructor
    def __init__(self,type = 0,
                 onoff="off"):
        self['type'] = type
        self['onoff'] = onoff;

    def __getitem__(self, name): return getattr(self, name)
    def __setitem__(self, name, value):

        if type(value) == str:
            value = value.replace('"','')
        
        if name == 'type':
            try: self.type = int(value)
            except: SetItemError(self.__class__,name, value)
        elif name == 'onoff':
            try: self.onoff = value
            except: SetItemError(self.__class__,name, value)
        else:
            AttrError(self.__class__, name)

    def repr(self,id):
        lines = []
        lines.append('@    s' + str(id) + ' baseline type ' + str(self.type));
        lines.append('@    s' + str(id) + ' baseline ' + str(self.onoff));
        return lines

#---------------------------------------------------------------------------
# Fill class
#---------------------------------------------------------------------------
class XMG_Fill:
    """Fill class for xmgrace dataset.
    """

    # constructor
    def __init__(self, colors,
                 type = 0,
                 rule = 0,
                 color = 1,
                 pattern = 1):
        self._colors = colors
        self['type'] = type;
        self['rule'] = rule;
        self['color'] = color;
        self['pattern'] = pattern;
        
    def __getitem__(self, name): return getattr(self, name)
    def __setitem__(self, name, value):

        if type(value) == str:
            value = value.replace('"','')
        
        if name == 'type':
            try: self.type = int(value)
            except: SetItemError(self.__class__,name, value)
        elif name == 'rule':
            try: self.rule = int(value)
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
        elif name == 'pattern':
            try: self.pattern = int(value)
            except: SetItemError(self.__class__,name, value)
        else:
            AttrError(self.__class__, name)

    def repr(self,id):
        lines = []
        lines.append('@    s' + str(id) + ' fill type ' + str(self.type));
        lines.append('@    s' + str(id) + ' fill rule ' + str(self.rule));
        lines.append('@    s' + str(id) + ' fill color %s' %
                     (type(self.color)==str and ("\"%s\"" % self.color) or self.color))
        lines.append('@    s' + str(id) + ' fill pattern ' + str(self.pattern));
        return lines
#---------------------------------------------------------------------------
# Annotated value class
#---------------------------------------------------------------------------
class XMG_AValue:
    """AValue (annotated value) class for xmgrace dataset.
    """

    # constructor
    def __init__(self, colors, fonts,
                 onoff = "off",
                 type = 2,
                 char_size = 1.0,
                 font = 0,
                 color = 1,
                 rot = 0,
                 format = "general",
                 prec = 3,
                 prepend = '',
                 append = '',
                 offset = (0.0,0.0)):
        self._colors = colors
        self._fonts = fonts
        self['onoff'] = onoff;
        self['type'] = type
        self['char_size'] = char_size;
        self['font'] = font;
        self['color'] = color;
        self['rot'] = rot;
        self['format'] = format;
        self['prec'] = prec;
        self['prepend'] = prepend;
        self['append'] = append;
        self['offset'] = offset

    def __getitem__(self, name): return getattr(self, name)

    def __setitem__(self, name, value):

        if type(value) == str:
            value = value.replace('"','')
        
        if name == 'onoff':
            try: self.onoff = value
            except: SetItemError(self.__class__,name, value)

        elif name == 'type':
            try: self.type = int(value)
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
        
        elif name == 'rot':
            try: self.rot = int(value)
            except: SetItemError(self.__class__,name, value)

        elif name == 'format':
            try: self.format =  value #this needs to be restricted.  What are the 'formats'?
            except: SetItemError(self.__class__,name, value)

        elif name == 'prec':
            try: self.prec = int(value)
            except: SetItemError(self.__class__,name, value)

        elif name == 'prepend':
            try: self.prepend =  value 
            except: SetItemError(self.__class__,name, value)
            
        elif name == "append":
            try: self.append =  value 
            except: SetItemError(self.__class__,name, value)
            
        elif name == 'offset':
            try:
                if not type(value) == tuple:
                    raise
                else: self.offset = value
            except:
                SetItemError(self.__class__, name, value)

        else:
            AttrError(self.__class_, name)

    def repr(self,id):
        lines = []
        lines.append('@    s' + str(id) + ' avalue ' + str(self.onoff));
        lines.append('@    s' + str(id) + ' avalue type ' + str(self.type));
        lines.append('@    s' + str(id) + ' avalue char size ' + str(self.char_size));
        lines.append('@    s' + str(id) + ' avalue font %s' %
                     (type(self.font)==str and ("\"%s\"" % self.font) or self.font))
        lines.append('@    s' + str(id) + ' avalue color %s' %
                     (type(self.color)==str and ("\"%s\"" % self.color) or self.color))
        lines.append('@    s' + str(id) + ' avalue rot ' + str(self.rot));
        lines.append('@    s' + str(id) + ' avalue format ' + str(self.format));
        lines.append('@    s' + str(id) + ' avalue prec ' + str(self.prec));
        lines.append('@    s' + str(id) + ' avalue prepend "' + str(self.prepend) + '"');
        lines.append('@    s' + str(id) + ' avalue append "' + str(self.append) + '"');
        lines.append('@    s' + str(id) + ' avalue offset ' + str(self.offset)[1:-1]);
        return lines
#---------------------------------------------------------------------------
# Errorbar class
#---------------------------------------------------------------------------
class XMG_ErrorBar:
    """Errorbar class for xmgrace dataset.
    """

    # constructor
    def __init__(self, colors,
                 onoff = "on",
                 place = "both",
                 color = 1,
                 pattern = 1,
                 size = 1.0,
                 linewidth = 1.0,
                 linestyle = 1,
                 riser_linewidth = 1.0,
                 riser_linestyle = 1,
                 riser_clip = "off",
                 riser_clip_length = 0.1):
        self._colors = colors
        self['onoff'] = onoff;
        self['place'] = place;
        self['color'] = color;
        self['pattern'] = pattern;
        self['size'] = size;
        self['linewidth'] = linewidth;
        self['linestyle'] = linestyle;
        self['riser_linewidth'] = riser_linewidth;
        self['riser_linestyle'] = riser_linestyle;
        self['riser_clip'] = riser_clip;
        self['riser_clip_length'] = riser_clip_length;
        
    def __getitem__(self, name): return getattr(self, name)
    def __setitem__(self, name, value):

        if type(value) == str:
            value = value.replace('"','')

        if name == 'onoff':
            try: self.onoff = value
            except: SetItemError(self.__class__,name, value)
        elif name == 'place':
            try: self.place = value #what are valid options for place attribute?
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
        elif name == 'pattern':
            try: self.pattern = int(value)
            except: SetItemError(self.__class__,name, value)

        elif name == 'size':
            try: self.size = float(value)
            except: SetItemError(self.__class__,name, value)
        elif name == 'linewidth':
            try: self.linewidth = float(value)
            except: SetItemError(self.__class__,name, value)
        elif name == 'linestyle':
            try:
                if linestyles.has_key(value):
                    self.linestyle = value
                else:
                    self.linestyle = int(value)
            except: SetItemError(self.__class__, name, value)
            
        elif name == 'riser_linewidth':
            try: self.riser_linewidth = float(value)
            except: SetItemError(self.__class__,name, value)
        elif name == 'riser_linestyle':
            try:
                if linestyles.has_key(value):
                    self.riser_linestyle = value
                else:
                    self.riser_linestyle = int(value)
            except: SetItemError(self.__class__, name, value)
            
        elif name == 'riser_clip':
            try: self.riser_clip = value
            except: SetItemError(self.__class__,name, value)
        elif name == 'riser_clip_length':
            try: self.riser_clip_length = float(value)
            except: SetItemError(self.__class__,name, value)
        else:
            AttrError(self.__class__, name)

    def repr(self,id):
        lines = []
        lines.append('@    s' + str(id) + ' errorbar ' + str(self.onoff));
        lines.append('@    s' + str(id) + ' errorbar place ' + str(self.place));
        lines.append('@    s' + str(id) + ' errorbar color %s' %
                     (type(self.color)==str and ("\"%s\"" % self.color) or self.color))  
        lines.append('@    s' + str(id) + ' errorbar pattern ' + str(self.pattern));
        lines.append('@    s' + str(id) + ' errorbar size ' + str(self.size));
        lines.append('@    s' + str(id) + ' errorbar linewidth ' + str(self.linewidth));
        lines.append('@    s' + str(id) + ' errorbar linestyle ' + str(self.linestyle));
        lines.append('@    s' + str(id) + ' errorbar riser linewidth ' + str(self.riser_linewidth));
        lines.append('@    s' + str(id) + ' errorbar riser linestyle ' + str(self.riser_linestyle));
        lines.append('@    s' + str(id) + ' errorbar riser clip ' + str(self.riser_clip));
        lines.append('@    s' + str(id) + ' errorbar riser clip length ' + str(self.riser_clip_length));
        
        return lines
#---------------------------------------------------------------------------
# Dataset class
#---------------------------------------------------------------------------
class DataSet:
    """

    """
    def __init__(self, data, colors, fonts,
                 idNumber=-1,
                 hidden='false',
                 type='xy',
                 symbol=None,
                 line=None,
                 baseline=XMG_Baseline(),
                 dropline="off",
                 fill=None,
                 avalue=None,
                 errorbar=None,
                 comment='',
                 legend=''):
        self._colors = colors
        self._fonts = fonts
        self['data'] = data;
        self['idNumber'] = idNumber
        self['hidden'] = hidden
        self['type'] = type
        self['baseline'] = baseline
        self['dropline'] = dropline
        self['comment'] = comment
        if not legend:
            self['legend'] = ''
        else:
            self['legend'] = legend
        #-----------------#
        if symbol:
            self.symbol = symbol
        else:
            self.symbol = XMG_Symbol(colors,fonts)
        if line:
            self.line = line
        else:
            self.line = XMG_Line(colors)
        if fill:
            self.fill = fill
        else:
            self.fill = XMG_Fill(colors)
        if avalue:
            self.avalue = avalue
        else:
            self.avalue = XMG_AValue(colors,fonts)
        if errorbar:
            self.errorbar = errorbar
        else:
            self.errorbar = XMG_ErrorBar(colors)

        #-----------------#

    def __getitem__(self, name): return getattr(self, name)
    def __setitem__(self, name, value):

        if type(value) == str:
            value = value.replace('"','')
            
            
        if name == 'data':
            if not type(value) == list:
                SetItemError(self.__class__, name, value)
            else:
                self.data = value
        elif name == 'idNumber':
            try: self.idNumber = int(value)
            except: SetItemError(self.__class__, name, value)
        elif name == 'hidden':
            if not (value == 'true' or value == 'false'):
                SetItemError(self.__class__, name, value)
            else:
                self.hidden = value
        elif name == 'type':
            try: self.type = value
            except: SetItemError(self.__class__, name, value)
        elif name == 'dropline':
            if not (value == 'on' or value == 'off'):
                SetItemError(self.__class__, name, value)
            else:
                self.dropline = value
        elif name == 'comment':
            try: self.comment = value
            except: SetItemError(self.__class__, name, value)
        elif name == 'legend':
            try: self.legend = value
            except: SetItemError(self.__class__, name, value )
        #-----------------------------------------------------#
        elif name == 'symbol':
            if not value.__class__ == XMG_Symbol:
                SetItemError(self.__class__,name, value)
            else:
                self.symbol = value
        elif name == 'line':
            if not value.__class__ == XMG_Line:
                SetItemError(self.__class__,name, value)
            else:
                self.line = value
        elif name == 'baseline':
            if not value.__class__ == XMG_Baseline:
                SetItemError(self.__class__,name, value)
            else:
                self.baseline = value
        elif name == 'fill':
            if not value.__class__ == XMG_Fill:
                SetItemError(self.__class__,name, value)
            else:
                self.fill = value
        elif name == 'avalue':
            if not value.__class__ == XMG_AValue:
                print type(value)
                SetItemError(self.__class__,name, value)
            else:
                self.avalue = value
        elif name == 'errorbar':
            if not value.__class__ == XMG_ErrorBar:
                SetItemError(self.__class__,name, value)
            else:
                self.errorbar = value
        #------------------------------------------------------#
        else:
            AttrError(self.__class__,name)
            
   #-----------------------------------------------------------#       

    def __repr__(self):
        lines = []

        lines.append('@    s' + str(self.idNumber) + ' hidden ' + str(self.hidden));
        lines.append('@    s' + str(self.idNumber) + ' type ' + str(self.type));

        lines.extend(self.symbol.repr(self.idNumber)) #XMG_Symbol

        lines.extend(self.line.repr(self.idNumber))   #XMG_Line

        lines.extend(self.baseline.repr(self.idNumber)) #XMG_Baseline

        lines.append('@    s' + str(self.idNumber) + ' dropline ' + str(self.dropline));

        lines.extend(self.fill.repr(self.idNumber)) #XMG_Fill

        lines.extend(self.avalue.repr(self.idNumber)) #XMG_AValue

        lines.extend(self.errorbar.repr(self.idNumber)) #XMG_ErrorBar

        lines.append('@    s' + str(self.idNumber) + ' comment "' + str(self.comment) + '"');
        lines.append('@    s' + str(self.idNumber) + ' legend "' + str(self.legend) + '"');        
	return '\n'.join(lines)

    def _repr_data(self):
        #datum = []
        #lines = []
        if self.type[:2]=='xy' or self.type[:3] =='bar': #any xy or bar data type                                                  

            lines = [' '.join(map(str,self.data[i])) for i in range(len(self.data))];

        else: #not yet supported
            lines = [];

        lines.append('&') #marker for end of dataset
        
        return '\n'.join(lines)

# =============================================================== Test function
if __name__ == '__main__':
    d = DataSet(None,DEFAULT_COLORS,DEFAULT_FONTS)
    d['idNumber'] = 1
    d['avalue']['char_size'] = 2.1
    print d
    

