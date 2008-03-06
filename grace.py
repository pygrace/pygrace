#!/usr/bin/env python
"""
Amaral Group
Northwestern University
8/1/2006

This module contains classes for creating, formatting, and writing xmgrace
plots from within Python.

Notes:

* ask everybody: are region definitions necessary?

"""

# import from standard libraries
from os import popen

# import from supporting modules
import sys
from other import Divider
from colors import DEFAULT_COLORS, Color
from fonts import DEFAULT_FONTS, Font
from timestamp import Timestamp
from grace_graph import Graph
from view import View,World
from dataset import *
##from sizeAdjust import adjust_labels
from xmg_exceptions import SetItemError, AttrError

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
		 backgroundColor='white', backgroundFill='off'
		 ):

	# initialize defaults as class attributes
        self.version = version
        self.width, self.height = width, height
        self.background_color = backgroundColor
        self.background_fill = backgroundFill        

	# initialize default colors and fonts
        self._colors = DEFAULT_COLORS
        self._colorIndex = len(self._colors)
        self._fonts = DEFAULT_FONTS
        self._fontIndex = len(self._fonts)

	# initialize grace objects
	self.timestamp = Timestamp(self._colors,self._fonts)

	self.graphs = []
        
        #--FOR MULTI Graphs--#
        self.graphs_rc = [] #graphs by row and column

        self.xoffset = .1
        self.rows = 1
        self.cols = 1

        # maximum frame ratios in viewport units
        if height>width:
            self.max_frame_width = 1.0;
            self.max_frame_height = float(height)/float(width);
        else:
            self.max_frame_width = float(width)/float(height);
            self.max_frame_height = 1.0;

        # used for fomatting multiple graphs
        self.frame_height = None   # height of one graph
        self.frame_width = None    # width of one graph
        self.hgap = None           # horizontal gap between graphs
        self.vgap = None           # vertical gap between graphs

        #--------------#
        self._graphIndex = INDEX_ORIGIN
        for i in range(nGraphs):
            self.add_graph()
        self.drawing_objects = []  #list of strings, lines, boxes and ellipses

    # ------------------------------------------------ Grace accessor functions
    # these two function allow access to class attributes just like a
    # dictionary (eg. instance['width'] = 424)

    def __getitem__(self, name): return getattr(self, name)
    def __setitem__(self, name, value):

        if type(value) == str:
            value = value.replace('"','')

        if name == 'version':
            self.version = value
        elif name == 'width':
            try: self.width = int(value)
            except: SetItemError(self.__class__, value, name)
        elif name == 'height':
            try: self.height = int(value)
            except: SetItemError(self.__class__, value, name)
        elif name == 'background_color':
            try:
                if self._colors.has_key(value):
                    self.background_color = value
                else:
                    intRepr = int(value)
                    if intRepr >= len(self._colors.keys()):
                        raise
                    else:
                        self.background_color = int(value)
            except:
               SetItemError(self.__class__,value,name)
        elif name == 'background_fill':
            self.background_fill = value
        elif name == 'timestamp':
            if not value.__class__ == Timestamp:
                SetItemError(self.__class__, value, name)
            else:
                self.timestamp = value

        #set 'graphs' attribute?
         
        else:
            AttrError(self.__class__, name)
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
        lines.append('@page background fill %s' % self.background_fill)
        lines.append(str(Divider('Font Definitions','-', 68)))
        lines.extend(map(str,self._sorted_fonts()))
        lines.append(str(Divider('Color Definitions','-', 68)))
        lines.extend(map(str, self._sorted_colors()))
        lines.append('@background color %s' %
                     (type(self.background_color)==str and ("\"%s\"" % self.background_color) \
                      or self.background_color))
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
        for drawobj in self.drawing_objects:
            lines.append(str(drawobj))
        lines.append(str(Divider('Graphs', '=', 68)))
	lines.extend(map(str,self.graphs))
        lines.append(str(Divider('Data', '=', 68)))
        for graph in self.graphs:
            for dataset in graph.datasets:
                idNumbers = (graph.idNumber, dataset.idNumber)
                lines.append('@target G%i.S%i' % idNumbers)
                lines.append('@type ' + dataset.type)
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

    def write_file(self, filename='temp.eps', filetype='EPS'):
        """write_file(filename='temp.eps', filetype='EPS') -> none.

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

        if filetype=='eps': filetype='EPS'

        # make command that will be piped to
        command = 'xmgrace -hardcopy -hdevice ' + filetype + \
                  ' -printfile "' + filename + '" -pipe'

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

    def get_graph(self,id):
        if id >= len(self.graphs):
            return None
        else:
            return self.graphs[id]

    def add_drawing_object(self,obj):
        self.drawing_objects.append(obj)

    def reset_colors(self):
        self._colors = {}
        self._colorIndex = 0
    def reset_fonts(self):
        self._fonts = {}
        self._fontIndex = 0


#------------------ FORMAT MULTIPLE GRAPHS -------------------------#

    def multi(self, rows, cols, hoffset=0.2, voffset=0.2,hgap=0.1, vgap=0.1,
              width_to_height_ratio=1.66):
        """Create a grid of graphs with the given number of <rows> and <cols>
           Makes graph frames all the same size.
        """
        self.graphs_rc = [[None for i in range(cols)] for j in range(rows)]

        self.hgap = hgap
        self.vgap = vgap
        self.hoffset = hoffset
        self.voffset = voffset
        self.rows = rows
        self.cols = cols

        #------ FRAME SIZING-----#
        # want to have frames all the same size, but also need to take
        # advantage of the entire canvas.  first check to see which
        # dimension will be more prohibitive (desired ratio is
        # width/height = 1.66)

        # proposed frame height and width of each graph
        self.frame_height = (self.max_frame_height - 2*voffset \
                             - (rows-1)*vgap)/rows
        self.frame_width = (self.max_frame_width - 2*hoffset \
                            - (cols-1)*hgap)/cols

        # want a width/height ratio of 1.66, see which dimension is
        # more prohibitive and change it
        if self.frame_width/self.frame_height > width_to_height_ratio:
            self.frame_width = width_to_height_ratio*self.frame_height
        else:
            self.frame_height = self.frame_width/width_to_height_ratio;
        
        #------------------------#

        if rows*cols >= len(self.graphs):
            nPlots = len(self.graphs)
        else:
            nPlots = rows*cols

        r=0;c=0
        for i in range(nPlots):
            self.put(self.graphs[i],r,c)
            c += 1
            if c>=cols:
                c=0
                r+=1
                
    def put(self,g, row, col): # ZERO BASED INDEXING.  Places a graph at postion [row][col]
        if row >= self.rows:
            raise
        if col >= self.cols:
            raise

        self.graphs_rc[row][col] = g

        g['view']['xmin'] = self.hoffset+(self.hgap+self.frame_width)*col
        g['view']['ymin'] = self.max_frame_height - self.voffset - \
                            self.vgap*row - self.frame_height*(row+1)
        g['view']['xmax'] = g['view']['xmin'] + self.frame_width
        g['view']['ymax'] = g['view']['ymin'] + self.frame_height

        ## sys.stderr.write(str(row)+ ' ' + str(col)+'\n')
##         sys.stderr.write(str(g['view']['xmin'])+'\n')
##         sys.stderr.write(str(g['view']['ymin'])+'\n')
        
    def get_rc(self,row,col):
        """Returns the graph in position [row][col]"""
        return self.graphs_rc[row][col]
        

    def set_fonts(self,font_type):
        """Set all fonts in grace object to be font_type
        """

        self.timestamp.font = font_type;
        for graph in self.graphs:
            graph.title.font = font_type
            graph.subtitle.font = font_type;
            graph.legend.font = font_type
            graph.xaxis.label.label.font = font_type;
            graph.yaxis.label.label.font = font_type;
            graph.xaxis.ticklabel.font = font_type;
            graph.yaxis.ticklabel.font = font_type;

            for dataset in graph.datasets:
                dataset.symbol.char_font = font_type;
                dataset.avalue.font = font_type
                
    def get_eps_frame_coords(self):
        """For each graph, obtain the eps coordinates of the frame
        within the figure.  This is useful for aligning things in
        external programs such as xfig.
        """
        eps_frame_coords = []
        for graph in self.graphs:

            # height is the limiting dimension in viewport coordinates
            if self.width>self.height:
                lim_dimension = float(self.height)
            else:
                lim_dimension = float(self.width)
            xmin = graph.view.xmin*lim_dimension
            xmax = graph.view.xmax*lim_dimension
            ymin = graph.view.ymin*lim_dimension
            ymax = graph.view.ymax*lim_dimension
            eps_frame_coords.append((xmin,xmax,ymin,ymax))
        return eps_frame_coords
            
        

# =============================================================== Test function
if __name__ == '__main__':
    
    
    x = Grace()
    d = DataSet([(-1,-2),(1,1),(2,3)], x._colors, x._fonts)
    e = DataSet([(0,0),(1.5,2),(2,2.8)],x._colors, x._fonts)
    g = Graph(x._colors,x._fonts)
##     g.world = World((.1,.1),(2,3))
    #g.yaxis['scale'] = 'Logarithmic'

    g.add_dataset(d)
    g.add_dataset(e)
    x.add_graph(g)
    #d.legend = 'blah'

    #g.legend['loc'] = (.8,.8)

    #g.legend['color'] = 'red'
    #g.legend['font'] = "Helvetica"
    
    #g.frame.color = 'red'
    #g.frame['type'] = 1



    x.define_color('babybrown', (155, 135, 95))
    #x['backgroundColor'] = 'babybrown'
    #sys.err.write(_colors["red"])

##     x.timestamp['onoff'] = 'on'
##     x.timestamp['rot'] = 5

##     d1, d2 = DataSet(), DataSet()
##     g1 = Graph()

##     g1.add_dataset(d1)
##     g1.add_dataset(d2)

##     x.add_graph(g1)

    #adjust_labels(g,.5)
    
    print x
    x.write_agr()
    x.write_file()
    

