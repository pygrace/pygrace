#!/usr/bin/env python
# 
# Michael McKerns
# mmckerns@caltech.edu 
from pygrace import __doc__ as gracedoc
__doc__ = gracedoc

def grace():
    '''get usage: gr = grace(); gr.doc()'''
    from pygrace import grace as graceFactory
    return graceFactory()

def copyright():
    from pygrace import __license__
    return __license__
   #return "pygrace module: Copyright (c) 2005-2009 Michael McKerns"

#built with:  Grace-5.1.14, grace_np-2.7, gracePlot-0.5.1
