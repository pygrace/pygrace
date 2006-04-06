#!/usr/bin/env python
"""
Amaral Group
Northwestern University

Major needed attributes

- symbol
- line
- fill
- avalue
- errorbar
- label (for legend)

"""

class DataSet:
    """

    """
    def __init__(self, idNumber=-1,
                 datatype='xy'):
        self.idNumber = idNumber
        self.datatype = datatype

    def __getitem__(self, name): return getattr(self, name)
    def __setitem__(self, name, value): setattr(self, name, value)

    def __repr__(self):
	return '#     S' + str(self.idNumber) + ' formatting info'

    def _repr_data(self):
        return '# data goes here...\n#'
        
# =============================================================== Test function
if __name__ == '__main__':
    print DataSet()


