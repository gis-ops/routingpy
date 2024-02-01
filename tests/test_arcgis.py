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

"""Tests for the ArcGIS module."""

from copy import deepcopy

import responses

import tests as _test
from routingpy import ArcGIS
from routingpy.direction import Direction
from tests.test_helper import *

class ArcGISTest(_test.TestCase):
    name = "arcgis"

    def setUp(self):
        self.key = "sample_key"
        self.client = ArcGIS(api_key=self.key)

    @responses.activate
    def test_directions(self):
        query = deepcopy(ENDPOINTS_QUERIES[self.name]["directions"])

        responses.add(
            responses.GET,
            "https://route.arcgis.com/arcgis/rest/services/World/Route/NAServer/Route_World/solve",
            status=200,
            json=ENDPOINTS_RESPONSES[self.name]["directions"],
            content_type="application/json",
        )

        routes = self.client.directions(**query)
        self.assertEqual(1, len(responses.calls))
        self.assertURLEqual(
            "https://route.arcgis.com/arcgis/rest/services/World/Route/NAServer/Route_World/solve?token=sample_key&stops=8.688641%2C49.420577%3B8.680916%2C49.415776&f=json",
            responses.calls[0].request.url,
        )

        self.assertIsInstance(routes, Direction)
        self.assertIsInstance(routes.duration, int)
        self.assertIsInstance(routes.distance, int)
        self.assertIsInstance(routes.raw, dict)