#!/usr/bin/env python
"""
Amaral Group
Northwestern University
6/26/2006

This module holds the View class that is used in the grace.py module.

"""

from xmg_exceptions import SetItemError, AttrError

# =================  View class =================================

class View:

    def __init__(self, low_left=(0.15,0.15), up_right=(1.15,0.85)):

        self['xmin'] = low_left[0]
        self['xmax'] = up_right[0]
        self['ymin'] = low_left[1]
        self['ymax'] = up_right[1]

    def __getitem__(self,name): return getattr(self, name)

    def __setitem__(self,name,value):

        if type(value) == str:
            value = value.replace('"','')
        
        if name == 'xmin' or name == 'xmax' or name == 'ymin' or name == 'ymax':
            try:
                setattr(self, name, float(value))
            except:
                SetItemError(self.__class__, name, value)
        else:
            AttrError(self.__class__, name)

    def __repr__(self):

        lines = []
        lines.append('@    view xmin %.10f' % self.xmin)
        lines.append('@    view xmax %.10f' % self.xmax)
        lines.append('@    view ymin %.10f' % self.ymin)
        lines.append('@    view ymax %.10f' % self.ymax)

        return '\n'.join(lines)

#-------------------------------------------------------------------#
#-------------------------World Class-------------------------------#

class World:
    
    def __init__(self, low_left=(0,0), up_right=(1,1),
             stack_world=(0,0,0,0), znorm=1):

        self['xmin'] = low_left[0]
        self['xmax'] = up_right[0]
        self['ymin'] = low_left[1]
        self['ymax'] = up_right[1]
        self['stack_world'] = stack_world #should these two attributes
        self['znorm'] = znorm             #be in this class? 

    def __getitem__(self,name): return getattr(self, name)

    def __setitem__(self,name,value):

        if type(value) == str:
            value = value.replace('"','')

        if name == 'xmin' or name == 'xmax' or name == 'ymin' or name == 'ymax':
            try:
                setattr(self, name, float(value))
            except:
                SetItemError(self.__class__, name, value)
        elif name == 'stack_world':#value should be string 
            try:
                if type(value) == tuple:
                    self.stack_world = value
                else: #for reading in from file
                    self.stack_world = tuple(map(int,tuple(''.join(value).replace(',',''))))#format a string list to an int tuple - ugly
            except:
                SetItemError(self.__class__, name, value)
        elif name == 'znorm':
            try:
                self.znorm = int(value)
            except:
                SetItemError(self.__class__, name, value)
        else:
            AttrError(self.__class__, name)

    def __repr__(self):

        lines = []
        lines.append('@    world xmin %.10f' % self.xmin)
        lines.append('@    world xmax %.10f' % self.xmax)
        lines.append('@    world ymin %.10f' % self.ymin)
        lines.append('@    world ymax %.10f' % self.ymax)
        lines.append('@    stack world %s' %
                     str(self.stack_world).replace('(','').replace(')',''))
        lines.append('@    znorm %s' % self.znorm)

        return '\n'.join(lines)
