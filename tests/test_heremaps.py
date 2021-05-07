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
"""Tests for the HereMaps module."""

from routingpy import HereMaps
from routingpy.direction import Direction, Directions
from routingpy.isochrone import Isochrones, Isochrone
from routingpy.matrix import Matrix

from tests.test_helper import *
import tests as _test

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
            json=ENDPOINTS_RESPONSES[self.name]['directions'],
            content_type='application/json'
        )

        self.client.directions(**query)
        self.assertEqual(1, len(responses.calls))
        self.assertURLEqual(
            'https://route.api.here.com/routing/7.2/calculateroute.json?alternatives=3&app_code=sample_app_code&'
            'app_id=sample_app_id&avoidAreas=49.420577%2C8.688641%3B49.415776%2C8.680916%2149.445776%2C8.780916%3B49.445776%2C8.780916&'
            'avoidLinks=-53623477&avoidSeasonalClosures=true&avoidTurns=difficult&combineChange=false&consumptionModel=default&'
            'departure=2021-03-29T03%3A00%3A00&excludeCountries=AUT%2CCHE&excludeZoneTypes=vignette%2CcongestionPricing&'
            'excludeZones=510%2C511&generalizationTolerances=0.1%2C0.01&height=20&instructionFormat=text&jsonAttributes=9&'
            'legAttributes=maneuvers%2Cwaypoint%2Clength%2CtravelTime&length=10&licensePlate=lastcharacter%3A5&limitedWeight=10&'
            'linkAttributes=shape%2CspeedLimit&maneuverAttributes=position%2Clength%2CtravelTime&maxNumberOfChanges=5&'
            'metricSystem=metric&mode=fastest%3Btruck&requestId=101&resolution=300%3A300&returnElevation=true&'
            'routeAttributes=waypoints%2Csummary%2CsummaryByCountry%2Cshape%2CboundingBox%2Clegs%2Cnotes%2Clines%2CrouteId%2Cgroups%2Ctickets%2Cincidents%2Czones&'
            'shippedHazardousGoods=gas%2Cflammable&speedProfile=fast&trailersCount=3&truckRestrictionPenalty=soft&truckType=truck&vehicleType=diesel%2C5.5&'
            'viewBounds=49.420577%2C8.688641%3B49.415776%2C8.680916&waypoint0=geo%2149.420577%2C8.688641&waypoint1=geo%2149.415776%2C8.680916&'
            'waypoint2=geo%2149.445776%2C8.780916&weightPerAxle=100&width=10',
            responses.calls[0].request.url
        )

    @responses.activate
    def test_directions_object_response(self):
        query = ENDPOINTS_QUERIES[self.name]['directions']
        query['alternatives'] = 1

        responses.add(
            responses.GET,
            'https://route.api.here.com/routing/7.2/calculateroute.json',
            status=200,
            json=ENDPOINTS_RESPONSES[self.name]['directions'],
            content_type='application/json'
        )

        routes = self.client.directions(**query)
        self.assertEqual(1, len(responses.calls))
        self.assertURLEqual(
            'https://route.api.here.com/routing/7.2/calculateroute.json?alternatives=1&app_code=sample_app_code&'
            'app_id=sample_app_id&avoidAreas=49.420577%2C8.688641%3B49.415776%2C8.680916%2149.445776%2C8.780916%3B49.445776%2C8.780916&'
            'avoidLinks=-53623477&avoidSeasonalClosures=true&avoidTurns=difficult&combineChange=false&consumptionModel=default&'
            'departure=2021-03-29T03%3A00%3A00&excludeCountries=AUT%2CCHE&excludeZoneTypes=vignette%2CcongestionPricing&'
            'excludeZones=510%2C511&generalizationTolerances=0.1%2C0.01&height=20&instructionFormat=text&jsonAttributes=9&'
            'legAttributes=maneuvers%2Cwaypoint%2Clength%2CtravelTime&length=10&licensePlate=lastcharacter%3A5&limitedWeight=10&'
            'linkAttributes=shape%2CspeedLimit&maneuverAttributes=position%2Clength%2CtravelTime&maxNumberOfChanges=5&'
            'metricSystem=metric&mode=fastest%3Btruck&requestId=101&resolution=300%3A300&returnElevation=true&'
            'routeAttributes=waypoints%2Csummary%2CsummaryByCountry%2Cshape%2CboundingBox%2Clegs%2Cnotes%2Clines%2CrouteId%2Cgroups%2Ctickets%2Cincidents%2Czones&'
            'shippedHazardousGoods=gas%2Cflammable&speedProfile=fast&trailersCount=3&truckRestrictionPenalty=soft&truckType=truck&vehicleType=diesel%2C5.5&'
            'viewBounds=49.420577%2C8.688641%3B49.415776%2C8.680916&waypoint0=geo%2149.420577%2C8.688641&waypoint1=geo%2149.415776%2C8.680916&'
            'waypoint2=geo%2149.445776%2C8.780916&weightPerAxle=100&width=10',
            responses.calls[0].request.url
        )

        self.assertIsInstance(routes, Direction)
        self.assertIsInstance(routes.geometry, list)
        self.assertIsInstance(routes.duration, int)
        self.assertIsInstance(routes.distance, int)
        self.assertIsInstance(routes.raw, dict)

    @responses.activate
    def test_directions_object_response_alternatives(self):
        query = ENDPOINTS_QUERIES[self.name]['directions']
        query['alternatives'] = 3
        responses.add(
            responses.GET,
            'https://route.api.here.com/routing/7.2/calculateroute.json',
            status=200,
            json=ENDPOINTS_RESPONSES[self.name]['directions'],
            content_type='application/json'
        )

        routes = self.client.directions(**query)
        self.assertEqual(1, len(responses.calls))
        self.assertURLEqual(
            'https://route.api.here.com/routing/7.2/calculateroute.json?alternatives=3&app_code=sample_app_code&'
            'app_id=sample_app_id&avoidAreas=49.420577%2C8.688641%3B49.415776%2C8.680916%2149.445776%2C8.780916%3B49.445776%2C8.780916&'
            'avoidLinks=-53623477&avoidSeasonalClosures=true&avoidTurns=difficult&combineChange=false&consumptionModel=default&'
            'departure=2021-03-29T03%3A00%3A00&excludeCountries=AUT%2CCHE&excludeZoneTypes=vignette%2CcongestionPricing&'
            'excludeZones=510%2C511&generalizationTolerances=0.1%2C0.01&height=20&instructionFormat=text&jsonAttributes=9&'
            'legAttributes=maneuvers%2Cwaypoint%2Clength%2CtravelTime&length=10&licensePlate=lastcharacter%3A5&limitedWeight=10&'
            'linkAttributes=shape%2CspeedLimit&maneuverAttributes=position%2Clength%2CtravelTime&maxNumberOfChanges=5&'
            'metricSystem=metric&mode=fastest%3Btruck&requestId=101&resolution=300%3A300&returnElevation=true&'
            'routeAttributes=waypoints%2Csummary%2CsummaryByCountry%2Cshape%2CboundingBox%2Clegs%2Cnotes%2Clines%2CrouteId%2Cgroups%2Ctickets%2Cincidents%2Czones&'
            'shippedHazardousGoods=gas%2Cflammable&speedProfile=fast&trailersCount=3&truckRestrictionPenalty=soft&truckType=truck&vehicleType=diesel%2C5.5&'
            'viewBounds=49.420577%2C8.688641%3B49.415776%2C8.680916&waypoint0=geo%2149.420577%2C8.688641&waypoint1=geo%2149.415776%2C8.680916&'
            'waypoint2=geo%2149.445776%2C8.780916&weightPerAxle=100&width=10',
            responses.calls[0].request.url
        )

        self.assertIsInstance(routes, Directions)
        self.assertEqual(3, len(routes))
        for route in routes:
            self.assertIsInstance(route, Direction)
            self.assertIsInstance(route.geometry, list)
            self.assertIsInstance(route.duration, int)
            self.assertIsInstance(route.distance, int)
            self.assertIsInstance(route.raw, dict)

    @responses.activate
    def test_full_isochrones_response_object(self):
        query = ENDPOINTS_QUERIES[self.name]['isochrones']

        responses.add(
            responses.GET,
            'https://isoline.route.api.here.com/routing/7.2/calculateisoline.json',
            status=200,
            json=ENDPOINTS_RESPONSES[self.name]['isochrones'],
            content_type='application/json'
        )

        isochrones = self.client.isochrones(**query)

        self.assertEqual(1, len(responses.calls))
        self.assertURLEqual(
            'https://isoline.route.api.here.com/routing/7.2/calculateisoline.json?app_code=sample_app_code&'
            'app_id=sample_app_id&mode=fastest%3Bcar&quality=1&range=1000%2C2000%2C3000&rangeType=distance&'
            'singleComponent=false&start=geo%2148.23424%2C8.34234', responses.calls[0].request.url
        )

        self.assertIsInstance(isochrones, Isochrones)
        self.assertEqual(3, len(isochrones))
        for iso in isochrones:
            self.assertIsInstance(iso, Isochrone)
            self.assertIsInstance(iso.geometry, list)
            self.assertIsInstance(iso.center, list)
            self.assertIsInstance(iso.interval, int)

    @responses.activate
    def test_full_matrix(self):
        query = ENDPOINTS_QUERIES[self.name]['matrix']

        responses.add(
            responses.GET,
            'https://matrix.route.api.here.com/routing/7.2/calculatematrix.json',
            status=200,
            json=ENDPOINTS_RESPONSES[self.name]['matrix'],
            content_type='application/json'
        )

        matrix = self.client.matrix(**query)

        self.assertEqual(1, len(responses.calls))
        self.assertURLEqual(
            'https://matrix.route.api.here.com/routing/7.2/calculatematrix.json?app_code=sample_app_code&'
            'app_id=sample_app_id&destination0=geo%2149.445776%2C8.780916&height=20&length=10&limitedWeight=10&'
            'mode=fastest%3Bcar&shippedHazardousGoods=gas%2Cflammable&start0=geo%2149.420577%2C8.688641&'
            'start1=geo%2149.415776%2C8.680916&summaryAttributes=traveltime%2Ccostfactor&trailersCount=3&truckType=truck&'
            'weightPerAxle=100&width=10', responses.calls[0].request.url
        )

        self.assertIsInstance(matrix, Matrix)
        self.assertIsInstance(matrix.durations, list)
        self.assertIsInstance(matrix.distances, list)
        self.assertIsInstance(matrix.raw, dict)

    def test_index_sources_matrix(self):
        query = deepcopy(ENDPOINTS_QUERIES[self.name]['matrix'])
        query['sources'] = [100]

        self.assertRaises(IndexError, lambda: self.client.matrix(**query))

    def test_index_destinations_matrix(self):
        query = deepcopy(ENDPOINTS_QUERIES[self.name]['matrix'])
        query['destinations'] = [100]

        self.assertRaises(IndexError, lambda: self.client.matrix(**query))


class HereMapsKeyTest(_test.TestCase):
    name = 'heremaps'

    def setUp(self):
        self.api_key = 'sample_api_key'
        self.client = HereMaps(api_key=self.api_key)

    @responses.activate
    def test_full_directions(self):
        query = ENDPOINTS_QUERIES[self.name]['directions']

        responses.add(
            responses.GET,
            'https://route.ls.hereapi.com/routing/7.2/calculateroute.json',
            status=200,
            json=ENDPOINTS_RESPONSES[self.name]['directions'],
            content_type='application/json'
        )

        self.client.directions(**query)
        self.assertEqual(1, len(responses.calls))
        self.assertURLEqual(
            'https://route.ls.hereapi.com/routing/7.2/calculateroute.json?alternatives=3&apikey=sample_api_key&'
            'avoidAreas=49.420577%2C8.688641%3B49.415776%2C8.680916%2149.445776%2C8.780916%3B49.445776%2C8.780916&'
            'avoidLinks=-53623477&avoidSeasonalClosures=true&avoidTurns=difficult&combineChange=false&consumptionModel=default&'
            'departure=2021-03-29T03%3A00%3A00&excludeCountries=AUT%2CCHE&excludeZoneTypes=vignette%2CcongestionPricing&'
            'excludeZones=510%2C511&generalizationTolerances=0.1%2C0.01&height=20&instructionFormat=text&jsonAttributes=9&'
            'legAttributes=maneuvers%2Cwaypoint%2Clength%2CtravelTime&length=10&licensePlate=lastcharacter%3A5&limitedWeight=10&'
            'linkAttributes=shape%2CspeedLimit&maneuverAttributes=position%2Clength%2CtravelTime&maxNumberOfChanges=5&'
            'metricSystem=metric&mode=fastest%3Btruck&requestId=101&resolution=300%3A300&returnElevation=true&'
            'routeAttributes=waypoints%2Csummary%2CsummaryByCountry%2Cshape%2CboundingBox%2Clegs%2Cnotes%2Clines%2CrouteId%2Cgroups%2Ctickets%2Cincidents%2Czones&'
            'shippedHazardousGoods=gas%2Cflammable&speedProfile=fast&trailersCount=3&truckRestrictionPenalty=soft&truckType=truck&vehicleType=diesel%2C5.5&'
            'viewBounds=49.420577%2C8.688641%3B49.415776%2C8.680916&waypoint0=geo%2149.420577%2C8.688641&waypoint1=geo%2149.415776%2C8.680916&'
            'waypoint2=geo%2149.445776%2C8.780916&weightPerAxle=100&width=10',
            responses.calls[0].request.url
        )

    @responses.activate
    def test_directions_object_response(self):
        query = ENDPOINTS_QUERIES[self.name]['directions']
        query['alternatives'] = 1

        responses.add(
            responses.GET,
            'https://route.ls.hereapi.com/routing/7.2/calculateroute.json',
            status=200,
            json=ENDPOINTS_RESPONSES[self.name]['directions'],
            content_type='application/json'
        )

        routes = self.client.directions(**query)
        self.assertEqual(1, len(responses.calls))
        self.assertURLEqual(
            'https://route.ls.hereapi.com/routing/7.2/calculateroute.json?alternatives=1&apikey=sample_api_key&'
            'avoidAreas=49.420577%2C8.688641%3B49.415776%2C8.680916%2149.445776%2C8.780916%3B49.445776%2C8.780916&'
            'avoidLinks=-53623477&avoidSeasonalClosures=true&avoidTurns=difficult&combineChange=false&consumptionModel=default&'
            'departure=2021-03-29T03%3A00%3A00&excludeCountries=AUT%2CCHE&excludeZoneTypes=vignette%2CcongestionPricing&'
            'excludeZones=510%2C511&generalizationTolerances=0.1%2C0.01&height=20&instructionFormat=text&jsonAttributes=9&'
            'legAttributes=maneuvers%2Cwaypoint%2Clength%2CtravelTime&length=10&licensePlate=lastcharacter%3A5&limitedWeight=10&'
            'linkAttributes=shape%2CspeedLimit&maneuverAttributes=position%2Clength%2CtravelTime&maxNumberOfChanges=5&'
            'metricSystem=metric&mode=fastest%3Btruck&requestId=101&resolution=300%3A300&returnElevation=true&'
            'routeAttributes=waypoints%2Csummary%2CsummaryByCountry%2Cshape%2CboundingBox%2Clegs%2Cnotes%2Clines%2CrouteId%2Cgroups%2Ctickets%2Cincidents%2Czones&'
            'shippedHazardousGoods=gas%2Cflammable&speedProfile=fast&trailersCount=3&truckRestrictionPenalty=soft&truckType=truck&vehicleType=diesel%2C5.5&'
            'viewBounds=49.420577%2C8.688641%3B49.415776%2C8.680916&waypoint0=geo%2149.420577%2C8.688641&waypoint1=geo%2149.415776%2C8.680916&'
            'waypoint2=geo%2149.445776%2C8.780916&weightPerAxle=100&width=10',
            responses.calls[0].request.url
        )

        self.assertIsInstance(routes, Direction)
        self.assertIsInstance(routes.geometry, list)
        self.assertIsInstance(routes.duration, int)
        self.assertIsInstance(routes.distance, int)
        self.assertIsInstance(routes.raw, dict)

    @responses.activate
    def test_directions_object_response_alternatives(self):
        query = ENDPOINTS_QUERIES[self.name]['directions']
        query['alternatives'] = 3
        responses.add(
            responses.GET,
            'https://route.ls.hereapi.com/routing/7.2/calculateroute.json',
            status=200,
            json=ENDPOINTS_RESPONSES[self.name]['directions'],
            content_type='application/json'
        )

        routes = self.client.directions(**query)
        self.assertEqual(1, len(responses.calls))
        self.assertURLEqual(
            'https://route.ls.hereapi.com/routing/7.2/calculateroute.json?alternatives=3&apikey=sample_api_key&'
            'avoidAreas=49.420577%2C8.688641%3B49.415776%2C8.680916%2149.445776%2C8.780916%3B49.445776%2C8.780916&'
            'avoidLinks=-53623477&avoidSeasonalClosures=true&avoidTurns=difficult&combineChange=false&consumptionModel=default&'
            'departure=2021-03-29T03%3A00%3A00&excludeCountries=AUT%2CCHE&excludeZoneTypes=vignette%2CcongestionPricing&'
            'excludeZones=510%2C511&generalizationTolerances=0.1%2C0.01&height=20&instructionFormat=text&jsonAttributes=9&'
            'legAttributes=maneuvers%2Cwaypoint%2Clength%2CtravelTime&length=10&licensePlate=lastcharacter%3A5&limitedWeight=10&'
            'linkAttributes=shape%2CspeedLimit&maneuverAttributes=position%2Clength%2CtravelTime&maxNumberOfChanges=5&'
            'metricSystem=metric&mode=fastest%3Btruck&requestId=101&resolution=300%3A300&returnElevation=true&'
            'routeAttributes=waypoints%2Csummary%2CsummaryByCountry%2Cshape%2CboundingBox%2Clegs%2Cnotes%2Clines%2CrouteId%2Cgroups%2Ctickets%2Cincidents%2Czones&'
            'shippedHazardousGoods=gas%2Cflammable&speedProfile=fast&trailersCount=3&truckRestrictionPenalty=soft&truckType=truck&vehicleType=diesel%2C5.5&'
            'viewBounds=49.420577%2C8.688641%3B49.415776%2C8.680916&waypoint0=geo%2149.420577%2C8.688641&waypoint1=geo%2149.415776%2C8.680916&'
            'waypoint2=geo%2149.445776%2C8.780916&weightPerAxle=100&width=10',
            responses.calls[0].request.url
        )

        self.assertIsInstance(routes, Directions)
        self.assertEqual(3, len(routes))
        for route in routes:
            self.assertIsInstance(route, Direction)
            self.assertIsInstance(route.geometry, list)
            self.assertIsInstance(route.duration, int)
            self.assertIsInstance(route.distance, int)
            self.assertIsInstance(route.raw, dict)

    @responses.activate
    def test_full_isochrones_response_object(self):
        query = ENDPOINTS_QUERIES[self.name]['isochrones']

        responses.add(
            responses.GET,
            'https://isoline.route.ls.hereapi.com/routing/7.2/calculateisoline.json',
            status=200,
            json=ENDPOINTS_RESPONSES[self.name]['isochrones'],
            content_type='application/json'
        )

        isochrones = self.client.isochrones(**query)

        self.assertEqual(1, len(responses.calls))
        self.assertURLEqual(
            'https://isoline.route.ls.hereapi.com/routing/7.2/calculateisoline.json?apikey=sample_api_key&'
            'mode=fastest%3Bcar&quality=1&range=1000%2C2000%2C3000&rangeType=distance&'
            'singleComponent=false&start=geo%2148.23424%2C8.34234', responses.calls[0].request.url
        )

        self.assertIsInstance(isochrones, Isochrones)
        self.assertEqual(3, len(isochrones))
        for iso in isochrones:
            self.assertIsInstance(iso, Isochrone)
            self.assertIsInstance(iso.geometry, list)
            self.assertIsInstance(iso.center, list)
            self.assertIsInstance(iso.interval, int)

    @responses.activate
    def test_full_matrix(self):
        query = ENDPOINTS_QUERIES[self.name]['matrix']

        responses.add(
            responses.GET,
            'https://matrix.route.ls.hereapi.com/routing/7.2/calculatematrix.json',
            status=200,
            json=ENDPOINTS_RESPONSES[self.name]['matrix'],
            content_type='application/json'
        )

        matrix = self.client.matrix(**query)

        self.assertEqual(1, len(responses.calls))
        self.assertURLEqual(
            'https://matrix.route.ls.hereapi.com/routing/7.2/calculatematrix.json?apikey=sample_api_key&'
            'destination0=geo%2149.445776%2C8.780916&height=20&length=10&limitedWeight=10&'
            'mode=fastest%3Bcar&shippedHazardousGoods=gas%2Cflammable&start0=geo%2149.420577%2C8.688641&'
            'start1=geo%2149.415776%2C8.680916&summaryAttributes=traveltime%2Ccostfactor&trailersCount=3&truckType=truck&'
            'weightPerAxle=100&width=10', responses.calls[0].request.url
        )

        self.assertIsInstance(matrix, Matrix)
        self.assertIsInstance(matrix.durations, list)
        self.assertIsInstance(matrix.distances, list)
        self.assertIsInstance(matrix.raw, dict)

    def test_index_sources_matrix(self):
        query = deepcopy(ENDPOINTS_QUERIES[self.name]['matrix'])
        query['sources'] = [100]

        self.assertRaises(IndexError, lambda: self.client.matrix(**query))

    def test_index_destinations_matrix(self):
        query = deepcopy(ENDPOINTS_QUERIES[self.name]['matrix'])
        query['destinations'] = [100]

        self.assertRaises(IndexError, lambda: self.client.matrix(**query))
