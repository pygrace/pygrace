#!/usr/bin/env python
"""
Amaral Group
Northwestern University

Major needed attributes:

- title
- subtitle
- xaxis
- yaxis
- legend
- frame
- datasets

"""

from dataset import DataSet

INDEX_ORIGIN = 0  # zero or one (one is for losers)

class Graph:
    """Graph class

    """
    def __init__(self, idNumber=-1,
                 nDataSets=0):

        self.idNumber = idNumber
        self.datasets = []
        self._datasetIndex = INDEX_ORIGIN
        for i in range(nDataSets):
            self.add_dataset()

    def __getitem__(self, name): return getattr(self, name)
    def __setitem__(self, name, value): setattr(self, name, value)

    def __repr__(self):
        lines = []

        lines.append('# G' + str(self.idNumber) + ' formatting info')
        lines.extend(map(str,self.datasets))

	return '\n'.join(lines)

    def add_dataset(self, dataset=False):
        """add_dataset() -> none

        Temporary stub to test main Grace output
        """
        idNumber = self._datasetIndex

        if not dataset:
            self.datasets.append(DataSet(idNumber))
        else:
            self.datasets.append(dataset)
            dataset['idNumber'] = idNumber
        
        self._datasetIndex += 1
        return idNumber

# =============================================================== Test function
if __name__ == '__main__':
    print DataSet()


