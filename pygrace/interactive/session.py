#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 2004-2016 California Institute of Technology.
# Copyright (c) 2016-2023 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/pygrace/pygrace/blob/altmerge/LICENSE
#
__license__ = """    
Copyright (c) 2004-2016 California Institute of Technology.
Copyright (c) 2016-2023 The Uncertainty Quantification Foundation.
All rights reserved.

This software is available subject to the conditions and terms laid
out below. By downloading and using this software you are agreeing
to the following conditions.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met::

    - Redistribution of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.

    - Redistribution in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentations and/or other materials provided with the distribution.

    - Neither the names of the copyright holders nor the names of any of
      the contributors may be used to endorse or promote products derived
      from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

If you use this software to do productive scientific research that leads to
publication, we ask that you acknowledge use of the software by citing the
following in your publication:

    "pygrace: python bindings to the Grace plotting package", Michael McKerns,
    http://pygrace.github.io
"""


__author__='Mike McKerns'
__doc__ = '''Instructions for pygrace:
Import the grace class          >>> from pygrace import grace
Instantiate the grace class     >>> pg = grace()
Get help                        >>> pg.doc()
'''

from math import *
from numpy import *


class grace:   #Nathan Gray's gracePlot with interactive prompt added
    '''Python-grace bindings
Methods:
  prompt() --> start interactive session
  eval(command) --> execute a xmgrace command
  put(name,val) --> put variable into interactive session
  get(name) --> get variable from interactive session
  who([name]) --> return the existing xmgrace variables
  delete(name) --> destroy selected xmgrace variables
  restart() --> restart a xmgrace window
  saveall(filename) --> save project to xmgrace.agr or given filename
Notes:
  xmgrace and numpy must be installed, xmgrace also relies on (open)motif
'''
    _privdoc='''Private methods:
 _validate(name) --> raise NameError if is invalid python name
 _putlocal(name,value) --> add a variable to local store
 _getlocal(name) --> return variable value from local store
 _poplocal(name) --> delete variable from local store, return value
 _wholist() --> get list of strings containing xmgrace variables 
 _exists(name) --> True if is a variable in xmgrace
'''

    def __init__(self):
        from .plot import gracePlot as grace_plot
        self.session = grace_plot()
        self.whos = {}
        self.reserved = ['and','assert','break','class','continue','def','del',
                         'elif','else','except','exec','finally','for','from',
                         'global','if','import','in','is','lambda','not','or',
                         'pass','print','raise','return','try','while','yield',
                         'as','None']
        return

    def __getattr__(self,name):
        _locals = dict(self=self, name=name)
        try:
            code = 'from math import *; from numpy import *;'
            code += 'attr = self.session.'+name
            code = compile(code, '<string>', 'exec')
            exec(code, _locals)
            attr = _locals['attr']
        except:
            code = 'from math import *; from numpy import *;'
            code += 'attr = self.get("'+name+'")'
            code = compile(code, '<string>', 'exec')
            exec(code, _locals)
            attr = _locals['attr']
        return attr

    def __setattr__(self,name,value):
        if name in ['session','whos','reserved']:
            self.__dict__[name] = value
            return
        self.put(name,value)
        return

    def __call__(self,*args):
        for arg in args:
            self.eval(arg)
        return

    def _validate(self,name):
        '''_validate(name) --> raise NameError if is invalid python name'''
        #a valid python name begins with a letter or underscore,
        #and can include only alphanumeric symbols and the underscore.
        #python also does not allow redefinition of reserved words.
        if not name: raise NameError("invalid name")
        import re
        if re.compile('[_a-zA-Z]').sub('',name[0]):
            raise NameError("invalid first character '%s'" % name[0])
        badc = re.compile('[_a-zA-Z0-9]').sub('',name)
        if badc: raise NameError("invalid name '%s'; remove '%s'" % (name,badc))
        if name.lower() in self.reserved:
            raise NameError("invalid name '%s'; is a reserved word" % name)
        return

    def _putlocal(self,name,value):
        '''_putlocal(name,value) --> add a variable to local store'''
        self._validate(name)
        self.whos[name] = value
        return

    def _getlocal(self,name,skip=True):
        '''_getlocal(name) --> return variable value from local store'''
        if name in self.whos:
            return self.whos[name]
        if skip: return #name not found in local store
        raise NameError("'%s' is not defined locally" % str(name))

    def _poplocal(self,name):
        '''_poplocal(name) --> delete variable from local store, return value'''
        return self.whos.pop(name,None)

    def _wholist(self):
        '''_wholist() --> get list of strings containing xmgrace variables''' 
        return list(self.whos.keys())

    def _exists(self,name):
        '''_exists(name) --> True if is a variable in xmgrace'''
        exists = self._wholist().count(name)
        if exists: return True
        return False

    def doc(self):
        print(self.__doc__)
        print(__license__[:153]) # print copyright
        print(__license__[-291:]) # print reference
        return

    def restart(self):
        '''restart() --> restart a xmgrace window'''
        vars = self.who()
        self.exit()
        self.session = None
        self.__init__()
        self.session.whos = vars
        return

    def put(self,name,val):
        '''put(name,val) --> add variable to xmgrace session'''
        _locals = dict(self=self, name=name, val=val)
        if name.count('[') or name.count('.') or name.count('('):
            varlist = self._wholist()
            for var in varlist: #put whos into locals()
                code = 'from math import *; from numpy import *;'
                code += var+" = self._getlocal('"+var+"')"
                code = compile(code, '<string>', 'exec')
                exec(code, _locals)
                locals()[var] = _locals[var]
            if (type(val) is type(array([]))):
                val = val.tolist()
                code = 'from math import *; from numpy import *;'
                code += name+' = array('+str(val)+')'
            else: code = name+' = '+str(val)
            code = compile(code, '<string>', 'exec')
            exec(code, _locals)
            locals()[name] = _locals[name]
            for var in varlist: #use varlist to update state variables
                _locals[var] = locals()[var]
                code = 'from math import *; from numpy import *;'
                code += 'self._putlocal("'+var+'",locals()["'+var+'"])'
                code = compile(code, '<string>', 'exec')
                exec(code, _locals)
            return
        return self._putlocal(name,val)

    def get(self,name):
        '''get(name) --> value; get value from xmgrace session'''
        #if name.count('+') or ...
        #if name.count('[') or name.count('.') or name.count('('):
        _locals = dict(self=self, name=name)
        varlist = self._wholist()
        for var in varlist: #put whos into locals()
            code = 'from math import *; from numpy import *;'
            code += var+" = self._getlocal('"+var+"')"
            code = compile(code, '<string>', 'exec')
            exec(code, _locals)
            locals()[var] = _locals[var]
        code = 'from math import *; from numpy import *;'
        code += '___ = '+name
        code = compile(code, '<string>', 'exec')
        exec(code, _locals)
        ___ = _locals['___'] #get from _locals as temp variable
        return ___
        #return self._getlocal(name)

    def who(self,name=None):
        '''who([name]) --> return the existing xmgrace variables'''
        if name: return self._getlocal(name,skip=False)
        return self.whos

    def delete(self,name):
        '''delete(name) --> destroy selected xmgrace variables'''
        if not name.count(','):
            self._poplocal(name)
            return
        vars = name.split(',')
        for var in vars:
            self.delete(var.strip())
        return

    def saveall(self,filename=None):
        '''saveall(filename) --> save project to xmgrace.agr or given filename'''
        if filename is None: filename = 'xmgrace.agr'
        com = 'saveall "%s"' % filename
        return self.eval(com)

    def eval(self,com):
        '''eval(command) --> execute a xmgrace command'''
        outlist = []
        _locals = dict(outlist=outlist, self=self, com=com)
        if self.whos: #add to outlist
            for name,val in list(self.whos.items()):
#               if numerix:
                if (type(val) is type(array([]))):
                    val = val.tolist()
                    code = 'from math import *; from numpy import *;'
                    code += name+' = array('+str(val)+');'
                else: code = name+' = '+str(val)+';'
                code += 'outlist.append("'+name+'")'
                code = compile(code, '<string>', 'exec')
                exec(code, _locals)
                locals()[name] = _locals[name]
            outlist[:] = _locals['outlist']
        if com == 'exit':
            return
        try: #if intended for python
            code = 'from math import *; from numpy import *;'
            code = compile(code+com, '<string>', 'exec')
            exec(code, _locals)
            if com.startswith('del '):
                names = com.split('del ')[1].strip()
                self.delete(names)
                return
            if com.count('='):
                name = com.split('=')[0].strip()
                if not name.count('['):
                    outlist.append(name)
                    locals()[name] = _locals[name]
        except:
            try: #if intended for gracePlot
                code = 'from math import *; from numpy import *;'
                code += 'self.session.'+com
                code = compile(code, '<string>', 'exec')
                exec(code, _locals)
            except:
                try: #if intended for grace
                    self.session._send(com)
                except: #is unknown command
                    raise RuntimeError(com)
        for name in outlist: #use outlist to update state variables
            if name in list(locals().keys()):
                _locals[name] = locals()[name]
                code = 'from math import *; from numpy import *;'
                code += 'self._putlocal("'+name+'",locals()["'+name+'"])'
                code = compile(code, '<string>', 'exec')
                exec(code, _locals)
        return

    def prompt(self):
        '''an interactive xmgrace session'''
        outlist = []
        _locals = dict(outlist=outlist, self=self)
        print("grace interface:")
        if self.whos: #print 'put' variables, add to outlist
            print("vars=")
            for name,val in list(self.whos.items()):
#               if numerix:
                if (type(val) is type(array([]))):
                    val = val.tolist()
                    code = 'from math import *; from numpy import *;'
                    code += name+' = array('+str(val)+');'
                else: code = name+' = '+str(val)+';'
                code += 'print("     "+"'+name+'");'
                code += 'outlist.append("'+name+'")'
                code = compile(code, '<string>', 'exec')
                exec(code, _locals)
                locals()[name] = _locals[name]
            outlist[:] = _locals['outlist']
        while 1:
            com = input('grace> ')
##          print(com)
            if com == 'exit':
                break
            elif com == 'exit()':
                self.session.exit()
                break
            else:
                try: #if intended for python
                    code = 'from math import *; from numpy import *;'
                    code = compile(code+com, '<string>', 'exec')
                    exec(code, _locals)
                    if com.startswith('del '):
                        names = com.split('del ')[1].strip()
                        vars = names.split(',')
                        for var in vars:
                            self.delete(var.strip())
                            outlist.remove(var.strip())
                    if com.count('='):
                        name = com.split('=')[0].strip()
                        if not name.count('['):
                            outlist.append(name)
                            locals()[name] = _locals[name]
                except:
                    try: #if intended for gracePlot
                        code = 'from math import *; from numpy import *;'
                        code += 'self.session.'+com
                        code = compile(code, '<string>', 'exec')
                        exec(code, _locals)
                    except:
                        try: #if intended for grace
                            self.session._send(com)
                        except: #is unknown command
                            print("RuntimeError: %s" % com)
        for name in outlist: #use outlist to update state variables
            if name in list(locals().keys()):
                _locals[name] = locals()[name]
                code = 'from math import *; from numpy import *;'
                code += 'self._putlocal("'+name+'",locals()["'+name+'"])'
                code = compile(code, '<string>', 'exec')
                exec(code, _locals)
        return

#           elif com.startswith('python('):
#               pcom = com[7:-1]
#               try:
#                   exec(pcom)
#               except:
#                   print("PythonError: %s" % pcom)
#           elif com.startswith('*'):
#               pcom = com[1:]
#               try:
#                   exec('self.session.'+pcom)
#               except:
#                   print("GraceError: %s" % pcom)
#           else:
#               self.session._send(com)

