#!/usr/bin/env python
"""
Amaral Group
Northwestern University

Subtitle class, inherits XMG_String
"""
from xmg_string import XMG_String
class Subtitle(XMG_String):
    def __repr__(self):
	return self.contents('@    subtitle')
# =============================================================== Test function
if __name__ == '__main__':
    print Subtitle()


