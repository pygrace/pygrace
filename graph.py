from base import GraceObject
from drawing_objects import DrawingObject
from dataset import DataSet, SYMBOLS, INDEX2SYMBOLS, LINESTYLES, \
    INDEX2LINESTYLES
from axis import Axis,LINEAR_SCALE,LOGARITHMIC_SCALE
import math

INDEX_ORIGIN = 0  # zero or one (one is for losers)

class Subtitle(GraceObject):
    _staticType = 'Subtitle'
    def __init__(self, parent,
                 text='',
                 font=4,
                 color=1,
                 size=1.75,
                 **kwargs
                 ):
        GraceObject.__init__(self, parent, locals())

    def __str__(self):
        return \
"""@    subtitle "%(text)s"
@    subtitle font %(font)s
@    subtitle size %(size)s
@    subtitle color %(color)s""" % self

class Title(GraceObject):
    _staticType = 'Title'
    def __init__(self, parent,
                 text='',
                 font=4,
                 color=1,
                 size=1.75,
                 **kwargs
                 ):
        GraceObject.__init__(self, parent, locals())

    def __str__(self):
        return \
"""@    title "%(text)s"
@    title font %(font)s
@    title size %(size)s
@    title color %(color)s""" % self

class View(GraceObject):
    _staticType = 'View'
    def __init__(self, parent,
                 xmin=0.15,
                 xmax=1.15,
                 ymin=0.15,
                 ymax=0.85,
                 **kwargs
                 ):
        GraceObject.__init__(self, parent, locals())

    def __str__(self):
        return \
"""@    view xmin %(xmin)s
@    view xmax %(xmax)s
@    view ymin %(ymin)s
@    view ymax %(ymax)s""" % self

class World(GraceObject):
    _staticType = 'World'
    def __init__(self, parent,
                 xmin=0,
                 xmax=1,
                 ymin=0,
                 ymax=1,
                 stack_world=(0,0,0,0),
                 znorm=1,
                 **kwargs
                 ):
        GraceObject.__init__(self, parent, locals())
        self._formatting_template = \
            {'stack_world': '%.20f, %.20f, %.20f, %.20f'}

    def __setattr__(self, key, value):

        # check type of Frame specific attribute
        if key == 'znorm':
            self._check_type((float, int), key, value)
        elif key == 'stack_world':
            self._check_type(tuple, key, value)

        GraceObject.__setattr__(self, key, value)

    def __str__(self):
        return \
"""@    world xmin %(xmin)s
@    world xmax %(xmax)s
@    world ymin %(ymin)s
@    world ymax %(ymax)s
@    stack world %(stack_world)s
@    znorm %(znorm)s""" % self

class Frame(GraceObject):
    _staticType = 'Frame'
    def __init__(self, parent,
                 type = 0,
                 linestyle = 1,
                 linewidth = 2.0,
                 color = 1,
                 pattern = 1,
                 background_color = 0,
                 background_pattern = 0,
                 **kwargs
                 ):
        GraceObject.__init__(self, parent, locals())

    def __setattr__(self, key, value):

        # check type of Frame specific attribute
        if key == 'type':
            self._check_type(int, key, value)
            self._check_range(key, value, 0, 6, includeMax=False)
        GraceObject.__setattr__(self, key, value)

    def __str__(self):
        return \
"""@    frame type %(type)s
@    frame linestyle %(linestyle)s
@    frame linewidth %(linewidth)s
@    frame color %(color)s
@    frame pattern %(pattern)s
@    frame background color %(background_color)s
@    frame background pattern %(background_pattern)s""" % self

class Legend(GraceObject):
    _staticType = 'Legend'
    def __init__(self, parent,
                 onoff = 'on',         # must be 'on' or 'off'
                 loctype = 'view',     # must be 'view' or 'world'
                 loc = (0.85, 0.75),   # coordinates by upper left corner
                 box_color = 1,
                 box_pattern =  1,
                 box_linewidth = 2.0,
                 box_linestyle = 1,
                 box_fill_color = 0,
                 box_fill_pattern = 1,
                 font = 4,
                 char_size = 1.65,
                 color = 1,
                 length = 3,
                 vgap = 1,
                 hgap = 1,
                 invert = 'false',
                 **kwargs
                 ):
        GraceObject.__init__(self, parent, locals())
        self._formatting_template = {'loc': '%.20f, %.20f'}

    def __setattr__(self, key, value):

        # check Legend specific attributes
        if key == 'loc':
            self._check_type(tuple, key, value)
        elif key == 'invert':
            self._check_type(str, key, value)
            self._check_membership(key, value, ('true', 'false'))
        elif key == 'hgap' or key == 'vgap':
            self._check_type((float, int), key, value)
            
        GraceObject.__setattr__(self, key, value)
      
    def __str__(self):
        return \
"""@    legend %(onoff)s
@    legend loctype %(loctype)s
@    legend %(loc)s
@    legend box color %(box_color)s
@    legend box pattern %(box_pattern)s
@    legend box linewidth %(box_linewidth)s
@    legend box linestyle %(box_linestyle)s
@    legend box fill color %(box_fill_color)s
@    legend box fill pattern %(box_fill_pattern)s
@    legend font %(font)s
@    legend char size %(char_size)s
@    legend color %(color)s
@    legend length %(length)s
@    legend vgap %(vgap)s
@    legend hgap %(hgap)s
@    legend invert %(invert)s""" % self

class Graph(GraceObject):
    _staticType = 'Graph'
    def __init__(self, parent, index,
                 onoff='on',
                 hidden='false',
                 type='XY',
                 stacked = 'false',
                 bar_hgap=0.00,
                 **kwargs
                 ):
        GraceObject.__init__(self, parent, locals())
        self.legend = Legend(self)
        self.frame = Frame(self)
        self.xaxis = Axis(self, 'x')
        self.yaxis = Axis(self, 'y')
        self.altxaxis = Axis(self, 'x', 'alt', 'off')
        self.altyaxis = Axis(self, 'y', 'alt', 'off')
        self.title = Title(self)
        self.subtitle = Subtitle(self)
        self.view = View(self)
        self.world = World(self)

        self.datasets = []
        self._datasetIndex = INDEX_ORIGIN

        self.drawing_objects = []

    def __setattr__(self, key, value):

        # check Graph specific attributes
        if key == 'type':
            self._check_type(str, key, value)
        elif key == 'stacked':
            self._check_type(str, key, value)
            self._check_membership(key, value, ('true', 'false'))
        elif key == 'bar_hgap':
            self._check_type((float, int), key, value)

        GraceObject.__setattr__(self, key, value)

    def __str__(self):
        graphString = \
"""@g%(index)s %(onoff)s
@g%(index)s hidden %(hidden)s
@g%(index)s type %(type)s
@g%(index)s stacked %(stacked)s
@g%(index)s bar hgap %(bar_hgap)s
@with g%(index)s
%(world)s
%(view)s
%(title)s
%(subtitle)s
%(legend)s
%(frame)s
%(xaxis)s
%(yaxis)s
%(altxaxis)s
%(altyaxis)s""" % self
        datasetString = '\n'.join(str(dataset) for dataset in self.datasets)
        doString = '\n'.join(str(do) for do in self.drawing_objects)
        return '\n'.join((doString, graphString, datasetString))

    def add_dataset(self, data, cls=DataSet, *args, **kwargs):

        # make sure that cls is a subclass of Dataset
        if not issubclass(cls, DataSet):
            message = '%s is not a subclass of DataSet' % cls.__name__
            raise TypeError(message)

        # make an instance of the dataset class and add to list
        dataset = cls(parent=self, data=data, index=self._datasetIndex,
                      *args, **kwargs)
        self.datasets.append(dataset)

        # increment counter and return the dataset instance
        self._datasetIndex += 1
        return dataset

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

    def remove_extraworld_drawing_objects(self):
        """Remove drawing objects that are outside of the world
        coordinates.  Get it, 'extraworld' is like
        'extra-terrestrial'.
        """
        new_dos = []
        old_dos = []
        xmin,ymin,xmax,ymax = self.get_world()
        for do in self.drawing_objects:
            if do.loctype=="view":
                new_dos.append(do)
            else:
                do_xmin,do_ymin,do_xmax,do_ymax = do.limits()
                if (xmin<=do_xmin and do_xmax<=xmax and 
                    ymin<=do_ymin and do_ymax<=ymax):
                    new_dos.append(do)
                else:
                    old_dos.append(do)
        self.drawing_objects = new_dos
        for do in old_dos:
            del do                

    def alldata(self):
        result = []
        for dataset in self.datasets:
            result.extend(dataset.data)
        return result

    def move_dataset_to_front(self, dataset):
        """Move data set to the front.  This emulates the functionality of the
        xmgrace GUI.
        """

        _dataset = self.datasets.pop(dataset.index-INDEX_ORIGIN)
        _index = _dataset.index
        assert _dataset==dataset, "Not the same dataset"
        self.datasets.append(dataset)
        for index,dataset in enumerate(self.datasets):
            dataset.index = index + INDEX_ORIGIN

    def move_dataset_to_back(self, dataset):
        """Move data set to the back.  This emulates the functionality of the
        xmgrace GUI.
        """

        _dataset = self.datasets.pop(dataset.index-INDEX_ORIGIN)
        assert _dataset==dataset, "Not the same dataset"
        self.datasets.insert(0, dataset)
        for index,dataset in enumerate(self.datasets):
            dataset.index = index + INDEX_ORIGIN

    def move_dataset_forward(self, dataset):
        """Move data set forward by one dataset.  This emulates the 
        functionality of the xmgrace GUI.
        """

        _dataset = self.datasets.pop(dataset.index-INDEX_ORIGIN)
        _index = _dataset.index
        assert _dataset==dataset, "Not the same dataset"
        self.datasets.insert(_index-INDEX_ORIGIN+1, dataset)
        for index,dataset in enumerate(self.datasets):
            dataset.index = index + INDEX_ORIGIN

    def move_dataset_backward(self, dataset):
        """Move data set backward by one dataset.  This emulates the 
        functionality of the xmgrace GUI.
        """

        _dataset = self.datasets.pop(dataset.index-INDEX_ORIGIN)
        _index = _dataset.index
        assert _dataset==dataset, "Not the same dataset"
        _newListIndex = max(0, _index-INDEX_ORIGIN-1) 
        self.datasets.insert(_newListIndex, dataset)
        for index,dataset in enumerate(self.datasets):
            dataset.index = index + INDEX_ORIGIN

    def set_dataset_order(self, datasets):
        """Specify the order of the data sets.
        """

        # make sure that the lengths of order and datasets are the same
        assert len(datasets)==len(self.datasets),\
            "'datasets' not same length as Graph.datasets."

        # use the move_dataset_to_back
        for dataset in datasets:
            self.move_dataset_to_back(dataset)

    def logy(self): self.yaxis.set_log()
    def logx(self): self.xaxis.set_log()
    def logxy(self):
        self.xaxis.set_log()
        self.yaxis.set_log()

    def liny(self): self.yaxis.set_lin()
    def linx(self): self.xaxis.set_lin()
    def linxy(self):
        self.xaxis.set_lin()
        self.yaxis.set_lin()

    def data_smallest_positive(self,only_visible=True):
        all = []
        for dataset in self.datasets:
            result = dataset.smallest_positive(only_visible=only_visible)
            all.append(result)
        if all:
            xmins, ymins = zip(*all)
            xmins = [i for i in xmins if not i is None and i > 0]
            ymins = [i for i in ymins if not i is None and i > 0]
            return min(xmins), min(ymins)
        else:
            return None, None
        
    def drawing_object_smallest_positive(self):
        all = []
        for drawing_object in self.drawing_objects:
            if drawing_object.loctype=="world":
                result = drawing_object.smallest_positive()
                all.append(result)
        if all:
            xmins, ymins = zip(*all)
            xmins = [i for i in xmins if not i is None and i > 0]
            ymins = [i for i in ymins if not i is None and i > 0]
            return min(xmins), min(ymins)
        else:
            return None, None
        
    def smallest_positive(self,only_visible=True):
        data_sp = self.data_smallest_positive(only_visible=only_visible)
        drawing_object_sp = self.drawing_object_smallest_positive()
        if None not in drawing_object_sp and None not in data_sp:
            xmins, ymins = zip(data_sp,drawing_object_sp)
            return min(xmins), min(ymins)
        elif None not in drawing_object_sp:
            return drawing_object_sp
        elif None not in data_sp:
            return data_sp
        else:
            message="""
In Graph.smallest_positive()...
There are no datasets or drawing_objects on which to determine the
smallest positive number.
"""
            raise TypeError, message
        
    def data_limits(self,only_visible=True):
        all = []
        for dataset in self.datasets:
            result = dataset.limits(only_visible=only_visible)
            if not None in result:
                all.append(result)
        if len(all):
            xmins, ymins, xmaxs, ymaxs = zip(*all)
            return min(xmins), min(ymins), max(xmaxs), max(ymaxs)
        else:
            return None, None, None, None

    def drawing_object_limits(self):
        all = []
        for drawing_object in self.drawing_objects:
            result = drawing_object.limits()
            if drawing_object.loctype=="world" and not None in result:
                all.append(result)
        if len(all):
            xmins, ymins, xmaxs, ymaxs = zip(*all)
            return min(xmins), min(ymins), max(xmaxs), max(ymaxs)
        else:
            return None, None, None, None

    def limits(self,only_visible=True):
        data_limits = self.data_limits(only_visible=only_visible)
        drawing_object_limits = self.drawing_object_limits()
        if None not in drawing_object_limits and None not in data_limits:
            xmins, ymins, xmaxs, ymaxs = zip(data_limits,drawing_object_limits)
            return min(xmins), min(ymins), max(xmaxs), max(ymaxs)
        elif None not in drawing_object_limits:
            return drawing_object_limits
        elif None not in data_limits:
            return data_limits
        else:
            message="""
In Graph.limits()...
There are no datasets or drawing_objects on which to determine the limits.
"""
            raise TypeError, message

    def set_world_to_limits(self, epsilon=1e-12):
        xmin, ymin, xmax, ymax = self.limits()
        self.world.xmin = xmin - epsilon
        self.world.xmax = xmax + epsilon
        self.world.ymin = ymin - epsilon
        self.world.ymax = ymax + epsilon
        
    def autoscale_old(self):
        self.set_world_to_limits()
        
    def set_view(self, xmin, ymin, xmax, ymax):
        self.view.xmin = xmin
        self.view.xmax = xmax
        self.view.ymin = ymin
        self.view.ymax = ymax

    def get_view(self):
        return (self.view.xmin,
                self.view.ymin,
                self.view.xmax,
                self.view.ymax)

    def set_labels(self, xLabel, yLabel):
        self.xaxis.label.text = xLabel 
        self.yaxis.label.text = yLabel

    def get_dataset(self,num):
        if num >= len(self.datasets):
            return None
        else:
            return self.datasets[num]

    def calculate_ticks(self, iMin, iMax,
                        lowTarget=3, highTarget=7, scale=LINEAR_SCALE):
        
        # variables
        n1s = [1,2,10,20]
        n4s = [5,50]
        ns = n1s + n4s

        # trick functionality for log axes
        if scale == LINEAR_SCALE:
            domain = iMin, iMax
        if scale == LOGARITHMIC_SCALE:
            domain = math.log10(iMin), math.log10(iMax)
        
        # determine appropriate scale for ticks
        iRange = domain[1] - domain[0]
        if iRange > 0:
            _scale = int(math.floor(math.log10(iRange) - 1.0))
        else:
            _scale = 0
            

        # find number of major ticks
        for n in ns:
            nTry = int(math.floor(iRange / (n * 10**_scale)))
            if nTry >= lowTarget and nTry <= highTarget:
                break

        major = 10**_scale*n
        if scale == LOGARITHMIC_SCALE:
            major = 10**math.ceil(major)

        # determine the number of minor ticks
        if n in n1s:
            n_minor_ticks=1
        elif n in n4s:
            n_minor_ticks=4
        if scale==LOGARITHMIC_SCALE:
            n_minor_ticks = 8

        return major, n_minor_ticks

    def set_world(self, xMin, yMin, xMax, yMax):
        self.world.xmin = xMin
        self.world.xmax = xMax
        self.world.ymin = yMin
        self.world.ymax = yMax

    def get_world(self):
        return (self.world.xmin,
                self.world.ymin,
                self.world.xmax,
                self.world.ymax)

    def calculate_sizes(self, printWidth):
        charSize = 2.3 * printWidth ** -0.4
        lineWidth = 3.45 * printWidth ** -0.5
        offset = 0.023 * printWidth ** -0.5
        return charSize, lineWidth, offset

    def format_for_print(self, printWidth):
        charSize, lineWidth, offset = self.calculate_sizes(printWidth)
        self.set_linewidths(lineWidth)
        self.set_suffix(charSize * 1.1, 'size', True)
        self.set_suffix(charSize, '_size', True)
        self.set_suffix(charSize * 0.67, 'minor_size', True)
        megaset = []
        for dataset in self.datasets:
            megaset.extend(dataset.data)
        try:
            mul = 1.75 * len(megaset)**-.35
            mul = 1 * len(megaset)**-.35
        except ZeroDivisionError:
            pass
        for dataset in self.datasets:
            dataset.set_suffix(charSize * mul, 'size', True)
        self.xaxis.ticklabel.offset_loc = 'spec'
        self.yaxis.ticklabel.offset_loc = 'spec'
        self.xaxis.ticklabel.offset_tup = (0, offset)
        self.yaxis.ticklabel.offset_tup = (0, offset)

    def autoformat(self, printWidth=6.5):
        self.autoscale()
        self.format_for_print(printWidth)

    def autoscalex(self, pad=0, only_visible=True):
        xMin, yMin, xMax, yMax = self.limits(only_visible=only_visible)
        if self.xaxis.scale==LINEAR_SCALE:
            xMajor, nxMinor = self.calculate_ticks(xMin, xMax)
            xMinor = xMajor / float(nxMinor + 1)
            if nxMinor == 1:
                self.world.xmax = math.ceil(xMax / float(xMinor)) * xMinor + \
                    pad*xMinor
                self.world.xmin = math.floor(xMin / float(xMinor)) * xMinor - \
                    pad*xMinor
            else:
                self.world.xmax = math.ceil(xMax / float(xMajor)) * xMajor + \
                    pad*xMajor
                self.world.xmin = math.floor(xMin / float(xMajor)) * xMajor - \
                    pad*xMajor
        elif self.xaxis.scale==LOGARITHMIC_SCALE:

            # if x has a zero value, autoscale with second smallest
            if xMin <= 0:
                xMin, dummy = self.smallest_positive(only_visible=only_visible)
            
            xMajor, nxMinor = self.calculate_ticks(xMin, xMax,
                                                   scale=LOGARITHMIC_SCALE)
            self.world.xmax = 10**(math.ceil(math.log10(xMax) /
                                             float(math.log10(xMajor)))
                                   * math.log10(xMajor) + pad*math.log10(xMajor))
            self.world.xmin = 10**(math.floor(math.log10(xMin) /
                                             float(math.log10(xMajor)))
                                   * math.log10(xMajor) - pad*math.log10(xMajor))
        else:
            message = "'%s' is an unknown x-axis scale"%self.xaxis.scale
            raise TypeError(message)

        self.xaxis.tick.major = xMajor
        self.xaxis.tick.minor_ticks = nxMinor
        self.xaxis.auto_precision()

    def autoscaley(self, pad=0, only_visible=True):
        xMin, yMin, xMax, yMax = self.limits(only_visible=only_visible)
        if self.yaxis.scale==LINEAR_SCALE:
            yMajor, nyMinor = self.calculate_ticks(yMin, yMax)
            yMinor = yMajor / float(nyMinor + 1)
            if nyMinor == 1:
                self.world.ymax = math.ceil(yMax / float(yMinor)) * yMinor + \
                    pad*yMinor
                self.world.ymin = math.floor(yMin / float(yMinor)) * yMinor - \
                    pad*yMinor
            else:
                self.world.ymax = math.ceil(yMax / float(yMajor)) * yMajor + \
                    pad*yMajor
                self.world.ymin = math.floor(yMin / float(yMajor)) * yMajor - \
                    pad*yMajor
        elif self.yaxis.scale==LOGARITHMIC_SCALE:

            # if y has a zero value, autoscale with second smallest
            if yMin <= 0:
                dummy, yMin = self.smallest_positive(only_visible=only_visible)

            yMajor, nyMinor = self.calculate_ticks(yMin, yMax,
                                                   scale=LOGARITHMIC_SCALE)
            self.world.ymax = 10**(math.ceil(math.log10(yMax) /
                                             float(math.log10(yMajor)))
                                   * math.log10(yMajor))
            self.world.ymin = 10**(math.floor(math.log10(yMin) /
                                             float(math.log10(yMajor)))
                                   * math.log10(yMajor))

        else:
            message = "'%s' is an unknown y-axis scale"%self.yaxis.scale
            raise TypeError(message)

        self.yaxis.tick.major = yMajor
        self.yaxis.tick.minor_ticks = nyMinor
        self.yaxis.auto_precision()

    def autoscale(self, padx=0, pady=0, only_visible=True):
        self.autoscalex(pad=padx,only_visible=only_visible)
        self.autoscaley(pad=pady,only_visible=only_visible)

    def autotickx(self):
        """Automatically generate x-axis ticks based on world coords.
        """
        xmin, ymin, xmax, ymax = self.get_world()
        scale = self.xaxis.scale
        major, n_minor_ticks = self.calculate_ticks(xmin,xmax,scale=scale)
        self.xaxis.tick.major = major
        self.xaxis.tick.minor_ticks = n_minor_ticks
        self.xaxis.auto_precision()

    def autoticky(self):
        """Automatically generate y-axis ticks based on world coords.
        """
        xmin, ymin, xmax, ymax = self.get_world()
        scale = self.yaxis.scale
        major, n_minor_ticks = self.calculate_ticks(ymin,ymax,scale=scale)
        self.yaxis.tick.major = major
        self.yaxis.tick.minor_ticks = n_minor_ticks
        self.yaxis.auto_precision()

    def autotick(self):
        """Automatically generate ticks based on world coords.
        """
        self.autotickx()
        self.autoticky()

    def set_different_colors(self, skip=1, attr='name', exclude=('White',),
                             colorsList=[]):
        """Set datasets in graph to different colors.  This function behaves
        similarly to the similar function in the xmgrace GUI.  Can 
        alternatively specify a list of colors for ordering the colors.
        """

        # make sure attr argument is the right type
        if attr not in ('name', 'index'):
            message = "attr must be 'name' or 'index' (got %s)" % attr
            raise ValueError(message)

        # put all color indexes or color names that should be excluded from
        # the list in a dictionary, and make color names case insensitive
        lookup = {}
        for item in exclude:
            if isinstance(item, str):
                item = item.upper()
            lookup[item] = None

        # put colors into a list
        if not colorsList:
            colorsList = []
            for color in self.root.colors:
                if not (color.name.upper() in lookup or color.index in lookup):
                    colorsList.append(getattr(color, attr))
                
        # set datasets to different colors
        nColors = len(colorsList)
        for index, dataset in enumerate(self.datasets):
            color = colorsList[(skip *index) % nColors]
            dataset.set_suffix(color, 'color')

    def set_different_symbols(self, skip=1, attr="index", exclude=(0,),
                              symbolsList=[]):
        """Set datasets in graph to different symbols.  This function behaves
        similarly to the similar function in the xmgrace GUI.  Can
        alternatively specify a list of symbols for ordering the symbol
        shapes.
        """

        # make sure attr argument is the right type
        if attr not in ('name', 'index'):
            message = "attr must be 'name' or 'index' (got %s)" % attr
            raise ValueError(message)

        # put all symbol indexes that should be excluded from the list
        # in a dictionary
        lookup = {}
        for item in exclude:
            if isinstance(item, str):
                item = SYMBOLS[item]
            lookup[item] = None

        # put symbols into a list
        indices = INDEX2SYMBOLS.keys()
        indices.sort()
        if not symbolsList:
            symbolsList = []
            for index in indices:
                if index not in lookup:
                    symbolsList.append(index)
        
        # set datasets to different symbols
        nSymbols = len(symbolsList)
        for index, dataset in enumerate(self.datasets):
            shape = symbolsList[(skip *index) % nSymbols]
            dataset.symbol.set_suffix(shape, "shape")

    def set_different_linestyles(self, skip=1, attr="index", exclude=(0,),
                                 linestylesList=[]):
        """Set datasets in graph to different linestyles.  This function
        behaves similarly to the similar function in the xmgrace
        GUI.  Can alternatively specify a list of linestyles for ordering the 
        line styles.
        """

        # make sure attr argument is the right type
        if attr not in ('name', 'index'):
            message = "attr must be 'name' or 'index' (got %s)" % attr
            raise ValueError(message)

        # put all linestyle indexes that should be excluded from the list
        # in a dictionary
        lookup = {}
        for item in exclude:
            if isinstance(item, str):
                item = LINESTYLES[item]
            lookup[item] = None

        # put line styles into a list
        indices = INDEX2LINESTYLES.keys()
        indices.sort()
        if not linestylesList:
            linestylesList = []
            for index in indices:
                if index not in lookup:
                    linestylesList.append(index)
        
        # set datasets to different line styles
        nLinestyles = len(linestylesList)
        for index, dataset in enumerate(self.datasets):
            linestyle = linestylesList[(skip *index) % nLinestyles]
            dataset.line.set_suffix(linestyle, "linestyle")

    def set_different_linewidths(self, skip=0.5, start=0.5,linewidthsList=[]):
        """Set datasets in graph to different linewidths.  This function
        behaves similarly to the similar function in the xmgrace
        GUI.  Can alternatively specify a list of line widths.
        """

        # determine linewidths
        if not linewidthsList:
            linewidthsList = [skip*index+start 
                              for index in range(len(self.datasets))]
        
        # set datasets to different line widths
        for index, dataset in enumerate(self.datasets):
            dataset.line.set_suffix(linewidthsList[index], "linewidth")

    def half_open(self):
        """Make frame half open
        """
        self.frame.type = 1
        self.xaxis.bar.linestyle = 0
        self.xaxis.tick.place = "normal"
        self.yaxis.bar.linestyle = 0
        self.yaxis.tick.place = "normal"

