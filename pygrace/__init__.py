#-----------------------------------------------------------------------------
#  Copyright (c) 2013, Daniel Stouffer. All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are met:
#
#    o Redistributions of source code must retain the above copyright notice,
#      this list of conditions, and the disclaimer that follows.
#
#    o Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions, and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#
#    o Neither the name of the copyright holders nor the names of its
#      contributors may be used to endorse or promote products derived from
#      this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
#  ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
#  LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
#  CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
#  SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
#  INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
#  CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
#  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
#  POSSIBILITY OF SUCH DAMAGE.
#-----------------------------------------------------------------------------

__all__ = [
    'axis',
    'colors',
    'dataset',
    'drawing_objects',
    'fonts',
    'grace',
    'graph',
    'parser',
	]
 
import axis
import colors
import dataset
import drawing_objects
import fonts
import graph
import parser
 
# dealing with backward compatibility
if __name__ == 'PyGrace':
       # backward compatibility for PyGrace
       from PyGrace import grace
       del plot #FIXME: somehow this is getting imported
 
elif __name__ == 'pygrace':
       __all__.append('plot')
       __all__.append('session')

       import plot
       import session

       # backward compatibility for pygrace
       def grace():
               from pygrace import session as interactive
               return interactive.grace()

# EOF
