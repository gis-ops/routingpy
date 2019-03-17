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

from routingpy import Graphhopper
from tests.test_helper import *
import tests as _test

import json
import responses
from copy import deepcopy


class GraphhopperTest(_test.TestCase):
    name = 'graphhopper'

    def setUp(self):
        self.key = 'b163fba5-2dbf-4338-8736-7cd414f22444'
        self.client = Graphhopper(key=self.key)

    @responses.activate
    def test_full_directions(self):
        query = ENDPOINTS_QUERIES[self.name]['directions']

        responses.add(responses.GET,
                      'https://graphhopper.com/api/1/route',
                      status=200,
                      json={},
                      content_type='application/json')

        routes = self.client.directions(**query)
        self.assertEqual(1, len(responses.calls))
        self.assertURLEqual('https://graphhopper.com/api/1/route?avoid=motorway%3Btoll&elevation=true&instructions=false&key=b163fba5-2dbf-4338-8736-7cd414f22444&point=49.415776%2C8.680916&point=49.420577%2C8.688641&point=49.445776%2C8.780916&points_encoded=true&profile=car&type=json',
            responses.calls[0].request.url)

    @responses.activate
    def test_full_isochrones(self):
        query = ENDPOINTS_QUERIES[self.name]['isochrones']

        responses.add(responses.GET,
                      'https://graphhopper.com/api/1/isochrone',
                      status=200,
                      json={},
                      content_type='application/json')

        matrix = self.client.isochrones(**query)

        self.assertEqual(1, len(responses.calls))
        self.assertURLEqual('https://graphhopper.com/api/1/isochrone?key=b163fba5-2dbf-4338-8736-7cd414f22444&point=48.23424%2C8.34234&profile=car',
            responses.calls[0].request.url)

    @responses.activate
    def test_full_matrix(self):
        query = ENDPOINTS_QUERIES[self.name]['matrix']

        responses.add(responses.GET,
                      'https://graphhopper.com/api/1/matrix',
                      status=200,
                      json={},
                      content_type='application/json')

        matrix = self.client.distance_matrix(**query)

        self.assertEqual(1, len(responses.calls))
        self.assertURLEqual('https://graphhopper.com/api/1/matrix?from_point=49.415776%2C8.680916&from_point=49.420577%2C8.688641&key=b163fba5-2dbf-4338-8736-7cd414f22444&out_array=distance&out_array=times&out_array=weights&profile=car&to_point=49.445776%2C8.780916',
            responses.calls[0].request.url)

    def test_no_destinations_matrix(self):
        query = deepcopy(ENDPOINTS_QUERIES[self.name]['matrix'])
        del query['destinations']

        self.assertRaises(ValueError, lambda: self.client.distance_matrix(**query))

    def test_no_sources_matrix(self):
        query = deepcopy(ENDPOINTS_QUERIES[self.name]['matrix'])
        del query['sources']

        self.assertRaises(ValueError, lambda: self.client.distance_matrix(**query))

    def test_index_sources_matrix(self):
        query = deepcopy(ENDPOINTS_QUERIES[self.name]['matrix'])
        query['sources'] = [100]

        self.assertRaises(IndexError, lambda: self.client.distance_matrix(**query))

    def test_index_destinations_matrix(self):
        query = deepcopy(ENDPOINTS_QUERIES[self.name]['matrix'])
        query['destinations'] = [100]

        self.assertRaises(IndexError, lambda: self.client.distance_matrix(**query))
  

