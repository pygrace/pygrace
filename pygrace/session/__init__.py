#!/usr/bin/env python
# 
# Michael McKerns
# mmckerns@caltech.edu 
from .interactive import __doc__ as gracedoc
__doc__ = gracedoc

def grace():
    '''create an interactive instance of xmgrace'''
    from .interactive import grace as graceFactory
    return graceFactory()

def copyright():
    from .interactive import __license__
    return __license__
