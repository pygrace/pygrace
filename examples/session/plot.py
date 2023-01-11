from pygrace.session.plot import gracePlot
import numpy as np

def _test():
    from time import sleep
    p = gracePlot()
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
