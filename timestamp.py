#!/usr/bin/env python
"""
Amaral Group
Northwestern University
4/5/2006

This module contains the Timestamp class, to be used in grace.py.
"""

import time

# ============================================================= Timestamp class
class Timestamp:
    """Timestamp class

    This is used to output a timestamp to an xmgrace file.

    Example:

    >> a = Timestamp()
    >> a['onoroff'] = 'on'
    >> a['color'] = 'blue'
    >> a['angle'] = 15
    >> print a

    @timestamp on
    @timestamp 0.03, 0.03
    @timestamp color \"blue\"
    @timestamp rot 15
    @timestamp font \"Helvetica\"
    @timestamp char size 1.000000
    @timestamp def \"Thu Apr  6 14:38:47 2006\"
    """
    def __init__(self, onoroff='off',
                 x = 0.03, y = 0.03,
                 color = 'black', font = 'Helvetica',
                 angle = 0, size = 1.0
                 ):
        
	# set defaults as class attributes
	self.onoroff = onoroff
	self.x, self.y = x, y
	self.color = color
	self.angle = angle
	self.font = font
	self.size = size

    # access class attributes like a dictionary
    def __getitem__(self, name): return getattr(self, name)
    def __setitem__(self, name, value): setattr(self, name, value)
	
    def _string_time(self):
        """_string_time() -> str

        Return a nicely formatted string with the time.
        """
	return time.ctime()

    def __repr__(self):
	lines = []
	
	lines.append('@timestamp %s' % self.onoroff)
	lines.append('@timestamp %.02f, %.02f' % (self.x, self.y))
	lines.append('@timestamp color "%s"' % self.color)
	lines.append('@timestamp rot %s' % self.angle)
	lines.append('@timestamp font "%s"' % self.font)
	lines.append('@timestamp char size %.06f' % self.size)
	lines.append('@timestamp def "%s"' % self._string_time())
	
	return '\n'.join(lines)

        
# =============================================================== Test function
if __name__ == '__main__':
    a = Timestamp()

    a['onoroff'] = 'on'
    a['color'] = 'blue'
    a['angle'] = 15

    print a

