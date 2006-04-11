#!/usr/bin/env python
"""
Amaral Group
Northwestern University

Generic xmgrace string class that only has 4 attributes:

-label
-font
-color
-size

can be used as a whole or inherited from
"""

class XMG_String:
    """

    """
    def __init__(self, label='The Dogs Bollocks',font='Helvetica',
                 color='black',size=1.5):
        self.font=font
        self.color=color
        self.size=size
        self.label=label

    def __getitem__(self, name): return getattr(self, name)
    def __setitem__(self, name, value): setattr(self, name, value)
    
    def contents(self,prefix):
        lines = []

        lines.append(prefix + ' "'+ str(self.label)+'"')
        lines.append(prefix + ' color "' + str(self.color)+'"')
        lines.append(prefix + ' size ' + str(self.size))
        lines.append(prefix + ' font "' + str(self.font)+'"')

        return '\n'.join(lines)

    """
    Strictly speaking, the __repr__ function should not be used from this class
    It is there for testing purposes but because of the variety of strings used
    In XMGrace, this class is merely an over-hyped dictionary for storing values
    """
    def __repr__(self):
        lines = []

        lines.append(str(self.label));
        lines.append('color ' + str(self.color));
        lines.append('size ' + str(self.size));
        lines.append('font ' + str(self.font));
	return '\n'.join(lines)
        
# =============================================================== Test function
if __name__ == '__main__':
    print XMG_String()


