#!/usr/bin/env python
"""
Amaral Group
Northwestern University

"""

from dataset import DataSet
from axis import Axis
from title import Title
from subtitle import Subtitle
from view import View,World
from xmg_string import XMG_String
from xmg_exceptions import SetItemError, AttrError
from frame import Frame
from legend import Legend
from fonts import DEFAULT_FONTS
from colors import DEFAULT_COLORS

INDEX_ORIGIN = 0  # zero or one (one is for losers)

class Graph:
    """Graph class

    """
    def __init__(self, colors, fonts, idNumber=-1,title=None,
                 subtitle=None,
                 xaxis=None,
                 yaxis=None,
                 legend = None,
                 frame = None,
                 view = None,
                 world = None,
                 onoff='on',
                 hidden='false',
                 type='XY',
                 stacked = 'false',
                 bar_hgap=0.00,
                 nDataSets=0):
        self._colors = colors     # local copy of global colors dictionary
        self._fonts = fonts       # local copy of global fonts dictionary
       
        self['idNumber'] = idNumber

        #--------------------------------------------------------------#
        if legend:
            self['legend'] = legend
        else:
            self['legend'] = Legend(self._colors, self._fonts)
        if frame:
            self['frame'] = frame
        else:
            self['frame'] = Frame(self._colors, self._fonts)
        if xaxis:
            self['xaxis'] = xaxis
        else:
            self['xaxis'] = Axis(self._colors,self._fonts,orientation='x')
        if yaxis:
            self['yaxis'] = yaxis
        else:
            self['yaxis'] = Axis(self._colors,self._fonts,orientation='y')
        if title:
            self['title'] = title
        else:
            self['title'] = Title(colors,fonts)
        if subtitle:
            self['subtitle']=subtitle
        else:
            self['subtitle'] = Subtitle(colors,fonts,size=1.0)
        if view:
            self['view'] = view
        else:
            self['view'] = View()
        if world:
            self['world'] = world
        else:
            self['world'] = World()
        self['onoff'] = onoff
        self['hidden'] = hidden
        self['type'] = type
        self['stacked'] = stacked
        self['bar_hgap'] = bar_hgap
        
        #-------------------------------------------------------------#
        self.datasets = []
        self._datasetIndex = INDEX_ORIGIN
        for i in range(nDataSets):
            self.add_dataset()

    def __getitem__(self, name): return getattr(self, name)
    def __setitem__(self, name, value):

        if type(value) == str:
            value = value.replace('"','')
        
        if name == 'legend':
            if not value.__class__ == Legend:
                SetItemError(self.__class__,value,name)
            else:
                self.legend = value
        elif name == 'frame':
            if not value.__class__ == Frame:
                SetItemError(self.__class__,value,name)
            else:
                self.frame = value
        elif name == 'xaxis' or name == 'yaxis':
            if not value.__class__ == Axis:
                SetItemError(self.__class__,value,name)
            else:
                setattr(self,name,value)
        elif name == 'title':
            if not value.__class__ == Title:
                SetItemError(self.__class__,value,name)
            else:
                self.title = value
        elif name == 'subtitle':
            if not value.__class__ == Subtitle:
                SetItemError(self.__class__,value,name)
            else:
                self.subtitle = value
        elif name == 'view':
            if not value.__class__ == View:
                SetItemError(self.__class__,value,name)
            else:
                self.view = value
        elif name == 'world':
            if not value.__class__ == World:
                SetItemError(self.__class__,value,name)
            else:
                self.world = value
        elif name == 'onoff':
            try: self.onoff = value
            except: SetItemError(self.__class__,value,name)
        elif name == 'hidden':
            try: self.hidden = value
            except: SetItemError(self.__class__,value,name)
        elif name == 'type':
            try: self.type = value
            except: SetItemError(self.__class__,value,name)
        elif name == 'stacked':
            try: self.stacked = value
            except: SetItemError(self.__class__,value,name)
        elif name == 'bar_hgap':
            try: self.bar_hgap = float(value)
            except: SetItemError(self.__class__,value,name)
        elif name == 'idNumber':
            try: self.idNumber = int(value)
            except: SetItemError(self.__class__,value,name)
        else:
            AttrError(self.__class__, name)

            
    def __repr__(self):
        lines = []

        lines.append('@g' + str(self.idNumber) + ' ' + str(self.onoff))
        lines.append('@g' + str(self.idNumber) + ' hidden ' + str(self.hidden))
        lines.append('@g' + str(self.idNumber) + ' type ' + str(self.type))
        lines.append('@g' + str(self.idNumber) + ' stacked ' + str(self.stacked))
        lines.append('@g' + str(self.idNumber) + ' bar hgap ' + str(self.bar_hgap))  
        lines.append('@with g' + str(self.idNumber))
        lines.append(str(self.world))
        lines.append(str(self.view))
        lines.append(self.title.contents('@    title'))
        lines.append(self.subtitle.contents('@    subtitle'))
        lines.append(str(self.legend))
        lines.append(str(self.frame))
        lines.append(str(self.xaxis))
        lines.append(str(self.yaxis))
        lines.extend(map(str,self.datasets))

	return '\n'.join(lines)

    def add_dataset(self, dataset=False):
        """add_dataset() -> none

        Temporary stub to test main Grace output
        """
        idNumber = self._datasetIndex

        if not dataset:
            self.datasets.append(DataSet(idNumber))
        else:
            self.datasets.append(dataset)
            dataset['idNumber'] = idNumber
        
        self._datasetIndex += 1
        return idNumber

    def get_dataset(self,num):
        if num >= len(self.datasets):
            return None
        else:
            return self.datasets[num]


class fixedpoint: #unfinished
    """Fixedpoint class"""
    def __init__(onoff='off',type=0,xy = (0.00,0.00),format = ('general','general'),prec=(6,6)):
        pass
    pass

# =============================================================== Test function

if __name__ == '__main__':
    print Graph(DEFAULT_COLORS,DEFAULT_FONTS)


