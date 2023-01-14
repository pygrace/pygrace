#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 2004-2016 California Institute of Technology.
# Copyright (c) 2023 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/uqfoundation/pygrace/blob/master/LICENSE
#
if __name__ == '__main__':
    import time

    # get the low-level parameter command interface
    # for an interactive grace instance
    from pygrace import grace
    gr = grace()
    p = gr.session.pexec

    # send some initialization commands to xmgrace:
    p('world xmax 100')
    p('world ymax 10000')
    p('xaxis tick major 20')
    p('xaxis tick minor 10')
    p('yaxis tick major 2000')
    p('yaxis tick minor 1000')
    p('s0 on')
    p('s0 symbol 1')
    p('s0 symbol size 0.3')
    p('s0 symbol fill pattern 1')
    p('s1 on')
    p('s1 symbol 1')
    p('s1 symbol size 0.3')
    p('s1 symbol fill pattern 1')

    # display sample data
    for i in range(1,101):
        p('g0.s0 point %d, %d' % (i, i))
        p('g0.s1 point %d, %d' % (i, i * i))
        # update the xmgrace display after every ten steps
        if i % 10 == 0:
            p('redraw')
            # wait a second, just to simulate some time needed for
            # calculations. Your real application shouldn't wait.
            time.sleep(1)

    # tell xmgrace to save the data:
    gr.saveall('process.agr')

    # close xmgrace:
    gr.exit()
