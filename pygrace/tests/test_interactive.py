#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 2004-2016 California Institute of Technology.
# Copyright (c) 2023 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/uqfoundation/pygrace/blob/master/LICENSE
#
from pygrace import grace
from numpy import *

import unittest
import time

class PyGrace_PyGrace_TestCase(unittest.TestCase):
    def setUp(self):
        '''grace: instantiate a grace session'''
        time.sleep(1)
        self.session = grace()
        self.int = 1
        self.list = [1,2]
        self.array = array(self.list)
        self.dict = {}
        self.matrix = [[1,2,3],[4,5,6]]
        self.none = None
        self.str = 'foo'
        self.bytearray = array(self.str)
        self.strlist = ["hello", "world"]
        return #FIXME: do I want a new session for each test?

    def tearDown(self):
        '''grace: destroy a grace session'''
        self.session.exit()
        self.session = None
        return #FIXME: do I want a new session for each test?

    def test_grace_getlocal(self):
        '''grace: return variable value from local store'''
        Z = 666
        self.session.whos['a'] = self.int
        self.session.whos['b'] = self.list
        self.session.whos['c'] = self.array
        self.session.whos['n'] = self.none
        self.session.whos['s'] = self.str
        self.session.whos['z'] = Z
        self.assertEqual(self.int, self.session._getlocal('a'))
        self.assertEqual(self.list, self.session._getlocal('b'))
        self.assertEqual(self.array.tolist(),\
                         self.session._getlocal('c').tolist())
        self.assertEqual(self.none, self.session._getlocal('n'))
        self.assertEqual(self.str, self.session._getlocal('s'))
        self.assertEqual(Z, self.session._getlocal('z'))
        self.assertEqual(None, self.session._getlocal('x')) #KeyError not raised
        self.assertEqual(self.int, self.session._getlocal('a',skip=False))
        self.assertRaises(NameError, self.session._getlocal,'x',skip=False)
        return

    def test_grace_poplocal(self):
        '''grace: delete variable from local store'''
        Z = 666
        self.session.whos['a'] = self.int
        self.session.whos['b'] = self.list
        self.session.whos['c'] = self.array
        self.session.whos['n'] = self.none
        self.session.whos['s'] = self.str
        self.session.whos['z'] = Z
        self.assertEqual(self.int, self.session._poplocal('a'))
        self.assertEqual(self.list, self.session._poplocal('b'))
        self.assertEqual(self.array.tolist(),\
                         self.session._poplocal('c').tolist())
        self.assertEqual(self.none, self.session._poplocal('n'))
        self.assertEqual(self.str, self.session._poplocal('s'))
        self.assertEqual(Z, self.session._poplocal('z'))
        self.assertEqual(None, self.session._poplocal('x')) #KeyError not raised
        self.assertEqual({},self.session.whos)
        return

    def test_grace_validate(self):
        '''grace: fail upon invalid name'''
        self.assertTrue(self.session._validate("foo") == None,
                     "failure to validate a valid variable")
        self.assertTrue(self.session._validate("f_o1o") == None,
                     "failure to validate a valid variable")
        self.assertRaises(NameError,self.session._validate,'1foo')
        self.assertRaises(NameError,self.session._validate,'$foo')
        self.assertRaises(NameError,self.session._validate,'f.oo')
        self.assertRaises(NameError,self.session._validate,'foo!')
        self.assertRaises(NameError,self.session._validate,'for')
        return

    def test_gracedelete(self):
        '''grace: delete grace variables'''
        self.session.put("a",1)
        self.session.put("b",2)
        self.session.put("c",3)
        self.assertTrue(self.session.delete("c") == None,
                     "failure to delete a grace variable")
        whos = {'a': 1, 'b': 2}
        self.assertEqual(whos, self.session.who())
        self.assertTrue(self.session.delete("a, b") == None,
                     "failure to delete a grace variable tuple")
        whos = {}
        self.assertEqual(whos, self.session.who())
        self.assertTrue(self.session.delete("z") == None,
                     "failure to skip delete for unknown variable")
        whos = {}
        self.assertEqual(whos, self.session.who())
        self.assertTrue(self.session.delete("[0,1]") == None,
                     "failure to skip delete for bad syntax")
        whos = {}
        self.assertEqual(whos, self.session.who())
        return

    def test_graceevalgrace(self):
        '''grace: evaluate a gracePlot expression'''
        self.assertTrue(self.session.eval("redraw()") == None,
                     "failure to evaluate a gracePlot expression")
        self.assertTrue(self.session.eval("s0 line color 2") == None,
                     "failure to evaluate a grace expression")
        return

    def test_gracerestart(self):
        '''grace: restart a grace window'''
        self.session.eval('a = 1')
        self.assertTrue(self.session.restart() == None,
                     "failure to restart grace window")
        whos = {} #FIXME: {'a': 1} # session preserved across window close?
        self.assertEqual(whos, self.session.who())
        self.assertTrue(self.session.redraw() == None,
                     "failure to reinitialize grace session")
        return

    def test_gracewho(self):
        '''grace: inquire who are the grace variables'''
        self.session.put('a',self.int)
        self.session.put('b',self.list)
        self.session.put('c',self.array)
        self.session.put('s',self.str)
        whos = {'a':self.int, 'b':self.list, 's':self.str, 'c':self.array}
        self.assertEqual(self.int,self.session.who('a'))
        self.assertEqual(self.list,self.session.who('b'))
        self.assertEqual(self.array.tolist(),self.session.who('c').tolist())
        self.assertEqual(self.str,self.session.who('s'))
        self.assertEqual(whos,self.session.who())
        whos['n'] = self.none
        self.session.put('n',None)
        self.assertEqual(self.none,self.session.who('n'))
        self.assertEqual(whos,self.session.who())
        self.assertRaises(NameError,self.session.who,'x')
        self.assertRaises(NameError,self.session.who,'a, b') #XXX: allow this?
        self.assertEqual(whos,self.session.who())
        return

#   def test_gracedependancy(self):
#       '''grace: check package dependancies'''
#       self.assert_(exec 'import numpy' == None,"failure to import numpy")
#       return

    def test_grace__getattr__(self):
        '''grace: call grace method if gracePlot method is implicit'''
        self.assertTrue(self.session.redraw() == None,"implicit method not found ")
        #self.assertRaises(AttributeError,self.session.foo,'x')
        return

    def test_grace_putlocal(self):
        '''grace: add variable to local store'''
        Z = 666
        self.assertTrue(self.session._putlocal("a",self.int) == None,
                     "failure to add scalar to local store")
        self.assertTrue(self.session._putlocal("b",self.list) == None,
                     "failure to add list to local store")
        self.assertTrue(self.session._putlocal("c",self.array) == None,
                     "failure to add array to local store")
        self.assertTrue(self.session._putlocal("n",self.none) == None,
                     "failure to add None to local store")
        self.assertTrue(self.session._putlocal("s",self.str) == None,
                     "failure to add string to local store")
        self.assertTrue(self.session._putlocal("z",Z) == None,
                     "failure to add to named local store")
        self.assertEqual(self.int, self.session.whos['a'])
        self.assertEqual(self.list, self.session.whos['b'])
        self.assertEqual(self.array.tolist(), self.session.whos['c'].tolist())
        self.assertEqual(self.none, self.session.whos['n'])
        self.assertEqual(self.str, self.session.whos['s'])
        self.assertEqual(Z, self.session.whos['z'])
        self.assertRaises(NameError,self.session._putlocal,'foo!',69)
        return

    def test_grace_wholist(self):
        '''grace: check list of string names for all grace variables'''
        self.session.eval("a = 1")
        self.session.eval("b = [1,2]")
        self.session.eval("s = 'foo'")
        self.session.put("n",None)
        wholist = ['a', 'b', 's', 'n']
        self.assertEqual(wholist, self.session._wholist())
        return

    def test_grace_exists(self):
        '''grace: check if grace variable exists'''
        self.session.eval("a = 1")
        self.assertEqual(True, self.session._exists('a'))
        self.assertEqual(False, self.session._exists('b'))
        return

    def test_graceput(self):
        '''grace: pass a variable into grace'''
        self.assertTrue(self.session.put("a",self.int) == None,
                     "failure to pass an int to grace")
        self.assertTrue(self.session.put("b",self.list) == None,
                     "failure to pass a list to grace")
        self.assertTrue(self.session.put("c",self.array) == None,
                     "failure to pass an array to grace")
        self.assertTrue(self.session.put("s",self.str) == None,
                     "failure to pass a string to IDL")
        whos = {'a': self.int, 'c': self.array, 'b': self.list, 's': self.str}
        self.assertEqual(whos, self.session.who())
        self.assertEqual(self.int, self.session.get('a'))
        self.assertEqual(self.list, self.session.get('b'))
        self.assertEqual(self.array.tolist(), self.session.get('c').tolist())
        self.assertEqual(self.str, self.session.get('s'))
        self.assertRaises(NameError,self.session.put,'x[0]',1)
        self.assertRaises(NameError,self.session.put,'a+a',2)
        self.assertRaises(TypeError,self.session.put,'a[1:3]',0)
        self.assertRaises(IndexError,self.session.put,'b[100]',0)
        self.assertRaises(SyntaxError,self.session.put,'b[]',0)
        self.assertEqual(whos, self.session.who())
        return

    def test_graceget(self):
        '''grace: extract a variable from grace'''
        self.session.put("a",self.int)
        self.session.put("b",self.list)
        self.session.put("c",self.array)
        self.session.put("s",self.str)
        whos = {'a': self.int, 'c': self.array, 'b': self.list, 's': self.str}
        self.assertTrue(self.session.get('a') == whos['a'],
                     "failure to extract an int from grace")
        self.assertTrue(self.session.get('b') == whos['b'],
                     "failure to extract a list from grace")
        self.assertTrue((self.session.get('c') == whos['c']).all(),
                     "failure to extract an array from grace")
        self.assertTrue(self.session.get('s') == whos['s'],
                     "failure to extract a string from grace")
        self.assertRaises(NameError,self.session.get,'x')
        self.assertRaises(NameError,self.session.get,'sin(x)')
        self.assertEqual(whos,self.session.who())
        self.assertEqual(self.list[0],self.session.get('b[0]'))
        self.assertEqual(self.list[0]+self.int,self.session.get('b[0]+a'))
        self.assertRaises(SyntaxError,self.session.get,'x[]')
        return

#   def test_graceeval(self):
#       '''grace: eval TESTS NOT IMPLEMENTED'''
#       pass

    def test_graceevalpython(self):
        '''grace: evaluate a python expression'''
        self.assertTrue(self.session.eval("a = 1") == None,
                     "failure to eval an int")
        self.assertTrue(self.session.eval("b = [1,2]") == None,
                     "failure to eval a list")
        self.assertTrue(self.session.eval("c = array([[1,2,3,4]])") == None,
                     "failure to eval a 2D array")
        self.assertTrue(self.session.eval("import os") == None,
                     "failure to eval a python builtin")
        whos = {'a': 1, 'c': array([[1, 2, 3, 4]]).tolist(), 'b': [1, 2]}
        who_ = self.session.who()
        who_['c'] = who_['c'].tolist() # assertEqual with lists not arrays
        self.assertEqual(whos, who_)
        return

    def test_graceevalexit(self):
        '''grace: do nothing upon 'exit' command'''
        self.session.eval('a = 1')
        whos = {'a': 1}
        self.assertTrue(self.session.eval("exit") == None,
                     "failure to skip 'exit' command")
        self.assertEqual(whos, self.session.who())
        return

    def test_graceevalbigexit(self):
        '''grace: exit a grace window upon 'exit()' command'''
        self.session.eval('a = 1')
        whos = {'a': 1}
        self.assertTrue(self.session.eval("exit()") == None,
                     "failure to exit grace window")
        self.assertEqual(whos, self.session.who())
        self.assertRaises(ValueError,self.session.plot,[1,2],[3,4])
        return

    def test_graceevaldel(self):
        '''grace: delete a grace variable upon 'del' command'''
        self.session.eval("a = 1")
        self.session.eval("b = 2")
        self.session.eval("c = 3")
        self.assertTrue(self.session.eval("del b, c") == None,
                     "failure to perform 'del' command")
        whos = {'a': 1}
        self.assertEqual(whos, self.session.who())
        return

    def test_graceevalundefined(self):
        '''grace: let grace catch all command errors internally'''
        self.assertTrue(self.session.eval("foo()") == None,
                     "failure of grace to catch command error internally")
        self.assertTrue(self.session.eval("s = t") == None,
                     "failure of grace to catch command error internally")
        whos = {}
        self.assertEqual(whos, self.session.who())
#       '''grace: fail when expression is undefined'''
#       self.assertRaises(RuntimeError,self.session.eval,"foo()")
#       self.assertRaises(RuntimeError,self.grace.eval,"s = t")
        return #FIXME: is this the desired behavior?

#   def test_graceprompt(self):
#       '''grace: prompt TESTS NOT IMPLEMENTED'''
#       pass


if __name__ == "__main__":
    import shutil
    installed = bool(shutil.which('xmgrace'))
    if installed:
        suite0 = unittest.makeSuite(PyGrace_PyGrace_TestCase)
        alltests = (suite0,)
        alltests = unittest.TestSuite(alltests)
        unittest.TextTestRunner(verbosity=2).run(alltests)
    else:
        print('xmgrace was not found on $PATH')


#  End of file 
