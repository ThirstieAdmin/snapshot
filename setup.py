#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Note: To use the 'upload' functionality of this file, you must:
#   $ pip install twine

import io
import os
import sys
from shutil import rmtree


from setuptools import find_packages, setup, Command

NAME = 'snapshot'
DESCRIPTION = 'Friendly tool to backup and restore MySQL databases'
URL = 'https://github.com/ThirstieAdmin/snapshot'
AUTHOR = 'Brendan Berg'
EMAIL = 'brendan@thirstie.com'
VERSION = (0, 1, 1)

REQUIRED = [
    # 'requests',
]

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()


# ============================================================================
# The actual call to setuptools:
# ----------------------------------------------------------------------------

setup(
    name=NAME,
    version='.'.join(map(str, VERSION)),
    description=DESCRIPTION,
    long_description=long_description,
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    packages=find_packages(exclude=('tests',)),

    # entry_points={
    #     'console_scripts': ['snapshot=snapshot'],
    # },
    scripts=['bin/snapshot'],

    include_package_metadata=True,
    license='MIT',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
    ],
)
