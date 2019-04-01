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
"""
Core client functionality, common across all API requests.
"""

from .base import Router
from routingpy import utils
from routingpy.direction import Direction
from routingpy.isochrone import Isochrone
from routingpy.matrix import Matrix


class ORS(Router):
    """Performs requests to the ORS API services."""

    _DEFAULT_BASE_URL = 'https://api.openrouteservice.org'

    def __init__(self,
                 api_key=None,
                 base_url=_DEFAULT_BASE_URL,
                 user_agent=None,
                 timeout=None,
                 retry_timeout=None,
                 requests_kwargs=None,
                 retry_over_query_limit=False):
        """
        Initializes an openrouteservice client.

        :param key: Mapbox API key. Required
        :type key: str

        :param base_url: The base URL for the request. Defaults to the ORS API
            server. Should not have a trailing slash.
        :type base_url: str

        :param timeout: Combined connect and read timeout for HTTP requests, in
            seconds. Specify "None" for no timeout.
        :type timeout: int

        :param retry_timeout: Timeout across multiple retriable requests, in
            seconds.
        :type retry_timeout: int

        :param requests_kwargs: Extra keyword arguments for the requests
            library, which among other things allow for proxy auth to be
            implemented. See the official requests docs for more info:
            http://docs.python-requests.org/en/latest/api/#main-interface
        :type requests_kwargs: dict

        :param retry_over_query_limit: If True, the client will retry when query
            limit is reached (HTTP 429). Default False.
        :type retry_over_query_limit: bool
        """

        if base_url == self._DEFAULT_BASE_URL and api_key is None:
            raise KeyError("API key must be specified.")

        requests_kwargs = requests_kwargs or {}
        headers = requests_kwargs.get('headers') or {}
        headers.update({'Authorization': api_key})
        requests_kwargs.update({'headers': headers})

        super(ORS, self).__init__(base_url, user_agent, timeout, retry_timeout,
                                  requests_kwargs, retry_over_query_limit)

    def directions(self,
                   coordinates,
                   profile,
                   format='geojson',
                   preference=None,
                   units=None,
                   language=None,
                   geometry=None,
                   geometry_simplify=None,
                   instructions=None,
                   instructions_format=None,
                   roundabout_exits=None,
                   attributes=None,
                   radiuses=None,
                   maneuvers=None,
                   bearings=None,
                   continue_straight=None,
                   elevation=None,
                   extra_info=None,
                   suppress_warnings=None,
                   options=None,
                   dry_run=None):
        """Get directions between an origin point and a destination point.

        For more information, visit https://openrouteservice.org/documentation/.

        :param coordinates: The coordinates tuple the route should be calculated
            from in order of visit.
        :type coordinates: list, tuple

        :param profile: Specifies the mode of transport to use when calculating
            directions. One of ["driving-car", "driving-hgv", "foot-walking",
            "foot-hiking", "cycling-regular", "cycling-road",
          , "cycling-mountain", "cycling-electric",]. Default "driving-car".
        :type profile: str

        :param format: Specifies the response format. One of ['json', 'geojson']. Default "json".
            Geometry format for "json" is Google's encodedpolyline.
        :type format: str

        :param preference: Specifies the routing preference. One of ["fastest, "shortest",
            "recommended"]. Default fastest.
        :type preference: str

        :param units: Specifies the distance unit. One of ["m", "km", "mi"]. Default "m".
        :type units: str

        :param language: Language for routing instructions. One of ["en", "de", "cn",
            "es", "ru", "dk", "fr", "it", "nl", "br", "se", "tr", "gr"].
        :type language: str

        :param geometry: Specifies whether geometry should be returned. Default True.
        :type geometry: bool

        :param geometry_simplify: Specifies whether to simplify the geometry.
            Default False.
        :type geometry_simplify: bool

        :param instructions: Specifies whether to return turn-by-turn instructions.
            Default True.
        :type instructions: bool

        :param instructions_format: Specifies the the output format for instructions.
            One of ["text", "html"]. Default "text".
        :type instructions_format: string

        :param roundabout_exits: Provides bearings of the entrance and all passed
            roundabout exits. Adds the 'exit_bearings' array to the 'step' object
            in the response. Default False.
        :type roundabout_exits: bool

        :param attributes: Returns route attributes on ["avgspeed", "detourfactor", "percentage"].
            Must be a list of strings. Default None.
        :type attributes: list, tuple of str

        :param maneuvers: Specifies whether the maneuver object is included into the step object or not. Default: False.
        :type maneuvers bool

        :param radiuses: A list of maximum distances (measured in
            meters) that limit the search of nearby road segments to every given waypoint.
            The values must be greater than 0, the value of -1 specifies no limit in
            the search. The number of radiuses must correspond to the number of waypoints.
            Default 50 km (ORS backend).
        :type radiuses: list or tuple

        :param bearings: Specifies a list of pairs (bearings and
            deviations) to filter the segments of the road network a waypoint can
            snap to. For example bearings=[[45,10],[120,20]]. Each pair is a
            comma-separated list that can consist of one or two float values, where
            the first value is the bearing and the second one is the allowed deviation
            from the bearing. The bearing can take values between 0 and 360 clockwise
            from true north. If the deviation is not set, then the default value of
            100 degrees is used. The number of pairs must correspond to the number
            of waypoints. Setting optimized=false is mandatory for this feature to
            work for all profiles. The number of bearings corresponds to the length
            of waypoints-1 or waypoints. If the bearing information for the last waypoint
            is given, then this will control the sector from which the destination
            waypoint may be reached.
        :type bearings: list, tuple

        :param continue_straight: Forces the route to keep going straight at waypoints not
            restricting u-turns even if u-turns would be faster. Default False.
        :type continue_straight: bool

        :param elevation: Specifies whether to return elevation values for points.
            Default False.
        :type elevation: bool

        :param extra_info: Returns additional information on ["steepness", "suitability",
            "surface", "waycategory", "waytype", "tollways", "traildifficulty", "roadaccessrestrictions"].
            Must be a list of strings. Default None.
        :type extra_info: list, tuple of str

        :param suppress_warnings: Tells the system to not return any warning messages in extra_info.
        :type suppress_warnings: bool

        :param options: Refer to https://openrouteservice.org/documentation for
            detailed documentation. Construct your own dict() options object and paste it to your code.
        :type options: dict

        :param dry_run: Print URL and parameters without sending the request.
        :param dry_run: bool

        :returns: A route from provided coordinates and restrictions.
        :rtype: :class:`routingpy.direction.Direction`
        """

        params = {"coordinates": coordinates, "profile": profile}

        if preference:
            params["preference"] = preference

        if units:
            params["units"] = units

        if language:
            params["language"] = language

        if geometry is not None:
            params["geometry"] = geometry

        if geometry_simplify is not None:
            params["geometry_simplify"] = geometry_simplify

        if instructions is not None:
            params["instructions"] = instructions

        if instructions_format:
            params["instructions_format"] = instructions_format

        if roundabout_exits is not None:
            params["roundabout_exits"] = roundabout_exits

        if attributes:
            params["attributes"] = attributes

        if radiuses:
            params["radiuses"] = radiuses

        if maneuvers is not None:
            params['maneuvers'] = maneuvers

        if bearings:
            params["bearings"] = bearings

        if continue_straight is not None:
            params["continue_straight"] = continue_straight

        if elevation is not None:
            params["elevation"] = elevation

        if extra_info:
            params["extra_info"] = extra_info

        if suppress_warnings is not None:
            params['suppress_warnings'] = suppress_warnings

        if options:
            params['options'] = options

        return self._parse_direction_json(
            self._request(
                "/v2/directions/" + profile + '/' + format,
                get_params={},
                post_params=params,
                dry_run=dry_run), format, units)

    @staticmethod
    def _parse_direction_json(response, format, units):
        if response is None:
            return None

        units_factor = 1
        if units == 'mi':
            units_factor = 0.621371 * 1000
        elif units == 'km':
            units_factor = 1000

        if format == 'geojson':
            geometry = response['features'][0]['geometry']['coordinates']
            duration = int(response['features'][0]['properties']['duration'])
            distance = int(response['features'][0]['properties']['distance'])
        elif format == 'json':
            geometry = [
                list(reversed(coord)) for coord in utils.decode_polyline6(
                    response['routes'][0]['geometry'])
            ]
            duration = int(response['routes'][0]['summary']['duration'])
            distance = int(
                response['routes'][0]['summary']['distance'] * units_factor)

        return Direction(
            geometry=geometry,
            duration=duration,
            distance=distance,
            raw=response)

    def isochrones(self,
                   coordinates,
                   profile,
                   range,
                   range_type,
                   interval=None,
                   units=None,
                   location_type=None,
                   smoothing=None,
                   attributes=None,
                   intersections=None,
                   dry_run=None):
        """Gets isochrones or equidistants for a range of time/distance values around a given set of coordinates.

        :param coordinates: One pair of lng/lat values.
        :type coordinates: list, tuple

        :param profile: Specifies the mode of transport to use when calculating
            directions. One of ["driving-car", "driving-hgv", "foot-walking",
            "foot-hiking", "cycling-regular", "cycling-safe", "cycling-mountain",
            "cycling-electric",]. Default "driving-car".
        :type profile: str

        :param range_type: Set 'time' for isochrones or 'distance' for equidistants.
            Default 'time'.
        :type sources: str

        :param range: Ranges to calculate distances/durations for. This can be
            a list of multiple ranges, e.g. [600, 1200, 1400] or a single value list.
            In the latter case, you can also specify the 'interval' variable to break
            the single value into more isochrones. In meters or seconds.
        :type range: list of int

        :param interval: Segments isochrones or equidistants for one 'range' value.
            Only has effect if used with a single 'range' value.
            In meters or seconds.
        :type interval: int

        :param units: Specifies the unit system to use when displaying results.
            One of ["m", "km", "m"]. Default "m".
        :type units: str

        :param location_type: 'start' treats the location(s) as starting point,
            'destination' as goal. Default 'start'.
        :type location_type: str

        :param smoothing: Applies a level of generalisation to the isochrone polygons generated.
            Value between 0 and 1, whereas a value closer to 1 will result in a more generalised shape.
        :type smoothing: float

        :param attributes: 'area' returns the area of each polygon in its feature
            properties. 'reachfactor' returns a reachability score between 0 and 1.
            'total_pop' returns population statistics from https://ghsl.jrc.ec.europa.eu/about.php.
            One or more of ['area', 'reachfactor', 'total_pop']. Default 'area'.
        :type attributes: list of str

        :param intersections: Write smth.
        :type intersections: bool

        :param dry_run: Print URL and parameters without sending the request.
        :param dry_run: bool

        :returns: An isochrone with the specified range.
        :rtype: list of :class:`routingpy.isochrone.Isochrone`
        """

        params = {
            "locations": coordinates,
            "profile": profile,
            "range": range,
            "range_type": range_type
        }

        if interval:
            params['interval'] = interval

        if units:
            params["units"] = units

        if location_type:
            params["location_type"] = location_type

        if smoothing:
            params["smoothing"] = smoothing

        if attributes:
            params["attributes"] = attributes

        if intersections:
            params["intersections"] = intersections

        return self._parse_isochrone_json(
            self._request(
                "/v2/isochrones/" + profile + '/geojson',
                get_params={},
                post_params=params,
                dry_run=dry_run), range)

    @staticmethod
    def _parse_isochrone_json(response, range):
        if response is None:
            return None
        return [
            Isochrone(isochrone['geometry']['coordinates'], range[idx],
                      isochrone)
            for idx, isochrone in enumerate(response['features'])
        ]

    def distance_matrix(self,
                        coordinates,
                        profile,
                        sources=None,
                        destinations=None,
                        metrics=None,
                        resolve_locations=None,
                        units=None,
                        dry_run=None):
        """ Gets travel distance and time for a matrix of origins and destinations.

        :param coordinates: One or more pairs of lng/lat values.
        :type coordinates: a single location, or a list of locations, where a
            location is a list or tuple of lng,lat values

        :param profile: Specifies the mode of transport to use when calculating
            directions. One of ["driving-car", "driving-hgv", "foot-walking",
            "foot-hiking", "cycling-regular", "cycling-road", "cycling-mountain",
            "cycling-electric",]. Default "driving-car".
        :type profile: str

        :param sources: A list of indices that refer to the list of locations
            (starting with 0). If not passed, all indices are considered.
        :type sources: list or tuple

        :param destinations: A list of indices that refer to the list of locations
            (starting with 0). If not passed, all indices are considered.
        :type destinations: list or tuple

        :param metrics: Specifies a list of returned metrics. One or more of ["distance",
            "duration"]. Default ['duration'].
        :type metrics: list of str

        :param resolve_locations: Specifies whether given locations are resolved or
            not. If set 'true', every element in destinations and sources will
            contain the name element that identifies the name of the closest street.
            Default False.
        :type resolve_locations: bool

        :param units: Specifies the unit system to use when displaying results.
            One of ["m", "km", "m"]. Default "m".
        :type units: str

        :param dry_run: Print URL and parameters without sending the request.
        :param dry_run: bool

        :returns: A matrix from the specified sources and destinations.
        :rtype: :class:`routingpy.matrix.Matrix`
        """

        params = {"locations": coordinates, "profile": profile}

        if sources:
            params['sources'] = sources

        if destinations:
            params['destinations'] = destinations

        if metrics:
            params["metrics"] = metrics

        if resolve_locations is not None:
            params["resolve_locations"] = resolve_locations

        if units:
            params["units"] = units

        return self._parse_matrix_json(
            self._request(
                "/v2/matrix/" + profile + '/json',
                get_params={},
                post_params=params,
                dry_run=dry_run))

    @staticmethod
    def _parse_matrix_json(response):
        if response is None:
            return None
        durations = response.get('durations')
        distances = response.get('distances')
        return Matrix(durations, distances, response)
