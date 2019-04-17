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

from .base import Router, DEFAULT
from routingpy import utils
from routingpy.direction import Direction
from routingpy.isochrone import Isochrone, Isochrones
from routingpy.matrix import Matrix

from operator import itemgetter


class Valhalla(Router):
    """Performs requests to a Valhalla instance."""

    def __init__(self,
                 base_url,
                 api_key=None,
                 user_agent=None,
                 timeout=DEFAULT,
                 retry_timeout=None,
                 requests_kwargs=None,
                 retry_over_query_limit=False,
                 skip_api_error=None):
        """
        Initializes a Valhalla client.

        :param api_key: Mapbox API key. Required if base_url='https://api.mapbox.com/valhalla/v1'.
        :type api_key: str

        :param base_url: The base URL for the request. Defaults to the ORS API
            server. Should not have a trailing slash.
        :type base_url: str

        :param user_agent: User Agent to be used when requesting.
            Default :attr:`routingpy.routers.options.default_user_agent`.
        :type user_agent: str

        :param timeout: Combined connect and read timeout for HTTP requests, in
            seconds. Specify ``None`` for no timeout. Default :attr:`routingpy.routers.options.default_timeout`.
        :type timeout: int or None

        :param retry_timeout: Timeout across multiple retriable requests, in
            seconds.  Default :attr:`routingpy.routers.options.default_retry_timeout`.
        :type retry_timeout: int

        :param requests_kwargs: Extra keyword arguments for the requests
            library, which among other things allow for proxy auth to be
            implemented. **Note**, that ``proxies`` can be set globally
            in :attr:`routingpy.routers.options.default_proxies`.

            Example:

            >>> from routingpy.routers import Valhalla
            >>> router = Valhalla(my_key, requests_kwargs={'proxies': {'https': '129.125.12.0'}})
            >>> print(router.proxies)
            {'https': '129.125.12.0'}
        :type requests_kwargs: dict

        :param retry_over_query_limit: If True, client will not raise an exception
            on HTTP 429, but instead jitter a sleeping timer to pause between
            requests until HTTP 200 or retry_timeout is reached.
            Default :attr:`routingpy.routers.options.default_over_query_limit`.
        :type retry_over_query_limit: bool

        :param skip_api_error: Continue with batch processing if a :class:`routingpy.exceptions.RouterApiError` is
            encountered (e.g. no route found). If False, processing will discontinue and raise an error.
            Default :attr:`routingpy.routers.options.default_skip_api_error`.
        :type skip_api_error: bool
        """

        self.api_key = api_key

        super(Valhalla, self).__init__(base_url, user_agent, timeout,
                                       retry_timeout, requests_kwargs,
                                       retry_over_query_limit, skip_api_error)

    class Waypoint(object):
        """
        Constructs a waypoint with additional information, such as via or encoded lines.

        Example:

        >>> waypoint = Valhalla.WayPoint(position=[8.15315, 52.53151], type='break', heading=120, heading_tolerance=10, minimum_reachability=10, radius=400)
        >>> route = Valhalla('http://localhost/v1').directions(locations=[[[8.58232, 51.57234]], waypoint, [7.15315, 53.632415]])
        """

        def __init__(self,
                     position,
                     type=None,
                     heading=None,
                     heading_tolerance=None,
                     minimum_reachability=None,
                     radius=None,
                     rank_candidates=None):
            """

            :param type: Type of location. One of ['break', 'through']. A break is a stop, so the first
            and last locations must be of type break. A through location is one that the route path travels
            through, and is useful to force a route to go through location. The path is not allowed to
            reverse direction at the through locations. If no type is provided, the type is assumed to be a break.
            The order has to correspond to ``coordinates`` and be of the same length.
            More info at: https://github.com/valhalla/valhalla/blob/master/docs/api/turn-by-turn/api-reference.md#locations
            :type type: list of str

            :param heading: Preferred direction of travel for the start from the location. The heading is indicated
                in degrees from north in a clockwise direction, where north is 0°, east is 90°,
                south is 180°, and west is 270°.
            :type heading: list of int

            :param heading_tolerance: How close in degrees a given street's angle must be in order for it
                to be considered as in the same direction of the heading parameter. The default value is 60 degrees.
            :type heading_tolerance: list of int

            :param minimum_reachability: Minimum number of nodes (intersections) reachable for a given edge (road between
                intersections) to consider that edge as belonging to a connected region. When correlating this
                location to the route network, try to find candidates who are reachable from this many or more
                nodes (intersections). If a given candidate edge reaches less than this number of nodes its considered
                to be a disconnected island and we'll search for more candidates until we find at least one that
                isn't considered a disconnected island. If this value is larger than the configured service limit
                it will be clamped to that limit. The default is a minimum of 50 reachable nodes.
            :type minimum_reachability: list of int

            :param radius: The number of meters about this input location within which edges (roads between intersections)
                will be considered as candidates for said location. When correlating this location to the route network,
                try to only return results within this distance (meters) from this location. If there are no candidates
                within this distance it will return the closest candidate within reason. If this value is larger than
                the configured service limit it will be clamped to that limit. The default is 0 meters.
            :type radius: list of int

            :param rank_candidates: Whether or not to rank the edge candidates for this location. The ranking is used
                as a penalty within the routing algorithm so that some edges will be penalized more heavily than others.
                If true candidates will be ranked according to their distance from the input and various other attributes.
                If false the candidates will all be treated as equal which should lead to routes that are just the most
                optimal path with emphasis about which edges were selected.
            :type rank_candidates: list of bool
            """

            self._position = position
            self._type = type
            self._heading = heading
            self._heading_tolerance = heading_tolerance
            self._minimum_reachability = minimum_reachability
            self._radius = radius
            self._rank_candidates = rank_candidates

        def _make_waypoint(self):

            waypoint = {'lon': self._position[0], 'lat': self._position[1]}

            if self._type:
                waypoint['type'] = self._type

            if self._heading:
                waypoint['heading'] = self._heading

            if self._heading_tolerance:
                waypoint['heading_tolerance'] = self._heading_tolerance

            if self._minimum_reachability:
                waypoint['minimum_reachability'] = self._minimum_reachability

            if self._radius:
                waypoint['radius'] = self._radius

            if self._rank_candidates is not None:
                waypoint['rank_candidates'] = self._rank_candidates

            return waypoint

    def directions(self,
                   locations,
                   profile,
                   options=None,
                   units=None,
                   language=None,
                   directions_type=None,
                   avoid_locations=None,
                   date_time=None,
                   id=None,
                   dry_run=None):
        """Get directions between an origin point and a destination point.

        For more information, visit https://github.com/valhalla/valhalla/blob/master/docs/api/turn-by-turn/api-reference.md.

        :param locations: The coordinates tuple the route should be calculated
            from in order of visit. Can be a list/tuple of [lon, lat] or :class:`Valhalla.WayPoint` instance or
            a combination of both.
        :type locations: list of list or list of :class:`Valhalla.WayPoint`

        :param profile: Specifies the mode of transport to use when calculating
            directions. One of ["auto", "auto_shorter", "bicycle", "bus", "hov", "motor_scooter",
            "motorcycle", "multimodal", "pedestrian".
        :type profile: str

        :param options: Profiles can have several options that can be adjusted to develop the route path,
            as well as for estimating time along the path. Only specify the actual options dict, the profile
            will be filled automatically. For more information, visit:
            https://github.com/valhalla/valhalla/blob/master/docs/api/turn-by-turn/api-reference.md#costing-options
        :type options: dict

        :param units: Distance units for output. One of ['mi', 'km']. Default km.
        :type units: str

        :param language: The language of the narration instructions based on the IETF BCP 47 language tag string.
            One of ['ca', 'cs', 'de', 'en', 'pirate', 'es', 'fr', 'hi', 'it', 'pt', 'ru', 'sl', 'sv']. Default 'en'.
        :type language: str

        :param directions_type: 'none': no instructions are returned. 'maneuvers': only maneuvers are returned.
            'instructions': maneuvers with instructions are returned. Default 'instructions'.
        :type directions_type: str

        :param avoid_locations: A set of locations to exclude or avoid within a route.
            Specified as a list of coordinates, similar to coordinates object.
        :type avoid_locations: list of list or list of :class:`Valhalla.WayPoint`

        :param date_time: This is the local date and time at the location. Field ``type``: 0: Current departure time,
            1: Specified departure time. Field ``value```: the date and time is specified
            in ISO 8601 format (YYYY-MM-DDThh:mm), local time.
            E.g. date_time = {type: 0, value: 2019-03-03T08:06:23}
        :type date_time: dict

        :param id: Name your route request. If id is specified, the naming will be sent thru to the response.
        :type id: str

        :param dry_run: Print URL and parameters without sending the request.
        :param dry_run: bool

        :returns: A route from provided coordinates and restrictions.
        :rtype: :class:`routingpy.direction.Direction`
        """

        params = dict(costing=profile)

        params['locations'] = self._build_locations(locations)

        if options:
            params['costing_options'] = dict()
            profile = profile if profile != 'multimodal' else 'transit'
            params['costing_options'][profile] = options

        if any((units, language, directions_type)):
            params['directions_options'] = dict()
            if units:
                params['directions_options']['units'] = units
            if language:
                params['directions_options']['language'] = language
            if directions_type:
                params['directions_options'][
                    'directions_type'] = directions_type

        if avoid_locations:
            params['avoid_locations'] = self._build_locations(avoid_locations)

        if date_time:
            params['date_time'] = date_time

        if id:
            params['id'] = id

        get_params = {'access_token': self.api_key} if self.api_key else {}

        return self._parse_direction_json(
            self._request(
                "/route",
                get_params=get_params,
                post_params=params,
                dry_run=dry_run), units)

    @staticmethod
    def _parse_direction_json(response, units):
        if response is None:  # pragma: no cover
            return Direction()

        geometry, duration, distance = [], 0, 0
        for leg in response['trip']['legs']:
            geometry.extend([
                list(reversed(coord))
                for coord in utils.decode_polyline6(leg['shape'])
            ])
            duration += leg['summary']['time']

            factor = 0.621371 if units == 'mi' else 1
            distance += int(leg['summary']['length'] * 1000 * factor)

        return Direction(
            geometry=geometry,
            duration=int(duration),
            distance=int(distance),
            raw=response)

    def isochrones(self,
                   locations,
                   profile,
                   intervals,
                   colors=None,
                   polygons=None,
                   denoise=None,
                   generalize=None,
                   options=None,
                   units=None,
                   language=None,
                   directions_type=None,
                   avoid_locations=None,
                   date_time=None,
                   id=None,
                   dry_run=None):
        """Gets isochrones or equidistants for a range of time values around a given set of coordinates.

        For more information, visit https://github.com/valhalla/valhalla/blob/master/docs/api/isochrone/api-reference.md.

        :param locations: One pair of lng/lat values. Takes the form [Longitude, Latitude].
        :type locations: list of float

        :param profile: Specifies the mode of transport to use when calculating
            directions. One of ["auto", "bicycle", "multimodal", "pedestrian".
        :type profile: str

        :param intervals: Time ranges to calculate isochrones for. Up to 4 ranges are possible. In seconds.
        :type intervals: list of int

        :param colors: The color for the output of the contour. Specify it as a Hex value, but without the #, such as
            "color":"ff0000" for red. If no color is specified, the isochrone service will assign a default color to the output.
        :type colors: list of str

        :param polygons: Controls whether polygons or linestrings are returned in GeoJSON geometry. Default False.
        :type polygons: bool

        :param denoise: Can be used to remove smaller contours. In range [0, 1]. A value of 1 will only return the largest contour
            for a given time value. A value of 0.5 drops any contours that are less than half the area of the largest
            contour in the set of contours for that same time value. Default 1.
        :type denoise: float

        :param generalize: A floating point value in meters used as the tolerance for Douglas-Peucker generalization.
            Note: Generalization of contours can lead to self-intersections, as well as intersections of adjacent contours.
        :type generalize: float

        :param options: Profiles can have several options that can be adjusted to develop the route path,
            as well as for estimating time along the path. Only specify the actual options dict, the profile
            will be filled automatically. For more information, visit:
            https://github.com/valhalla/valhalla/blob/master/docs/api/turn-by-turn/api-reference.md#costing-options
        :type options: dict

        :param units: Distance units for output. One of ['mi', 'km']. Default km.
        :type units: str

        :param language: The language of the narration instructions based on the IETF BCP 47 language tag string.
            One of ['ca', 'cs', 'de', 'en', 'pirate', 'es', 'fr', 'hi', 'it', 'pt', 'ru', 'sl', 'sv']. Default 'en'.
        :type language: str

        :param avoid_locations: A set of locations to exclude or avoid within a route.
            Specified as a list of coordinates, similar to coordinates object.
        :type avoid_locations: list of list

        :param date_time: This is the local date and time at the location. Field ``type``: 0: Current departure time,
            1: Specified departure time. Field ``value```: the date and time is specified
            in format YYYY-MM-DDThh:mm, local time.

            E.g. date_time = {type: 0, value: 2019-03-03T08:06}
        :type date_time: dict

        :param id: Name your route request. If id is specified, the naming will be sent thru to the response.
        :type id: str

        :param dry_run: Print URL and parameters without sending the request.
        :param dry_run: bool

        :returns: An isochrone with the specified range.
        :rtype: :class:`routingpy.isochrone.Isochrones`
        """

        locations = self._build_locations(locations)

        contours = []
        for idx, r in enumerate(intervals):
            d = {'time': int(r / 60)}
            if colors:
                try:
                    d.update(color=colors[idx])
                except IndexError:
                    raise IndexError(
                        "Colors object must have same length as Range object.")
            contours.append(d)

        params = {
            "locations": locations,
            "costing": profile,
            "contours": contours,
        }

        if options:
            params['costing_options'] = dict()
            profile = profile if profile != 'multimodal' else 'transit'
            params['costing_options'][profile] = options

        if polygons is not None:
            params['polygons'] = polygons

        if denoise:
            params['denoise'] = denoise

        if generalize:
            params['generalize'] = generalize

        if avoid_locations:
            params['avoid_locations'] = self._build_locations(avoid_locations)

        if date_time:
            params['date_time'] = date_time

        if id:
            params['id'] = id

        get_params = {'access_token': self.api_key} if self.api_key else {}
        return self._parse_isochrone_json(
            self._request(
                "/isochrone",
                get_params=get_params,
                post_params=params,
                dry_run=dry_run), intervals, list(locations[0].values()))

    @staticmethod
    def _parse_isochrone_json(response, intervals, center):
        if response is None:  # pragma: no cover
            return Isochrones()

        return Isochrones([
            Isochrone(
                geometry=isochrone['geometry']['coordinates'],
                interval=intervals[idx],
                center=center) for idx, isochrone in enumerate(
                    list(reversed(response['features'])))
        ], response)

    def matrix(self,
               locations,
               profile,
               sources=None,
               destinations=None,
               options=None,
               avoid_locations=None,
               units=None,
               id=None,
               dry_run=None):
        """ Gets travel distance and time for a matrix of origins and destinations.

        :param locations: Multiple pairs of lng/lat values.
        :type locations: list of list

        :param profile: Specifies the mode of transport to use when calculating
            matrices. One of ["auto", "bicycle", "multimodal", "pedestrian".
        :type profile: str

        :param sources: A list of indices that refer to the list of locations
            (starting with 0). If not passed, all indices are considered.
        :type sources: list of int

        :param destinations: A list of indices that refer to the list of locations
            (starting with 0). If not passed, all indices are considered.
        :type destinations: list of int

        :param options: Profiles can have several options that can be adjusted to develop the route path,
            as well as for estimating time along the path. Only specify the actual options dict, the profile
            will be filled automatically. For more information, visit:
            https://github.com/valhalla/valhalla/blob/master/docs/api/turn-by-turn/api-reference.md#costing-options
        :type options: dict

        :param avoid_locations: A set of locations to exclude or avoid within a route.
            Specified as a list of coordinates, similar to coordinates object.
        :type avoid_locations: list of list

        :param units: Distance units for output. One of ['mi', 'km']. Default km.
        :type units: str

        :param id: Name your route request. If id is specified, the naming will be sent through to the response.
        :type id: str

        :param dry_run: Print URL and parameters without sending the request.
        :param dry_run: bool

        :returns: A matrix from the specified sources and destinations.
        :rtype: :class:`routingpy.matrix.Matrix`
            """

        params = {
            'costing': profile,
        }

        locations = self._build_locations(locations)

        sources_coords = locations
        if sources is not None:
            sources_coords = itemgetter(*sources)(sources_coords)
            if isinstance(sources_coords, dict):
                sources_coords = [sources_coords]
        params['sources'] = sources_coords

        dest_coords = locations
        if destinations is not None:
            dest_coords = itemgetter(*destinations)(dest_coords)
            if isinstance(dest_coords, dict):
                dest_coords = [dest_coords]
        params['targets'] = dest_coords

        if options:
            params['costing_options'] = dict()
            profile = profile if profile != 'multimodal' else 'transit'
            params['costing_options'][profile] = options

        if avoid_locations:
            params['avoid_locations'] = self._build_locations(avoid_locations)

        if units:
            params["units"] = units

        if id:
            params['id'] = id

        get_params = {'access_token': self.api_key} if self.api_key else {}

        return self._parse_matrix_json(
            self._request(
                '/sources_to_targets',
                get_params=get_params,
                post_params=params,
                dry_run=dry_run), units)

    @staticmethod
    def _parse_matrix_json(response, units):
        if response is None:  # pragma: no cover
            return Matrix()

        factor = 0.621371 if units == 'mi' else 1
        durations = [[destination['time'] for destination in origin]
                     for origin in response['sources_to_targets']]
        distances = [[
            int(destination['distance'] * 1000 * factor)
            for destination in origin
        ] for origin in response['sources_to_targets']]

        return Matrix(durations=durations, distances=distances, raw=response)

    def _build_locations(self, coordinates):
        """Build the locations object for all methods"""

        locations = []

        # Isochrones only support one coordinate tuple, so check for type of first element
        if isinstance(coordinates[0], (list, tuple, self.Waypoint)):
            for idx, coord in enumerate(coordinates):
                if isinstance(coord, (list, tuple)):
                    locations.append({'lon': coord[0], 'lat': coord[1]}),
                elif isinstance(coord, self.Waypoint):
                    locations.append(coord._make_waypoint())
                else:
                    raise TypeError(
                        "Location type {} at index {} is not supported: {}".
                        format(type(coord), idx, coord))
        elif isinstance(coordinates[0], float):
            locations.append({'lon': coordinates[0], 'lat': coordinates[1]})

        return locations
