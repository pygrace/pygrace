#! /usr/bin/env python
# $Id: grace_np.py,v 1.1 2004/09/18 22:37:38 mmckerns Exp $

"""A python replacement for grace_np.c, a pipe-based interface to xmgrace.

Copyright (C) 1999 Michael Haggerty

Written by Michael Haggerty <mhagger@alum.mit.edu>.  Based on
grace_np.c distributed with grace, which was written by Henrik Seidel
and the Grace Development Team.

    This library is free software; you can redistribute it and/or
    modify it under the terms of the GNU Library General Public
    License as published by the Free Software Foundation; either
    version 2 of the License, or (at your option) any later version.

    This library is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
    Library General Public License for more details; it is available
    at <http://www.fsf.org/copyleft/lgpl.html>, or by writing to the
    Free Software Foundation, Inc., 59 Temple Place - Suite 330,
    Boston, MA 02111-1307, USA.

Grace (xmgrace) is a very nice X program for doing 2-D graphics.  It
is very flexible, produces beautiful output, and has a graphical user
interface.  It is available from
<http://plasma-gate.weizmann.ac.il/Grace/>.  Grace is the successor to
ACE/gr and xmgr.

This module implements a pipe-based interface to grace similar to the
one provided by the grace_np library included with grace.  I haven't
used it very much so it is likely that it still has bugs.  I am
releasing it in the hope that it might be of use to the community.  If
you find a problem or have a suggestion, please let me know at
<mhagger@blizzard.harvard.edu>.  Other feedback is also welcome.

For a demonstration, run this file by typing `python grace_np.py'.
See the bottom of the file to see how the demonstration is programmed.

About the module:

At first I tried just to translate grace_np from C to python, but then
I realized that it is possible to do a much nicer job using classes.
The main class here is GraceProcess, which creates a running copy of
the grace program, and creates a pipe connection to it.  Through an
instance of this class you can send commands to grace.

Note that grace interprets command streams differently depending on
their source.  The pipe represented by this class is connected in such
a way that grace expects `parameter-file'-style commands (without the
@ or & or whatever).

[Details: this class communicates to grace through a -dpipe which
specified an open file descriptor from which it is to read commands.
This is the same method used by the grace_np that comes with grace.  I
thought that the -pipe option might be more convenient--just pipe
commands to standard input.  However, grace interprets commands
differently when it receives them from these two sources: -dpipe
expects parameter-file information, whereas -pipe expects datafile
information.  Also -pipe doesn't seem to respond to the `close'
command (but maybe the same effect could be had by just closing the
pipe).]

"""

__version__ = '1.0'
__cvs_version__ = 'CVS version $Revision: 1.1 $'

import sys, os, signal, errno

# global variables:
OPEN_MAX = 64 # copied from C header file sys/syslimits.h ###


class Error(Exception):
    """All exceptions thrown by this class are descended from Error."""
    pass

class Disconnected(Error):
    """Thrown when xmgrace unexpectedly disconnects from the pipe.

    This exception is thrown on an EPIPE error, which indicates that
    xmgrace has stopped reading the pipe that is used to communicate
    with it.  This could be because it has been closed (e.g., by
    clicking on the exit button), crashed, or sent an exit command."""
    pass


# Three possible states for a GraceProcess, shown with their desired
# indicators:
#
#   1. Healthy (pipe and pid both set)
#   2. Disconnected but alive (pipe.closed is set, pid still set)
#   3. Disconnected and dead (pipe.closed is set and pid is None)
#
# The error handling is such as to try to keep the above indicators
# set correctly.

class GraceProcess:
    """Represents a running xmgrace program."""

    def __init__(self, bufsize=-1, debug=0, fixedsize=None, ask=None):
        """Start xmgrace, reading from a pipe that we control.

        Parameters:
          bufsize -- choose the size of the buffer used in the
                     communication.  grace won't act on commands that
                     haven't been flushed from the buffer, but speed
                     should supposedly be better with some buffering.
                     The default is -1, which means use the default
                     (full) buffering.  0 would mean use no buffering.
          debug -- when set, each command that is passed to xmgrace is
                   also echoed to stderr.
          fixedsize -- if set to None, the grace window is
                       freely resizable (`-free').  Otherwise set to a
                       tuple, which will set the fixed size of the
                       grace canvas.  (I don't know what units are
                       used.###)
          ask -- if set, xmgrace will ask before doing `dangerous'
                 things, like overwriting a file or even clearing the
                 display.  Default is not to ask.
        """

        self.debug = debug
        self.fixedsize = fixedsize
        self.ask = ask

        cmd = ('xmgrace',)

        if self.fixedsize is None:
            cmd = cmd + ('-free',)
        else:
            cmd = cmd + ('-fixed', `self.fixedsize[0]`, `self.fixedsize[1]`)

        if self.ask is None:
            cmd = cmd + ('-noask',)

        # Python, by default, ignores SIGPIPE signals anyway
        #signal.signal(signal.SIGPIPE, signal.SIG_IGN)

        # Don't exit when our child "grace" exits (which it could if
        # the user clicks on `exit'):
        signal.signal(signal.SIGCHLD, signal.SIG_IGN)

        # Make the pipe that will be used for communication:
        (fd_r, fd_w) = os.pipe()
        cmd = cmd + ('-dpipe', `fd_r`)

        # Fork the subprocess that will start grace:
        self.pid = os.fork()

        # If we are the child, replace ourselves with grace
        if self.pid == 0:
            try:
                # This whole thing is within a try block to make sure
                # the child can't escape.
                for i in range(OPEN_MAX):
                    # close everything except stdin, stdout, stderr
                    # and the read part of the pipe
                    if i not in (fd_r,0,1,2):
                        try:
                            os.close(i)
                        except OSError:
                            pass
                try:
                    os.execvp('xmgrace', cmd)
                except:
                    # we have to be careful in the child process.  We
                    # don't want to throw an exception because that would
                    # allow two threads to continue running.
                    sys.stderr.write('GraceProcess: Could not start xmgrace\n')
                    os._exit(1) # exit this forked process but not the parent
            except:
                sys.stderr.write('Unexpected exception in child!\n')
                os._exit(2) # exit child but not parent

        # We are the parent -> keep only the writeable side of the pipe
        os.close(fd_r)

        # turn the writeable side into a buffered file object:
        self.pipe = os.fdopen(fd_w, 'w', bufsize)

    def command(self, cmd):
        """Issue a command to grace followed by a newline.

        Unless the constructor was called with bufsize=0, this
        interface is buffered, and command execution may be delayed.
        To flush the buffer, either call self.flush() or send the
        command via self(cmd)."""

        if self.debug:
            sys.stderr.write('Grace command: "%s"\n' % cmd)

        try:
            self.pipe.write(cmd + '\n')
        except IOError, err:
            if err.errno == errno.EPIPE:
                self.pipe.close()
                raise Disconnected()
            else:
                raise

    def flush(self):
        """Flush any pending commands to grace."""

        try:
            self.pipe.flush()
        except IOError, err:
            if err.errno == errno.EPIPE:
                # grace is no longer reading from the pipe:
                self.pipe.close()
                raise Disconnected()
            else:
                raise

    def __call__(self, cmd):
        """Send the command to grace, then flush the write queue."""

        self.command(cmd)
        self.flush()

    # was `GraceClosePipe':
    def __del__(self):
        """Disconnect from xmgrace process but leave it running.

        If a GraceProcess is destroyed without calling exit(), it
        disconnects from the xmgrace program but does not kill it,
        under the assumption that the user may want to continue
        manipulating the graph through the X interface.  If you want
        to force xmgrace to terminate, call self.exit()."""

        if self.is_open():
            try:
                # Ask grace to close its end of the pipe (this also
                # flushes pending commands):
                self('close')
            except Disconnected:
                # Looks like grace has already disconnected.
                pass
            else:
                # Close our end of the pipe (actually, it should be closed
                # automatically when it's deleted, but...):
                self.pipe.close()

    def is_open(self):
        """Return 1 iff the pipe is not known to have been closed."""

        # we could potentially send a kind of null-command to grace
        # here to see if it is really still alive...
        return not self.pipe.closed

    def exit(self):
        """Cause xmgrace to exit.

        Ask xmgrace to exit (i.e., for the program to shut down).  If
        it isn't listening, try to kill the process with a SIGTERM."""

        # First try--ask politely for xmgrace to exit:
        if not self.pipe.closed:
            try:
                self('exit') # this also flushes the queue
            except Disconnected:
                # self.pipe will have been closed by whomever
                # generated the exception.
                pass # drop through kill code below
            else:
                os.waitpid(self.pid, 0)
                self.pipe.close()
                self.pid = None
                return

        # Second try--kill it via a SIGTERM
        if self.pid is not None:
            try:
                os.kill(self.pid, signal.SIGTERM)
            except OSError, err:
                if err.errno == errno.ESRCH:
                    # No such process; it must already be dead
                    self.pid = None
                    return
                else:
                    raise
            os.waitpid(self.pid, 0)
            self.pid = None


if __name__ == '__main__':
    # Test
    import time

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

