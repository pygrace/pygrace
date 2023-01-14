#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 2004-2016 California Institute of Technology.
# Copyright (c) 2023 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/uqfoundation/pygrace/blob/master/LICENSE
#
from .session import __doc__ as gracedoc
__doc__ = gracedoc
del gracedoc

from .project import Project, Graph
from .process import Process

def grace(*args, **kwds):
    from .session import grace as graceFactory
    return graceFactory(*args, **kwds)
grace.__doc__ = Project.__init__.__doc__

session = grace

def copyright():
    from .interactive import __license__
    return __license__
