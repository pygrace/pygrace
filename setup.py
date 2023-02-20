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
#  - https://github.com/uqfoundation/pygrace/blob/master/LICENSE

import os
import sys
# drop support for older python
if sys.version_info < (3, 7):
    unsupported = 'Versions of Python before 3.7 are not supported'
    raise ValueError(unsupported)

# get distribution meta info
here = os.path.abspath(os.path.dirname(__file__))
sys.path.append(here)
from version import (__version__, __author__, __contact__ as AUTHOR_EMAIL,
                     get_license_text, get_readme_as_rst, write_info_file)
LICENSE = get_license_text(os.path.join(here, 'LICENSE'))
README = get_readme_as_rst(os.path.join(here, 'README.md'))

# write meta info file
write_info_file(here, 'pygrace', doc=README, license=LICENSE,
                version=__version__, author=__author__)
del here, get_license_text, get_readme_as_rst, write_info_file

# check if setuptools is available
try:
    from setuptools import setup
    from setuptools.dist import Distribution
    has_setuptools = True
except ImportError:
    from distutils.core import setup
    Distribution = object
    has_setuptools = False

# build the 'setup' call
setup_kwds = dict(
    name='pygrace',
    version=__version__,
    description='Python bindings to xmgrace',
    long_description = README.strip(),
    author = __author__,
    author_email = AUTHOR_EMAIL,
    maintainer = __author__,
    maintainer_email = AUTHOR_EMAIL,
    license = 'BSD-3-Clause',
    platforms = ['Linux', 'Mac'],
    url = 'https://github.com/uqfoundation/pygrace',
    download_url = 'https://pypi.org/project/pygrace/#files',
    project_urls = {
        'Documentation':'http://pygrace.rtfd.io',
        'Source Code':'https://github.com/uqfoundation/pygrace',
        'Bug Tracker':'https://github.com/uqfoundation/pygrace/issues',
    },
    python_requires = '>=3.7',
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development',
    ],
    packages = ['pygrace',
                'pygrace.interactive',
                'pygrace.extensions',
                'pygrace.styles',
                'pygrace.styles.colorbrewer',
                'pygrace.tests'],
    package_dir = {'pygrace':'pygrace',
                   'pygrace.interactive':'pygrace/interactive',
                   'pygrace.extensions':'pygrace/extensions',
                   'pygrace.styles':'pygrace/styles',
                   'pygrace.styles.colorbrewer':'pygrace/styles/colorbrewer',
                   'pygrace.tests':'pygrace/tests'},
    package_data={'pygrace.styles.colorbrewer':['*.dat','*.pdf']},
    scripts=['scripts/pygrace_cdf'],
)

# force python-, abi-, and platform-specific naming of bdist_wheel
class BinaryDistribution(Distribution):
    """Distribution which forces a binary package with platform name"""
    def has_ext_modules(foo):
        return True

# define dependencies
grace_version = 'grace>=5.1.14'
cython_version = 'cython>=0.29.30' #XXX: required to build numpy from source
numpy_version = 'numpy>=1.0'
mpmath_version = 'mpmath>=0.19'
# add dependencies
depend = [numpy_version, mpmath_version] # also: grace_version
extras = {'xmgrace': [grace_version]} #FIXME: xmgrace auto-install...?
# update setup kwds
if has_setuptools:
    setup_kwds.update(
        zip_safe=False,
        # distclass=BinaryDistribution,
        install_requires=depend,
        # extras_require=extras,
    )

# call setup
setup(**setup_kwds)

# if dependencies are missing, print a warning
try:
    import numpy
    import mpmath
    #import cython
    from os import devnull
    from subprocess import call
    xmgrace_missing = call("xmgrace -v", stdout=open(devnull, 'wb'), shell=True)
    if xmgrace_missing:
        raise ImportError
except ImportError:
    print("\n***********************************************************")
    print("WARNING: One of the following dependencies is unresolved:")
    print("    %s" % numpy_version)
    print("    %s" % mpmath_version)
    #print("    %s" % cython_version)
    print("    %s" % grace_version)
    print("***********************************************************\n")
