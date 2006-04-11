#!/usr/bin/env python
"""
Amaral Group
Northwestern University

Major needed attributes:

- title  (Sam attempted this, check out the xmg_string class)
- subtitle  (ditto by Sam)
- xaxis
- yaxis
- legend
- frame
- datasets

"""

from dataset import DataSet
from xmg_string import XMG_String

INDEX_ORIGIN = 0  # zero or one (one is for losers)

class Graph:
    """Graph class

    """
    def __init__(self, idNumber=-1,title=XMG_String(),
                 subtitle=XMG_String(),nDataSets=0):
        self.title=title
        subtitle["label"]="AKA the best of the best"
        subtitle["size"]=1.0
        self.subtitle=subtitle
        self.idNumber = idNumber
        self.datasets = []
        self._datasetIndex = INDEX_ORIGIN
        for i in range(nDataSets):
            self.add_dataset()

    def __getitem__(self, name): return getattr(self, name)
    def __setitem__(self, name, value): setattr(self, name, value)

    def __repr__(self):
        lines = []

        lines.append('@g' + str(self.idNumber) + ' on')
        lines.append('@with g' + str(self.idNumber))
        lines.append('@    view xmin 0.150000')
        lines.append('@    view xmax 1.150000')
        lines.append('@    view ymin 0.150000')
        lines.append('@    view ymax 0.850000')
        lines.append(self.title.contents('@    title'))
        lines.append(self.subtitle.contents('@    subtitle'))
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
# can dean check this in?  Mos Def!
if __name__ == '__main__':
    print DataSet()


