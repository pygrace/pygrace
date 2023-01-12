#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Author: Daniel Stouffer (daniel @stoufferlab.org)
# Copyright (c) 2004-2016 California Institute of Technology.
# Copyright (c) 2013 Daniel Stouffer.
# Copyright (c) 2023 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/pygrace/pygrace/blob/altmerge/LICENSE
#
__all__ = [
    'axis',
    'colors',
    'dataset',
    'drawing_objects',
    'fonts',
    'grace',
    'graph',
    'parser',
	]
 
from . import axis
from . import colors
from . import dataset
from . import drawing_objects
from . import fonts
from . import graph
from . import parser
 
# dealing with backward compatibility
if __name__ == 'PyGrace':
    # backward compatibility for PyGrace
    from PyGrace import grace
    try: del plot
    except: pass
    try: del project
    except: pass
 
elif __name__ == 'pygrace':
    __all__.append('project')
    __all__.append('interactive')

    from . import project
    from . import interactive

    # backward compatibility for pygrace
    def grace(*args, **kwds):
        from pygrace import interactive
        return interactive.session(*args, **kwds)
    grace.__doc__ = interactive.session.__doc__

