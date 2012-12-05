from distutils.core import setup

setup(
    name = "PyGrace",
    version = "1.0",
    description = "Python wrapper for writing Grace files",
    author = "Daniel B. Stouffer",
    author_email = "daniel@stoufferlab.org",
    url = "http://pygrace.github.com",
    packages = ['PyGrace',
                'PyGrace.Extensions',
                'PyGrace.Styles',
                'PyGrace.Styles.ColorBrewer',
                ],
    package_data={'PyGrace.Styles.ColorBrewer': ['*.dat'],
                  },
    scripts=['PyGrace/Scripts/pg_cdf'],

)
