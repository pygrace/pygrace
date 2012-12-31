__all__ = [
    'axis',
    'colors',
    'dataset',
    'drawing_objects',
    'fonts',
    'graph',
    'PyGrace',
    'Session',
    ]

import axis
import colors
import dataset
import drawing_objects
import fonts
import graph

def PyGrace():
    from pygrace import canvas
    return canvas.Grace()

def Session():
    from pygrace import session as interactive
    return interactive.session()


# backward compatibility
grace = Session


# EOF
