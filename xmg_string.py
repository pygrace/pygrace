#!/usr/bin/env python
"""
Amaral Group
Northwestern University

Generic xmgrace string class that only has 4 attributes:

-label
-font
-color
-size
-type  (this is used to discern between title or label type string, important for some outputs)

can be used as a whole or inherited from
"""

class XMG_String:
    """

    """
    def __init__(self, label='The Dogs Bollocks',font='Helvetica',
                 color='black',size=1.5,type='title'):
        self.font=font
        self.color=color
        self.size=size
        self.label=label
        self.type=type

    def __getitem__(self, name): return getattr(self, name)
    def __setitem__(self, name, value): setattr(self, name, value)
    
    def contents(self,prefix):
        lines = []

        lines.append(prefix + ' "'+ str(self.label)+'"')
        lines.append(prefix + ' color "' + str(self.color)+'"')
        if(self.type == 'title'):
            lines.append(prefix + ' size ' + str(self.size))

        if(self.type == 'label'):
            lines.append(prefix + ' char size ' + str(self.size))
        
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


