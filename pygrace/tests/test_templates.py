#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 2004-2016 California Institute of Technology.
# Copyright (c) 2023 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/uqfoundation/pygrace/blob/master/LICENSE
#
import os
this = os.path.abspath(os.path.dirname(__file__) or os.path.curdir)
examples = this.rsplit(os.path.sep, 2)[0] + os.path.sep + 'examples'
try:
    os.chdir(examples)
except FileNotFoundError:
    print("'examples' tests not found")
    exit()
import sys
sys.path.append(examples)
from test_examples import test_runner
PASSED = 'PASSED' == test_runner()
from clean_examples import clean_generated
clean_generated()
os.chdir(this)

assert PASSED
