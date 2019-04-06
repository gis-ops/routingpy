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

from routingpy import MapBoxOSRM
from routingpy import convert
from tests.test_helper import *
import tests as _test

import responses
from copy import deepcopy
import json


class MapboxOSRMTest(_test.TestCase):
    name = 'mapbox_osrm'

    def setUp(self):
        self.client = MapBoxOSRM(api_key='sample_key')

    @responses.activate
    def test_full_directions(self):
        query = ENDPOINTS_QUERIES[self.name]['directions']
        expected = ENDPOINTS_EXPECTED[self.name]['directions']
        coords = convert._delimit_list(
            [convert._delimit_list(pair) for pair in query['coordinates']],
            ';')

        responses.add(
            responses.POST,
            'https://api.mapbox.com/directions/v5/mapbox/{}'.format(
                query['profile']),
            status=200,
            json=query,
            content_type='application/json')

        routes = self.client.directions(**query)

        self.assertEqual(1, len(responses.calls))
        self.assertEqual(expected, json.loads(responses.calls[0].request.body))

    @responses.activate
    def test_full_matrix(self):
        query = ENDPOINTS_QUERIES[self.name]['matrix']
        coords = convert._delimit_list(
            [convert._delimit_list(pair) for pair in query['coordinates']],
            ';')

        responses.add(
            responses.GET,
            'https://api.mapbox.com/directions-matrix/v1/mapbox/{}/{}'.format(
                query['profile'], coords),
            status=200,
            json={},
            content_type='application/json')

        matrix = self.client.distance_matrix(**query)

        self.assertEqual(1, len(responses.calls))
        self.assertURLEqual(
            'https://api.mapbox.com/directions-matrix/v1/mapbox/driving/8.688641,49.420577;8.680916,49.415776;8.780916,49.445776?'
            'access_token=sample_key&annotations=distance%2Cduration&fallback_speed=50',
            responses.calls[0].request.url)

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
            'https://api.mapbox.com/directions-matrix/v1/mapbox/{}/{}'.format(
                query['profile'], coords),
            status=200,
            json={},
            content_type='application/json')

        resp = self.client.distance_matrix(**query)

        self.assertEqual(1, len(responses.calls))
        self.assertURLEqual(
            'https://api.mapbox.com/directions-matrix/v1/mapbox/driving/8.688641,49.420577;8.680916,49.415776;8.780916,49.445776?'
            'access_token=sample_key&annotations=distance%2Cduration&destinations=0%3B2&fallback_speed=50&sources=1%3B2',
            responses.calls[0].request.url)
