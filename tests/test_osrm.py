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
        coords = convert._delimit_list([convert._delimit_list(pair) for pair in query['locations']], ';')

        responses.add(
            responses.GET,
            'https://router.project-osrm.org/route/v1/{}/{}'.format(query['profile'], coords),
            status=200,
            json=ENDPOINTS_RESPONSES['osrm']['directions_geojson'],
            content_type='application/json'
        )

        routes = self.client.directions(**query)
        self.assertEqual(1, len(responses.calls))
        self.assertURLEqual(
            'https://router.project-osrm.org/route/v1/car/8.688641,49.420577;8.680916,49.415776;8.780916,49.445776?'
            'alternatives=false&annotations=true&bearings=50%2C50%3B50%2C50%3B50%2C50&continue_straight=true&'
            'geometries=geojson&overview=simplified&radiuses=500%3B500%3B500&steps=true',
            responses.calls[0].request.url
        )
        self.assertIsInstance(routes, Direction)
        self.assertIsInstance(routes.distance, int)
        self.assertIsInstance(routes.duration, int)
        self.assertIsInstance(routes.geometry, list)
        self.assertIsInstance(routes.raw, dict)

    @responses.activate
    def test_full_directions_alternatives(self):
        query = ENDPOINTS_QUERIES[self.name]['directions']
        coords = convert._delimit_list([convert._delimit_list(pair) for pair in query['locations']], ';')

        responses.add(
            responses.GET,
            'https://router.project-osrm.org/route/v1/{}/{}'.format(query['profile'], coords),
            status=200,
            json=ENDPOINTS_RESPONSES['osrm']['directions_geojson'],
            content_type='application/json'
        )

        routes = self.client.directions(**query)
        self.assertEqual(1, len(responses.calls))
        self.assertURLEqual(
            'https://router.project-osrm.org/route/v1/car/8.688641,49.420577;8.680916,49.415776;8.780916,49.445776?'
            'alternatives=true&annotations=true&bearings=50%2C50%3B50%2C50%3B50%2C50&continue_straight=true&'
            'geometries=geojson&overview=simplified&radiuses=500%3B500%3B500&steps=true',
            responses.calls[0].request.url
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
    def test_directions_polyline5(self):
        query = deepcopy(ENDPOINTS_QUERIES[self.name]['directions'])
        query['geometries'] = 'polyline'
        coords = convert._delimit_list([convert._delimit_list(pair) for pair in query['locations']], ';')

        responses.add(
            responses.GET,
            'https://router.project-osrm.org/route/v1/{}/{}'.format(query['profile'], coords),
            status=200,
            json=ENDPOINTS_RESPONSES['osrm']['directions_polyline'],
            content_type='application/json'
        )

        routes = self.client.directions(**query)
        self.assertEqual(1, len(responses.calls))
        self.assertIsInstance(routes, Directions)
        self.assertEqual(
            routes[0].geometry, [
                (49.00585, 8.4201), (49.00655, 8.42081), (49.0055, 8.42431), (49.0031, 8.424),
                (49.00007, 8.42706), (48.99931, 8.42977), (48.99861, 8.43061), (48.99733, 8.43029),
                (48.99557, 8.42693), (48.99343, 8.41368), (48.99001, 8.40377), (48.98914, 8.39766),
                (48.98963, 8.39105), (48.99326, 8.37727), (48.99509, 8.37446), (49.00109, 8.36855),
                (49.00498, 8.36562), (49.00826, 8.36039), (49.00985, 8.35546), (49.01329, 8.35302),
                (49.01578, 8.35314), (49.01875, 8.35509), (49.03112, 8.3599), (49.03059, 8.36915),
                (49.03056, 8.36984), (49.02964, 8.36965), (49.02721, 8.36776), (49.02735, 8.36538),
                (49.0228, 8.36605), (49.02084, 8.3655), (49.01628, 8.36188), (49.01146, 8.35694),
                (49.01009, 8.3583), (49.00863, 8.35403), (49.0016, 8.34494), (48.99962, 8.34374),
                (48.99366, 8.34198), (48.96147, 8.30189), (48.9617, 8.30051), (48.96001, 8.29851),
                (48.96046, 8.29766), (48.96137, 8.29873)
            ]
        )

    @responses.activate
    def test_directions_polyline6(self):
        query = deepcopy(ENDPOINTS_QUERIES[self.name]['directions'])
        query['geometries'] = 'polyline6'
        coords = convert._delimit_list([convert._delimit_list(pair) for pair in query['locations']], ';')

        responses.add(
            responses.GET,
            'https://router.project-osrm.org/route/v1/{}/{}'.format(query['profile'], coords),
            status=200,
            json=ENDPOINTS_RESPONSES['osrm']['directions_polyline6'],
            content_type='application/json'
        )

        routes = self.client.directions(**query)
        self.assertEqual(1, len(responses.calls))
        self.assertIsInstance(routes, Directions)
        self.assertEqual(
            routes[0].geometry, [
                (49.005852, 8.420095), (49.006554, 8.420812), (49.005502, 8.424311),
                (49.003102, 8.424003), (49.000065, 8.427062), (48.999306, 8.429772),
                (48.998613, 8.430605), (48.99733, 8.430293), (48.99557, 8.426928), (48.993431, 8.413683),
                (48.990011, 8.403766), (48.989135, 8.397659), (48.989626, 8.391053),
                (48.993257, 8.377274), (48.995086, 8.374464), (49.001092, 8.36855), (49.00498, 8.365623),
                (49.008261, 8.360386), (49.00985, 8.355457), (49.013291, 8.353019),
                (49.015775, 8.353144), (49.018752, 8.355086), (49.031121, 8.359899),
                (49.030589, 8.369147), (49.030558, 8.369837), (49.029636, 8.369651),
                (49.027214, 8.36776), (49.027346, 8.365381), (49.0228, 8.366047), (49.020841, 8.365496),
                (49.016277, 8.361875), (49.011464, 8.356935), (49.010093, 8.358296),
                (49.008632, 8.354033), (49.001596, 8.344937), (48.999617, 8.343743),
                (48.993659, 8.341978), (48.961471, 8.301892), (48.961703, 8.300508),
                (48.960006, 8.298506), (48.960459, 8.297656), (48.96137, 8.298731)
            ]
        )

    @responses.activate
    def test_full_matrix(self):
        query = ENDPOINTS_QUERIES[self.name]['matrix']
        coords = convert._delimit_list([convert._delimit_list(pair) for pair in query['locations']], ';')

        responses.add(
            responses.GET,
            'https://router.project-osrm.org/table/v1/{}/{}'.format(query['profile'], coords),
            status=200,
            json=ENDPOINTS_RESPONSES['osrm']['matrix'],
            content_type='application/json'
        )

        matrix = self.client.matrix(**query)

        self.assertEqual(1, len(responses.calls))
        self.assertURLEqual(
            'https://router.project-osrm.org/table/v1/car/8.688641,49.420577;8.680916,49.415776;8.780916,49.445776',
            responses.calls[0].request.url
        )
        self.assertIsInstance(matrix, Matrix)
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
            'https://router.project-osrm.org/table/v1/{}/{}'.format(query['profile'], coords),
            status=200,
            json=ENDPOINTS_RESPONSES['osrm']['matrix'],
            content_type='application/json'
        )

        resp = self.client.matrix(**query)

        self.assertEqual(1, len(responses.calls))
        self.assertURLEqual(
            'https://router.project-osrm.org/table/v1/car/8.688641,49.420577;8.680916,49.415776;8.780916,49.445776?'
            'destinations=0%3B2&sources=1%3B2', responses.calls[0].request.url
        )
