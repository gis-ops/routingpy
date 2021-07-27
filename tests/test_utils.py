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
"""Tests for utils module."""

from routingpy import utils
import tests as _test


class UtilsTest(_test.TestCase):
    def setUp(self):
        self.coords2d_5prec = r"smslH__`t@~\fo@"
        self.coords3d_5prec = r"smslH__`t@_sV~\fo@etjG"
        self.coords2d_6prec = r"aqkg}Aa_iqO`kHxaN"
        self.coords3d_6prec = r"aqkg}Aa_iqO_sV`kHxaNetjG"

    def test_polyline5_2d_decoding(self):

        decoded = [(8.68864, 49.42058), (8.68092, 49.41578)]
        self.assertEqual(decoded, utils.decode_polyline5(self.coords2d_5prec))

    def test_polyline5_3d_decoding(self):

        decoded = [(8.68864, 49.42058, 120.96), (8.68092, 49.41578, 1491.39)]
        self.assertEqual(decoded, utils.decode_polyline5(self.coords3d_5prec, True))

    def test_polyline6_2d_decoding(self):

        decoded = [(8.688641, 49.420577), (8.680916, 49.415776)]
        self.assertEqual(decoded, utils.decode_polyline6(self.coords2d_6prec))

    def test_polyline6_3d_decoding(self):

        decoded = [(8.688641, 49.420577, 120.96), (8.680916, 49.415776, 1491.39)]
        self.assertEqual(decoded, utils.decode_polyline6(self.coords3d_6prec, True))

    def test_polyline6_3d_decoding_latlng(self):

        decoded = [(49.420577, 8.688641, 120.96), (49.415776, 8.680916, 1491.39)]
        self.assertEqual(decoded, utils.decode_polyline6(self.coords3d_6prec, True, order="latlng"))

    def test_get_ordinal(self):

        self.assertEqual(utils.get_ordinal(0), "th")
        self.assertEqual(utils.get_ordinal(1), "st")
        self.assertEqual(utils.get_ordinal(2), "nd")
        self.assertEqual(utils.get_ordinal(3), "rd")
