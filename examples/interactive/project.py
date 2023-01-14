#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 2004-2016 California Institute of Technology.
# Copyright (c) 2023 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/uqfoundation/pygrace/blob/master/LICENSE
#
from pygrace import grace
import numpy as np

def _test():
    from time import sleep
    p = grace()
    joe = np.arange(5,50)
    p.plot(joe, joe**2, symbols=1)
    p.title('Parabola')
    sleep(2)
    p.multi(2,2)
    p.focus(1,1)
    p.plot(joe, joe, styles=1)
    p.hold(1)
    p.plot(joe, np.log(joe), styles=1)
    p.legend(['Linear', 'Logarithmic'])
    p.xlabel('Abscissa')
    p.ylabel('Ordinate')
    sleep(2)
    p.focus(1,0)
    p.histoPlot(np.sin(joe*3.14/49.0), 5./49.*3.14, 3.14)
    sleep(2)
    p.exit()

if __name__=="__main__":
   _test()
