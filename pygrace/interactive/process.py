#!/usr/local/bin/python -t
"""a pipe-based interface to xmgrace, similar to grace_np.c

The primary class is Process, which creates a running process of
the xmgrace program, and creates a pipe connected to it. The
Process class instance is used to send commands to grace.
"""
import sys
import os
import signal
import errno

__all__ = ['OPEN_MAX','Error','Disconnected','Process']

# globals
OPEN_MAX = 64


class Error(Exception):
    """Default exception for pygrace.interactive.process"""
    pass

class Disconnected(Error):
    """Error resulting from xmgrace unexpectedly connecting from the pipe.

    Thrown on an EPIPE error, which indicates that xmgrace has been
    disconnected from reading the pipe that is used to send commands.
    The pipe could be closed because xmgrace has crashed, has sent an
    exit command, or the user has clicked on the exit button."""
    pass

class Process:
    """Interface to an instance of a running xmgrace program"""

    def __init__(self, bufsize=-1, debug=0, fixedsize=None,
                 ask=None, safe=None, batch=None, project=None):
        """Start xmgrace and read from the pipe controlled by pygrace.

        Input:
          bufsize -- int, size of the buffer used. xmgrace won't
                     respond to sent commands that haven't been flushed
                     from the buffer, however the speed should improve
                     with buffering. Default is -1, which provdes full
                     buffering.  `bufsize=0` signifies no buffering.
          debug -- bool, if True, each command passed to xmgrace is
                   also sent to stderr. Default is to not debug.
          fixedsize -- tuple, used to set the fixed size of the
                       grace canvas. Default is None, which causes
                       the grace window to be freely resizable.
          ask -- bool, if True, xmgrace will ask before overwriting
                 a file, clearing the display, etc. Default is to not ask.
          safe -- bool, if True, xmgrace will ignore commands like `saveall',
                  which write to files. Default is not to be overly safe.
          batch -- str, path to command batch_file to be executed on startup
                   of xmgrace. Default is to not use a batch file.
          project -- str, path to xmgrace project file (.agr) to be executed
                     on startup. Default is to use the xmgrace default project.
        """
        self.debug = debug
        self.fixedsize = fixedsize
        self.ask = ask
        self.safe = safe
        self.batch = batch
        self.project = project

        # build the command to launch xmgrace
        com = ('xmgrace',)
        if self.fixedsize in (None, False):
            com = com + ('-free',)
        else:
            com = com + ('-fixed', repr(self.fixedsize[0]), repr(self.fixedsize[1]))
        if self.ask in (None, False):
            com = com + ('-noask',)
        if self.safe in (None, False):
            com = com + ('-nosafe',)
        if self.batch not in (None, False, ''):
            if not os.path.exists(self.batch):
                open(self.batch, 'r') # raise FileNotFoundError
            else:
                com = com + ('-batch', self.batch)

        # Don't exit when xmgrace exits (e.g. user clicks `exit')
        signal.signal(signal.SIGCHLD, signal.SIG_IGN)

        # Create a numbered pipe used for communication to xmgrace
        (fd_r, fd_w) = os.pipe()
        if hasattr(os, 'set_inheritable'):
            os.set_inheritable(fd_w, True)
            os.set_inheritable(fd_r, True)
        com = com + ('-dpipe', repr(fd_r))

        # Open project file, if given [needs to be last]
        if self.project not in (None, False, ''):
            if not os.path.exists(self.project):
                open(self.project, 'r') # raise FileNotFoundError
            else:
                com = com + (self.project,)

        # Fork the subprocess that starts xmgrace
        self.pid = os.fork()

        # Replace the child process with grace
        if self.pid == 0:
            try:
                # Ensure the child can't escape by closing everything
                # except stdin, stdout, stderr, and fd_r
                for i in range(OPEN_MAX):
                    if i not in (fd_r,0,1,2):
                        try:
                            os.close(i)
                        except OSError:
                            pass
                try:
                    os.execvp('xmgrace', com)
                except:
                    # carefully handle the child process, as an exception
                    # would enable two threads to continue running.
                    sys.stderr.write('Process: could not start xmgrace\n')
                    os._exit(1) # exit the forked process but not the parent
            except:
                sys.stderr.write('Process: exception in child process\n')
                os._exit(2) # exit the child but not the parent

        # close the readable end of the pipe
        os.close(fd_r)

        # convert the writeable end of the pipe into a buffered file object:
        self.pipe = os.fdopen(fd_w, 'w', bufsize)

    def command(self, com):
        """send a command to xmgrace

        Input:
          com -- str, command to send to xmgrace

        A newline will be added to the command. Unless the instance of
        the Process class was created using bufsize=0, the interface will
        be buffered, and thus the execution of the command may be delayed.
        To flush the buffer, use self.flush(), or alternately, send commands
        that are automatically flushed, using self(com)."""

        if self.debug:
            sys.stderr.write('pexec: "%s"\n' % com)

        try:
            self.pipe.write(com + '\n')
        except IOError as err:
            if err.errno == errno.EPIPE:
                self.pipe.close()
                raise Disconnected()
            else:
                raise

    def flush(self):
        """flush any pending commands for xmgrace"""
        try:
            self.pipe.flush()
        except IOError as err:
            if err.errno == errno.EPIPE:
                # grace is no longer reading from the pipe
                self.pipe.close()
                raise Disconnected()
            else:
                raise

    def __call__(self, com):
        """send a command to xmgrace, then flush the write queue"""
        self.command(com)
        self.flush()

    def __del__(self):
        """disconnect from a xmgrace process, but leave xmgrace running

        If a Process instance is deleted without calling exit(), it
        disconnects from xmgrace without killing xmgrace. This assumes
        that the user may want to continue manipulating the graph through
        the xmgrace GUI interface. To force xmgrace to terminate, use
        self.exit()"""
        if self.is_open():
            try:
                # ask xmgrace to close its end of the pipe,
                # flushing any pending commands
                self('close')
            except Disconnected:
                # xmgrace has already disconnected
                pass
            else:
                # close the write end of the pipe. It should be closed
                # automatically when the instance is deleted, however
                # we help out by closing it explcitly
                self.pipe.close()

    def is_open(self):
        """True, if the pipe has not been closed"""

        # we could potentially send a kind of null-command to grace
        # here to see if it is really still alive...
        return not self.pipe.closed

    def exit(self):
        """cause xmgrace to exit

        nicely ask xmgrace to exit (i.e. terminate), however, if xmgrace
        doesn't respond then try to kill the process with a SIGTERM."""

        # ask politely for xmgrace to exit
        if not self.pipe.closed:
            try:
                self('exit') # also flushes the queue
            except Disconnected:
                # self.pipe has been closed, and generated an exception
                pass # skip the hard kill below
            else:
                try:
                    os.waitpid(self.pid, 0)
                except OSError:
                    # no such process; assume the process is already dead
                    pass
                self.pipe.close()
                self.pid = None
                return

        # kill xmgrace using SIGTERM
        if self.pid is not None:
            try:
                os.kill(self.pid, signal.SIGTERM)
            except OSError as err:
                if err.errno == errno.ESRCH:
                    # no such process; assume the process is already dead
                    self.pid = None
                    return
                else:
                    raise
            os.waitpid(self.pid, 0)
            self.pid = None

