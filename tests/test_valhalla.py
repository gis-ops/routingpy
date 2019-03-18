# -*- coding: utf-8 -*-
# Copyright 2014 Google Inc. All rights reserved.
#
# Modifications Copyright (C) 2018 HeiGIT, University of Heidelberg.
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

"""Tests for the Valhalla module."""

from routingpy import Valhalla
from tests.test_helper import *
import tests as _test

import json
import responses
from copy import deepcopy


class ValhallaTest(_test.TestCase):

    name = 'valhalla'
            
    def setUp(self):
        self.client = Valhalla('https://api.mapbox.com/valhalla/v1')

    @responses.activate
    def test_full_directions(self):
        query = ENDPOINTS_QUERIES[self.name]['directions']
        expected = ENDPOINTS_EXPECTED[self.name]['directions']

        responses.add(responses.POST,
                      'https://api.mapbox.com/valhalla/v1/route',
                      status=200,
                      json=expected,
                      content_type='application/json')
        routes = self.client.directions(**query)

        self.assertEqual(1, len(responses.calls))
        self.assertEqual(json.loads(responses.calls[0].request.body), expected)

    def test_too_little_types(self):
        payload = deepcopy(self.locations_valid)
        del payload['types'][0]

        with self.assertRaises(ValueError):
            self.client.directions(profile='auto', **payload)

    @responses.activate
    def test_full_isochrones(self):
        query = ENDPOINTS_QUERIES[self.name]['isochrones']
        expected = ENDPOINTS_EXPECTED[self.name]['isochrones']

        responses.add(responses.POST,
                      'https://api.mapbox.com/valhalla/v1/isochrone',
                      status=200,
                      json=expected,
                      content_type='application/json')

        routes = self.client.isochrones(**query)

        self.assertEqual(1, len(responses.calls))
        self.assertEqual(json.loads(responses.calls[0].request.body), expected)

    # TODO: test colors having less items than range
    @responses.activate
    def test_full_matrix(self):
        query = ENDPOINTS_QUERIES[self.name]['matrix']
        expected = ENDPOINTS_EXPECTED[self.name]['matrix']

        responses.add(responses.POST,
                      'https://api.mapbox.com/valhalla/v1/sources_to_targets',
                      status=200,
                      json=expected,
                      content_type='application/json')

        routes = self.client.distance_matrix(**query)

        self.assertEqual(1, len(responses.calls))
        self.assertEqual(json.loads(responses.calls[0].request.body), expected)

    @responses.activate
    def test_few_sources_destinations_matrix(self):
        query = deepcopy(ENDPOINTS_QUERIES[self.name]['matrix'])
        query['sources'] = [2]
        query['destinations'] = [0]

        expected = deepcopy(ENDPOINTS_EXPECTED[self.name]['matrix'])
        del expected['sources'][0]
        del expected['sources'][0]
        del expected['targets'][1]
        del expected['targets'][1]

        responses.add(responses.POST,
                      'https://api.mapbox.com/valhalla/v1/sources_to_targets',
                      status=200,
                      json=expected,
                      content_type='application/json')

        routes = self.client.distance_matrix(**query)

        self.assertEqual(1, len(responses.calls))
        self.assertEqual(json.loads(responses.calls[0].request.body), expected)

    # @responses.activate
    # def test_bearings(self):
    #     # First: test correct output for bearings
    #     # Second: should switch to optimized=false bcs bearings was specified
    #     responses.add(responses.GET,
    #                   'https://api.openrouteservice.org/directions',
    #                   body='{"status":"OK","routes":[]}',
    #                   status=200,
    #                   content_type='application/json')
    #
    #     # Simplest directions request. Driving directions by default.
    #     routes = self.client.directions(self.coords_valid,
    #                                     bearings=[[100,100],[200,200]])
    #
    #     self.assertEqual(1, len(responses.calls))
    #     self.assertURLEqual('https://api.openrouteservice.org/directions?'
    #                         'api_key={}&coordinates=8.34234%2C48.23424%7C8.34423%2C48.26424&'
    #                         'profile=driving-car&bearings=100%2C100%7C200%2C200&optimized=false'.format(self.key),
    #                         responses.calls[0].request.url)
    #
    # @responses.activate
    # def test_continue_straight(self):
    #     # Should switch to optimized=false bcs continue_straight is set true
    #     responses.add(responses.GET,
    #                   'https://api.openrouteservice.org/directions',
    #                   body='{"status":"OK","routes":[]}',
    #                   status=200,
    #                   content_type='application/json')
    #
    #     # Simplest directions request. Driving directions by default.
    #     routes = self.client.directions(self.coords_valid,
    #                                     profile='cycling-regular',
    #                                     continue_straight='true')
    #
    #     self.assertEqual(1, len(responses.calls))
    #     self.assertURLEqual('https://api.openrouteservice.org/directions?'
    #                         'api_key={}&coordinates=8.34234%2C48.23424%7C8.34423%2C48.26424&'
    #                         'profile=cycling-regular&continue_straight=true&optimized=false'.format(self.key),
    #                         responses.calls[0].request.url)

