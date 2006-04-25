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


class Symbol:
    """Symbol class for xmgrace dataset
    """

    # constructor
    def __init__(self,shape = 0,
                 size = 1.0,
                 color = 1,
                 pattern = 1,
                 linewidth = 1.0,
                 linestyle = 1,
                 char = 65,
                 char_font = 0,
                 skip = 0):
        self.shape = shape;
        self.size = size;
        self.color = color;
        self.pattern = pattern;
        self.linewidth = linewidth;
        self.linestyle = linestyle;
        self.char = char;
        self.char_font = char_font;
        self.skip = skip;

class Line:
    """Line class for xmgrace dataset
    """

    # constructor
    def __init__(self,type = 1,
                 linestyle = 1,
                 linewidth = 1.0,
                 color = 1,
                 pattern = 1):
        self.type = type;
        self.linestyle = linestyle;
        self.linewidth = linewidth;
        self.color = color;
        self.pattern = pattern;

      
class DataSet:
    """

    """
    def __init__(self, idNumber=-1,
                 hidden='false',
                 datatype='xy',
                 symbol=xmgSymbol,
                 line=xmgLine,
                 baseline=xmgBaseline,
                 dropline=xmgDropline,
                 fill=xmgFill,
                 avalue=xmgAvalue,
                 errorbar=xmgErrorbar,
                 comment='',
                 legend=''):
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

        lines.append('@     s' + str(self.idNumber) + ' hidden ' + str(self.hidden));
        lines.append('@     s' + str(self.idNumber) + ' type ' + str(self.datatype));
        lines.append('@     s' + str(self.idNumber) + ' symbol ' + str(self.symbol.shape));
        lines.append('@     s' + str(self.idNumber) + ' symbol size ' + str(self.symbol.size));
        lines.append('@     s' + str(self.idNumber) + ' symbol color ' + str(self.symbol.color));
        lines.append('@     s' + str(self.idNumber) + ' symbol pattern ' + str(self.symbol.pattern));
        lines.append('@     s' + str(self.idNumber) + ' symbol fill color ' + str(self.symbol.fill_color));
        lines.append('@     s' + str(self.idNumber) + ' symbol fill pattern ' + str(self.symbol.fill_pattern));
        lines.append('@     s' + str(self.idNumber) + ' symbol linewidth ' + str(self.symbol.linewidth));
        lines.append('@     s' + str(self.idNumber) + ' symbol linestyle ' + str(self.symbol.linestyle));
        lines.append('@     s' + str(self.idNumber) + ' symbol char ' + str(self.symbol.char));
        lines.append('@     s' + str(self.idNumber) + ' symbol char font' + str(self.symbol.char_font));
        lines.append('@     s' + str(self.idNumber) + ' symbol skip ' + str(self.symbol.skip));
        lines.append('@     s' + str(self.idNumber) + ' line type ' + str(self.line.type));
        lines.append('@     s' + str(self.idNumber) + ' line linestyle ' + str(self.line.style));
        lines.append('@     s' + str(self.idNumber) + ' line linewidth ' + str(self.line.width));
        lines.append('@     s' + str(self.idNumber) + ' line color ' + str(self.line.color));
        lines.append('@     s' + str(self.idNumber) + ' line pattern ' + str(self.line.pattern));
        lines.append('@     s' + str(self.idNumber) + ' baseline type ' + str(self.baseline.type));
        lines.append('@     s' + str(self.idNumber) + ' baseline ' + str(self.baseline));
        lines.append('@     s' + str(self.idNumber) + ' dropline ' + str(self.dropline));
        lines.append('@     s' + str(self.idNumber) + ' fill ' + str(self.fill.type));
        lines.append('@     s' + str(self.idNumber) + ' fill ' + str(self.fill.rule));
        lines.append('@     s' + str(self.idNumber) + ' fill ' + str(self.fill.color));
        lines.append('@     s' + str(self.idNumber) + ' fill ' + str(self.fill.pattern));
        lines.append('@     s' + str(self.idNumber) + ' avalue ' + str(self.avalue));
        lines.append('@     s' + str(self.idNumber) + ' avalue type ' + str(self.avalue.type));
        lines.append('@     s' + str(self.idNumber) + ' avalue char size ' + str(self.avalue.char_size));
        lines.append('@     s' + str(self.idNumber) + ' avalue font ' + str(self.avalue.font));
        lines.append('@     s' + str(self.idNumber) + ' avalue color ' + str(self.avalue.color));
        lines.append('@     s' + str(self.idNumber) + ' avalue rot ' + str(self.avalue.rot));
        lines.append('@     s' + str(self.idNumber) + ' avalue format ' + str(self.avalue.format));
        lines.append('@     s' + str(self.idNumber) + ' avalue prec ' + str(self.avalue.precision));
        lines.append('@     s' + str(self.idNumber) + ' avalue prepend ' + str(self.avalue.prepend));
        lines.append('@     s' + str(self.idNumber) + ' avalue append ' + str(self.avalue.append));
        lines.append('@     s' + str(self.idNumber) + ' avalue offset ' + str(self.avalue.offset));
        lines.append('@     s' + str(self.idNumber) + ' errorbar ' + str(self.errorbar));
        lines.append('@     s' + str(self.idNumber) + ' errorbar place' + str(self.errorbar.location));
        lines.append('@     s' + str(self.idNumber) + ' errorbar color ' + str(self.errorbar.color));
        lines.append('@     s' + str(self.idNumber) + ' errorbar pattern ' + str(self.errorbar.pattern));
        lines.append('@     s' + str(self.idNumber) + ' errorbar size ' + str(self.errorbar.size));
        lines.append('@     s' + str(self.idNumber) + ' errorbar linewidth ' + str(self.errorbar.linewidth));
        lines.append('@     s' + str(self.idNumber) + ' errorbar linestyle ' + str(self.errorbar.linestyle));
        lines.append('@     s' + str(self.idNumber) + ' errorbar riser linewidth ' + str(self.errorbar.riser_linewidth));
        lines.append('@     s' + str(self.idNumber) + ' errorbar riser linestyle ' + str(self.errorbar.riser_linestyle));
        lines.append('@     s' + str(self.idNumber) + ' errorbar clip ' + str(self.errorbar.riser_clip_status));
        lines.append('@     s' + str(self.idNumber) + ' errorbar clip length ' + str(self.errorbar.riser_clip_length));
        lines.append('@     s' + str(self.idNumber) + ' comment ' + str(self.comment));
        lines.append('@     s' + str(self.idNumber) + ' legend ' + str(self.legend));        
	return '\n'.join(lines)

    def _repr_data(self):
        return '# data goes here...\n#'

# =============================================================== Test function
if __name__ == '__main__':
    print DataSet()


