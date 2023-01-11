#!/usr/local/bin/python -t
"""a pipe-based interface to xmgrace

This module implements a pipe-based interface to grace similar to the
one provided by the grace_np library included with grace.

The main class here is GraceProcess, which creates a running copy of
the grace program, and creates a pipe connection to it.  Through an
instance of this class you can send commands to grace.
"""

import sys, os, signal, errno

# global variables:
OPEN_MAX = 64


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


class GraceProcess:
    """Represents a running xmgrace program."""

    def __init__(self, bufsize=-1, debug=0, fixedsize=None, ask=None, safe=None):
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
          safe -- if set, xmgrace will ignore commands like `saveall',
                  which write to files. Default is not to be overly safe.
        """

        self.debug = debug
        self.fixedsize = fixedsize
        self.ask = ask
        self.safe = safe

        cmd = ('xmgrace',)

        if self.fixedsize in (None, False):
            cmd = cmd + ('-free',)
        else:
            cmd = cmd + ('-fixed', repr(self.fixedsize[0]), repr(self.fixedsize[1]))

        if self.ask in (None, False):
            cmd = cmd + ('-noask',)

        if self.safe in (None, False):
            cmd = cmd + ('-nosafe',)

        # Python, by default, ignores SIGPIPE signals anyway
        #signal.signal(signal.SIGPIPE, signal.SIG_IGN)

        # Don't exit when our child "grace" exits (which it could if
        # the user clicks on `exit'):
        signal.signal(signal.SIGCHLD, signal.SIG_IGN)

        # Make the pipe that will be used for communication:
        (fd_r, fd_w) = os.pipe()
        if hasattr(os, 'set_inheritable'):
            os.set_inheritable(fd_w, True)
            os.set_inheritable(fd_r, True)
        cmd = cmd + ('-dpipe', repr(fd_r))

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
        #os.close(fd_r)

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
        except IOError as err:
            if err.errno == errno.EPIPE:
                self.pipe.close()
                raise Disconnected()
            else:
                raise

    def flush(self):
        """Flush any pending commands to grace."""

        try:
            self.pipe.flush()
        except IOError as err:
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
                try:
                    os.waitpid(self.pid, 0)
                except OSError:
                    # No such process; it must already be dead
                    pass
                self.pipe.close()
                self.pid = None
                return

        # Second try--kill it via a SIGTERM
        if self.pid is not None:
            try:
                os.kill(self.pid, signal.SIGTERM)
            except OSError as err:
                if err.errno == errno.ESRCH:
                    # No such process; it must already be dead
                    self.pid = None
                    return
                else:
                    raise
            os.waitpid(self.pid, 0)
            self.pid = None

