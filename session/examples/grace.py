print "build python list"
print '''>>> from numpy import *
>>> from numpy import newaxis as NewAxis
>>> x = pi*arange(21)/10.
>>> y = cos(x)'''
from numpy import *
from numpy import newaxis as NewAxis
x = pi*arange(21)/10.
y = cos(x)

print '''build a numpy matrix'''
print '''>>> xm = x[:,NewAxis]
>>> ym = y[NewAxis,:]
>>> m = (sin(xm) + 0.1*xm) - ym**2'''
xm = x[:,NewAxis]
ym = y[NewAxis,:]
m = (sin(xm) + 0.1*xm) - ym**2

print '''instantiate the grace class'''
print '''>>> from pygrace import grace
>>> gr = grace()'''
from pygrace import grace
gr = grace()

#get help
#>>> gr.doc()

#create a colormap directly from python
#GRACE (5.1.18) CANNOT CREATE COLORMAP

#create a surface plot from within grace
#GRACE (5.1.18) CANNOT CREATE SURFACE PLOT

print '''delete a variable within grace'''
print '''>>> gr.m = m
>>> gr.delete('m')'''
gr.m = m
gr.delete('m')

print '''create a lineplot directly from python'''
print '''>>> gr.plot(x,sin(x))'''
gr.plot(x,sin(x))
raw_input("Press 'Return' to continue...")

print '''create a formatted lineplot from within grace'''
print '''>>> gr.x = x
>>> gr.y = cos(x)
>>> gr('plot(x,y)')
>>> gr('s0 line color "green"')
>>> gr('s0 symbol 1')
>>> gr('s0 symbol fill pattern 1')
>>> gr('redraw()')'''
gr.x = x
gr.y = cos(x)
gr('plot(x,y)')
gr('s0 line color "green"')
gr('s0 symbol 1')
gr('s0 symbol fill pattern 1')
gr('redraw()')
raw_input("Press 'Return' to continue...")

print '''create a histogram using the grace session interface'''
print '''#   TYPE THE FOLLOWING IN THE PROMPT:
#   grace> title "foobar"
#   grace> histoPlot(y)
#   grace> exit'''
print '''>>> gr.prompt()'''
gr.prompt()

print '''inspect variables within grace'''
print '''>>> gr.who().keys()'''
print gr.who().keys()
print '''>>> gr.who('x')'''
print gr.who('x')

print '''get variables from grace into python'''
print '''>>> gr.y'''
print gr.y
print '''>>> gr.y[0]'''
print gr.y[0]
