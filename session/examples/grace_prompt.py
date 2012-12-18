#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# 2/11/2005 version 0.0.1a
# mmckerns@caltech.edu
# (C) 2005 All Rights Reserved
#
# <see __licence__ in pygrace.py>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
__author__ = 'Mike McKerns'


x = [1,2,3,4,5]
y = [1,4,9,16,25]
print 'x: %s' % x
print 'y: %s' % y
raw_input('Please press return to continue...\n')

##### grace #####
from pygrace import grace
pg = grace()
#pg.doc()
pg.plot(x,y)
print '''EXAMPLE SCRIPT:
 grace> z = [2,8,18,32,50]
 grace> histoPlot(z)
 grace> s0 fill color 3
 grace> redraw()
 grace> exit
'''
pg.prompt()
