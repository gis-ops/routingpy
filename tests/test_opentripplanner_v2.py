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

import urllib.parse
from copy import deepcopy

import responses

import tests as _test
from routingpy import OpenTripPlannerV2, convert
from routingpy.direction import Direction, Directions
from routingpy.isochrone import Isochrone, Isochrones
from routingpy.raster import Raster
from tests.test_helper import *


class OpenTripPlannerV2Test(_test.TestCase):
    name = "otp_v2"

    def setUp(self):
        self.client = OpenTripPlannerV2()

    @responses.activate
    def test_directions(self):
        query = deepcopy(ENDPOINTS_QUERIES[self.name]["directions"])
        responses.add(
            responses.POST,
            "http://localhost:8080/otp/routers/default/index/graphql",
            status=200,
            json=ENDPOINTS_RESPONSES["otp_v2"]["directions"],
            content_type="application/json",
        )
        direction = self.client.directions(**query)
        self.assertEqual(1, len(responses.calls))
        self.assertURLEqual(
            "http://localhost:8080/otp/routers/default/index/graphql",
            responses.calls[0].request.url,
        )
        self.assertIsInstance(direction, Direction)
        self.assertIsInstance(direction.distance, int)
        self.assertIsInstance(direction.duration, int)
        self.assertIsInstance(direction.geometry, list)
        self.assertIsInstance(direction.departure_datetime, datetime.datetime)
        self.assertEqual(direction.departure_datetime.tzinfo, datetime.timezone.utc)
        self.assertIsInstance(direction.arrival_datetime, datetime.datetime)
        self.assertEqual(direction.arrival_datetime.tzinfo, datetime.timezone.utc)

    @responses.activate
    def test_directions_alternative(self):
        query = ENDPOINTS_QUERIES[self.name]["directions_alternative"]
        responses.add(
            responses.POST,
            "http://localhost:8080/otp/routers/default/index/graphql",
            status=200,
            json=ENDPOINTS_RESPONSES["otp_v2"]["directions"],
            content_type="application/json",
        )
        directions = self.client.directions(**query)
        self.assertEqual(1, len(responses.calls))
        self.assertURLEqual(
            "http://localhost:8080/otp/routers/default/index/graphql",
            responses.calls[0].request.url,
        )
        self.assertIsInstance(directions, Directions)
        self.assertEqual(1, len(directions))
        for direction in directions:
            self.assertIsInstance(direction, Direction)
            self.assertIsInstance(direction.duration, int)
            self.assertIsInstance(direction.distance, int)
            self.assertIsInstance(direction.geometry, list)
            self.assertIsInstance(direction.raw, dict)
            self.assertIsInstance(direction.departure_datetime, datetime.datetime)
            self.assertEqual(direction.departure_datetime.tzinfo, datetime.timezone.utc)
            self.assertIsInstance(direction.arrival_datetime, datetime.datetime)
            self.assertEqual(direction.arrival_datetime.tzinfo, datetime.timezone.utc)

    @responses.activate
    def test_isochrones(self):
        query = deepcopy(ENDPOINTS_QUERIES[self.name]["isochrones"])
        url = "http://localhost:8080/otp/traveltime/isochrone"
        params = [
            ("location", convert.delimit_list(reversed(query["locations"]), ",")),
            ("time", query["time"].isoformat()),
            ("modes", query["profile"]),
            ("arriveBy", "false"),
        ]
        for cutoff in query["cutoffs"]:
            params.append(("cutoff", convert.seconds_to_iso8601(cutoff)))

        responses.add(
            responses.GET,
            url + "?" + urllib.parse.urlencode(params),
            status=200,
            json=ENDPOINTS_RESPONSES[self.name]["isochrones"],
            content_type="application/json",
        )
        isochrones = self.client.isochrones(**query)
        self.assertEqual(1, len(responses.calls))
        self.assertIsInstance(isochrones, Isochrones)
        self.assertEqual(2, len(isochrones))
        self.assertIsInstance(isochrones.raw, dict)
        for isochrone in isochrones:
            self.assertIsInstance(isochrone, Isochrone)
            self.assertIsInstance(isochrone.geometry, list)
            self.assertIsInstance(isochrone.interval, int)
            self.assertEqual(isochrone.interval_type, "time")

    @responses.activate
    def test_raster(self):
        query = deepcopy(ENDPOINTS_QUERIES[self.name]["raster"])
        url = "http://localhost:8080/otp/traveltime/surface"
        params = [
            ("location", convert.delimit_list(reversed(query["locations"]), ",")),
            ("time", query["time"].isoformat()),
            ("modes", query["profile"]),
            ("arriveBy", "false"),
            ("cutoff", convert.seconds_to_iso8601(query["cutoff"])),
        ]
        with open("tests/raster_example.tiff", "rb") as raster_file:
            image = raster_file.read()
            responses.add(
                responses.GET,
                url + "?" + urllib.parse.urlencode(params),
                status=200,
                body=image,
                content_type="image/tiff",
            )
            raster = self.client.raster(**query)
            self.assertIsInstance(raster, Raster)
            self.assertEqual(raster.image, image)
            self.assertEqual(raster.max_travel_time, query["cutoff"])
