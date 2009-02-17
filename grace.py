import time
import os

from base import GraceObject
from graph import Graph
from drawing_objects import DrawingObject
from colors import default as default_colors
from fonts import default as default_fonts

HEADER_COMMENT = '# Amaral Group python interface for xmgrace. OH YEAH!'
INDEX_ORIGIN = 0  # zero or one (one is for losers)

class Grace(GraceObject):
    def __init__(self,
                 width=792,
                 height=612,
		 background_color=0,
                 background_fill='off',
                 version='50114',
                 verbose=False,
                 colors=None,
		 ): 
        GraceObject.__init__(self, None, locals())

	self.timestamp = Timestamp(self)

        # set these first, so that children inherit this color scheme
        self.colors = colors or default_colors
        self.fonts = default_fonts

        self._graphIndex = INDEX_ORIGIN
	self.graphs = []

        self.drawing_objects = []
        
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

    def __setattr__(self, key, value):

        # check Grace specific attributes
        if key == 'width' or key == 'height':
            self._check_type(int, key, value)
            self._check_range(key, value, 0, None)
        elif key == 'verbose':
            self._check_type(bool, key, value)
        elif key == 'version':
            self._check_type(str, key, value)
        elif key == 'background_fill':
            self._check_type(str, key, value)
            self._check_membership(key, value, ('on', 'off'))
            
        GraceObject.__setattr__(self, key, value)
        
    def set_portrait(self):
        self.width = 612
        self.height = 792
        return 1.0, 792.0 / 612.0
    
    def set_landscape(self):
        self.width = 792
        self.height = 612
        return 792.0 / 612.0, 1.0

    def autoscale(self):
        for graph in self.graphs:
            graph.autoscale()

    def autoformat(self, printWidth=6.5):
        for graph in self.graphs:
            graph.autoformat(printWidth)

    def _header_string(self):
        lines = []
        lines.append('@version %s' % self.version)
        lines.append('@page size %i, %i' % (self.width, self.height))
        lines.append('@page background fill %s' % self.background_fill)
        lines.append(str(self.fonts))
        lines.append(str(self.colors))
        lines.append('@background color %s' % self.background_color)
	lines.append(str(self.timestamp))
        return '\n'.join(lines)
    
    def __str__(self):
        lines = []
        lines.append('# Grace project file')
        lines.append(HEADER_COMMENT)
	lines.append(self._header_string())
        lines.extend(map(str, self.drawing_objects))
	lines.extend(map(str, self.graphs))
        for graph in self.graphs:
            for dataset in graph.datasets:
                lines.append('@target G%i.S%i' % (graph.index, dataset.index))
                lines.append('@type %s' % dataset.type)
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

    def write_file(self, filename='temp.eps', filetype=None):
        """write_file(filename='temp.eps', filetype=None) -> none.

        This function uses gracebat to output a image file of the specified
        type.  Here are the allowed types (for version 5.1.14):

        X11 PostScript EPS MIF SVG PNM JPEG PNG Metafile

        Note: The popen command is confusing - see the python documentation
        for a bad description.  The key is that popen with the 'w' option
        returns a file object in write mode, that will be sent to the command
        once the file object is closed (after writing stuff to it).
        """

        # dictionary for converting file extensions to proper gracebat
        # file types
        ext2filetype = {"eps":"EPS",
                        "ps":"PostScript",
                        "mif":"MIF",
                        "svg":"SVG",
                        "pnm":"PNM",
                        "jpg":"JPEG",
                        "jpeg":"JPEG",
                        "png":"PNG",
                        }

        # find extension of file
        root,ext = os.path.splitext(filename)
        ext = ext[1:].lower()

        if ext=="agr" or (filetype and filetype.lower() == 'agr'):
            self.write_agr(filename)
            return
        elif ext in ext2filetype and filetype is None:
            filetype = ext2filetype[ext]
        elif filetype is None:
            message = """
Grace.write_file tries to guess the gracebat file type from the given
file name.  In this case, Grace.write_file does not recognize the file
type of file '%s'.  Please specify the gracebat file type manually
using the 'filetype' keyword argument.
"""%(filename)
            raise TypeError, message

        # make command that will be piped to
        command = 'gracebat -hardcopy -hdevice %s -printfile "%s" -pipe' % \
                  (filetype, filename)

        # set up a file as an INPUT pipe to command
        pipeInput = os.popen(command, 'w')

        # write grace file to input pipe, and close.  once the input pipe is
        # closed, the command runs and xmgrace outputs a file
        pipeInput.write(str(self))
        pipeInput.close()

    def add_color(self, red, green, blue, name=None):
        color = self.colors.add_color(red, green, blue, name)
        return color
        
    def add_graph(self, cls=Graph, *args, **kwargs):

        # make sure that cls is a subclass of Graph
        if not issubclass(cls, Graph):
            message = '%s is not a subclass of Graph' % cls.__name__
            raise TypeError(message)

        # make an instance of the graph class and add to list
        graph = cls(parent=self, index=self._graphIndex, *args, **kwargs)
        self.graphs.append(graph)

#        if len(self.graphs) > 1:
#            self.multi(1, len(self.graphs))

        # increment counter and return the graph object
        self._graphIndex += 1
        return graph

    def clone_graph(self,graph,cls=Graph,*args,**kwargs):
        """Clone graph 'graph' by adding a new graph (the clone) and
        then copying the format of 'graph'.

        This is a convenience method which is handy for graphs that
        have drawing objects in them.  When drawing objects are in a
        graph, the drawing object is placed over the axes, frame,
        etc. and it makes the graphs rather ugly looking.
        """

        clone = self.add_graph(Graph,*args,**kwargs)
        clone.copy_format(graph)
        return clone
                
    def add_drawing_object(self, cls, *args, **kwargs):

        # make sure that cls is a subclass of DrawingObject
        if not issubclass(cls, DrawingObject):
            message = '%s is not a subclass of DrawingObject' % cls.__name__
            raise TypeError(message)

        # here, the class argument is mandatory, because there are many built
        # in types of drawing objects
        drawingObject = cls(parent=self, *args, **kwargs)
        self.drawing_objects.append(drawingObject)

        # return the instance of the drawing object
        return drawingObject

    def get_graph(self, index):
        return self.graphs[index]

    def get_rc(self,row,col):
        """Returns the graph in position [row][col]"""
        return self.graphs_rc[row][col]

    def put(self, g, row, col):
        # ZERO BASED INDEXING.  Places a graph at postion [row][col]
        if row >= self.rows:
            raise
        if col >= self.cols:
            raise

        self.graphs_rc[row][col] = g

        g.view.xmin = self.hoffset[0]+(self.hgap+self.frame_width)*col
        g.view.ymin = self.max_frame_height - self.voffset[0] - \
                      self.vgap*row - self.frame_height*(row+1)
        g.view.xmax = g.view.xmin + self.frame_width
        g.view.ymax = g.view.ymin + self.frame_height

    def _calculate_graph_frame(self, rows, cols, hoffset, voffset,
                               hgap, vgap,
                               width_to_height_ratio):
        
        # want to have frames all the same size, but also need to take
        # advantage of the entire canvas.  first check to see which
        # dimension will be more prohibitive (desired ratio is
        # width/height = 1.66)

        # proposed frame height and width of each graph
        self.frame_height = (self.max_frame_height - (voffset[0]+voffset[1]) \
                             - (rows-1)*vgap)/rows
        self.frame_width = (self.max_frame_width - (hoffset[0]+hoffset[1]) \
                            - (cols-1)*hgap)/cols

        # want a particular width/height, see which dimension is
        # more prohibitive and change it
        if self.frame_width/self.frame_height > width_to_height_ratio:
            self.frame_width = width_to_height_ratio*self.frame_height
        else:
            self.frame_height = self.frame_width/width_to_height_ratio;
        
    def multi(self, rows, cols, hoffset=(0.15,0.05), voffset=(0.05,0.15),
              hgap=0.1, vgap=0.1,
              width_to_height_ratio=1.0/0.7):
        """Create a grid of graphs with the given number of <rows> and <cols>
           Makes graph frames all the same size.
        """
        self.graphs_rc = [[None for i in range(cols)] for j in range(rows)]

        # for backward compatibility, allow hoffset and voffset to be
        # floats, which is interpretted as a symmetric offset
        if type(hoffset)==type(0.0):
            hoffset = (hoffset,hoffset)
        if type(voffset)==type(0.0):
            voffset = (voffset,voffset)

        self.hgap = hgap
        self.vgap = vgap
        self.hoffset = hoffset
        self.voffset = voffset
        self.rows = rows
        self.cols = cols

        # compute the frame sizes
        self._calculate_graph_frame(rows,cols,hoffset,voffset,hgap,vgap,
                                    width_to_height_ratio)

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

    def automulti(self, maxrows=5, maxcols=5,
                  hoffset=(0.15,0.05), voffset=(0.05,0.15), 
                  hgap=0.1, vgap=0.1,
                  width_to_height_ratio=1.62):
        """Automatically determine the number of rows and columns to
        add based on the number of graphs currently in the grace.  The
        number of rows and columns is determined by trying to maximize
        the area of canvas that is used (by a non-optimized brute
        force approach).
        """

        # for backward compatibility, allow hoffset and voffset to be
        # floats, which is interpretted as a symmetric offset
        if type(hoffset)==type(0.0):
            hoffset = (hoffset,hoffset)
        if type(voffset)==type(0.0):
            voffset = (voffset,voffset)

        optrows, optcols, optarea = None, None, 0.0
        for rows in range(1,maxrows+1):
            for cols in range(1,maxcols+1):
                if rows*cols>=len(self.graphs):
                    self._calculate_graph_frame(rows,cols,hoffset,voffset,
                                                hgap,vgap,
                                                width_to_height_ratio)
                    area = len(self.graphs)*\
                           self.frame_height*self.frame_width
                    if area>optarea:
                        optrows = rows
                        optcols = cols
                        optarea = area

        # now that I have the optimum layout, do the multi
        self.multi(optrows,optcols,hoffset,voffset,hgap,vgap,
                   width_to_height_ratio)

    def hide_redundant_xaxislabels(self):
        """Hide all x-axis axis labels on the interior of a multigraph that
        are redundant, but only if all labels on the interior of the
        multigraph are the same.
        """

        if not self.graphs_rc:
            message = """
Grace.autohide_multi_labels only works with a multigraph
"""
            raise TypeError,message

        # iterate through each column of graphs
        for c in range(self.cols):
            
            # find the lowest graph
            _rows = self.rows
            for r in range(self.rows-1,-1,-1):
                graph = self.graphs_rc[r][c]
                if graph is not None:
                    _rows = r
                    break
            
            # hide redundant labels in this column
            if _rows>0:

                # find redundant labels
                redundant_axislabel = True
                for r in range(_rows):
                    g = self.graphs_rc[r][c]
                    if not g.xaxis.label==graph.xaxis.label:
                        redundant_axislabel = False
                
                # hide redundant labels
                for r in range(_rows):
                    if redundant_axislabel:
                        self.graphs_rc[r][c].xaxis.label.text = ''
        
    def hide_redundant_xticklabels(self):
        """Hide all x-axis tick labels on the interior of a multigraph that
        are redundant, but only if all labels on the interior of the
        multigraph are the same.
        """

        if not self.graphs_rc:
            message = """
Grace.autohide_multi_labels only works with a multigraph
"""
            raise TypeError,message

        # iterate through each column of graphs
        for c in range(self.cols):
            
            # find the lowest graph
            _rows = self.rows
            for r in range(self.rows-1,-1,-1):
                graph = self.graphs_rc[r][c]
                if graph is not None:
                    _rows = r
                    break
            
            # hide redundant labels in this column
            if _rows>0:

                # find redundant labels
                redundant_ticklabel = True
                for r in range(_rows):
                    g = self.graphs_rc[r][c]
                    if not g.xaxis.ticklabel==graph.xaxis.ticklabel:
                        redundant_ticklabel = False
                
                # hide redundant labels
                for r in range(_rows):
                    if redundant_ticklabel:
                        self.graphs_rc[r][c].xaxis.ticklabel.onoff = "off"
        
    def hide_redundant_xlabels(self):
        """Hide all x-axis tick and axis labels on the interior of a
        multigraph that are redundant, but only if all labels on the
        interior of the multigraph are the same.
        """
        self.hide_redundant_xaxislabels()
        self.hide_redundant_xticklabels()

    def hide_redundant_yaxislabels(self):
        """Hide all y-axis axis labels on the interior of a multigraph that
        are redundant, but only if all labels on the interior of the
        multigraph are the same.
        """

        if not self.graphs_rc:
            message = """
Grace.autohide_multi_labels only works with a multigraph
"""
            raise TypeError,message

        # iterate through each column of graphs
        for r in range(self.rows):
            
            # find the left-most graph
            _cols = 0
            for c in range(self.cols):
                graph = self.graphs_rc[r][c]
                if graph is not None:
                    _cols = c+1
                    break
            
            # hide redundant labels in this column
            if _cols<self.cols:

                # find redundant labels
                redundant_axislabel = True
                for c in range(_cols,self.cols):
                    g = self.graphs_rc[r][c]
                    if not g.yaxis.label==graph.yaxis.label:
                        redundant_axislabel = False
                
                # hide redundant labels
                for c in range(_cols,self.cols):
                    if redundant_axislabel:
                        self.graphs_rc[r][c].yaxis.label.text = ''
        
    def hide_redundant_yticklabels(self):
        """Hide all y-axis tick labels on the interior of a multigraph that
        are redundant, but only if all labels on the interior of the
        multigraph are the same.
        """

        if not self.graphs_rc:
            message = """
Grace.autohide_multi_labels only works with a multigraph
"""
            raise TypeError,message

        # iterate through each column of graphs
        for r in range(self.rows):
            
            # find the lowest graph
            _cols = self.cols
            for c in range(self.cols):
                graph = self.graphs_rc[r][c]
                if graph is not None:
                    _cols = c+1
                    break
            
            # hide redundant labels in this column
            if _cols<self.cols:

                # find redundant labels
                redundant_ticklabel = True
                for c in range(_cols,self.cols):
                    g = self.graphs_rc[r][c]
                    if not g.yaxis.ticklabel==graph.yaxis.ticklabel:
                        redundant_ticklabel = False
                
                # hide redundant labels
                for c in range(_cols,self.cols):
                    if redundant_ticklabel:
                        self.graphs_rc[r][c].yaxis.ticklabel.onoff = "off"
        
    def hide_redundant_ylabels(self):
        """Hide all y-axis tick and axis labels on the interior of a
        multigraph that are redundant, but only if all labels on the
        interior of the multigraph are the same.
        """
        self.hide_redundant_yaxislabels()
        self.hide_redundant_yticklabels()

    def hide_redundant_axislabels(self):
        """Hide all redundant labels.
        """
        self.hide_redundant_xaxislabels()
        self.hide_redundant_yaxislabels()

    def hide_redundant_ticklabels(self):
        """Hide all redundant labels.
        """
        self.hide_redundant_xticklabels()
        self.hide_redundant_yticklabels()

    def hide_redundant_labels(self):
        """Hide all redundant labels.
        """
        self.hide_redundant_xlabels()
        self.hide_redundant_ylabels()

    def set_col_yaxislabel(self,col,label,perpendicular_offset=0.08,
                           opposite_side=False,
                           *args,**kwargs):
        """Add a single y-axis label to a particular column of multi plot.
        """

        # turn off y-axis labels for all panels in this column
        for row in range(self.rows):
            graph = self.graphs_rc[row][col]
            graph.yaxis.label.text = ''

        # determine offsets for resulting new label
        if self.rows%2==1:
            row = int(float(self.rows)/2.0)
            graph = self.graphs_rc[row][col]
            parallel_offset = 0.0
        else:
            row = self.rows/2
            graph = self.graphs_rc[row][col]
            graph_up = self.graphs_rc[row-1][col]
            upmid = 0.5*(graph_up.view.ymax + graph_up.view.ymin)
            dnmid = 0.5*(graph.view.ymax + graph.view.ymin)
            parallel_offset = 0.5*(upmid - dnmid)

        # set label
        graph.yaxis.label.configure(text=label,
                                    place_loc='spec',
                                    place_tup=(parallel_offset,
                                               perpendicular_offset),
                                    *args,**kwargs)

        # place label on the opposite side (rotate text and place tick
        # mark labels there, too)
        if opposite_side:
            for row in range(self.rows):
                graph = self.graphs_rc[row][col]
                graph.yaxis.label.place = 'opposite'
                graph.yaxis.ticklabel.place = 'opposite'
                text = graph.yaxis.label.text
                graph.yaxis.label.text = r"\t{-1 0 0 -1}" + text + r"\t{}"
            
    def set_row_xaxislabel(self,row,label,perpendicular_offset=0.08,
                           opposite_side=False,
                           *args,**kwargs):
        """Add a single x-axis label to a particular row of multi plot.
        """

        # turn off y-axis labels for all panels in this column
        for col in range(self.cols):
            graph = self.graphs_rc[row][col]
            graph.xaxis.label.text = ''

        # determine offsets for resulting new label
        if self.cols%2==1:
            col = int(float(self.cols)/2.0)
            graph = self.graphs_rc[row][col]
            parallel_offset = 0.0
        else:
            col = self.cols/2
            graph = self.graphs_rc[row][col]
            graph_left = self.graphs_rc[row][col-1]
            lmid = 0.5*(graph_left.view.xmax + graph_left.view.xmin)
            rmid = 0.5*(graph.view.xmax + graph.view.xmin)
            parallel_offset = 0.5*(lmid - rmid)

        # set label
        graph.xaxis.label.configure(text=label,
                                    place_loc='spec',
                                    place_tup=(parallel_offset,
                                               perpendicular_offset),
                                    *args,**kwargs)
            

        # place axis and tick labels on the opposite side
        if opposite_side:
            for col in range(self.cols):
                graph = self.graphs_rc[row][col]
                graph.xaxis.label.place = 'opposite'
                graph.xaxis.ticklabel.place = 'opposite'
            
    def align_axislabelx(self,place_tup=(0, 0.08)):
        """Align the x-axis labels with place_tup for all graphs in
        this Grace instance.
        """
        for graph in self.graphs:
            graph.xaxis.label.place_loc = "spec"
            graph.xaxis.label.place_tup = place_tup

    def align_axislabely(self,place_tup=(0, 0.08)):
        """Align the y-axis labels with place_tup for all graphs in
        this Grace instance.
        """
        for graph in self.graphs:
            graph.yaxis.label.place_loc = "spec"
            graph.yaxis.label.place_tup = place_tup

    def align_axislabel(self,xplace_tup=(0, 0.08),yplace_tup=(0,0.08)):
        """Align the x- and y-axis labels with place_tup for all
        graphs in this Grace instance.
        """
        self.align_axislabelx(xplace_tup)
        self.align_axislabely(yplace_tup)

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

class Timestamp(GraceObject):
    """A string representation of the time is created at time of printing."""
    _staticType = 'Timestamp'
    def __init__(self, parent,
                 onoff='off',
                 x = 0.03,
                 y = 0.03,
                 color = 1,
                 font = 4,
                 rot = 0,
                 char_size = 1.0,
                 ):
        GraceObject.__init__(self, parent, locals())

    def __str__(self):
        self.time = time.ctime()
        return \
"""@timestamp %(onoff)s
@timestamp %(x)s, %(y)s
@timestamp color %(color)s
@timestamp rot %(rot)s
@timestamp font %(font)s
@timestamp char size %(char_size)s
@timestamp def "%(time)s" """ % self

