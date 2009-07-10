from PyGrace.grace import Grace
from PyGrace.graph import Graph, INDEX_ORIGIN, Legend
from PyGrace.dataset import DataSet
from PyGrace.axis import Tick, TickLabel, Axis, AxisLabel, \
     LINEAR_SCALE, LOGARITHMIC_SCALE
from PyGrace.Extensions.colorbar import ColorBar
from PyGrace.Extensions.panel import PanelLabel

#------------------------------------------------------------------------------
# The 'El' style of data sets
#------------------------------------------------------------------------------
class ElRightStairsDataSet(DataSet):
    def __init__(self, color, *args, **kwargs):
        DataSet.__init__(self, *args, **kwargs)

        # make right stairs dataset (no symbols)
        self.symbol.configure(shape=0, fill_color=color, color=color)
        self.line.configure(type=3, linestyle=1, color=color)

class ElLineDataSet(DataSet):
    def __init__(self, color, *args, **kwargs):
        DataSet.__init__(self, *args, **kwargs)

        # line only (no symbols)
        self.symbol.configure(shape=0, fill_color=color, color=color)
        self.line.configure(type=1, linestyle=1, color=color)

class ElShadedDataSet(DataSet):
    def __init__(self, color, *args, **kwargs):
        DataSet.__init__(self, *args, **kwargs)

        # shading and line
        self.symbol.configure(shape=0, fill_color=color, color=color)
        self.line.configure(type=1, linestyle=1, color=color)
        self.fill.configure(type=2, color=color, pattern=1)
        self.baseline.type = 3

class ElCircleDataSet(DataSet):
    def __init__(self, color, *args, **kwargs):
        DataSet.__init__(self, *args, **kwargs)

        # make right stairs dataset (no symbols)
        self.symbol.configure(shape=1, fill_color=color, color=1)
        self.line.configure(type=0, linestyle=0, color=color)

#------------------------------------------------------------------------------
# The 'El' style of graphs
#------------------------------------------------------------------------------
class ElTick(Tick):
    def __init__(self, *args, **kwargs):
        Tick.__init__(self, *args, **kwargs)

        # alter the tick sizes
        self.major_size = 1.25
        self.minor_size = 0.75

class ElLinTick(ElTick):
    def __init__(self, *args, **kwargs):
        ElTick.__init__(self, *args, **kwargs)

        # alter the tick sizes
        self.major = 0.2

class ElLogTick(ElTick):
    def __init__(self, *args, **kwargs):
        ElTick.__init__(self, *args, **kwargs)

        # alter the tick sizes
        self.major = 10
        self.minor_ticks = 8

class ElTickLabel(TickLabel):
    def __init__(self, *args, **kwargs):
        TickLabel.__init__(self, *args, **kwargs)

        # set char size
        self.char_size = 1.0

class ElLinTickLabel(ElTickLabel):
    def __init__(self, *args, **kwargs):
        ElTickLabel.__init__(self, *args, **kwargs)

        # set defaults
        self.format = "decimal"
        self.prec = 1

class ElLogTickLabel(ElTickLabel):
    def __init__(self, *args, **kwargs):
        ElTickLabel.__init__(self, *args, **kwargs)

        # set defaults
        self.format = "power"
        self.prec = 0

class ElAxisLabel(AxisLabel):
    def __init__(self, *args, **kwargs):
        AxisLabel.__init__(self, *args, **kwargs)

        # set char size
        self.char_size = 1.5

class ElAxis(Axis):
    def __init__(self, *args, **kwargs):
        Axis.__init__(self, *args, **kwargs)

        # incorporate my ticks
        if self.scale==LINEAR_SCALE:
            self.tick = ElLinTick(self)
            self.ticklabel = ElLinTickLabel(self)
        else:
            self.tick = ElLogTick(self)
            self.ticklabel = ElLogTickLabel(self)

        # add axis label
        self.label = ElAxisLabel(self)

class ElLegend(Legend):
    def __init__(self, *args, **kwargs):
        Legend.__init__(self, *args, **kwargs)

        self.box_color = 0
        self.box_pattern = 0
        self.box_linewidth = 0.0
        self.box_linestyle = 0
        self.box_fill_color = 0
        self.box_fill_pattern = 0
        self.font = 4
        self.length = 2
        self.char_size = 1.0

class ElGraph(Graph):
    def __init__(self, *args, **kwargs):
        Graph.__init__(self, *args, **kwargs)

        # incorporate default axes
        self.xaxis = ElAxis(self,'x')
        self.yaxis = ElAxis(self,'y')
        self.altxaxis = ElAxis(self,'x','alt','off')
        self.altyaxis = ElAxis(self,'x','alt','off')

        # set legend
        self.legend = ElLegend(self,char_size=1.0)

class ElSquareGraph(ElGraph):
    def __init__(self, *args, **kwargs):
        ElGraph.__init__(self,*args,**kwargs)

        # make the graph square
        self.view.xmax = self.view.xmin + (self.view.ymax - self.view.ymin)

class ElEmptyGraph(ElGraph):
    def __init__(self, *args, **kwargs):
        ElGraph.__init__(self, *args, **kwargs)
        
        # get rid of the frame and all tick and tick labels
        self.frame.linestyle = 0
        self.frame.linewidth = 0
        for axis in [self.xaxis,self.yaxis]:
            axis.bar.onoff = "off"
            axis.tick.major_size = 0
            axis.tick.minor_size = 0
            axis.ticklabel.onoff = "off"
            axis.tick.onoff = "off"

class ElEmptySquareGraph(ElSquareGraph):
    def __init__(self, *args, **kwargs):
        ElSquareGraph.__init__(self, *args, **kwargs)
        
        # get rid of the frame and all tick and tick labels
        self.frame.linestyle = 0
        self.frame.linewidth = 0
        for axis in [self.xaxis,self.yaxis]:
            axis.bar.onoff = "off"
            axis.tick.major_size = 0
            axis.tick.minor_size = 0
            axis.ticklabel.onoff = "off"
            axis.tick.onoff = "off"

class ElColorBar(ColorBar):
    def __init__(self,*args,**kwargs):
        ColorBar.__init__(self,*args,**kwargs)

        # place the axis label
        self.yaxis.label.copy_format(ElAxisLabel)
        self.yaxis.label.place = "opposite"
        
        # place the tick label
        self.yaxis.tick.copy_format(ElTick)
        self.yaxis.ticklabel.copy_format(ElTickLabel)
        self.yaxis.ticklabel.place = "opposite"

        # make the tick labels slightly smaller
        self.yaxis.scale_suffix(0.5,"major_size")
        self.yaxis.scale_suffix(0.5,"minor_size")

class ElLinColorBar(ElColorBar):
    def __init__(self,*args,**kwargs):
        ElColorBar.__init__(self,*args,**kwargs)

        # place the tick label
        self.yaxis.tick.copy_format(ElLinTick)
        self.yaxis.ticklabel.copy_format(ElLinTickLabel)
        self.yaxis.ticklabel.place = "opposite"

        # make the tick labels slightly smaller
        self.yaxis.scale_suffix(0.5,"major_size")
        self.yaxis.scale_suffix(0.5,"minor_size")

class ElLogColorBar(ElColorBar):
    def __init__(self,*args,**kwargs):
        ElColorBar.__init__(self,*args,**kwargs)

        # place the tick label
        self.yaxis.tick.copy_format(ElLogTick)
        self.yaxis.ticklabel.copy_format(ElLogTickLabel)
        self.yaxis.ticklabel.place = "opposite"

        # make the tick labels slightly smaller
        self.yaxis.scale_suffix(0.5,"major_size")
        self.yaxis.scale_suffix(0.5,"minor_size")

