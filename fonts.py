#!/usr/bin/env python
"""
Amaral Group
Northwestern University
4/5/2006

This module holds the Font class and the dictionary of DEFAULT_FONTS that is
used in the grace.py module.  To include more default fonts, just change the
default font dictionary.
"""

_DEFAULT_FONT_DICTIONARY = {
#   "nick name":             [index, "official name"]        
    "Times-Roman":           [0,     "Times-Roman"],
    "Times-Italic":          [1,     "Times-Italic"],
    "Times-Bold":            [2,     "Times-Bold"],
    "Times-BoldItalic":      [3,     "Times-BoldItalic"],
    "Helvetica":             [4,     "Helvetica"],
    "Helvetica-Oblique":     [5,     "Helvetica-Oblique"],
    "Helvetica-Bold":        [6,     "Helvetica-Bold"],
    "Helvetica-BoldOblique": [7,     "Helvetica-BoldOblique"],
    "Courier":               [8,     "Courier"],
    "Courier-Oblique":       [9,     "Courier-Oblique"],
    "Courier-Bold":          [10,    "Courier-Bold"],
    "Courier-BoldOblique":   [11,    "Courier-BoldOblique"],
    "Symbol":                [12,    "Symbol"],
    "ZapfDingbats":          [13,    "ZapfDingbats"]
    }

# ================================================================== Font class
class Font:
    """Font class

    Used to map fonts to names in xmgrace (NAMES DO NOT WORK, THOUGH).

    Example:

    >> print Font(42, 'smarmy', 'Helvetica')
    @map color 42 to 'Helvetica', \"smarmy\"

    Later, either 42 or \"smarmy\" can be used to set the font of an xmgrace
    object (eg. @timestamp font 0, NOT @timestamp font \"smarmy\")
    """
    def __init__(self,
                 index = 4,
                 nickName = '',
                 officialName = ''
                 ):
        self.index = index
        self.nickName = nickName
	self.officialName = officialName

    def __getitem__(self, name):
        return getattr(self, name)

    def __setitem__(self, name, value):
        setattr(self, name, value)

    def __repr__(self):
        return '@map font %i to "%s", "%s"'\
               % (self.index, self.officialName, self.nickName)

# Build list of default Colors from dictionary
DEFAULT_FONTS = {}
for nickName in _DEFAULT_FONT_DICTIONARY:
    index, officialName = _DEFAULT_FONT_DICTIONARY[nickName]
    DEFAULT_FONTS[nickName] = Font(index, nickName, officialName)

# =============================================================== Test function
if __name__ == '__main__':
    print Font(0, 'fontOne', 'Times-Roman')
    print Font(42, 'fontFortyTwo', 'ZapfDingbats')


