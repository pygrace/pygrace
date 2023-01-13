"""
a high-level interface to a xmgrace project session

The intended purpose of Project is to allow easy programmatic and interactive
command line plotting with convenience functions for the most common commands. 
The Grace UI (or pygrace.interactive.process) can be used if more advanced
low-level functionality needs to be accessed. 

The data model in Grace, (mirrored in Project) goes like this:  Each grace 
session is like virtual sheet of paper called a Project.  Each Project can have 
multiple Graphs, which are sets of axes (use Project.multi() to get multiple
axes in Project).  Each Graph has multiple data Sets.  Data Sets are added to
graphs with the plot and histoPlot functions in Project.

The main python functions are plot() and histoPlot().  See their docstrings 
for usage information.  They can be called with any mix of Numpy arrays,
lists, tuples, or other sequences.  In general, data is considered to be
stored in columns, so a matrix with three vectors x1, x2 and x3 would be:
    
    [ [ x1[0], x2[0], x3[0] ],
      [ x1[1], x2[1], x3[1] ],
      [ x1[2], x2[2], x3[2] ],
      [ x1[3], x2[3], x3[3] ] ]

Here's a simple example of a Project session:

    >>> from pygrace.interactive import project
    >>> p = project.Project()  # A interactive grace project begins
    >>> # Sequence arguments to plot() are X, Y, dy
    >>> p.plot( [1,2,3,4,5], [10, 4, 2, 4, 10], [0.1, 0.4, 0.2, 0.4, 0.1],
    ... symbols=1 )  # A plot with errorbars
         
If you're using a lot of histograms then consider using Scientific Python:
    http://starship.python.net/crew/hinsen/scientific.html

histoPlot() knows how to automatically plot Histogram instances from the 
Scientific.Statistics.Histogram module, so histogramming ends up being simple:
    
    >>> from Scientific.Statistics.Histogram import Histogram
    >>> joe = Histogram( some_data, 40 )  # 40 = number of bins
    >>> p.histoPlot( joe )  # A histogram plot with correct axis limits

An important thing to realize about Project is that it only has a one-way
communications channel with the Grace session.  This means that if you make
changes to your plot in the GUI (e.g. by changing number/layout of graphs)
then Project will have NO KNOWLEDGE of the changes.  This should not often
be an issue, since the only state that Project saves is the number and
layout of graphs, the number of Sets that each graph has, and the hold state
for each graph.
"""
# --UPDATES--
# 03/02/09: ported to numpy by Mike McKerns (mmckerns@caltech.edu)
# 01/10/23: ported to python 3 by Mike McKerns (mmckerns@uqfoundation.org)

__version__ = "0.5.2"
__author__ = "Nathaniel Gray <n8gray@caltech.edu>"
#__date__ = "September 16, 2001"

from . import process
import numpy as np

try:
    from Scientific.Statistics.Histogram import Histogram
    haveHisto = 1
except ImportError:
    haveHisto = 0

__all__ = ['Project','Graph']

class Project:
    
    def __init__(self, *args, **kwds):
        self.grace = process.Process(*args, **kwds)
        self.g = [ Graph(self.grace, 0) ]
        self.curr_graph = self.g[0]
        self.rows = 1
        self.cols = 1
        self.focus(0,0)
    __init__.__doc__ = process.Process.__init__.__doc__
        
    def _send(self, cmd): 
        self.grace.command(cmd)
        
    def _flush(self):
        self.grace.flush()

    def pexec(self, cmd):
        self.grace.command(cmd)
        self.grace.flush()

    def __del__(self):
        """Destroy the pipe but leave the grace window open for interaction.
        This is the best action for the destructor so that unexpected crashes
        don't needlessly destroy plots."""
        self.grace = None

    def exit(self):
        """Nuke the grace session.  (more final than Project.__del__())"""
        self.grace.exit()

    def redraw(self):
        """Refresh the plot"""
        #print('redraw')
        self.grace('redraw')
        
    def multi(self, rows, cols, offset=0.1, hgap=0.1, vgap=0.15):
        """Create a grid of graphs with the given number of <rows> and <cols>
        """
        self._send( 'ARRANGE( %s, %s, %s, %s, %s )' % ( rows, cols, offset, 
                                                        hgap, vgap ) )
        self.rows = rows
        self.cols = cols
        if rows*cols > len(self.g):
            nPlots = len(self.g)
            for i in range( nPlots, (rows*cols - nPlots)+1 ):
                self.g.append( Graph(self.grace, i) )
        # Should we trim the last graphs if we now have *fewer* than before?
        # I say yes.
        elif rows*cols < len(self.g):
            del self.g[rows*cols:]
        self._flush()
        self.redraw()
        
    def saveall(self, filename='xmgrace.agr', format=None):
        """Save the current plot

        Default format is Grace '.agr' file, but other possible formats
        are: x11, postscript, eps, pdf, mif, svg, pnm, jpeg, png, metafile

        Note: Not all drivers are created equal. See the Grace documentation
        or caveats that apply to some of these formats."""
        devs = {'agr':'.agr', 'eps':'.eps', 'jpeg':'.jpeg', 'metafile':'',
                'mif':'', 'pdf':'.pdf', 'png':'.png', 'pnm':'', 
                'postscript':'.ps', 'svg':'', 'x11':''}
        if format is None:
            try:
                format = filename.rsplit('.', 1)[1]
            except IndexError:
                format = ''
        try:
            ext = devs[str.lower(format)]
        except KeyError:
            print('Unknown format. Known formats are\n%s' % list(devs.keys()))
            return
            
        if filename[-len(ext):] != ext:
            filename = filename + ext
        if ext == '.agr':
            self._send('saveall "%s"' % filename)
        else:
            self._send('hardcopy device "%s"' % str.lower(format) )
            self._send('print to "%s"' % filename)
            self._send('print')
        self._flush()
    
        
    def focus( self, row, col ):
        """Set the currently active graph"""
        self.curr_graph = self.g[row*self.cols + col]
        self._send('focus g%s' % self.curr_graph.gID)
        self._send('with g%s' % self.curr_graph.gID)
        self._flush()
        self.redraw()
        
        for i in ['plot', 'histoPlot', 'title', 'subtitle', 'xlabel', 'ylabel',
                  'kill', 'clear', 'legend', 'hold', 'xlimit', 'ylimit',
                  'redraw']:
            setattr( self, i, getattr(self.curr_graph, i) )
        return self.curr_graph        

    def resize( self, xdim, ydim, rescale=1 ):
        """Change the page dimensions (in pp).  If rescale==1, then also
        rescale the current plot accordingly.  Don't ask me what a pp is--I
        don't know."""
        if rescale:
            self._send('page resize %s %s' % (xdim, ydim))
        else:
            self._send('page size %s %s' % (xdim, ydim))

    def __getitem__( self, item ):
        """Access a specific graph.  Can use either p[num] or p[row, col]."""
        if type(item) == type(1):
            return self.g[item]
        elif type(item) == type( () ) and len(item) <= 2:
            if item[0] >= self.rows or item[1] >= self.cols:
                raise IndexError('graph index out of range')
            return self.g[item[0]*self.cols + item[1]]
        else:
            raise TypeError('graph index must be integer or two integers')

class Graph:
    
    def __init__(self, grace, gID):

        self._hold = 0       # Set _hold=1 to add datasets to a graph
        self.grace = grace
        self.nSets = 0
        self.gID = gID
    
    def _send(self, cmd):
        self.grace.command(cmd)
        
    def _flush(self):
        self.grace.flush()

    def pexec(self, cmd):
        self.grace.command(cmd)
        self.grace.flush()

    def _send_2(self, var, X, Y):
        send = self.grace.command
        for i in range(len(X)):
            send( 'g%s.s%s point %s, %s' % (self.gID, var, X[i], Y[i]) )
            if i%50 == 0:
                self._flush()
        self._flush()

    def _send_3(self, var, X, Y, Z):
        self._send_2(var, X, Y)
        send = self.grace.command
        for i in range(len(Z)):
            send( 'g%s.s%s.y1[%s] = %s' % 
                    (self.gID, var, i, Z[i]) )
            if i%50 == 0:
                self._flush()
        self._flush()

    def hold(self, onoff=None):
        """Turn on/off overplotting for this graph.
        
        Call as hold() to toggle, hold(1) to turn on, or hold(0) to turn off.
        Returns the previous hold setting.
        """
        lastVal = self._hold
        if onoff is None:
            self._hold = not self._hold
            return lastVal
        if onoff not in [0, 1]:
            raise RuntimeError("Valid arguments to hold() are 0 or 1.")
        self._hold = onoff
        return lastVal
    
    def title(self, titlestr):
        """Change the title of the plot"""
        self._send('with g%s' % self.gID)
        self._send('title "' + str(titlestr) + '"')
        self.redraw()
        
    def subtitle(self, titlestr):
        """Change the subtitle of the plot"""
        self._send('with g%s' % self.gID)
        self._send('subtitle "' + str(titlestr) + '"')
        self.redraw()
        
    def redraw(self):
        """Refresh the plot"""
        self.grace('redraw')
        
    def xlabel(self, label):
        """Change the x-axis label"""
        self._send('with g%s' % self.gID)
        self._send('xaxis label "' + str(label) + '"')
        self.redraw()
        
    def ylabel(self, label):
        """Change the y-axis label"""
        self._send('with g%s' % self.gID)
        self._send('yaxis label "' + str(label) + '"')
        self.redraw()
        
    def xlimit(self, lower=None, upper=None):
        """Set the lower and/or upper bounds of the x-axis."""
        self._limHelper( 'x', lower, upper)
        
    def ylimit(self, lower=None, upper=None):
        """Set the lower and/or upper bounds of the y-axis."""
        self._limHelper( 'y', lower, upper)
    
    def _limHelper(self, ax, lower, upper):
        send = self._send
        if lower is not None:
            send('with g%s; world %smin %s' % (self.gID, ax, lower))
        if upper is not None:
            send('with g%s; world %smax %s' % (self.gID, ax, upper))
        self.redraw()
        
    def kill(self):
        """Kill the plot"""
        self._send('kill g%s' % self.gID)
        self._send('g%s on' % self.gID)
        self.redraw()
        self.nSets = 0
        self._hold = 0
        
    def clear(self):
        """Erase all lines from the plot and set hold to 0"""
        for i in range(self.nSets):
            self._send('kill g%s.s%s' % (self.gID, i))
        self.redraw()
        self.nSets=0
        self._hold=0
        
    def legend(self, labels):
        """Set the legend labels for the plot
        Takes a list of strings, one string per dataset on the graph.
        Note: <ctrl>-L allows you to reposition legends using the mouse.
        """
        if len(labels) != self.nSets:
            raise RuntimeError('Wrong number of legends (%s) for number' \
                    ' of lines in plot (%s).' % (len(labels), self.nSets))
            
        for i in range(len(labels)):
            self._send( ('g%s.s%s legend "' % (self.gID, i)) + labels[i] + '"' )
            self._send('with g%s; legend on' % self.gID)
        self.redraw()
        
    def histoPlot(self, y, x_min=0, x_max=None, dy=None, edges=0, 
                  fillcolor=2, edgecolor=1, labeled=0):
        """Plot a histogram

        y contains a vector of bin counts
        By default, bin counts are plotted against bin numbers unless 
        x_min and/or x_max are specified.
        By default, edges == 0, where x_min and x_max specify the lower
        and upper edges of the first and last bins, respectively. Otherwise,
        x_min and x_max specify the centers of the first and last bins.
        If dy is specified symmetric errorbars are plotted.
        fillcolor and edgecolor are color numbers (0-15)
        If labeled is set to 1 then labels are placed at each bin to show
        the bin count.

        Note that this function can create *two* datasets in grace if you
        specify error bars."""
        if haveHisto and isinstance(y, Histogram):
            self.histoPlot( y.array[:,1], x_min=y.min, x_max=y.max, edges=1,
                            dy=dy, fillcolor=fillcolor, edgecolor=edgecolor, 
                            labeled=labeled )
            return
        
        # this is going to be ugly
        y = np.array(y)
        if x_max is None:
            x_max = len(y)-1 + x_min
            edges = 0
        
        if x_max <= x_min:
            raise RuntimeError("x_max must be > x_min")
            
        if dy is not None:
            if len(dy) != len(y):
                raise RuntimeError('len(dy) != len(y)')
            dy = np.array(dy)
        
        if not self._hold: self.clear()
        
        if edges:
            # x_min and x_max are the outside edges of the first/last bins
            binwidth = (x_max-x_min)/float(len(y))
            edge_x = np.arange(len(y)+1 , dtype='d')*binwidth + x_min
            cent_x = (edge_x + 0.5*binwidth)[0:-1]
        else:
            # x_min and x_max are the centers of the first/last bins
            binwidth = (x_max-x_min)/float(len(y)-1)
            cent_x = np.arange(len(y), dtype='d')*binwidth + x_min
            edge_x = cent_x - 0.5*binwidth
            edge_x = np.resize(edge_x, (len(cent_x)+1,))
            edge_x[-1] = edge_x[-2] + binwidth
        edge_y = y.copy() #np.zeros(len(y)+1)
        edge_y = np.resize(edge_y, (len(y)+1,))
        edge_y[-1] = 0
        
        # Draw the edges:
        me = 'g%s.s%s ' % (self.gID, self.nSets)
        self._send( me + 'type xy' )
        self._send( me + 'dropline on' )
        self._send( me + 'line type 3' ) # step to right
        self._send( me + 'line color ' + str(edgecolor) )
        if fillcolor is not None:
            self._send( me + 'fill type 2' ) #Solid
            self._send( me + 'fill color ' + str(fillcolor) )
        if labeled:
            self._send( me + 'avalue on' )
        self._flush()
        self._send_2( self.nSets, edge_x, edge_y )
        self.nSets = self.nSets + 1
        
        # Draw the errorbars (if given)
        if dy is not None:
            me = 'g%s.s%s ' % (self.gID, self.nSets)
            self._send( me + 'type xydy' )
            self._send( me + 'line linestyle 0' ) #No connecting lines
            self._send( me + 'errorbar color ' + str(edgecolor) )
            self._flush()
            self._send_3( self.nSets, cent_x, y, dy )
            self.nSets = self.nSets + 1
            #self._errPlot( cent_x, y, dy )
            
        self._send('with g%s' % self.gID)
        self._send('world ymin 0.0') # Make sure the y-axis starts at 0
        self._send('autoscale')
        self._send('redraw')
        self._flush()
        
    def _errPlot(self, X, Y, dy=None, symbols=None, styles=None, pType = 'xydy' ):
        """Line plot with error bars -- for internal use only
        Do not use this!  Use plot() with dy=something instead."""
        
        if dy is None:
            dy = Y
            Y = X
            X = np.arange(X.shape[0])
            
        # Guarantee rank-2 matrices
        if len(X.shape) == 1:
            X.shape = (X.shape[0], 1)
        if len(Y.shape) == 1:
            Y.shape = (Y.shape[0], 1)
        if len(dy.shape) == 1:
            dy.shape = (dy.shape[0], 1)
        
        if not ( Y.shape == dy.shape and
                 X.shape[0] == Y.shape[0] and
                 ( X.shape[1] == Y.shape[1] or X.shape[1] == 1 ) ):
            raise RuntimeError('X, Y, and dy have mismatched shapes')
            
        if not self._hold: self.clear()
        
        for i in range(self.nSets, Y.shape[1] + self.nSets):
            me = 'g%s.s%s ' % (self.gID, i)
            self._send( me + 'on')
            self._send( me + 'type ' + pType)
            mycolor = (i%15)+1
            self._send( '%s line color %s' % (me, mycolor) )
            self._send( '%s errorbar color %s' % (me, mycolor) )
            
            if symbols is not None:
                self._send( me + 'symbol %s' % ((i%10) + 1) ) # From 1 to 10
                self._send( '%s symbol color %s' % (me, mycolor) )
            if styles is not None:
                self._send( me + 'line linestyle %s' %((i%8) + 1) ) # 1 to 8
            self._flush()

        if X.shape[1] == 1:
            for i in range(Y.shape[1]):
                self._send_3( i+self.nSets, X[:,0], Y[:,i], dy[:,i] )
                # Send an upper and lower line too so that autoscaling works
                self._send_2( i+self.nSets+Y.shape[1], X[:,0], Y[:,i]+dy[:,i] )
                self._send_2( i+self.nSets+2*Y.shape[1], X[:,0], 
                              Y[:,i]-dy[:,i] )
        else:
            for i in range(Y.shape[1]):
                self._send_3( i+self.nSets, X[:,i], Y[:,i], dy[:,i] )
                self._send_2( i+self.nSets+Y.shape[1], X[:,i], Y[:,i]+dy[:,i] )
                self._send_2( i+self.nSets+2*Y.shape[1], X[:,i], 
                              Y[:,i]-dy[:,i] )

        self._send('with g%s' % self.gID)
        self._send('autoscale')
        #self._send('redraw')
        self.nSets = self.nSets + Y.shape[1]
        # Kill off the extra lines above/below
        for i in range(self.nSets, self.nSets+2*Y.shape[1]):
            self._send( 'KILL G%s.S%s' % (self.gID, i) )
        self._send('redraw')
        self._flush()

    def plot(self, X, Y=None, dy=None, symbols=None, styles=None):
        """2-D line plot, with or without error bars

        The arguments should be Numpy arrays of equal length.
        X, Y, and dy can be rank-1 or rank-2 arrays (vectors or matrices).
        In rank-2 arrays, each column is treated as a dataset. X can be
        rank-1, even if Y and DY are rank-2, as long as len(X) == len(Y[:,0]).
            
        If dy is not None then it must be the same shape as Y, and
        symmetric error bars will be plotted with total height 2*dy.
        Setting symbols=1 will give each dataset a unique symbol.
        Setting styles=1 will give each dataset a unique linestyle
        """

        X = np.array(X)
        # if there's no Y, then just use X
        if Y is None:
            Y = X
            X = np.arange(X.shape[0])
        else:
            Y = np.array(Y)
        
        if dy is not None:
            dy = np.array(dy)
            self._errPlot(X, Y, dy, symbols=symbols, styles=styles)
            return

        # Guarantee rank-2 matrices
        if len(X.shape) == 1:
            X.shape = (X.shape[0], 1)
        if len(Y.shape) == 1:
            Y.shape = (Y.shape[0], 1)

        if X.shape[0] != Y.shape[0] or (  # Different number of points per line
              X.shape[1] != X.shape[1] and  # Different number of lines
              X.shape[1] != 1):             # But if X is just 1 line it's ok.
            raise RuntimeError('X and Y have mismatched shapes')
            
        ############# Grace commands start here ###########
        
        if not self._hold: self.clear()
            
        pType = 'xy' # At some point this might become an option
        
        for i in range(self.nSets, Y.shape[1] + self.nSets):
            me = 'g%s.s%s ' % (self.gID, i)
            self._send( me + 'on')
            self._send( me + 'type ' + pType)
            self._send( '%s line color %s' % (me, (i%15)+1) )
            if symbols is not None:
                self._send( me + 'symbol %s' % ((i%15) + 1) ) # From 1 to 15
                self._send( '%s symbol color %s' % (me, (i%15)+1) )
            if styles is not None:
                self._send( me + 'line linestyle %s' %((i%8) + 1) ) # 1 to 8
            self._flush()

        if X.shape[1] == 1:
            for i in range(Y.shape[1]):
                self._send_2( i+self.nSets, X[:,0], Y[:,i] )
        else:
            for i in range(Y.shape[1]):
                self._send_2( i+self.nSets, X[:,i], Y[:,i] )

        self._send('with g%s' % self.gID)
        self._send('autoscale')
        self._send('redraw')
        self._flush()
        
        self.nSets = self.nSets + Y.shape[1]

