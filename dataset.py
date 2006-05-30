#!/usr/bin/env python
"""
Amaral Group
Northwestern University

Major needed attributes

- symbol
- line
- fill
- avalue
- errorbar
- label (for legend)

"""

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
    def __init__(self,shape = 0,
                 size = 1.0,
                 color = 1,
                 pattern = 1,
                 fill_color = 1,
                 fill_pattern = 0,
                 linewidth = 1.0,
                 linestyle = 1,
                 char = 65,
                 char_font = 0,
                 skip = 0):
        self.shape = shape;
        self.size = size;
        self.color = color;
        self.pattern = pattern;
        self.fill_color = fill_color;
        self.fill_pattern = fill_pattern;
        self.linewidth = linewidth;
        self.linestyle = linestyle;
        self.char = char;
        self.char_font = char_font;
        self.skip = skip;

#---------------------------------------------------------------------------
# Line class
#---------------------------------------------------------------------------
class XMG_Line:
    """Line class for xmgrace dataset
    """

    # constructor
    def __init__(self,type = 1,
                 style = 1,
                 width = 1.0,
                 color = 1,
                 pattern = 1):
        self.type = type;
        self.style = style;
        self.width = width;
        self.color = color;
        self.pattern = pattern;

#---------------------------------------------------------------------------
# baseline class
#---------------------------------------------------------------------------
class XMG_Baseline:
    """Baseline class for xmgrace dataset.
    """

    # constructor
    def __init__(self,type = 0,
                 onoff="off"):
        self.type = type
        self.onoff = onoff;

#---------------------------------------------------------------------------
# Fill class
#---------------------------------------------------------------------------
class XMG_Fill:
    """Fill class for xmgrace dataset.
    """

    # constructor
    def __init__(self,type = 0,
                 rule = 0,
                 color = 1,
                 pattern = 1):
        self.type = type;
        self.rule = rule;
        self.color = color;
        self.pattern = pattern;

#---------------------------------------------------------------------------
# Annotated value class
#---------------------------------------------------------------------------
class XMG_AValue:
    """AValue (annotated value) class for xmgrace dataset.
    """

    # constructor
    def __init__(self,onoff = "off",
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
        self.onoff = onoff;
        self.type = type
        self.char_size = char_size;
        self.font = font;
        self.color = color;
        self.rot = rot;
        self.format = format;
        self.prec = prec;
        self.prepend = prepend;
        self.append = append;
        self.offset = offset

#---------------------------------------------------------------------------
# Errorbar class
#---------------------------------------------------------------------------
class XMG_ErrorBar:
    """Errorbar class for xmgrace dataset.
    """

    # constructor
    def __init__(self,onoff = "on",
                 place = "both",
                 color = 1,
                 pattern = 1,
                 size = 1.0,
                 linewidth = 1.0,
                 linestyle = 1,
                 riser_linewidth = 1.0,
                 riser_linestyle = 1,
                 riser_clip_onoff = "off",
                 riser_clip_length = 0.1):
        self.onoff = onoff;
        self.place = place;
        self.color = color;
        self.pattern = pattern;
        self.size = size;
        self.linewidth = linewidth;
        self.linestyle = linestyle;
        self.riser_linewidth = riser_linewidth;
        self.riser_linestyle = riser_linestyle;
        self.riser_clip_onoff = riser_clip_onoff;
        self.riser_clip_length = riser_clip_length;

#---------------------------------------------------------------------------
# Dataset class
#---------------------------------------------------------------------------
class DataSet:
    """

    """
    def __init__(self, data,
                 idNumber=-1,
                 hidden='false',
                 datatype='xy',
                 symbol=XMG_Symbol(),
                 line=XMG_Line(),
                 baseline=XMG_Baseline(),
                 dropline="off",
                 fill=XMG_Fill(),
                 avalue=XMG_AValue(),
                 errorbar=XMG_ErrorBar(),
                 comment='',
                 legend=''):
        self.data = data;
        self.idNumber = idNumber
        self.hidden = hidden
        self.datatype = datatype
        self.symbol = symbol
        self.line = line
        self.baseline = baseline
        self.dropline = dropline
        self.fill = fill
        self.avalue = avalue
        self.errorbar = errorbar
        self.comment = comment
        self.legend = legend

    def __getitem__(self, name): return getattr(self, name)
    def __setitem__(self, name, value): setattr(self, name, value)

    def __repr__(self):
        lines = []

        lines.append('@    s' + str(self.idNumber) + ' hidden ' + str(self.hidden));
        lines.append('@    s' + str(self.idNumber) + ' type ' + str(self.datatype));
        lines.append('@    s' + str(self.idNumber) + ' symbol ' + str(self.symbol.shape));
        lines.append('@    s' + str(self.idNumber) + ' symbol size ' + str(self.symbol.size));
        lines.append('@    s' + str(self.idNumber) + ' symbol color ' + str(self.symbol.color));
        lines.append('@    s' + str(self.idNumber) + ' symbol pattern ' + str(self.symbol.pattern));
        lines.append('@    s' + str(self.idNumber) + ' symbol fill color ' + str(self.symbol.fill_color));
        lines.append('@    s' + str(self.idNumber) + ' symbol fill pattern ' + str(self.symbol.fill_pattern));
        lines.append('@    s' + str(self.idNumber) + ' symbol linewidth ' + str(self.symbol.linewidth));
        lines.append('@    s' + str(self.idNumber) + ' symbol linestyle ' + str(self.symbol.linestyle));
        lines.append('@    s' + str(self.idNumber) + ' symbol char ' + str(self.symbol.char));
        lines.append('@    s' + str(self.idNumber) + ' symbol char font ' + str(self.symbol.char_font));
        lines.append('@    s' + str(self.idNumber) + ' symbol skip ' + str(self.symbol.skip));
        lines.append('@    s' + str(self.idNumber) + ' line type ' + str(self.line.type));
        lines.append('@    s' + str(self.idNumber) + ' line linestyle ' + str(self.line.style));
        lines.append('@    s' + str(self.idNumber) + ' line linewidth ' + str(self.line.width));
        lines.append('@    s' + str(self.idNumber) + ' line color ' + str(self.line.color));
        lines.append('@    s' + str(self.idNumber) + ' line pattern ' + str(self.line.pattern));
        lines.append('@    s' + str(self.idNumber) + ' baseline type ' + str(self.baseline.type));
        lines.append('@    s' + str(self.idNumber) + ' baseline ' + str(self.baseline.onoff));
        lines.append('@    s' + str(self.idNumber) + ' dropline ' + str(self.dropline));
        lines.append('@    s' + str(self.idNumber) + ' fill type ' + str(self.fill.type));
        lines.append('@    s' + str(self.idNumber) + ' fill rule ' + str(self.fill.rule));
        lines.append('@    s' + str(self.idNumber) + ' fill color ' + str(self.fill.color));
        lines.append('@    s' + str(self.idNumber) + ' fill pattern ' + str(self.fill.pattern));
        lines.append('@    s' + str(self.idNumber) + ' avalue ' + str(self.avalue.onoff));
        lines.append('@    s' + str(self.idNumber) + ' avalue type ' + str(self.avalue.type));
        lines.append('@    s' + str(self.idNumber) + ' avalue char size ' + str(self.avalue.char_size));
        lines.append('@    s' + str(self.idNumber) + ' avalue font ' + str(self.avalue.font));
        lines.append('@    s' + str(self.idNumber) + ' avalue color ' + str(self.avalue.color));
        lines.append('@    s' + str(self.idNumber) + ' avalue rot ' + str(self.avalue.rot));
        lines.append('@    s' + str(self.idNumber) + ' avalue format ' + str(self.avalue.format));
        lines.append('@    s' + str(self.idNumber) + ' avalue prec ' + str(self.avalue.prec));
        lines.append('@    s' + str(self.idNumber) + ' avalue prepend "' + str(self.avalue.prepend) + '"');
        lines.append('@    s' + str(self.idNumber) + ' avalue append "' + str(self.avalue.append) + '"');
        lines.append('@    s' + str(self.idNumber) + ' avalue offset ' + str(self.avalue.offset)[1:-1]);
        lines.append('@    s' + str(self.idNumber) + ' errorbar ' + str(self.errorbar.onoff));
        lines.append('@    s' + str(self.idNumber) + ' errorbar place ' + str(self.errorbar.place));
        lines.append('@    s' + str(self.idNumber) + ' errorbar color ' + str(self.errorbar.color));
        lines.append('@    s' + str(self.idNumber) + ' errorbar pattern ' + str(self.errorbar.pattern));
        lines.append('@    s' + str(self.idNumber) + ' errorbar size ' + str(self.errorbar.size));
        lines.append('@    s' + str(self.idNumber) + ' errorbar linewidth ' + str(self.errorbar.linewidth));
        lines.append('@    s' + str(self.idNumber) + ' errorbar linestyle ' + str(self.errorbar.linestyle));
        lines.append('@    s' + str(self.idNumber) + ' errorbar riser linewidth ' + str(self.errorbar.riser_linewidth));
        lines.append('@    s' + str(self.idNumber) + ' errorbar riser linestyle ' + str(self.errorbar.riser_linestyle));
        lines.append('@    s' + str(self.idNumber) + ' errorbar riser clip ' + str(self.errorbar.riser_clip_onoff));
        lines.append('@    s' + str(self.idNumber) + ' errorbar riser clip length ' + str(self.errorbar.riser_clip_length));
        lines.append('@    s' + str(self.idNumber) + ' comment "' + str(self.comment) + '"');
        lines.append('@    s' + str(self.idNumber) + ' legend "' + str(self.legend) + '"');        
	return '\n'.join(lines)

    def _repr_data(self):
        if self.datatype=='xy':
            lines = [str(self.data[i][0]) + ' ' + str(self.data[i][1]) \
                     for i in range(len(self.data))];
        else:
            lines = [];
            
        return '\n'.join(lines)

# =============================================================== Test function
if __name__ == '__main__':
    print DataSet()


