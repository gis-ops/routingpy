# -*- coding: utf-8 -*-
# Copyright (C) 2019 GIS OPS UG
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

from routingpy import OSRM
from routingpy.direction import Direction, Directions
from routingpy.matrix import Matrix
from routingpy import convert
from tests.test_helper import *
import tests as _test

import responses
from copy import deepcopy


class OSRMTest(_test.TestCase):
    name = 'osrm'

    def setUp(self):
        self.client = OSRM()

    @responses.activate
    def test_full_directions(self):
        query = deepcopy(ENDPOINTS_QUERIES[self.name]['directions'])
        query['alternatives'] = False
        coords = convert._delimit_list(
            [convert._delimit_list(pair) for pair in query['coordinates']],
            ';')

        responses.add(
            responses.GET,
            'https://router.project-osrm.org/route/v1/{}/{}'.format(
                query['profile'], coords),
            status=200,
            json=ENDPOINTS_RESPONSES['osrm']['directions'],
            content_type='application/json')

        routes = self.client.directions(**query)
        self.assertEqual(1, len(responses.calls))
        self.assertURLEqual(
            'https://router.project-osrm.org/route/v1/car/8.688641,49.420577;8.680916,49.415776;8.780916,49.445776?'
            'alternatives=false&annotations=true&bearings=50%2C50%3B50%2C50%3B50%2C50&continue_straight=true&'
            'geometries=geojson&overview=simplified&radiuses=500%3B500%3B500&steps=true',
            responses.calls[0].request.url)
        self.assertIsInstance(routes, Direction)
        self.assertIsInstance(routes.distance, int)
        self.assertIsInstance(routes.duration, int)
        self.assertIsInstance(routes.geometry, list)

    @responses.activate
    def test_full_directions_alternatives(self):
        query = ENDPOINTS_QUERIES[self.name]['directions']
        coords = convert._delimit_list(
            [convert._delimit_list(pair) for pair in query['coordinates']],
            ';')

        responses.add(
            responses.GET,
            'https://router.project-osrm.org/route/v1/{}/{}'.format(
                query['profile'], coords),
            status=200,
            json=ENDPOINTS_RESPONSES['osrm']['directions'],
            content_type='application/json')

        routes = self.client.directions(**query)
        self.assertEqual(1, len(responses.calls))
        self.assertURLEqual(
            'https://router.project-osrm.org/route/v1/car/8.688641,49.420577;8.680916,49.415776;8.780916,49.445776?'
            'alternatives=true&annotations=true&bearings=50%2C50%3B50%2C50%3B50%2C50&continue_straight=true&'
            'geometries=geojson&overview=simplified&radiuses=500%3B500%3B500&steps=true',
            responses.calls[0].request.url)
        self.assertIsInstance(routes, Directions)
        self.assertIsInstance(routes[0], Direction)
        self.assertIsInstance(routes[0].duration, int)
        self.assertIsInstance(routes[0].distance, int)
        self.assertIsInstance(routes[0].geometry, list)

    @responses.activate
    def test_full_matrix(self):
        query = ENDPOINTS_QUERIES[self.name]['matrix']
        coords = convert._delimit_list(
            [convert._delimit_list(pair) for pair in query['coordinates']],
            ';')

        responses.add(
            responses.GET,
            'https://router.project-osrm.org/table/v1/{}/{}'.format(
                query['profile'], coords),
            status=200,
            json=ENDPOINTS_RESPONSES['osrm']['matrix'],
            content_type='application/json')

        matrix = self.client.distance_matrix(**query)

        self.assertEqual(1, len(responses.calls))
        self.assertURLEqual(
            'https://router.project-osrm.org/table/v1/car/8.688641,49.420577;8.680916,49.415776;8.780916,49.445776',
            responses.calls[0].request.url)
        self.assertIsInstance(matrix, Matrix)
        self.assertIsInstance(matrix.durations, list)

    @responses.activate
    def test_few_sources_destinations_matrix(self):
        query = deepcopy(ENDPOINTS_QUERIES[self.name]['matrix'])
        coords = convert._delimit_list(
            [convert._delimit_list(pair) for pair in query['coordinates']],
            ';')

        query['sources'] = [1, 2]
        query['destinations'] = [0, 2]

        responses.add(
            responses.GET,
            'https://router.project-osrm.org/table/v1/{}/{}'.format(
                query['profile'], coords),
            status=200,
            json=ENDPOINTS_RESPONSES['osrm']['matrix'],
            content_type='application/json')

        resp = self.client.distance_matrix(**query)

        self.assertEqual(1, len(responses.calls))
        self.assertURLEqual(
            'https://router.project-osrm.org/table/v1/car/8.688641,49.420577;8.680916,49.415776;8.780916,49.445776?'
            'destinations=0%3B2&sources=1%3B2', responses.calls[0].request.url)
