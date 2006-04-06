#!/usr/bin/env python
"""
Amaral Group
Northwestern University
4/5/2006

This module contains miscellaneous functions and classes for use in other
modules related to plotting in xmgrace.
"""

# =============================================================== Divider class
class Divider:
    """Divider class

    This class is meant to produce a line of symbols that separates regions
    of a file (for easier manual reading).

    Example:

    s = str(Divider('Great', '*', 42, '#'))

    will give a string that looks like this (total length = 42 characters):

    # 
    # ********************************** Great
    
    """
    def __init__(self, label, symbol='=', length=60, commentChar='#'):
	self.chars = ['#\n#',' ']
	self.chars.extend([char for char in ' ' + label])
	while len(self.chars) < length:
	    self.chars.insert(2,symbol)

    def __repr__(self):
	return ''.join(self.chars)

# =============================================================== Test function
if __name__ == '__main__':
    print Divider('Gomer', '-', 79)
    print Divider('DividerMaster2000', '*', 79)
    print Divider('Shorty', '>', 40)


