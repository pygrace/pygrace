#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @uqfoundation)
# Author: Daniel Stouffer (daniel @stoufferlab.org)
# Copyright (c) 2013 Daniel Stouffer.
# Copyright (c) 2023 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/uqfoundation/pygrace/blob/master/LICENSE
#
from ..extensions.panel import Panel, PanelLabel, MultiPanelProject

__all__ = ['NaturePanelLabel','NaturePanel','NatureMultiPanelProject', \
           'SciencePanelLabel','SciencePanel','ScienceMultiPanelProject']

#------------------------------------------------------------------------------
# Nature style
#------------------------------------------------------------------------------
class NaturePanelLabel(PanelLabel):
    def __init__(self, parent, index, *args, **kwargs):
        PanelLabel.__init__(self, parent, index, *args, **kwargs)

        # configure text
        self.label_scheme = "latin"

class NaturePanel(Panel):
    def __init__(self,*args,**kwargs):
        Panel.__init__(self,*args,**kwargs)
        
        index = self.panel_label.label_index
        self.panel_label = self.add_drawing_object(NaturePanelLabel,index)

class NatureMultiPanelProject(MultiPanelProject):
    def __init__(self,*args,**kwargs):
        MultiPanelProject.__init__(self,*args,**kwargs)
        
        # configure text
        self.set_label_scheme("latin")

#------------------------------------------------------------------------------
# Science style
#------------------------------------------------------------------------------
class SciencePanelLabel(PanelLabel):
    def __init__(self, parent, index, *args, **kwargs):
        PanelLabel.__init__(self, parent, index, *args, **kwargs)

        # configure text
        self.label_scheme = "LATIN"

class SciencePanel(Panel):
    def __init__(self,*args,**kwargs):
        Panel.__init__(self,parent,index)
        
        index = self.panel_label.label_index
        self.panel_label = self.add_drawing_object(SciencePanelLabel,index)

class ScienceMultiPanelProject(MultiPanelProject):
    def __init__(self,*args,**kwargs):
        MultiPanelProject.__init__(self,*args,**kwargs)
        
        # configure text
        self.set_label_scheme("LATIN")

# preserving backward compatibility with PyGrace
NatureMultiPlot = NatureMultiPanelProject
ScienceMultiPlot = ScienceMultiPanelProject
