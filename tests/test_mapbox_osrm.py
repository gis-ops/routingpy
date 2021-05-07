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
"""Tests for the Graphhopper module."""

from routingpy import MapboxOSRM
from routingpy import convert
from routingpy.direction import Directions, Direction
from routingpy.isochrone import Isochrones, Isochrone
from routingpy.matrix import Matrix
from tests.test_helper import *
import tests as _test

import responses
from copy import deepcopy
from collections import Counter


class MapboxOSRMTest(_test.TestCase):
    name = 'mapbox_osrm'

    def setUp(self):
        self.client = MapboxOSRM(api_key='sample_key')

    @responses.activate
    def test_full_directions(self):
        query = deepcopy(ENDPOINTS_QUERIES[self.name]['directions'])
        query['alternatives'] = False

        responses.add(
            responses.POST,
            'https://api.mapbox.com/directions/v5/mapbox/{}'.format(query['profile']),
            status=200,
            json=ENDPOINTS_RESPONSES['mapbox_osrm']['directions'],
            content_type='application/x-www-form-urlencoded',
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )

        routes = self.client.directions(**query)
        self.assertEqual(1, len(responses.calls))

        # python 3.5 dict doesn't guarantee the order when added input to x-www-form-urlencoded
        expected_url = (
            'coordinates=8.688641%2C49.420577%3B8.680916%2C49.415776%3B8.780916%2C49.445776&'
            'radiuses=500%3B500%3B500&bearings=50%2C50%3B50%2C50%3B50%2C50&alternatives=false&steps=true&'
            'continue_straight=true&annotations=duration%2Cdistance%2Cspeed&geometries=geojson&'
            'overview=simplified&exclude=motorway&approaches=%3Bcurb%3Bcurb%3Bcurb&banner_instuctions=true&'
            'language=de&roundabout_exits=true&voide_instructions=true&voice_units=metric&'
            'waypoint_names=a%3Bb%3Bc&waypoint_targets=%3B8.688641%2C49.420577%3B8.680916%2C49.415776%3B'
            '8.780916%2C49.445776'
        ).split("&")
        called_url = responses.calls[0].request.body.split("&")
        self.assertTrue(Counter(expected_url) == Counter(called_url))

        self.assertIsInstance(routes, Direction)
        self.assertIsInstance(routes.geometry, list)
        self.assertIsInstance(routes.duration, int)
        self.assertIsInstance(routes.distance, int)
        self.assertIsInstance(routes.raw, dict)

    @responses.activate
    def test_full_directions_alternatives(self):
        query = ENDPOINTS_QUERIES[self.name]['directions']

        responses.add(
            responses.POST,
            'https://api.mapbox.com/directions/v5/mapbox/{}'.format(query['profile']),
            status=200,
            json=ENDPOINTS_RESPONSES['mapbox_osrm']['directions'],
            content_type='application/x-www-form-urlencoded',
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )

        routes = self.client.directions(**query)

        self.assertEqual(1, len(responses.calls))

        # python 3.5 dict doesn't guarantee the order when added input to x-www-form-urlencoded
        expected_url = (
            'coordinates=8.688641%2C49.420577%3B8.680916%2C49.415776%3B8.780916%2C49.445776&'
            'radiuses=500%3B500%3B500&bearings=50%2C50%3B50%2C50%3B50%2C50&alternatives=3&steps=true&'
            'continue_straight=true&annotations=duration%2Cdistance%2Cspeed&geometries=geojson&'
            'overview=simplified&exclude=motorway&approaches=%3Bcurb%3Bcurb%3Bcurb&banner_instuctions=true&'
            'language=de&roundabout_exits=true&voide_instructions=true&voice_units=metric&'
            'waypoint_names=a%3Bb%3Bc&waypoint_targets=%3B8.688641%2C49.420577%3B8.680916%2C49.415776%3B'
            '8.780916%2C49.445776'
        ).split("&")
        called_url = responses.calls[0].request.body.split("&")
        self.assertTrue(Counter(expected_url) == Counter(called_url))

        self.assertIsInstance(routes, Directions)
        self.assertEqual(1, len(routes))
        self.assertIsInstance(routes[0], Direction)
        self.assertIsInstance(routes[0].geometry, list)
        self.assertIsInstance(routes[0].duration, int)
        self.assertIsInstance(routes[0].distance, int)
        self.assertIsInstance(routes.raw, dict)

    @responses.activate
    def test_full_isochrones(self):
        query = ENDPOINTS_QUERIES[self.name]['isochrones']

        responses.add(
            responses.GET,
            'https://api.mapbox.com/isochrone/v1/{}/{}'.format(
                query["profile"],
                convert._delimit_list(query["locations"]),
            ),
            status=200,
            json=ENDPOINTS_RESPONSES[self.name]['isochrones'],
            content_type='application/json'
        )

        iso = self.client.isochrones(**query)

        self.assertEqual(1, len(responses.calls))
        self.assertURLEqual(
            'https://api.mapbox.com/isochrone/v1/mapbox/driving/8.34234,48.23424?costing=mapbox/driving&access_token=sample_key&'
            'contours_colors=ff0000%2C00FF00&contours_minutes=10%2C20&denoise=0.1&generalize=0.5&polygons=True',
            responses.calls[0].request.url
        )
        self.assertIsInstance(iso, Isochrones)
        self.assertEqual(2, len(iso))
        for ischrone in iso:
            self.assertIsInstance(ischrone, Isochrone)
            self.assertIsInstance(ischrone.geometry, list)
            self.assertIsInstance(ischrone.interval, int)
            self.assertIsInstance(ischrone.center, list)

    @responses.activate
    def test_full_matrix(self):
        query = ENDPOINTS_QUERIES[self.name]['matrix']
        coords = convert._delimit_list([convert._delimit_list(pair) for pair in query['locations']], ';')

        responses.add(
            responses.GET,
            'https://api.mapbox.com/directions-matrix/v1/mapbox/{}/{}'.format(query['profile'], coords),
            status=200,
            json=ENDPOINTS_RESPONSES['mapbox_osrm']['matrix'],
            content_type='application/json'
        )

        matrix = self.client.matrix(**query)

        self.assertEqual(1, len(responses.calls))
        self.assertURLEqual(
            'https://api.mapbox.com/directions-matrix/v1/mapbox/driving/8.688641,49.420577;8.680916,49.415776;8.780916,49.445776?'
            'access_token=sample_key&annotations=distance%2Cduration&fallback_speed=50',
            responses.calls[0].request.url
        )
        self.assertIsInstance(matrix, Matrix)
        self.assertIsInstance(matrix.distances, list)
        self.assertIsInstance(matrix.durations, list)
        self.assertIsInstance(matrix.raw, dict)

    @responses.activate
    def test_few_sources_destinations_matrix(self):
        query = deepcopy(ENDPOINTS_QUERIES[self.name]['matrix'])
        coords = convert._delimit_list([convert._delimit_list(pair) for pair in query['locations']], ';')

        query['sources'] = [1, 2]
        query['destinations'] = [0, 2]

        responses.add(
            responses.GET,
            'https://api.mapbox.com/directions-matrix/v1/mapbox/{}/{}'.format(query['profile'], coords),
            status=200,
            json=ENDPOINTS_RESPONSES['mapbox_osrm']['matrix'],
            content_type='application/json'
        )

        self.client.matrix(**query)

        self.assertEqual(1, len(responses.calls))
        self.assertURLEqual(
            'https://api.mapbox.com/directions-matrix/v1/mapbox/driving/8.688641,49.420577;8.680916,49.415776;8.780916,49.445776?'
            'access_token=sample_key&annotations=distance%2Cduration&destinations=0%3B2&fallback_speed=50&sources=1%3B2',
            responses.calls[0].request.url
        )
