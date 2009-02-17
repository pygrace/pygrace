from PyGrace.Extensions.panel import Panel, PanelLabel

#------------------------------------------------------------------------------
# Nature style
#------------------------------------------------------------------------------
class NaturePanelLabel(PanelLabel):
    def __init__(self, parent, index, *args, **kwargs):
        PanelLabel.__init__(self, parent, index, *args, **kwargs)

        # configure text
        self.add_scheme("Nature",self.label_schemes["latin"])
        self.configure(label_scheme="Nature")

class NaturePanel(Panel):
    def __init__(self,parent,index):
        Panel.__init__(self,parent,index)
        
        index = self.panel_label.label_index
        self.panel_label = self.add_drawing_object(NaturePanelLabel,index)

#------------------------------------------------------------------------------
# Science style
#------------------------------------------------------------------------------
class SciencePanelLabel(PanelLabel):
    def __init__(self, parent, index, *args, **kwargs):
        PanelLabel.__init__(self, parent, index, *args, **kwargs)

        # configure text
        self.add_scheme("Science",self.label_schemes["latin"])
        self.configure(label_scheme="Science")

class SciencePanel(Panel):
    def __init__(self,parent,index):
        Panel.__init__(self,parent,index)
        
        index = self.panel_label.label_index
        self.panel_label = self.add_drawing_object(SciencePanelLabel,index)
