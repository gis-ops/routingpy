# -*- coding: utf-8 -*-
# Copyright (C) 2021 GIS OPS UG
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
"""Converts Python types to string representations suitable for GET queries.
"""


def delimit_list(arg, delimiter=","):
    """Convert list to delimiter-separated string"""
    if not is_list(arg):
        raise TypeError("Expected a list or tuple, " "but got {}".format(type(arg).__name__))
    return delimiter.join(map(str, arg))


def convert_bool(boolean):
    """Convert to stringified boolean"""

    return str(boolean).lower()


def format_float(arg):
    """Formats a float value to be as short as possible.

    Trims extraneous trailing zeros and period to give API
    args the best possible chance of fitting within 2000 char
    URL length restrictions.

    For example:

    format_float(40) -> "40"
    format_float(40.0) -> "40"
    format_float(40.1) -> "40.1"
    format_float(40.001) -> "40.001"
    format_float(40.0010) -> "40.001"

    :param arg: The lat or lng float.
    :type arg: float

    :rtype: string
    """
    return "{}".format(round(float(arg), 6)).rstrip("0").rstrip(".")


def is_list(arg):
    """Checks if arg is list-like."""
    if isinstance(arg, dict):
        return False
    if isinstance(arg, str):  # Python 3-only, as str has __iter__
        return False
    return (
        not _has_method(arg, "strip") and _has_method(arg, "__getitem__") or _has_method(arg, "__iter__")
    )


def _has_method(arg, method):
    """Returns true if the given object has a method with the given name.

    :param arg: the object

    :param method: the method name
    :type method: string

    :rtype: bool
    """
    return hasattr(arg, method) and callable(getattr(arg, method))
