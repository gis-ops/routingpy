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
"""Tests for the HereMaps module."""

from routingpy import HereMaps
from tests.test_helper import *
import tests as _test

import json
import responses
from copy import deepcopy


class HereMapsTest(_test.TestCase):
    name = 'heremaps'

    def setUp(self):
        self.app_id = 'sample_app_id'
        self.app_code = 'sample_app_code'
        self.client = HereMaps(app_id=self.app_id, app_code=self.app_code)

    @responses.activate
    def test_full_directions(self):
        query = ENDPOINTS_QUERIES[self.name]['directions']

        responses.add(
            responses.GET,
            'https://route.api.here.com/routing/7.2/calculateroute.json',
            status=200,
            json={},
            content_type='application/json')

        routes = self.client.directions(**query)
        self.assertEqual(1, len(responses.calls))
        self.assertURLEqual(
            'https://route.api.here.com/routing/7.2/calculateroute.json?alternatives=3&app_code=sample_app_code&'
            'app_id=sample_app_id&avoidAreas=8.688641%2C49.420577%3B8.680916%2C49.415776%218.780916%2C49.445776%3B8.780916%2C49.445776&'
            'avoidLinks=-53623477&avoidSeasonalClosures=true&avoidTurns=difficult&combineChange=false&consumptionModel=default&'
            'departure=2019-03-29T03%3A00%3A00&excludeCountries=AUT%2CCHE&excludeZoneTypes=vignette%2CcongestionPricing&'
            'excludeZones=510%2C511&generalizationTolerances=0.1%2C0.01&height=20&instructionFormat=text&jsonAttributes=9&'
            'legAttributes=maneuvers%2Cwaypoint%2Clength%2CtravelTime&length=10&licensePlate=lastcharacter%3A5&limitedWeight=10&'
            'linkAttributes=shape%2CspeedLimit&maneuverAttributes=position%2Clength%2CtravelTime&maxNumberOfChanges=5&'
            'metricSystem=metric&mode=truck%3Bfastest&requestId=101&resolution=300%3A300&returnElevation=true&'
            'routeAttributes=waypoints%2Csummary%2CsummaryByCountry%2Cshape%2CboundingBox%2Clegs%2Cnotes%2Clines%2CrouteId%2Cgroups%2Ctickets%2Cincidents%2Czones&'
            'shippedHazardousGoods=gas%2Cflammable&speedProfile=fast&trailersCount=3&truckRestrictionPenalty=soft&truckType=truck&vehicleType=diesel%2C5.5&'
            'viewBounds=8.688641%2C49.420577%3B8.680916%2C49.415776&waypoint0=geo%218.688641%2C49.420577&waypoint1=geo%218.680916%2C49.415776&'
            'waypoint2=geo%218.780916%2C49.445776&weightPerAxle=100&width=10',
            responses.calls[0].request.url)

    @responses.activate
    def test_full_isochrones(self):
        query = ENDPOINTS_QUERIES[self.name]['isochrones']

        responses.add(
            responses.GET,
            'https://isoline.route.api.here.com/routing/7.2/calculateisoline.json',
            status=200,
            json={},
            content_type='application/json')

        matrix = self.client.isochrones(**query)

        self.assertEqual(1, len(responses.calls))
        self.assertURLEqual(
            'https://isoline.route.api.here.com/routing/7.2/calculateisoline.json?app_code=sample_app_code&'
            'app_id=sample_app_id&mode=car%3Bfastest&quality=1&range=1000%2C2000%2C3000&rangeType=distance&'
            'singleComponent=false&start=geo%218.34234%2C48.23424',
            responses.calls[0].request.url)

    @responses.activate
    def test_full_matrix(self):
        query = ENDPOINTS_QUERIES[self.name]['matrix']

        responses.add(
            responses.GET,
            'https://matrix.route.api.here.com/routing/7.2/calculatematrix.json',
            status=200,
            json={},
            content_type='application/json')

        matrix = self.client.distance_matrix(**query)

        self.assertEqual(1, len(responses.calls))
        self.assertURLEqual(
            'https://matrix.route.api.here.com/routing/7.2/calculatematrix.json?app_code=sample_app_code&'
            'app_id=sample_app_id&destination0=geo%218.780916%2C49.445776&height=20&length=10&limitedWeight=10&'
            'mode=car%3Bfastest&shippedHazardousGoods=gas%2Cflammable&start0=geo%218.688641%2C49.420577&'
            'start1=geo%218.680916%2C49.415776&summaryAttributes=traveltime%2Ccostfactor&trailersCount=3&truckType=truck&'
            'weightPerAxle=100&width=10', responses.calls[0].request.url)

    def test_index_sources_matrix(self):
        query = deepcopy(ENDPOINTS_QUERIES[self.name]['matrix'])
        query['sources'] = [100]

        self.assertRaises(
            IndexError, lambda: self.client.distance_matrix(**query))

    def test_none_sources_matrix(self):
        query = deepcopy(ENDPOINTS_QUERIES[self.name]['matrix'])
        query['sources'] = None

        self.assertRaises(
            TypeError, lambda: self.client.distance_matrix(**query))

    def test_index_destinations_matrix(self):
        query = deepcopy(ENDPOINTS_QUERIES[self.name]['matrix'])
        query['destinations'] = [100]

        self.assertRaises(
            IndexError, lambda: self.client.distance_matrix(**query))

    def test_none_destinations_matrix(self):
        query = deepcopy(ENDPOINTS_QUERIES[self.name]['matrix'])
        query['destinations'] = None

        self.assertRaises(
            TypeError, lambda: self.client.distance_matrix(**query))
