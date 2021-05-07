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
"""Tests for the Mapbox Valhalla module."""

from routingpy import MapboxValhalla
import tests as _test


class MapboxValhallaTest(_test.TestCase):
    name = 'valhalla'

    def setUp(self):
        self.key = 'sample_key'
        self.client = MapboxValhalla(api_key=self.key)

    def test_config(self):
        self.client.api_key = self.key
        self.client.base_url = self.client._base_url
