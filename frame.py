#!/usr/bin/env python
"""
Amaral Group
Northwestern University
4/11/2006

This module holds the Frame class that is used in the grace.py module.

"""

# ================= Frame class =================================
class Frame:
    
    """
    Frame class

    """
    def __init__(self,
                 type = 0,
                 linestyle = 1,
                 linewidth = 1.0,
                 color = 'black',
                 pattern = 1,
                 background_color = 0,
                 background_pattern = 0
                 ):
        self.type = type
        self.linestyle = linestyle
        self.linewidth = linewidth
        self.color = color
        self.pattern = pattern
        self.background_color = background_color
        self.background_pattern = background_pattern

    # access class attributes like a dictionary
    def __getitem__(self, name): return getattr(self, name)
    def __setitem__(self, name, value): setattr(self, name, value)

    # print
    def __repr__(self):
	lines = []

        lines.append('@    frame type %s' % self.type)
        lines.append('@    frame linestyle %s' % self.linestyle)
        lines.append('@    frame linewidth %.01f' % self.linewidth)
        lines.append('@    frame color "%s"' % self.color)
        lines.append('@    frame pattern %s' % self.pattern)
        lines.append('@    frame background color %s' %
                     self.background_color)
        lines.append('@    frame background pattern %s' %
                     self.background_pattern)
        
	return '\n'.join(lines)
