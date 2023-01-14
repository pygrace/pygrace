#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 2004-2016 California Institute of Technology.
# Copyright (c) 2023 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/uqfoundation/pygrace/blob/master/LICENSE
#
x = [1,2,3,4,5]
y = [1,4,9,16,25]
print('x: %s' % x)
print('y: %s' % y)
input('Please press return to continue...\n')

##### grace #####
from pygrace import grace
pg = grace()
#pg.doc()
pg.plot(x,y)
print('''EXAMPLE SCRIPT:
 grace> z = [2,8,18,32,50]
 grace> histoPlot(z)
 grace> s0 fill color 3
 grace> redraw()
 grace> exit
''')
pg.prompt()
