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

"""Tests for the MapQuest module."""

from copy import deepcopy

import responses

import tests as _test
from routingpy import MapQuest
from routingpy.direction import Direction
from tests.test_helper import *

class MapQuestTest(_test.TestCase):
    name = "mapquest"

    def setUp(self):
        self.key = "sample_key"
        self.client = MapQuest(api_key=self.key)

    @responses.activate
    def test_directions(self):
        query = deepcopy(ENDPOINTS_QUERIES[self.name]["directions"])

        responses.add(
            responses.GET,
            "https://www.mapquestapi.com/directions/v2/route",
            status=200,
            json=ENDPOINTS_RESPONSES[self.name]["directions"],
            content_type="application/json",
        )

        routes = self.client.directions(**query)
        self.assertEqual(1, len(responses.calls))
        self.assertURLEqual(
            "https://www.mapquestapi.com/directions/v2/route?key=sample_key&from=8.688641%2C49.420577&to=8.680916%2C49.415776",
            responses.calls[0].request.url,
        )

        self.assertIsInstance(routes, Direction)
        self.assertIsInstance(routes.duration, int)
        self.assertIsInstance(routes.distance, int)
        self.assertIsInstance(routes.raw, dict)