#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 2004-2016 California Institute of Technology.
# Copyright (c) 2016-2023 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/pygrace/pygrace/blob/altmerge/LICENSE
#
from .session import __doc__ as gracedoc
__doc__ = gracedoc

def grace():
    '''create an interactive instance of xmgrace'''
    from .session import grace as graceFactory
    return graceFactory()

session = grace

def copyright():
    from .interactive import __license__
    return __license__
