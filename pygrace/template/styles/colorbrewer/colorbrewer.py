"""Parse the output of the the ColorBrewer website, which is a collection of
color schemes for cartography.

http://www.personal.psu.edu/cab38/ColorBrewer/ColorBrewer.html

The accompanying file ("colorbrewer.dat"), contains the entire content
of the ColorBrewer output from the website (including the Apache-Style
license).  This module contains python code to parse the data file.
To use this module, probably the user will just want to call the
get_colors method of a color scheme.  For example,

>>> from colorbrewer import * # this just imports the dictionary 'schemes'
>>> scheme = schemes['Set1']
>>> scheme.get_colors(7, 'hex')

will return the 7-color version of the 'Set1' color brewer color
scheme, formatted as RGB hex strings.

For "Sequential" color schemes, the user can request more than the maximum
enumerated number of colors for a scheme, and the color scheme linearly
interpolates between the RGB values. For example,

>>> scheme = schemes['Blues']
>>> scheme.get_colors(50, 'int')

will return a list of RGB tuples, where each member of the tuple is an
integer from 0-255.

Following is a list of the names and the maximum number of enumerated
colors for each scheme:

Type            Name        Max N
----            ----        -----
Diverging       BrBG        11
Diverging       PRGn        11
Diverging       PiYG        11
Diverging       PuOr        11
Diverging       RdBu        11
Diverging       RdGy        11
Diverging       RdYlBu      11
Diverging       RdYlGn      11
Diverging       Spectral    11
Qualitative     Accent      8
Qualitative     Dark2       8
Qualitative     Paired      12
Qualitative     Pastel1     9
Qualitative     Pastel2     8
Qualitative     Set1        9
Qualitative     Set2        8
Qualitative     Set3        12
Sequential      Blues       9
Sequential      BuGn        9
Sequential      BuPu        9
Sequential      GnBu        9
Sequential      Greens      9
Sequential      Greys       9
Sequential      OrRd        9
Sequential      Oranges     9
Sequential      PuBu        9
Sequential      PuBuGn      9
Sequential      PuRd        9
Sequential      Purples     9
Sequential      RdPu        9
Sequential      Reds        9
Sequential      YlGn        9
Sequential      YlGnBu      9
Sequential      YlOrBr      9
Sequential      YlOrRd      9

Mike Stringer
Northwestern University
February 28, 2008
"""
import os



class ColorBrewerScheme(object):
    """This class stores the colors that are associated with a ColorBrewer
    scheme.  Also, it generates interpolated versions of the sequential and
    diverging ColorBrewer schemes.
    """

    def __init__(self, name, schemeType, lineList,
                 minColor=None, maxColor=None):
        """This init function parses the input in the format in which
        it is passed by the module."""

        # use this to store rgb values for each number of classes
        self.data = {}

        # set these descriptive attributes
        self.name = name
        self.schemeType = schemeType
        self.minColor = minColor
        self.maxColor = maxColor
        
        record = []
        for line in lineList:

            # split line on tabs and strip each entry in the list
            splitLine = [string.strip() for string in line.split('\t')]

            # get the name and type of scheme (if this is not emtpy)
            schemeName, schemeType = splitLine[0], splitLine[9]

            # only new sub-schemes have a non-empty schemeName -- so on this
            # flag, parse all of the previous lines if they exist.
            # otherwise, just add this line to the list of lines to parse
            # the next time.
            if schemeName:

                # if this is not the start of the first, it is the end of one
                # of them, so the record is complete, and parse with
                # ColorBrewerScheme object
                if record:
                    self.__add_subscheme(record)
                    
                # use this line as the first line of the next record
                record = [self.__parse_line(line)]
            else:
                record.append(self.__parse_line(line))

        # get the last line in there
        if record:
            self.__add_subscheme(record)

    def __add_subscheme(self, record):
        """Add subscheme (for certain n) to self"""

        self.data[len(record)] = tuple(record)

    def __parse_line(self, line):
        """Returns RGB values from a line in the correct format"""

        # split line on tabs and strip each entry in the list
        splitLine = [string.strip() for string in line.split('\t')]

        # get rgb values and convert to integers
        r, g, b = tuple(int(i) for i in splitLine[6:9])

        # return the tuple of rgb values
        return r, g, b

    def __scale(self, start, finish, length, i):
        """Return the value correct value of a number that is inbetween start
        and finish, for use in a loop of length *length*"""

        fraction = float(i) / (length - 1)
        raynge = finish - start

        return start + fraction * raynge

    def __hex_color(self, r, g, b):
        """Return the hex representation of a 3-tuple (r, g, b) value.
        r, g, and b don't need to be integers."""

        return '%02x%02x%02x' % (r, g, b)
            
    def __linear_gradient(self, rgbList, nColors):
        """Given a list of (r, g, b) tuples, will return a list of length
        nColors where the colors are linearly interpolated between the
        (r, g, b) tuples that are given.

        Example:
        linear_gradient([(0, 0, 0), (255, 0, 0), (255, 255, 0)], 100)
        """

        allColors = []

        # separate (r, g, b) pairs
        for start, end in zip(rgbList[:-1], rgbList[1:]):

            # linearly intepolate between pair of (r, g, b) and add to list
            nInterpolate = 765
            for index in range(nInterpolate):
                r = self.__scale(start[0], end[0], nInterpolate, index)
                g = self.__scale(start[1], end[1], nInterpolate, index)
                b = self.__scale(start[2], end[2], nInterpolate, index)
                allColors.append( (r, g, b) )

        # pick only nColors colors from the total list
        result = []
        for counter in range(nColors):
            fraction = float(counter) / (nColors - 1)
            index = int(fraction * (len(allColors) - 1))
            result.append(allColors[index])

        return result

    def max_number(self):
        """Returns the maximum number of classes that have been enumerated
        for this scheme.
        """
        return max(self.data.iterkeys())

    def min_number(self):
        """Returns the minimum number of classes that have been enumerated
        for this scheme.
        """
        return min(self.data.iterkeys())

    def get_max_colors(self, format='int'):
        """Returns the colors for the subscheme with the maximum number of
        colors that have been enumerated for this scheme.
        """
        return self.get_colors(self.max_number(), format=format)

    def pyfig_color_func(self, n, figColorClass):
        def cfunc(n):
            return tuple(
                figColorClass() for s in self.get_colors(n, format='hex')
                )

    def get_colors(self, n, format='int'):
        """Returns a list of colors (of length n) in the specified format.
        If there are more colors than have been explicitely enumerated in the
        ColorBrewer scheme, then linearly interpolate between RGB values.
        """

        # if the type of scheme is qualitative, only return a known subset
        # for an n that already is enumarated
        if self.schemeType == 'Qualitative':
            try:
                result = self.data[n]
            except KeyError:
                message = '%s (qualitative) doesnt have a %i class scheme.' \
                          % (self.name, n)
                raise KeyError(message)
        else:
            # if n is greater than pre-enumerated subschemes, linearly
            # interpolate between the rgb values of the maximum n
            if n > self.max_number():

                # if optional minColor or maxColor arguments are given,
                # then add them to the list to be interpolated
                colorList = self.get_max_colors()
                if self.minColor is not None:
                    colorList.insert(0, self.minColor)
                    colorList.insert(0, self.minColor)
                if self.maxColor is not None:
                    colorList.append(self.maxColor)
                    colorList.append(self.maxColor)
                    
                result = self.__linear_gradient(colorList, n)
                
            # if n is less than the lowest pre-enumerated subscheme
            elif n < self.min_number():
                message = '%s scheme does not have a %i class subset.' \
                          % (self.name, n)
                raise KeyError(message)

            # if n is in the pre-enumerated range
            else:
                result = self.data[n]

        # result is defined by this point, so convert to new format if
        # necessary
        if format == 'tuple':
            result = tuple(result)

        # rounded to nearest integer
        elif format == 'int':
            result = tuple((int(round(r)), int(round(g)), int(round(b))) \
                           for (r, g, b) in result)

        # scaled between 0 and 1
        elif format == 'scaled':
            result = tuple((r/255.0, g/255.0, b/255.0) for (r, g, b) in result)

        # converted to a hex string
        elif format == 'hex':
            result = tuple(self.__hex_color(*t) for t in result)

        # converted to a hex string with a pound sign in front
        elif format == '#hex':
            result = tuple('#%s' % self.__hex_color(*t) for t in result)

        # throw error if unknown format argument
        else:
            message = 'unknown format %s' % format
            raise ValueError(message)

        return result



# ------------------------------------------------------------------------------
# The following code just parses the accompanying 'colorbrewer.dat' file,
# and stores the color schemes in a dictionary called 'schemes.' The 'schemes'
# dictionary is the only thing that really should be imported from this
# module.

# strip the '.py' extension from the name of this module
thisBasename, dotPy = os.path.splitext(__file__)

# replace the extension with '.dat' --- this is where the colorbrewer
# information should be written
colorBrewerFile = '%s.dat' % thisBasename

# read the file into a string
colorBrewerStream = open(colorBrewerFile)
lineList = tuple(line for line in colorBrewerStream 
                 if line.strip() and not line.startswith('#'))
colorBrewerData = colorBrewerStream.read()
colorBrewerStream.close()

# run through the lines and parse
schemes = {}
record = []
for line in lineList[1:]:

    # split line on tabs and strip each entry in the list
    splitLine = [string.strip() for string in line.split('\t')]

    # get the name and type of scheme (if this is not empty)
    schemeName, schemeType = splitLine[0], splitLine[9]

    # only new schemes have a non-empty schemeType -- so on this flag, parse
    # all of the previous lines if they exist.  otherwise, just add this line
    # to the list of lines to parse the next time.
    if schemeType:

        # if this is not the start of the first, it is the end of one of them,
        # so the record is complete, and parse with ColorBrewerScheme object
        if record:
            schemes[oldName] = ColorBrewerScheme(oldName, oldType,
                                                 record)

        # use this line as the first line of the next record
        record = [line]
        oldName, oldType = schemeName, schemeType
    else:
        record.append(line)

# add the last entry
if record:
    schemes[oldName] = ColorBrewerScheme(oldName, oldType,
                                         record)



# here, the schemes dictionary is full of beautiful ColorBrewer color schemes
# only export schemes when 'from colorbrewer import *' syntax is used

__all__ = ['schemes']
