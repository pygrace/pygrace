__all__ = [
    'grace',
    'session',
    'template',
    ]

# backward compatibility for pygrace.session
def grace():
    from pygrace import session as interactive
    return interactive.session()

import session
import template

# EOF
