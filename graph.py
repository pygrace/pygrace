#!/usr/bin/env python
"""
Amaral Group
Northwestern University

Major needed attributes:

- title  (Sam attempted this, check out the xmg_string class)
- subtitle  (ditto by Sam)
- xaxis   (Sam is doing this
- yaxis   and this)
- legend
- frame
- datasets

"""

from dataset import DataSet
from axis import Axis
from title import Title
from subtitle import Subtitle
from xmg_string import XMG_String
from frame import Frame

INDEX_ORIGIN = 0  # zero or one (one is for losers)

class Graph:
    """Graph class

    """
<<<<<<< .mine
    def __init__(self, idNumber = -1,
                 title = XMG_String(),
                 subtitle = XMG_String(),
                 frame = Frame(),
                 nDataSets = 0):
=======
    def __init__(self, idNumber=-1,title=Title(),
                 subtitle=Subtitle(label='AKA the best of the best',size=1.0),
                 xaxis=Axis(label=XMG_String(type='label',label='Waggle'),orientation='x'),
                 yaxis=Axis(label=XMG_String(type='label',label='Wiggle'),orientation='y'),
                 nDataSets=0):
>>>>>>> .r10
        self.title=title
        self.subtitle=subtitle
        self.xaxis=xaxis
        self.yaxis=yaxis
        self.idNumber = idNumber
        self.frame = frame
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
<<<<<<< .mine
        lines.append(str(self.frame))
=======
        lines.append(self.xaxis.contents())
        lines.append(self.yaxis.contents())
>>>>>>> .r10
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


