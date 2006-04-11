#!/usr/bin/env python
"""
Amaral Group
Northwestern University

Title class, inherits XMG_String
"""
from xmg_string import XMG_String
class Title(XMG_String):
    def __repr__(self):
	return self.contents('@    title')
        
# =============================================================== Test function
if __name__ == '__main__':
    print Title()


