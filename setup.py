# -*- coding: utf-8 -*-
# Copyright (C) 2019 GIS OPS UG
#
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
#

import os

from setuptools import setup

from routingpy.__version__ import __title__, __version__, __author__, __author_email__, __description__, __url__

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = __description__

# Where the magic happens:
setup(
    name=__title__,
    version=__version__,
    description=__description__,
    long_description=long_description,
    #long_description_content_type='text/markdown',
    author=__author__,
    author_email=__author_email__,
    python_requires='>=3.6.0',
    url=__url__,
    packages=['routingpy'],
    install_requires=[
        'requests>=2.21.0',
    ],
    include_package_data=True,
    license='Apache 2.0',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        # 'Programming Language :: Python :: Implementation :: PyPy'
    ])
