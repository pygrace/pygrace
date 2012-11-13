from PyGrace.grace import Grace
from PyGrace.graph import Graph, INDEX_ORIGIN, Legend
from PyGrace.dataset import DataSet
from PyGrace.axis import Tick, TickLabel, Axis, AxisLabel, \
     LINEAR_SCALE, LOGARITHMIC_SCALE
from PyGrace.Extensions.colorbar import ColorBar
from PyGrace.Extensions.panel import PanelLabel

#------------------------------------------------------------------------------
# The 'Metra' style of data sets
#------------------------------------------------------------------------------
class MetraRightStairsDataSet(DataSet):
    def __init__(self, color, *args, **kwargs):
        DataSet.__init__(self, *args, **kwargs)

        # make right stairs dataset (no symbols)
        self.symbol.configure(shape=0, fill_color=color, color=color)
        self.line.configure(type=3, linestyle=1, color=color)

class MetraLineDataSet(DataSet):
    def __init__(self, color, *args, **kwargs):
        DataSet.__init__(self, *args, **kwargs)

        # line only (no symbols)
        self.symbol.configure(shape=0, fill_color=color, color=color)
        self.line.configure(type=1, linestyle=1, color=color)

class MetraShadedDataSet(DataSet):
    def __init__(self, color, *args, **kwargs):
        DataSet.__init__(self, *args, **kwargs)

        # shading and line
        self.symbol.configure(shape=0, fill_color=color, color=color)
        self.line.configure(type=1, linestyle=1, color=color)
        self.fill.configure(type=2, color=color, pattern=1)
        self.baseline.type = 3

class MetraCircleDataSet(DataSet):
    def __init__(self, color, *args, **kwargs):
        DataSet.__init__(self, *args, **kwargs)

        # make right stairs dataset (no symbols)
        self.symbol.configure(shape=1, fill_color=color, color=1)
        self.line.configure(type=0, linestyle=0, color=color)

#------------------------------------------------------------------------------
# The 'Metra' style of graphs
#------------------------------------------------------------------------------
class MetraTick(Tick):
    def __init__(self, *args, **kwargs):
        Tick.__init__(self, *args, **kwargs)

        # alter the tick sizes
        self.major_size = 1.25
        self.minor_size = 0.75

class MetraLinTick(MetraTick):
    def __init__(self, *args, **kwargs):
        MetraTick.__init__(self, *args, **kwargs)

        # alter the tick sizes
        self.major = 0.2

class MetraLogTick(MetraTick):
    def __init__(self, *args, **kwargs):
        MetraTick.__init__(self, *args, **kwargs)

        # alter the tick sizes
        self.major = 10
        self.minor_ticks = 8

class MetraTickLabel(TickLabel):
    def __init__(self, *args, **kwargs):
        TickLabel.__init__(self, *args, **kwargs)

        # set char size
        self.char_size = 1.5

class MetraLinTickLabel(MetraTickLabel):
    def __init__(self, *args, **kwargs):
        MetraTickLabel.__init__(self, *args, **kwargs)

        # set defaults
        self.format = "decimal"
        self.prec = 1

class MetraLogTickLabel(MetraTickLabel):
    def __init__(self, *args, **kwargs):
        MetraTickLabel.__init__(self, *args, **kwargs)

        # set defaults
        self.format = "power"
        self.prec = 0

class MetraAxisLabel(AxisLabel):
    def __init__(self, *args, **kwargs):
        AxisLabel.__init__(self, *args, **kwargs)

        # set char size
        self.char_size = 2.0

class MetraAxis(Axis):
    def __init__(self, *args, **kwargs):
        Axis.__init__(self, *args, **kwargs)

        # incorporate my ticks
        if self.scale==LINEAR_SCALE:
            self.tick = MetraLinTick(self)
            self.ticklabel = MetraLinTickLabel(self)
        else:
            self.tick = MetraLogTick(self)
            self.ticklabel = MetraLogTickLabel(self)

        # add axis label
        self.label = MetraAxisLabel(self)

class MetraLegend(Legend):
    def __init__(self, *args, **kwargs):
        Legend.__init__(self, *args, **kwargs)

        self.box_color = 0
        self.box_pattern = 0
        self.box_linewidth = 0.0
        self.box_linestyle = 0
        self.box_fill_color = 0
        self.box_fill_pattern = 0
        self.font = 4
        self.length = 3
        self.char_size = 1.5

class MetraGraph(Graph):
    def __init__(self, *args, **kwargs):
        Graph.__init__(self, *args, **kwargs)

        # incorporate default axes
        self.xaxis = MetraAxis(self,'x')
        self.yaxis = MetraAxis(self,'y')
        self.altxaxis = MetraAxis(self,'x','alt','off')
        self.altyaxis = MetraAxis(self,'x','alt','off')

        # set legend
        self.legend = MetraLegend(self)

class MetraSquareGraph(MetraGraph):
    def __init__(self, *args, **kwargs):
        MetraGraph.__init__(self,*args,**kwargs)

        # make the graph square
        self.view.xmax = self.view.xmin + (self.view.ymax - self.view.ymin)

class MetraEmptyGraph(MetraGraph):
    def __init__(self, *args, **kwargs):
        MetraGraph.__init__(self, *args, **kwargs)
        
        # get rid of the frame and all tick and tick labels
        self.frame.linestyle = 0
        self.frame.linewidth = 0
        for axis in [self.xaxis,self.yaxis]:
            axis.bar.onoff = "off"
            axis.tick.major_size = 0
            axis.tick.minor_size = 0
            axis.ticklabel.onoff = "off"
            axis.tick.onoff = "off"

class MetraEmptySquareGraph(MetraSquareGraph):
    def __init__(self, *args, **kwargs):
        MetraSquareGraph.__init__(self, *args, **kwargs)
        
        # get rid of the frame and all tick and tick labels
        self.frame.linestyle = 0
        self.frame.linewidth = 0
        for axis in [self.xaxis,self.yaxis]:
            axis.bar.onoff = "off"
            axis.tick.major_size = 0
            axis.tick.minor_size = 0
            axis.ticklabel.onoff = "off"
            axis.tick.onoff = "off"

class MetraColorBar(ColorBar):
    def __init__(self,*args,**kwargs):
        ColorBar.__init__(self,*args,**kwargs)

        # place the axis label
        self.yaxis.label.copy_format(MetraAxisLabel)
        self.yaxis.label.place = "opposite"
        
        # place the tick label
        self.yaxis.tick.copy_format(MetraTick)
        self.yaxis.ticklabel.copy_format(MetraTickLabel)
        self.yaxis.ticklabel.place = "opposite"

        # make the tick labels slightly smaller
        self.yaxis.scale_suffix(0.5,"major_size")
        self.yaxis.scale_suffix(0.5,"minor_size")

class MetraLinColorBar(MetraColorBar):
    def __init__(self,*args,**kwargs):
        MetraColorBar.__init__(self,*args,**kwargs)

        # place the tick label
        self.yaxis.tick.copy_format(MetraLinTick)
        self.yaxis.ticklabel.copy_format(MetraLinTickLabel)
        self.yaxis.ticklabel.place = "opposite"

        # make the tick labels slightly smaller
        self.yaxis.scale_suffix(0.5,"major_size")
        self.yaxis.scale_suffix(0.5,"minor_size")

class MetraLogColorBar(MetraColorBar):
    def __init__(self,*args,**kwargs):
        MetraColorBar.__init__(self,*args,**kwargs)

        # place the tick label
        self.yaxis.tick.copy_format(MetraLogTick)
        self.yaxis.ticklabel.copy_format(MetraLogTickLabel)
        self.yaxis.ticklabel.place = "opposite"

        # make the tick labels slightly smaller
        self.yaxis.scale_suffix(0.5,"major_size")
        self.yaxis.scale_suffix(0.5,"minor_size")

