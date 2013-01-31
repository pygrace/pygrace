#!/usr/bin/env python
# 
# Authors:
#  Michael McKerns    (mmckerns@caltech.edu)
#  Daniel B. Stouffer (daniel.stouffer@canterbury.ac.nz)
#  Dean Malmgren
#  Mike Stringer

try: # see if easy_install is available
    from setuptools import setup
    has_setuptools = True
except ImportError:
    from distutils.core import setup
    has_setuptools = False

# build the 'setup' call
setup_code = """
setup(name='pygrace',
      version='0.5',
      description='Python bindings and wrapper for grace',
      maintainer = 'Daniel B. Stouffer',
      maintainer_email = 'daniel.stouffer@canterbury.ac.nz',
      url = 'http://pygrace.github.com/',
      py_modules=['pygrace.axis',
                  'pygrace.base',
                  'pygrace.colors',
                  'pygrace.dataset',
                  'pygrace.drawing_objects',
                  'pygrace.fonts',
                  'pygrace.graph',
                  'pygrace.plot',
                  ],
      packages=['pygrace.session',
                'pygrace.extensions',
                'pygrace.styles',
                'pygrace.styles.colorbrewer',
                'PyGrace',
                'PyGrace.Extensions',
                'PyGrace.Styles',
                'PyGrace.Styles.ColorBrewer',
                ],
      package_dir={'PyGrace':'pygrace',
                   'PyGrace.Extensions':'pygrace/extensions',
                   'PyGrace.Styles':'pygrace/styles',
                   'PyGrace.Styles.ColorBrewer':'pygrace/styles/colorbrewer',
                   },
      package_data={'pygrace.template.styles.colorbrewer':['*.dat','*.pdf'],
                    'PyGrace.Styles.ColorBrewer':['*.dat','*.pdf'],
                    },
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
exec setup_code

# if dependencies are missing, print a warning
try:
    import numpy
    from os import devnull
    from subprocess import call
    xmgrace_missing = call("xmgrace -v", stdout=open(devnull, 'wb'), shell=True)
    if xmgrace_missing:
      raise ImportError
except ImportError:
    print "\n***********************************************************"
    print "WARNING: One of the following dependencies is unresolved:"
    print "    Numpy %s" % numpy_version
    print "    Grace %s" % grace_version
    print "***********************************************************\n"

# end of file
