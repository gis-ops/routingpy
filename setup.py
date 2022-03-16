# -*- coding: utf-8 -*-
#
# Copyright 2021 Kenneth Reitz
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
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

description = "One lib to route them all."

try:
    with open(os.path.join(here, "README.rst"), encoding="utf-8") as f:
        long_description = "\n" + f.read()
except FileNotFoundError:
    long_description = description

setup(
    name="routingpy",
    description=description,
    long_description=long_description,
    long_description_content_type="text/x-rst",
    author="Nils Nolde",
    author_email="nils@gis-ops.com",
    python_requires=">=3.7.0",
    url="https://github.com/gis-ops/routing-py",
    packages=find_packages(exclude=["*tests*"]),
    install_requires=["requests>=2.20.0"],
    license="Apache 2.0",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.1ß",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
)
