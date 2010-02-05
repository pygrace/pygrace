import random

from base import BaseSet
from Styles.ColorBrewer import colorbrewer

class Color(object):
    """Object that stores a mapping between an index an a name for a color,
    as well as the RGB tuple of the color."""
    def __init__(self, index, red, green, blue, name=''):
        self.index = index
        self.red = red
        self.green = green
        self.blue = blue
        self.name = name or ('color%i' % index)

    def __str__(self):
        return '@map color %i to (%i, %i, %i), "%s"' % \
            (self.index, self.red, self.green, self.blue, self.name)

    def rgb(self):
        """Return RGB tuple."""
        return self.red, self.green, self.blue

    def change_opacity(self, percent):
        if percent < 0 or percent > 100:
            message = 'Opacity percentage can only be changed to a value ' + \
            'between 0 and 100.'
            raise ValueError(message)
        new_rgb = []
        for color_channel in self.rgb():
            alpha = 1. - (color_channel /255.)
            alpha *= percent / 100.
            new_rgb.append((1. - alpha) * 255.)
        self.red, self.green, self.blue = new_rgb
            

class ColorScheme(BaseSet):
    """This subclass of the base set has a method that checks for conflicts
    in the color scheme."""
    def add_color(self, red, green, blue, name=None):
        try:
            color = self.get_item_by_name(name)
        except KeyError:
            return BaseSet.add_item(self, Color, red, green, blue, name)
        else:
            if not color.rgb() == (red, green, blue):
                message = "name '%s' cannot refer to two colors\n" % name
                message += ' ' * 12 + "old (%i, %i, %i)" % color.rgb()
                message += " != new (%i, %i, %i)" % (red, green, blue)
                raise ValueError(message)
            
    def change_opacity(self, percent, exclude_black=False):
        for color in self.items:
            if exclude_black and (color.red,color.green,color.blue)==(0,0,0):
                continue
            color.change_opacity(percent)


class ColorBrewerScheme(ColorScheme):
    """Instantiate with a name of the color brewer scheme (and an optional
    number of colors -- default is the maximum that is explicitly enumerated
    in the colorbrewer definition.  The first two colors (0 and 1) are always
    white and black."""
    def __init__(self, name, n=None, reverse=False,
                 randomize_order=False, seed=None):

        # get the colors from a color brewer scheme
        try:
            scheme = colorbrewer.schemes[name]
        except KeyError:
            message = "'%s' is not a valid colorbrewer scheme name" % name
            raise KeyError(message)
        else:
            nColors = n or scheme.max_number()
            rgbList = scheme.get_colors(nColors)

        # reverse the rgb list?
        if reverse:
            rgbList = list(rgbList)
            rgbList.reverse()
            rgbList = tuple(rgbList)

        # randomize the rgb list?
        if randomize_order:
            if seed is None:
                message = 'For randomizing order, you have to specify a seed'
                raise ValueError(message)
            random.seed(seed)
            rgbList = list(rgbList)
            random.shuffle(rgbList)
            rgbList = tuple(rgbList)

        # make color instance from the rgb values
        colors = [Color(0, 255, 255, 255, 'white'), Color(1, 0, 0, 0, 'black')]
        colors.extend([Color(index + 2, r, g, b, '%s-%i' % (name, index)) \
                           for index, (r, g, b) in enumerate(rgbList)])

        ColorScheme.__init__(self, colors)

class RandomColorScheme(ColorScheme):
    """Instantiate with random seed and the number of colors.  The first
    two colors (0 and 1) are always white and black.
    """
    def __init__(self, seed, n, reverse=False):

        # create a list of rgb values
        rgbList = []
        random.seed(seed)
        for i in range(n):
            rgbList.append((random.randint(0,255),
                            random.randint(0,255),
                            random.randint(0,255)))
        rgbList = tuple(rgbList)

        # reverse the rgb list?
        if reverse:
            rgbList = list(rgbList)
            rgbList.reverse()
            rgbList = tuple(rgbList)

        # make color instance from the rgb values
        name = "Rand-%d"%seed
        colors = [Color(0, 255, 255, 255, 'white'), Color(1, 0, 0, 0, 'black')]
        colors.extend([Color(index + 2, r, g, b, '%s-%i' % (name, index)) \
                           for index, (r, g, b) in enumerate(rgbList)])

        ColorScheme.__init__(self, colors)

class MarkovChainColorScheme(ColorScheme):
    """Instantiate with random seed and the number of colors.  The first
    two colors (0 and 1) are always white and black.  This identifies
    a Markov Chain of colors after that.
    """
    def __init__(self, seed, n, reverse=False, maxstep=25):

        # create a list of rgb values
        rgbList = []
        random.seed(seed)
        if n>0:
            rgbList.append((random.randint(0,255),
                            random.randint(0,255),
                            random.randint(0,255)))
        while len(rgbList)<n:
            rgb = list(rgbList[-1])
            drgb = [random.randint(-maxstep,maxstep),
                    random.randint(-maxstep,maxstep),
                    random.randint(-maxstep,maxstep)]
            rgb = [(rgb[i] + drgb[i])%256 for i in range(3)]
            rgbList.append(tuple(rgb))
        rgbList = tuple(rgbList)

        # reverse the rgb list?
        if reverse:
            rgbList = list(rgbList)
            rgbList.reverse()
            rgbList = tuple(rgbList)

        # make color instance from the rgb values
        name = "MC-%d-%d"%(maxstep,seed)
        colors = [Color(0, 255, 255, 255, 'white'), Color(1, 0, 0, 0, 'black')]
        colors.extend([Color(index + 2, r, g, b, '%s-%i' % (name, index)) \
                           for index, (r, g, b) in enumerate(rgbList)])

        ColorScheme.__init__(self, colors)

# these are the default colors in XMGrace
class DefaultColorScheme(ColorScheme):
    """Keepin' it real with the *original* xmgrace color scheme."""
    def __init__(self):
        colors = [Color(*params) for params in (
                (0, 255, 255, 255, 'white'),
                (1, 0, 0, 0, 'black'),
                (2, 255, 0, 0, 'red'),
                (3, 0, 255, 0, 'green'),
                (4, 0, 0, 255, 'blue'),
                (5, 255, 255, 0, 'yellow'),
                (6, 188, 143, 143, 'brown'),
                (7, 220, 220, 220, 'grey'),
                (8, 148, 0, 211, 'violet'),
                (9, 0, 255, 255, 'cyan'),
                (10, 255, 0, 255, 'magenta'),
                (11, 255, 165, 0, 'orange'),
                (12, 114, 33, 188, 'indigo'),
                (13, 103, 7, 72, 'maroon'),
                (14, 64, 224, 208, 'turquoise'),
                (15, 0, 139, 0, 'green4'),
                )]
        ColorScheme.__init__(self, colors)

