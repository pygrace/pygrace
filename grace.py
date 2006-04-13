#!/usr/bin/env python
"""
Amaral Group
Northwestern University
4/4/2006

This module contains classes for creating, formatting, and writing xmgrace
plots from within Python.

Notes:

* ask everybody: are region definitions necessary?

"""

# import from standard libraries
from os import popen

# import from supporting modules
from other import Divider
from colors import DEFAULT_COLORS, Color
from fonts import DEFAULT_FONTS, Font
from timestamp import Timestamp
from graph import Graph
from dataset import DataSet

HEADER_COMMENT = '# Amaral Group python interface for xmgrace. OH YEAH!'
INDEX_ORIGIN = 0  # zero or one (one is for losers)

# ================================================================= Grace class
class Grace:
    """
    Grace Class

    Write detailed comments here later explaining the functionality and
    examples of how to use...
    """
    def __init__(self, nGraphs=0,
		 version='50114',
		 width=792, height=612,
		 backgroundColor='white', backgroundFill='on'
		 ):

	# initialize defaults as class attributes
        self.version = version
        self.width, self.height = width, height
        self.backgroundColor = backgroundColor
        self.backgroundFill = backgroundFill        

	# initialize default colors and fonts
        self._colors = DEFAULT_COLORS
        self._colorIndex = len(self._colors)
        self._fonts = DEFAULT_FONTS
        self._fontIndex = len(self._fonts)

	# initialize grace objects
	self.timestamp = Timestamp()

	self.graphs = []
        self._graphIndex = INDEX_ORIGIN
        for i in range(nGraphs):
            self.add_graph()

    # ------------------------------------------------ Grace accessor functions
    # these two function allow access to class attributes just like a
    # dictionary (eg. instance['width'] = 424)

    def __getitem__(self, name): return getattr(self, name)
    def __setitem__(self, name, value): setattr(self, name, value)

    # ------------------------------------------------- Grace private functions
    # these functions are used internally by the grace class - there should be
    # no need to use these externally.

    def _sorted_colors(self):
        """_sorted_colors() -> list of Color() objects

        Uses decorate, sort, undecorate to sort dictionary by number.
        """
        decorated = [(self._colors[i]['index'], self._colors[i]['name']) \
                     for i in self._colors]
        decorated.sort()
        return [self._colors[name] for (i, name) in decorated]

    def _sorted_fonts(self):
        """_sorted_fonts() -> list of Font() objects

        Uses decorate, sort, undecorate to sort dictionary by number.
        """ 
        decorated = [(self._fonts[i]['index'], self._fonts[i]['nickName']) \
                     for i in self._fonts]
        decorated.sort()
        return [self._fonts[name] for (i, name) in decorated]

    def _header_string(self):
        lines = []

        lines.append('@version %s' % self.version)
        lines.append('@page size %i, %i' % (self.width, self.height))
        lines.append('@page background fill %s' % self.backgroundFill)
        lines.append(str(Divider('Font Definitions','-', 68)))
        lines.extend(map(str,self._sorted_fonts()))
        lines.append(str(Divider('Color Definitions','-', 68)))
        lines.extend(map(str, self._sorted_colors()))
        lines.append('@background color "%s"' % self.backgroundColor)
        lines.append(str(Divider('Timestamp','-', 68)))
	lines.append(str(self.timestamp))

        return '\n'.join(lines)
    
    # -------------------------------------------------- Grace output functions
    # the standard function __repr__ is defined to allow easy writing to
    # standard out and to files (eg. a = Grace(); print a; str(a); ...)

    def __repr__(self):
        lines = []

        lines.append('# Grace project file')
        lines.append(HEADER_COMMENT)
        lines.append(str(Divider('Header', '=', 68)))
	lines.append(self._header_string())
        lines.append(str(Divider('Graphs', '=', 68)))
	lines.extend(map(str,self.graphs))
        lines.append(str(Divider('Data', '=', 68)))
        for graph in self.graphs:
            for dataset in graph.datasets:
                idNumbers = (graph.idNumber, dataset.idNumber)
                lines.append('# @target G%i.S%i' % idNumbers)
                lines.append('# @type ' + dataset.datatype)
                lines.append(dataset._repr_data())

        return '\n'.join(lines)

    def write_agr(self, filename='temp.agr'):
        """write_agr(filename='temp.agr') -> none.

        This function writes an xmgrace (.agr) file.
        """
        # format filename (include the correct file extension)
        if not filename.split('.')[-1].upper() == 'AGR':
            filename = filename + '.agr'

        # write file
	outfile = open(filename,'w')
	outfile.write(str(self))
	outfile.close()

    def write_file(self, filename='temp.eps', filetype='eps'):
        """write_file(filename='temp.eps', filetype='eps') -> none.

        This function uses xmgrace to output a image file of the specified
        type.  Here are the allowed types (for version 5.1.14):

        X11 PostScript EPS MIF SVG PNM JPEG PNG Metafile

        Note: The popen command is confusing - see the python documentation
        for a bad description.  The key is that popen with the 'w' option
        returns a file object in write mode, that will be sent to the command
        once the file object is closed (after writing stuff to it).
        """
        # format filename (include correct file extension)
        if not filename.split('.')[-1].upper() == filetype.upper():
            filename = filename + '.' + filetype.lower()

        # make command that will be piped to
        command = 'xmgrace -hardcopy -hdevice ' + filetype.upper() + \
                  ' -printfile ' + filename + ' -pipe'

        # set up a file as an INPUT pipe to command
        pipeInput = popen(command, 'w')

        # write grace file to input pipe, and close.  once the input pipe is
        # closed, the command runs and xmgrace outputs a file
        pipeInput.write(str(self))
        pipeInput.close()

    # ----------------------------------------------- Grace interface functions
    # use these functions to modify grace objects, these should have helpful
    # docstring comments, because these are the functions that the user must
    # use.

    def define_color(self, name, (red, green, blue)):
        """define_color(name, (R,G,B)) -> none

        Specifies a name for an (R,G,B) color which can be used later as the
        color of any object.

        Example:

        a = Grace()
        a.define_color('deeppurple', (100, 10, 100))
        a['backgroundColor'] = 'deeppurple'

        The accomplishes the same effect as:

        a['backgroundColor'] = '(100, 10, 100)'   <--- note the quotes
        """
        self._colors[name] = Color(self._colorIndex, name, (red, green, blue))
        self._colorIndex += 1

    def define_font(self, nickName, officialName):
        """define_font(nickName, officialName) -> None

        Supposed to specify a name for a font, just like color - but it doesn't
        work (in xmgrace). To specify the font of something, use the full name
        or number as specified in the following list:

        0  Times-Roman
        1  Times-Italic
        2  Times-Bold
        3  Times-BoldItalic
        4  Helvetica
        5  Helvetica-Oblique
        6  Helvetica-Bold
        7  Helvetica-BoldOblique
        8  Courier
        9  Courier-Oblique
        10 Courier-Bold
        11 Courier-BoldOblique
        12 Symbol
        13 ZapfDingbats

        Example:

        a = Grace()
        a.timestamp['font'] = 'ZapfDingbats'

        In simpler words, this function is pretty much useless.
        """
        self._fonts[nickName] = Font(self._fontIndex, nickName, officialName)
	self._fontIndex += 1

    def add_graph(self, graph=False):
        """add_graph() -> none

        Stub to test main Grace output - will probably need to change
        """
        idNumber = self._graphIndex

        if not graph:
            self.graphs.append(Graph(idNumber))
        else:
            self.graphs.append(graph)
            graph['idNumber'] = idNumber
            
        self._graphIndex += 1
        return idNumber

# =============================================================== Test function
if __name__ == '__main__':
    
    d = DataSet()
    g = Graph()
    x = Grace()

    g.add_dataset(d)
    x.add_graph(g)

    g.frame.color = 'red'
    g.frame['type'] = 1

    x.define_color('babybrown', (155, 135, 95))
    x['backgroundColor'] = 'babybrown'

    x.timestamp['onoroff'] = 'on'
    x.timestamp['angle'] = 10

    d1, d2 = DataSet(), DataSet()
    g1 = Graph()

    g1.add_dataset(d1)
    g1.add_dataset(d2)
    x.add_graph(g1)
    
    print x
    x.write_agr()
    x.write_file()

    
