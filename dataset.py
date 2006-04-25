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
                 datatype='xy'):
        self.idNumber = idNumber
        self.datatype = datatype

    def __getitem__(self, name): return getattr(self, name)
    def __setitem__(self, name, value): setattr(self, name, value)

    def __repr__(self):
	return '#     S' + str(self.idNumber) + ' formatting info'

    def _repr_data(self):
        return '# data goes here...\n#'

# =============================================================== Test function
if __name__ == '__main__':
    print DataSet()


