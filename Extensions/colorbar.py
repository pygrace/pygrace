import math

from PyGrace.graph import Graph
from PyGrace.dataset import DataSet
from PyGrace.drawing_objects import DrawBox
from PyGrace.axis import LINEAR_SCALE, LOGARITHMIC_SCALE

class SolidRectangle(DataSet):
    """A dataset that shows up as a solid rectangle.

    data for the creating of the SolidRectangle must be the two
    corners of the rectangle.
    """
    def __init__(self, color, *args, **kwargs):
        DataSet.__init__(self, *args, **kwargs)
        if len(self.data) != 2:
            raise TypeError, 'Data for SolidRectangle MUST contain 2 points'
        x0 = self.data[0][0]
        x1 = self.data[1][0]
        y0 = min(self.data[0][1], self.data[1][1])
        y1 = max(self.data[0][1], self.data[1][1])
        self.data = [(x0, y1), (x1, y1), (x1, y0)]
        self.symbol.configure(shape=0)
        self.line.configure(linewidth=0, color=color)
        self.fill.configure(type=2, rule=0, color=color)
        self.baseline.configure(type=1)
    
class SolidOutlinedRectangle(DataSet):
    """A dataset that shows up as a solid rectangle with an outline.

    data for the creating of the SolidOutlinedRectangle must be the two
    corners of the rectangle.
    """
    def __init__(self, color, outline_color=1, *args, **kwargs):
        DataSet.__init__(self, *args, **kwargs)
        if len(self.data) != 2:
            raise TypeError, 'Data for SolidOutlinedRectangle MUST contain 2 points'
        x0 = self.data[0][0]
        x1 = self.data[1][0]
        y0 = min(self.data[0][1], self.data[1][1])
        y1 = max(self.data[0][1], self.data[1][1])
        self.data = [(x0, y1), (x1, y1), (x1, y0), (x0, y0), (x0,y1)]
        self.symbol.configure(shape=0)
        self.line.configure(linewidth=0, color=outline_color)
        self.fill.configure(type=2, rule=0, color=color)
        self.baseline.configure(type=1)
    

class ColorBar(Graph):
    def __init__(self, domain=(), scale=LINEAR_SCALE, autoscale=True,
                 color_range=(), *args, **kwargs):
        Graph.__init__(self,*args,**kwargs)

        # turn off the xaxis labels
        self.xaxis.ticklabel.onoff = "off"
        self.xaxis.tick.onoff = "off"

        # specify the scale on the yaxis
        self.set_scale(scale)

        # place labels on opposite side
        self.yaxis.ticklabel.place = 'opposite'
        self.yaxis.label.place = 'opposite'

        # make frame super skinny
        self.view.xmin = self.view.xmax - 0.1*(self.view.ymax - self.view.ymin)

        # remember the range of colors to be used
        if not color_range:
            if self.parent is None:
                self.color_range = []
            else:
                self.color_range = range(2,len(self.parent.colors))
        else:
            self.color_range = color_range

        # set the domain
        if domain:
            self.set_domain(domain,autoscale)
        else:
            self.set_domain((0,1),autoscale)

    def set_scale(self,scale):
        if scale==LOGARITHMIC_SCALE:
            self.logy()
        else:
            self.liny()

    # not sure why this is here but it is messing with things
    def _epsilon(self):
        """This is used to slightly alter the domain to correctly
        match values with colors that belong on this colorbar.
        """
        
        # slightly alter domain to get rid of numerical errors
        n = len(self.color_range)
        return 0.0001/float(n)

    def get_domain(self):
        return self.world.ymin,self.world.ymax

    def set_domain(self,domain,autoscale=True,pad=0):
        """set the domain of the yaxis by (1) adding a dummy dataset,
        (2) autoscaling, and (3) removing dummy dataset.
        """

        # slightly alter domain to get rid of numerical errors
        self.set_world(0,domain[0],1,domain[1])
        if autoscale:
            self.autoscale(pady=pad)
    
    def autoscalex(self, pad=0, only_visible=True):
        """Over ride autoscale behavior of Graph.
        """
        dataset = self.add_dataset([(self.world.xmin,self.world.ymin),
                                    (self.world.xmax,self.world.ymax)])
        Graph.autoscalex(self,pad=pad)
        self.datasets.pop()
        self._datasetIndex -= 1
    
    def autoscaley(self, pad=0, only_visible=True):
        """Over ride autoscale behavior of Graph.
        """
        dataset = self.add_dataset([(self.world.xmin,self.world.ymin),
                                    (self.world.xmax,self.world.ymax)])
        Graph.autoscaley(self,pad=pad)
        self.datasets.pop()
        self._datasetIndex -= 1

    def add_colors(self):
        """add colors
        first two colors are white and black, skip them
        """
        (xmin,ymin,xmax,ymax) = self.get_world()
        for i in range(len(self.color_range)):
            if self.yaxis.scale==LINEAR_SCALE:
                y0 = ymin + (ymax - ymin)*float(i)/float(len(self.color_range))
                y1 = ymin + (ymax - ymin)*float(i+1)/float(len(self.color_range))
            elif self.yaxis.scale==LOGARITHMIC_SCALE:
                y0 = ymin * math.pow(ymax/ymin,float(i)/float(len(self.color_range)))
                y1 = ymin * math.pow(ymax/ymin,float(i+1)/float(len(self.color_range)))
            else:
                message = "'%s' is an unknown axis type"%self.xaxis.scale
                raise TypeError,message
            # add a three-point dataset to show-up as a solid rectangle
            the_dataset = self.add_dataset([(0, y0), (1, y1)],
                                           SolidRectangle,
                                           self.color_range[i])
            self.move_dataset_to_back(the_dataset)

    def set_label(self,label):
        """Set the axis label. 
        """

        # this also rotates the axis label properly
        self.yaxis.label.text = r"\t{-1 0 0 -1}" + label + r"\t{}"

    def z2color(self,z):
        """Get the color that is associated with a particular value,
        z.
        """

        # fudge the bounds of the world coordinates for rounding problems
        (xmin,ymin,xmax,ymax) = self.get_world()
        if self.yaxis.scale==LINEAR_SCALE:
            ymin -= self._epsilon()
            ymax += self._epsilon()
        else:
            ymin /= 1.0 + self._epsilon()
            ymax *= 1.0 + self._epsilon()

        # find color
        n = len(self.color_range)
        if z<ymin or z>ymax:
            return None
        elif self.yaxis.scale==LINEAR_SCALE:
            i = int(float(n)*(z - ymin)/(ymax-ymin))
            return self.color_range[i]
        else:
            i = int(float(n)*math.log(z/ymin)/math.log(ymax/ymin))
            return self.color_range[i]

    def color2zs(self,color):
        """Get the range of values (zs) associated with a particular color,
        color.
        """

        i = self.color_range.index(color)
        n = len(self.color_range)
        (xmin,ymin,xmax,ymax) = self.get_world()
        if self.yaxis.scale==LINEAR_SCALE:
            zmin = float(i)/float(n)*(ymax - ymin) + ymin
            zmax = float(i+1)/float(n)*(ymax - ymin) + ymin
        else:
            zmin = ymin*math.power(zmax/zmin,float(i)/float(n))
            zmax = ymin*math.power(zmax/zmin,float(i+1)/float(n))

        return zmin,zmax

    def __str__(self):
        """Override the __str__ functionality to draw the colorbar at
        draw time.
        """
        self.add_colors()
        return Graph.__str__(self)
