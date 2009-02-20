from PyGrace.grace import Grace

class MultiGrace(Grace):
    def __init__(self,rows=None,cols=None,hgap=0.1,vgap=0.1,
                 hoffset=(0.15,0.05),voffset=(0.05,0.15),
		 width_to_height_ratio=1.0/0.7,*args,**kwargs): 
        Grace.__init__(self,*args,**kwargs)

        # add all of the keyword arguments as local attributes
        self._set_kwargs_attributes(locals())

        # useful for obtaining a graph from a particular row or column
        self.graphs_rc = []

        # used for fomatting multiple graphs
        self.frame_height = None   # height of one graph
        self.frame_width = None    # width of one graph

        # if rows and cols have been specified, add graphs to the
        # MultiGrace
        if self.rows is not None and self.cols is not None:
            for i in range(self.rows*self.cols):
                self.add_graph()
            self.multi(self.rows,self.cols,self.hoffset,self.voffset,
                       self.hgap,self.vgap,self.width_to_height_ratio)

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
        g.view.ymin = self.max_canvas_height - self.voffset[0] - \
                      self.vgap*row - self.frame_height*(row+1)
        g.view.xmax = g.view.xmin + self.frame_width
        g.view.ymax = g.view.ymin + self.frame_height

    def _calculate_graph_frame(self):
        
        # want to have frames all the same size, but also need to take
        # advantage of the entire canvas.  first check to see which
        # dimension will be more prohibitive (desired ratio is
        # width/height = 1.66)
        self.get_canvas_dimensions()

        # proposed frame height and width of each graph
        self.frame_height = (self.max_canvas_height - 
                             (self.voffset[0]+self.voffset[1]) \
                             - (self.rows-1)*self.vgap)/self.rows
        self.frame_width = (self.max_canvas_width - 
                            (self.hoffset[0]+self.hoffset[1]) \
                            - (self.cols-1)*self.hgap)/self.cols

        # want a particular width/height, see which dimension is
        # more prohibitive and change it
        if self.frame_width/self.frame_height > self.width_to_height_ratio:
            self.frame_width = self.width_to_height_ratio*self.frame_height
        else:
            self.frame_height = self.frame_width/self.width_to_height_ratio
        
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

        self.rows = rows
        self.cols = cols
        self.hgap = hgap
        self.vgap = vgap
        self.hoffset = hoffset
        self.voffset = voffset
        self.width_to_height_ratio = width_to_height_ratio

        # compute the frame sizes
        self._calculate_graph_frame()

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

    def automulti(self, maxrows=5, maxcols=7,
                  hoffset=(0.15,0.05), voffset=(0.05,0.15), 
                  hgap=0.1, vgap=0.1,
                  width_to_height_ratio=1.0/0.7):
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

        # set attributes here
        self.hoffset = hoffset
        self.voffset = voffset
        self.hgap = hgap
        self.vgap = vgap
        self.width_to_height_ratio = width_to_height_ratio

        # find optimal number of rows and columns that use the area
        optrows, optcols, optarea = None, None, 0.0
        for rows in range(1,maxrows+1):
            for cols in range(1,maxcols+1):
                if rows*cols>=len(self.graphs):
                    self.rows = rows
                    self.cols = cols
                    self._calculate_graph_frame()
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
                    if g is not None and g.xaxis.label!=graph.xaxis.label:
                        redundant_axislabel = False
                
                # hide redundant labels
                for r in range(_rows):
                    if redundant_axislabel:
                        if self.graphs_rc[r][c] is not None:
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
                    if (g is not None and 
                        g.xaxis.ticklabel!=graph.xaxis.ticklabel):
                        redundant_ticklabel = False
                
                # hide redundant labels
                for r in range(_rows):
                    if redundant_ticklabel:
                        if self.graphs_rc[r][c] is not None:
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
                    if g is not None and g.yaxis.label!=graph.yaxis.label:
                        redundant_axislabel = False
                
                # hide redundant labels
                for c in range(_cols,self.cols):
                    if redundant_axislabel:
                        if self.graphs_rc[r][c] is not None:
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
                    if (g is not None and 
                        g.yaxis.ticklabel!=graph.yaxis.ticklabel):
                        redundant_ticklabel = False
                
                # hide redundant labels
                for c in range(_cols,self.cols):
                    if redundant_ticklabel:
                        if self.graphs_rc[r][c] is not None:
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
                           opposite_side=False,rowspan=(None,None),
                           *args,**kwargs):
        """Add a single y-axis label to a particular column of multi plot.
        rowspan specifies the rows that label spans.  To span over
        rows 0-1, for example, specify rowspan=(0,1).
        rowspan=(None,None) is default and understood to mean all rows
        in that column.
        """

        # interpret default rowspan
        rowspan = list(rowspan)
        if rowspan[0] is None:
            rowspan[0] = 0
        if rowspan[1] is None:
            rowspan[1] = self.rows-1
        rowspan = tuple(rowspan)

        # make sure rowspan[0]<=rowspan[1]
        if rowspan[0]>rowspan[1]:
            message = """
rowspan[0]>rowspan[1].  Must have rowspan[0]<=rowspan[1] in 
set_row_xaxislabel.
"""
            raise TypeError, message

        # turn off y-axis labels for all panels in this column
        for row in range(rowspan[0],rowspan[1]+1):
            graph = self.graphs_rc[row][col]

            # To avoid error with trying to set NoneType attributes
            if graph is not None:
                graph.yaxis.label.text = ''

        # determine offsets for resulting new label
        if (rowspan[1]-rowspan[0]+1)%2==1:
            row = int(float(rowspan[1]-rowspan[0]+1)/2.0+rowspan[0])
            graph = self.graphs_rc[row][col]
            parallel_offset = 0.0
        else:
            row = (rowspan[1]-rowspan[0]+1)/2 + rowspan[0]
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
            for row in range(rowspan[0],rowspan[1]+1):
                graph = self.graphs_rc[row][col]
                graph.yaxis.label.place = 'opposite'
                graph.yaxis.ticklabel.place = 'opposite'
                text = graph.yaxis.label.text
                graph.yaxis.label.text = r"\t{-1 0 0 -1}" + text + r"\t{}"
            
    def set_row_xaxislabel(self,row,label,perpendicular_offset=0.08,
                           opposite_side=False,colspan=(None,None),
                           *args,**kwargs):
        """Add a single x-axis label to a particular row of multi plot.
        colspan specifies the cols that label spans.  To span over
        cols 0-1, for example, specify colspan=(0,1).
        colspan=(None,None) is default and understood to mean all cols
        in that row.
        """

        # interpret default colspan
        colspan = list(colspan)
        if colspan[0] is None:
            colspan[0] = 0
        if colspan[1] is None:
            colspan[1] = self.cols-1
        colspan = tuple(colspan)

        # make sure colspan[0]<=colspan[1]
        if colspan[0]>colspan[1]:
            message = """
colspan[0]>colspan[1].  Must have colspan[0]<=colspan[1] in 
set_row_xaxislabel.
"""
            raise TypeError, message

        # turn off y-axis labels for all panels in this column
        for col in range(colspan[0],colspan[1]+1):
            graph = self.graphs_rc[row][col]

            # To avoid error with trying to set NoneType attributes
            if graph is not None:
                graph.xaxis.label.text = ''

        # determine offsets for resulting new label
        if (colspan[1]-colspan[0]+1)%2==1:
            col = int(float(colspan[1]-colspan[0]+1)/2.0+colspan[0])
            graph = self.graphs_rc[row][col]
            parallel_offset = 0.0
        else:
            col = (colspan[1]-colspan[0]+1)/2+colspan[0]
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
            for col in range(colspan[0],colspan[1]+1):
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

