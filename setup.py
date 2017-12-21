#!/usr/bin/env python

from setuptools import setup

setup(name="python-dewildcard",
      py_modules = ['dewildcard'],
      entry_points = {
        'console_scripts': [
          'dewildcard = dewildcard:main',
        ],
      },
      description = "Expand wildcard imports in Python code",
      author = "Quentin Stafford-Fraser",
      author_email = "quentin@pobox.com",
      url = "http://github.com/quentinsf/dewildcard",
      download_url = 'https://github.com/quentinsf/dewildcard/tarball/0.1',
      keywords = 'pylint',
      setup_requires = ['setuptools_scm'],
      use_scm_version = True,
    )

