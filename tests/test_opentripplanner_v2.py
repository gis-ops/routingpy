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
"""Tests for the OpenTripPlannerV2 module."""

from copy import deepcopy

import responses

import tests as _test
from routingpy import OpenTripPlannerV2, convert
from routingpy.direction import Direction, Directions
from routingpy.isochrone import Isochrone, Isochrones
from tests.test_helper import *


class OpenTripPlannerV2Test(_test.TestCase):
    name = "opentripplanner_v2"

    def setUp(self):
        self.client = OpenTripPlannerV2()

    @responses.activate
    def test_full_directions(self):
        query = deepcopy(ENDPOINTS_QUERIES[self.name]["directions"])
        query["num_itineraries"] = 1

        responses.add(
            responses.POST,
            "http://localhost:8080/otp/routers/default/index/graphql",
            status=200,
            json=ENDPOINTS_RESPONSES["opentripplanner_v2"]["directions"],
            content_type="application/json",
        )

        routes = self.client.directions(**query)
        self.assertEqual(1, len(responses.calls))
        self.assertURLEqual(
            "http://localhost:8080/otp/routers/default/index/graphql",
            responses.calls[0].request.url,
        )
        self.assertIsInstance(routes, Direction)
        self.assertIsInstance(routes.distance, int)
        self.assertIsInstance(routes.duration, int)
        self.assertIsInstance(routes.geometry, list)
        self.assertIsInstance(routes.raw, dict)

    @responses.activate
    def test_full_directions_multiple_itinaries(self):
        query = ENDPOINTS_QUERIES[self.name]["directions"]

        responses.add(
            responses.POST,
            "http://localhost:8080/otp/routers/default/index/graphql",
            status=200,
            json=ENDPOINTS_RESPONSES["opentripplanner_v2"]["directions"],
            content_type="application/json",
        )

        routes = self.client.directions(**query)
        self.assertEqual(1, len(responses.calls))
        self.assertURLEqual(
            "http://localhost:8080/otp/routers/default/index/graphql",
            responses.calls[0].request.url,
        )
        self.assertIsInstance(routes, Directions)
        self.assertEqual(1, len(routes))
        for route in routes:
            self.assertIsInstance(route, Direction)
            self.assertIsInstance(route.duration, int)
            self.assertIsInstance(route.distance, int)
            self.assertIsInstance(route.geometry, list)
            self.assertIsInstance(route.raw, dict)

    @responses.activate
    def test_full_isochrones(self):
        query = deepcopy(ENDPOINTS_QUERIES[self.name]["isochrones"])
        coords = convert.delimit_list(reversed(query["locations"]), ",")

        url = f"http://localhost:8080/otp/traveltime/isochrone?location={coords}&mode={query['profile']}&arriveBy=false"

        for interval in query["intervals"]:
            cutoff = convert.seconds_to_iso8601(interval)
            url += f"&cutoff={cutoff}"

        responses.add(
            responses.GET,
            url,
            status=200,
            json=ENDPOINTS_RESPONSES[self.name]["isochrones"],
            content_type="application/json",
        )

        isochrones = self.client.isochrones(**query)

        self.assertEqual(1, len(responses.calls))
        self.assertIsInstance(isochrones, Isochrones)
        self.assertEqual(2, len(isochrones))
        self.assertIsInstance(isochrones.raw, dict)
        for iso in isochrones:
            self.assertIsInstance(iso, Isochrone)
            self.assertIsInstance(iso.geometry, list)
            self.assertIsInstance(iso.interval, int)
            self.assertEqual(iso.interval_type, "time")
