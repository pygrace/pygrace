#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Author: Daniel Stouffer (daniel @stoufferlab.org)
# Author: Dean Malmgren
# Author: Mike Stringer
# Copyright (c) 2004-2016 California Institute of Technology.
# Copyright (c) 2013 Daniel Stouffer.
# Copyright (c) 2023 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/pygrace/pygrace/blob/altmerge/LICENSE
#
try: # see if easy_install is available
    from setuptools import setup
    has_setuptools = True
except ImportError:
    from distutils.core import setup
    has_setuptools = False

# build the 'setup' call
setup_code = """
setup(name='pygrace',
      version='1.1',
      description='Python interface to xmgrace and xmgrace project files',
      author = 'Michael McKerns, Daniel B. Stouffer',
      author_email = 'mmckerns@uqfoundation.org, daniel@stoufferlab.org',
      maintainer = 'Michael McKerns',
      maintainer_email = 'mmckerns@uqfoundation.org',
      url = 'http://pygrace.github.com',
      py_modules=['pygrace.axis',
                  'pygrace.base',
                  'pygrace.colors',
                  'pygrace.dataset',
                  'pygrace.drawing_objects',
                  'pygrace.fonts',
                  'pygrace.graph',
                  'pygrace.parser',
                  'pygrace.project',
                  ],
      packages=['pygrace.interactive',
                'pygrace.extensions',
                'pygrace.styles',
                'pygrace.styles.colorbrewer',
                'pygrace.tests',
                ],
      package_data={'pygrace.styles.colorbrewer':['*.dat','*.pdf'],
                    },
      scripts=['scripts/pygrace_cdf'],
"""

# add dependencies
grace_version = '>=5.1.14'
numpy_version = '>=1.0'
if has_setuptools:
    setup_code += """
      install_requires=("numpy%s"),
""" % numpy_version

# close 'setup' call, and exec the code
setup_code += """    
      )
"""
exec(setup_code)

# if dependencies are missing, print a warning
try:
    import numpy
    from os import devnull
    from subprocess import call
    xmgrace_missing = call("xmgrace -v", stdout=open(devnull, 'wb'), shell=True)
    if xmgrace_missing:
      raise ImportError
except ImportError:
    print("\n***********************************************************")
    print("WARNING: One of the following dependencies is unresolved:")
    print("    Numpy %s" % numpy_version)
    print("    Grace %s" % grace_version)
    print("***********************************************************\n")
