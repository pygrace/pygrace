#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Author: Daniel Stouffer (daniel @stoufferlab.org)
# Copyright (c) 2004-2016 California Institute of Technology.
# Copyright (c) 2013 Daniel Stouffer.
# Copyright (c) 2023 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/uqfoundation/pygrace/blob/master/LICENSE

# author, version, license, and long description
try: # the package is installed
    from .__info__ import __version__, __author__, __doc__, __license__
except: # pragma: no cover
    import os
    import sys
    parent = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
    sys.path.append(parent)
    # get distribution meta info 
    from version import (__version__, __author__,
                         get_license_text, get_readme_as_rst)
    __license__ = get_license_text(os.path.join(parent, 'LICENSE'))
    __license__ = "\n%s" % __license__
    __doc__ = get_readme_as_rst(os.path.join(parent, 'README.md'))
    del os, sys, parent, get_license_text, get_readme_as_rst


__all__ = ['axis','colors','dataset','drawing_objects','fonts', \
           'grace','graph','parser','license','citation']
 
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


def license():
    """print license"""
    print(__license__)
    return

def citation():
    """print citation"""
    print(__doc__[-498:-330])
    return

# EOF
