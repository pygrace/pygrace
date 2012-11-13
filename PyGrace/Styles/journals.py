from PyGrace.Extensions.panel import Panel, PanelLabel, MultiPanelGrace

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

class NatureMultiGrace(MultiPanelGrace):
    def __init__(self,*args,**kwargs):
        MultiPanelGrace.__init__(self,*args,**kwargs)
        
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

class ScienceMultiGrace(MultiPanelGrace):
    def __init__(self,*args,**kwargs):
        MultiPanelGrace.__init__(self,*args,**kwargs)
        
        # configure text
        self.set_label_scheme("LATIN")
