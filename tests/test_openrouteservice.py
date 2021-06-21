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
"""Tests for the openrouteservice module."""

from routingpy import ORS
from routingpy.direction import Direction
from routingpy.isochrone import Isochrones, Isochrone
from routingpy.matrix import Matrix
from copy import deepcopy

from tests.test_helper import *
import tests as _test

import responses
import json


class ORSTest(_test.TestCase):
    name = "ors"

    def setUp(self):
        self.key = "sample_key"
        self.client = ORS(api_key=self.key)

    @responses.activate
    def test_directions_json(self):
        query = deepcopy(ENDPOINTS_QUERIES[self.name]["directions"])

        responses.add(
            responses.POST,
            "https://api.openrouteservice.org/v2/directions/{}/json".format(query["profile"]),
            status=200,
            json=ENDPOINTS_RESPONSES[self.name]["directions"]["json"],
            content_type="application/json",
        )

        routes = self.client.directions(**query, format="json")

        query["coordinates"] = query["locations"]
        del query["locations"]
        del query["profile"]

        self.assertEqual(1, len(responses.calls))
        self.assertEqual(query, json.loads(responses.calls[0].request.body.decode("utf-8")))

        self.assertIsInstance(routes, Direction)
        self.assertIsInstance(routes.geometry, list)
        self.assertIsInstance(routes.duration, int)
        self.assertIsInstance(routes.distance, int)
        self.assertIsInstance(routes.raw, dict)

    @responses.activate
    def test_directions_geojson(self):
        query = deepcopy(ENDPOINTS_QUERIES[self.name]["directions"])

        responses.add(
            responses.POST,
            "https://api.openrouteservice.org/v2/directions/{}/geojson".format(query["profile"]),
            status=200,
            json=ENDPOINTS_RESPONSES[self.name]["directions"]["geojson"],
            content_type="application/json",
        )

        routes = self.client.directions(**query, format="geojson")

        query["coordinates"] = query["locations"]
        del query["locations"]
        del query["profile"]

        self.assertEqual(1, len(responses.calls))
        self.assertEqual(query, json.loads(responses.calls[0].request.body.decode("utf-8")))

        self.assertIsInstance(routes, Direction)
        self.assertIsInstance(routes.geometry, list)
        self.assertIsInstance(routes.duration, int)
        self.assertIsInstance(routes.distance, int)
        self.assertIsInstance(routes.raw, dict)

    @responses.activate
    def test_full_isochrones(self):
        query = deepcopy(ENDPOINTS_QUERIES[self.name]["isochrones"])

        responses.add(
            responses.POST,
            "https://api.openrouteservice.org/v2/isochrones/{}/geojson".format(query["profile"]),
            status=200,
            json=ENDPOINTS_RESPONSES[self.name]["isochrones"],
            content_type="application/json",
        )

        isochrones = self.client.isochrones(**query)

        expected = query
        expected["locations"] = [expected["locations"]]
        expected["range"] = expected["intervals"]
        expected["range_type"] = expected["interval_type"]
        del expected["intervals"]
        del expected["interval_type"]

        self.assertEqual(1, len(responses.calls))
        self.assertEqual(expected, json.loads(responses.calls[0].request.body.decode("utf-8")))

        self.assertIsInstance(isochrones, Isochrones)
        self.assertEqual(4, len(isochrones))
        self.assertIsInstance(isochrones.raw, dict)
        for iso in isochrones:
            self.assertIsInstance(iso, Isochrone)
            self.assertIsInstance(iso.geometry, list)
            self.assertIsInstance(iso.center, list)
            self.assertIsInstance(iso.interval, int)

    @responses.activate
    def test_full_matrix(self):
        query = deepcopy(ENDPOINTS_QUERIES[self.name]["matrix"])

        responses.add(
            responses.POST,
            "https://api.openrouteservice.org/v2/matrix/{}/json".format(query["profile"]),
            status=200,
            json=ENDPOINTS_RESPONSES[self.name]["matrix"],
            content_type="application/json",
        )

        matrix = self.client.matrix(**query)

        expected = query

        self.assertEqual(1, len(responses.calls))
        self.assertEqual(expected, json.loads(responses.calls[0].request.body.decode("utf-8")))

        self.assertIsInstance(matrix, Matrix)
        self.assertIsInstance(matrix.durations, list)
        self.assertIsInstance(matrix.distances, list)
        self.assertIsInstance(matrix.raw, dict)

    @responses.activate
    def test_key_in_header(self):
        # Test that API key is being put in the Authorization header
        query = ENDPOINTS_QUERIES["ors"]["directions"]

        responses.add(
            responses.POST,
            "https://api.openrouteservice.org/v2/directions/{}/geojson".format(query["profile"]),
            json=ENDPOINTS_RESPONSES[self.name]["directions"]["geojson"],
            status=200,
            content_type="application/json",
        )

        self.client.directions(**query)

        self.assertDictContainsSubset({"Authorization": self.key}, responses.calls[0].request.headers)

    @responses.activate
    def test_alternative_routes_error(self):
        # Test that alternative route works and also throws right errors
        query = deepcopy(ENDPOINTS_QUERIES["ors"]["directions"])
        query["alternative_routes"] = {"target_count": 0, "a": 0, "weight_factor": 0}

        responses.add(
            responses.POST,
            "https://api.openrouteservice.org/v2/directions/{}/geojson".format(query["profile"]),
            json=ENDPOINTS_RESPONSES[self.name]["directions"]["geojson"],
            status=200,
            content_type="application/json",
        )

        with self.assertRaises(ValueError):
            self.client.directions(**query)

        query["alternative_routes"] = [0, 1, 2, 3]

        with self.assertRaises(TypeError):
            self.client.directions(**query)
