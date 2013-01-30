from base import BaseSet

class Font(object):
    """Object that stores a mapping between an index an a name for a font,
    and outputs a string representation suitable for XMGrace."""
    def __init__(self, index, name):
        self.index = index
        self.name = name

    def __str__(self):
        return '@map font %i to "%s", "%s"' % (self.index,self.name,self.name)

class FontSet(BaseSet):
    """A dummy subclass for storing fonts. Perhaps there will be some way to
    modify fonts in the future."""
    pass

# this is the default font mapping in XMGrace
default = FontSet([Font(*params) for params in (
            (0, 'Times-Roman'),
            (1, 'Times-Italic'),
            (2, 'Times-Bold'),
            (3, 'Times-BoldItalic'),
            (4, 'Helvetica'),
            (5, 'Helvetica-Oblique'),
            (6, 'Helvetica-Bold'),
            (7, 'Helvetica-BoldOblique'),
            (8, 'Courier'),
            (9, 'Courier-Oblique'),
            (10, 'Courier-Bold'),
            (11, 'Courier-BoldOblique'),
            (12, 'Symbol'),
            (13, 'ZapfDingbats'),
            )])
