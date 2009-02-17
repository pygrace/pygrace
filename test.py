"""This module is a wrapper that runs the scripts that generate figures using
PyFig.  If errors occur, full Tracebacks of the errors are sent to standard
out."""

from sys import stderr, stdout
from subprocess import Popen, PIPE
from os.path import sep, splitext

exampleList = [
    './Examples/00_helloworld.py',
    './Examples/01_singleplot.py',
    './Examples/02_multiplot.py',
    './Examples/03_simplesubclass.py',
    './Examples/04_classy.py',
    './Examples/05_colorplot.py',
    './Examples/06_logautoscale.py',
    './Examples/07_panels.py',
    './Examples/08_latexlabels.py',
    ]

if __name__ == '__main__':

    PYTHON_PATH = '/usr/bin/env python' 
    SHOW_DETAILED_ERROR_OUTPUT = True

    # output title message to shell
    print >> stderr, ('Running tests ' + '-' * 80)[:79]

    # initialize counters
    testNumber = 1
    nWork = 0
    nTests = len(exampleList)

    # run tests ---------------------------------------------------------------
    for scriptPath in exampleList:

        # extract script path
        print >> stderr, '%3i) %-67s' % (testNumber, scriptPath),

        # try to make figure using pyfig script (execute in shell)
        command = '%s %s' % (PYTHON_PATH, scriptPath)
        childProcess = Popen(command, shell=True, stderr=PIPE)

        # write output of error stream
        errorOutput = childProcess.stderr.read()
        if errorOutput:
            root, ext = splitext(scriptPath)
            errorStream = open('%s.log' % root, 'w')
            print >> errorStream, errorOutput
            errorStream.close()
        
        # tell the shell whether the script successfully ran
        if childProcess.wait():
            print >> stderr, 'failed'
        else:
            print >> stderr, 'passed'
            nWork += 1

        testNumber += 1

    # print output to shell depending on results of tests ---------------------
    if nWork == nTests:
        allPassed = 'PASSED'
    else:
        allPassed = 'FAILED'

    message = '\nTests %s: %i of %i were successful.' % \
              (allPassed, nWork, nTests)
    print >> stderr, message

    if allPassed == 'FAILED' and SHOW_DETAILED_ERROR_OUTPUT:

        message = """
The output of standard error for each test script are stored in the same file
as the output with a .log extension."""
        print >> stderr, message

    if allPassed == 'PASSED':

        message = """
All of the test scripts successfully ran, but make sure to check the figures
that were created, as they may not look right even though the scripts did not
throw an error."""
        print >> stderr, message

