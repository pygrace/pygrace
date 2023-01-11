if __name__ == '__main__':
    # Test
    import time

    from pygrace.session.process import GraceProcess
    g = GraceProcess()

    # Send some initialization commands to Grace:
    g('world xmax 100')
    g('world ymax 10000')
    g('xaxis tick major 20')
    g('xaxis tick minor 10')
    g('yaxis tick major 2000')
    g('yaxis tick minor 1000')
    g('s0 on')
    g('s0 symbol 1')
    g('s0 symbol size 0.3')
    g('s0 symbol fill pattern 1')
    g('s1 on')
    g('s1 symbol 1')
    g('s1 symbol size 0.3')
    g('s1 symbol fill pattern 1')

    # Display sample data
    for i in range(1,101):
        g('g0.s0 point %d, %d' % (i, i))
        g('g0.s1 point %d, %d' % (i, i * i))
        # Update the Grace display after every ten steps
        if i % 10 == 0:
            g('redraw')
            # Wait a second, just to simulate some time needed for
            # calculations. Your real application shouldn't wait.
            time.sleep(1)

    # Tell Grace to save the data:
    g('saveall "sample.agr"')

    # Close Grace:
    g.exit()
