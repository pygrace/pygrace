if __name__ == '__main__':
    # Test
    import time

    from pygrace import grace
    gr = grace()
    p = gr.session.pexec

    # Send some initialization commands to Grace:
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

    # Display sample data
    for i in range(1,101):
        p('g0.s0 point %d, %d' % (i, i))
        p('g0.s1 point %d, %d' % (i, i * i))
        # Update the Grace display after every ten steps
        if i % 10 == 0:
            p('redraw')
            # Wait a second, just to simulate some time needed for
            # calculations. Your real application shouldn't wait.
            time.sleep(1)

    # Tell Grace to save the data:
    p('saveall "sample.agr"')

    # Close Grace:
    gr.exit()
