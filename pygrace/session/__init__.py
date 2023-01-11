#!/usr/bin/env python
# 
# Michael McKerns
# mmckerns@caltech.edu 
from .interactive import __doc__ as gracedoc
__doc__ = gracedoc

def grace():
    '''get usage: gr = grace(); gr.doc()'''
    from .interactive import grace as graceFactory
    return graceFactory()

def copyright():
    from .interactive import __license__
    return __license__
   #return "pygrace module: Copyright (c) 2005-2009 Michael McKerns"
