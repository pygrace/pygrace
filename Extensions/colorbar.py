import math
from PyGrace.graph import Graph
from PyGrace.drawing_objects import DrawBox
from PyGrace.axis import LINEAR_SCALE, LOGARITHMIC_SCALE

class ColorBar(Graph):
    def __init__(self, domain=(0,1), scale=LINEAR_SCALE, autoscale=True,
                 color_range=[], *args, **kwargs):
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
        if len(color_range)==0:
            self.color_range = range(2,len(self.parent.colors))
        else:
            self.color_range = color_range

        # set the domain
        self.set_domain(domain,autoscale)

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

    def set_domain(self,domain,autoscale=True):
        """set the domain of the yaxis by (1) adding a dummy dataset,
        (2) autoscaling, and (3) removing dummy dataset.
        """

        # slightly alter domain to get rid of numerical errors
        if autoscale:
            dataset = self.add_dataset(zip([0,1],domain))
            self.autoscale()
            self.datasets.pop()
            self._datasetIndex -= 1
        else:
            self.set_world(0,domain[0],1,domain[1])

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
            self.add_drawing_object(DrawBox,
                                    lowleft = (0,y0),
                                    upright = (1,y1),
                                    loctype="world",
                                    fill_color=self.color_range[i],
                                    color=self.color_range[i],
                                    linestyle=0,
                                    linewidth=0,
                                    )

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
