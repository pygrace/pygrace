#!/usr/bin/env python
# 
# Michael McKerns
# mmckerns@caltech.edu 

try: # see if easy_install is available
    from setuptools import setup
    has_setuptools = True
except ImportError:
    from distutils.core import setup
    has_setuptools = False

# build the 'setup' call
setup_code = """
setup(name='pygrace',
      version='0.4',
      description='Python bindings for grace',
      author = 'Mike McKerns',
      author_email = 'mmckerns@caltech.edu',
      url = 'http://www.its.caltech.edu/~mmckerns/software/',
      packages=['pygrace'],
      package_dir={'pygrace':''},
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
    from os import system
    xmgrace_missing = system("xmgrace -v") #grep "Grace-" | sed -e "s/Grace-//"
    if xmgrace_missing: raise ImportError
except ImportError:
    print "\n***********************************************************"
    print "WARNING: One of the following dependencies is unresolved:"
    print "    Numpy %s" % numpy_version
    print "    Grace %s" % grace_version
    print "***********************************************************\n"

# end of file
