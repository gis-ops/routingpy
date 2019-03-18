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

"""Tests for the Graphhopper module."""

from routingpy import ORS
from tests.test_helper import *
import tests as _test

import responses
import json


class ORSTest(_test.TestCase):
    name = 'ors'

    def setUp(self):
        self.key = 'sample_key'
        self.client = ORS(api_key=self.key)

    @responses.activate
    def test_full_directions(self):
        query = ENDPOINTS_QUERIES[self.name]['directions']

        responses.add(responses.POST,
                      'https://api.openrouteservice.org/v2/directions/{}/geojson'.format(query['profile']),
                      status=200,
                      json=query,
                      content_type='application/json')

        routes = self.client.directions(**query, format='geojson')

        self.assertEqual(1, len(responses.calls))
        self.assertEqual(
            query,
            json.loads(responses.calls[0].request.body)
        )

    @responses.activate
    def test_full_isochrones(self):
        query = ENDPOINTS_QUERIES[self.name]['isochrones']

        responses.add(responses.POST,
                      'https://api.openrouteservice.org/v2/isochrones/{}/geojson'.format(query['profile']),
                      status=200,
                      json=query,
                      content_type='application/json')

        matrix = self.client.isochrones(**query)

        expected = query
        expected['locations'] = expected['coordinates']
        del expected['coordinates']

        self.assertEqual(1, len(responses.calls))
        self.assertEqual(
            expected,
            json.loads(responses.calls[0].request.body)
        )

    @responses.activate
    def test_full_matrix(self):
        query = ENDPOINTS_QUERIES[self.name]['matrix']

        responses.add(responses.POST,
                      'https://api.openrouteservice.org/v2/matrix/{}/json'.format(query['profile']),
                      status=200,
                      json=query,
                      content_type='application/json')

        matrix = self.client.distance_matrix(**query)

        expected = query
        expected['locations'] = expected['coordinates']
        del expected['coordinates']

        self.assertEqual(1, len(responses.calls))
        self.assertEqual(
            expected,
            json.loads(responses.calls[0].request.body)
        )

    @responses.activate
    def test_key_in_header(self):
        # Test that API key is being put in the Authorization header
        query = ENDPOINTS_QUERIES['ors']['directions']

        responses.add(responses.POST,
                      'https://api.openrouteservice.org/v2/directions/{}/geojson'.format(query['profile']),
                      json=query,
                      status=200,
                      content_type='application/json')

        resp = self.client.directions(**query)

        self.assertDictContainsSubset({'Authorization': self.key}, responses.calls[0].request.headers)
