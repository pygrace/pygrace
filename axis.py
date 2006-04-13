#!/usr/bin/env python
"""
Amaral Group
Northwestern University

Generic axis class.

As of now only contains a 'label'-type XMG_String and
an orientation attribute for either 'x' or 'y'
"""
from xmg_string import XMG_String

class Axis:
    """
    Note inclusion of stupid 'char' for label size.
    """
    def __init__(self, label=XMG_String(type='label',size=0.8),orientation='x'):
        self.label=label
        self.orientation=orientation

    def __getitem__(self, name): return getattr(self, name)
    def __setitem__(self, name, value): setattr(self, name, value)
    
    def _prefix(self):
        s='@    ' + self.orientation + 'axis'
        return s

    def contents(self):
        lines = []

        lines.append(self.label.contents(self._prefix() + ' label'));
	return '\n'.join(lines)
        
    """
    __repr__ is overriden in anticipation of additional lines
    """
    def __repr__(self):
        lines = []

        lines.append(self.label.contents(self._prefix() + ' label'));
	return '\n'.join(lines)
        
# =============================================================== Test function
if __name__ == '__main__':
    print Axis()


