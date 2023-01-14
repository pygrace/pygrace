#!/usr/bin/env python
# 
# Author: Mike McKerns (mmckerns @uqfoundation)
# Author: Daniel Stouffer (daniel @stoufferlab.org)
# Copyright (c) 2013 Daniel Stouffer.
# Copyright (c) 2023 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/uqfoundation/pygrace/blob/master/LICENSE
#
import os
import glob

files = ['*.agr', '*.pyc', '*.pyo', '*.log', '*~', 'cheatsheet.*']
cache = '__pycache__'

def clean_generated():
    # remove the generated files
    for pattern in files:
        for file in glob.glob(pattern):
            try:
                os.unlink(file)
            except (OSError, PermissionError):
                pass

    # empty the cache directory
    for file in glob.glob(cache + os.path.sep + '*'):
        try:
            os.unlink(file)
        except (OSError, PermissionError):
            pass

    # remove the empty cache directory
    try:
        os.rmdir('__pycache__')
    except (OSError, PermissionError):
        pass


if __name__ == '__main__':
    clean_generated()
