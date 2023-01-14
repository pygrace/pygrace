#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 2004-2016 California Institute of Technology.
# Copyright (c) 2023 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/uqfoundation/pygrace/blob/master/LICENSE
#
from pygrace import grace

if __name__ == "__main__":
    x = list(range(1,15))
    y = []
    for i in x:
        y.append(i*i)
    g = grace()
    g.plot(x,y)
    g.put('x',x)
    g.put('y',y)
    g.prompt()
    print(g.who())
    g.exit()

