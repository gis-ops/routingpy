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
"""Tests for convert module."""

import tests as _test
from routingpy import convert


class UtilsTest(_test.TestCase):  # noqa: E741
    def test_delimit_list(self):
        l = [(8.68864, 49.42058), (8.68092, 49.41578)]  # noqa: E741
        s = convert.delimit_list([convert.delimit_list(pair, ",") for pair in l], "|")
        self.assertEqual(s, "8.68864,49.42058|8.68092,49.41578")

    def test_delimit_list_error(self):
        falses = ["8", 8, {"a": "b", 3: "a", 4: 4}]
        for f in falses:
            with self.assertRaises(TypeError):
                convert.delimit_list(f)
