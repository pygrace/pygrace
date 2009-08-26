import time
import os

from base import GraceObject
from graph import Graph
from drawing_objects import DrawingObject
from colors import DefaultColorScheme
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
                 **kwargs
		 ): 
        GraceObject.__init__(self, None, locals())

	self.timestamp = Timestamp(self)

        # set these first, so that children inherit this color scheme
        self.colors = colors or DefaultColorScheme()
        self.fonts = default_fonts

        self._graphIndex = INDEX_ORIGIN
	self.graphs = []

        self.drawing_objects = []
        
        # maximum frame ratios in viewport units
        self.get_canvas_dimensions()

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

    def get_canvas_dimensions(self):
        """Get dimensions of Grace canvas
        """
        # maximum canvas ratios in viewport units
        if self.height>self.width:
            self.max_canvas_width = 1.0
            self.max_canvas_height = float(self.height)/float(self.width)
        else:
            self.max_canvas_width = float(self.width)/float(self.height)
            self.max_canvas_height = 1.0
        return self.max_canvas_width,self.max_canvas_height

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
        drawingObject = cls(self, *args, **kwargs)
        self.drawing_objects.append(drawingObject)

        # return the instance of the drawing object
        return drawingObject

    def get_graph(self, index):
        return self.graphs[index]

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

    #--------------------------------------------------------------------------
    # methods for rescaling graphs 
    #--------------------------------------------------------------------------
    def autoscale(self, padx=0,pady=0):
        for graph in self.graphs:
            graph.autoscale(padx=padx,pady=pady)

    def autoscalex_same(self, pad=0, graphs=(), exclude_graphs=()):
        """Autoscale all x-axes to have the same world coordinates
        """

        # make sure none of the graphs 
        if graphs and exclude_graphs:
            message = """keyword arguments 'graphs' and 'exclude_graphs' 
can not be used simultaneously.
"""
            raise TypeError,message
        
        # only autoscale these graphs
        if graphs:
            graphs = set(graphs)
        else:
            graphs = set(self.graphs)

        # make sure none of the excluded graphs are in 'graphs'
        for graph in exclude_graphs:
            graphs.remove(graph)
        graphs = tuple(graphs)

        # find the world coordinates of all of the graphs
        worlds = []
        for graph in graphs:
            graph.autoscalex(pad=pad)
            worlds.append(graph.get_world())
        
        # find the least restrictive world coordinates to share for
        # all graphs
        xmins,ymins,xmaxs,ymaxs = zip(*worlds)
        xmin = min(xmins)
        xmax = max(xmaxs)
        for graph in graphs:
            world = graph.get_world()
            graph.set_world(xmin,world[1],xmax,world[3])

        # set the ticks now
        for graph in graphs:
            graph.autotickx()

    def autoscaley_same(self,pad=0, graphs=(), exclude_graphs=()):
        """Autoscale all y-axes to have the same world coordinates
        """

        # make sure none of the graphs 
        if graphs and exclude_graphs:
            message = """keyword arguments 'graphs' and 'exclude_graphs' 
can not be used simultaneously.
"""
            raise TypeError,message
        
        # only autoscale these graphs
        if graphs:
            graphs = set(graphs)
        else:
            graphs = set(self.graphs)

        # make sure none of the excluded graphs are in 'graphs'
        for graph in exclude_graphs:
            graphs.remove(graph)
        graphs = tuple(graphs)

        # find the world coordinates of all of the graphs
        worlds = []
        for graph in graphs:
            graph.autoscaley(pad=pad)
            worlds.append(graph.get_world())
        
        # find the least restrictive world coordinates to share for
        # all graphs
        xmins,ymins,xmaxs,ymaxs = zip(*worlds)
        ymin = min(ymins)
        ymax = max(ymaxs)
        for graph in graphs:
            world = graph.get_world()
            graph.set_world(world[0],ymin,world[2],ymax)

        # set the ticks now
        for graph in graphs:
            graph.autoticky()

    def autoscale_same(self,padx=0,pady=0, graphs=(), exclude_graphs=()):
        """Autoscale all graphs in a this MultiGrace to have the same x,y
        world coordinates.
        """
        self.autoscalex_same(pad=padx,graphs=graphs,
                             exclude_graphs=exclude_graphs)
        self.autoscaley_same(pad=pady,graphs=graphs,
                             exclude_graphs=exclude_graphs)

    def set_world_same(self,xmin,ymin,xmax,ymax):
        """Rescale all graphs in a MultiGrace to have the same x,y world
        coordinates.
        """
        for graph in self.graphs:
            graph.set_world(xmin,ymin,xmax,ymax)

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
                 **kwargs
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

