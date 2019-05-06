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

from .base import Router, DEFAULT
from routingpy import convert
from routingpy import utils
from routingpy.direction import Direction, Directions
from routingpy.isochrone import Isochrone, Isochrones
from routingpy.matrix import Matrix


class Graphhopper(Router):
    """Performs requests to the Graphhopper API services."""

    _DEFAULT_BASE_URL = "https://graphhopper.com/api/1"

    def __init__(self,
                 api_key=None,
                 base_url=_DEFAULT_BASE_URL,
                 user_agent=None,
                 timeout=DEFAULT,
                 retry_timeout=None,
                 requests_kwargs={},
                 retry_over_query_limit=False,
                 skip_api_error=None):
        """
        Initializes an graphhopper client.

        :param api_key: GH API key. Required if https://graphhopper.com/api is used.
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

            >>> from routingpy.routers import Graphhopper
            >>> router = Graphhopper(my_key, requests_kwargs={'proxies': {'https': '129.125.12.0'}})
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

        if base_url == self._DEFAULT_BASE_URL and api_key is None:
            raise KeyError("API key must be specified.")
        self.key = api_key

        super(Graphhopper, self).__init__(
            base_url, user_agent, timeout, retry_timeout, requests_kwargs,
            retry_over_query_limit, skip_api_error)

    def directions(self,
                   locations,
                   profile,
                   format=None,
                   optimize=None,
                   instructions=None,
                   locale=None,
                   elevation=None,
                   points_encoded=None,
                   calc_points=None,
                   debug=None,
                   point_hint=None,
                   details=None,
                   ch_disable=None,
                   weighting=None,
                   heading=None,
                   heading_penalty=None,
                   pass_through=None,
                   block_area=None,
                   avoid=None,
                   algorithm=None,
                   round_trip_distance=None,
                   round_trip_seed=None,
                   alternative_route_max_paths=None,
                   alternative_route_max_weight_factor=None,
                   alternative_route_max_share_factor=None,
                   dry_run=None):
        """Get directions between an origin point and a destination point.

        For more information, visit https://docs.graphhopper.com/#tag/Routing-API/paths/~1route/get.

        :param locations: The coordinates tuple the route should be calculated
            from in order of visit.
        :type locations: list of list or tuple of tuple

        :param profile: The vehicle for which the route should be calculated. One of ["car" "bike" "foot" "hike" "mtb"
            "racingbike" "scooter" "truck" "small_truck"]. Default "car".
        :type profile: str

        :param format: Specifies the resulting format of the route, for json the content type will be application/json.
            Default "json".
        :type format: str

        :param locale: Language for routing instructions. The locale of the resulting turn instructions.
            E.g. pt_PT for Portuguese or de for German. Default "en".
        :type locale: str

        :param optimize: If false the order of the locations will be identical to the order of the point parameters.
            If you have more than 2 points you can set this optimize parameter to ``True`` and the points will be sorted
            regarding the minimum overall time - e.g. suiteable for sightseeing tours or salesman.
            Keep in mind that the location limit of the Route Optimization API applies and the credit costs are higher!
            Note to all customers with a self-hosted license: this parameter is only available if your package includes
            the Route Optimization API. Default False.
        :type optimize: bool

        :param instructions: Specifies whether to return turn-by-turn instructions.
            Default True.
        :type instructions: bool

        :param elevation: If true a third dimension - the elevation - is included in the polyline or in the GeoJson.
            IMPORTANT: If enabled you have to use a modified version of the decoding method or set points_encoded to false.
            See the points_encoded attribute for more details. Additionally a request can fail if the vehicle does not
            support elevation. See the features object for every vehicle.
            Default False.
        :type elevation: bool

        :param points_encoded: If ``False`` the coordinates in point and snapped_waypoints are returned as array using the order
            [lon,lat,elevation] for every point. If true the coordinates will be encoded as string leading to less bandwith usage.
            Default True.
        :type points_encoded: bool

        :param calc_points: If the points for the route should be calculated at all, printing out only distance and time.
            Default True.
        :type calc_points: bool

        :param debug: If ``True``, the output will be formated.
            Default False.
        :type debug: bool

        :param point_hint: Optional parameter. Specifies a hint for each point parameter to prefer a certain street for the
            closest location lookup. E.g. if there is an address or house with two or more neighboring streets you can control
            for which street the closest location is looked up.
        :type point_hint: bool

        :param details: Optional parameter. Optional parameter to retrieve path details. You can request additional details for the
            route: street_name and time. For all motor vehicles we additionally support max_speed, toll (no, all, hgv),
            road_class (motorway, primary, ...), road_environment, and surface. The returned format for one details
            is [fromRef, toRef, value]. The ref references the points of the response. Multiple details are possible
            via multiple key value pairs details=time&details=toll
        :type details: list of str

        :param ch_disable: Always use ch_disable=true in combination with one or more parameters of this table.
            Default False.
        :type ch_disable: bool

        :param weighting: Which kind of 'best' route calculation you need. Other options are shortest
            (e.g. for vehicle=foot or bike) and short_fastest if not only time but also distance is expensive.
            Default "fastest".
        :type weighting: str

        :param heading: Optional parameter. Favour a heading direction for a certain point. Specify either one heading for the start point or as
            many as there are points. In this case headings are associated by their order to the specific points.
            Headings are given as north based clockwise angle between 0 and 360 degree.
        :type heading: list of int

        :param heading_penalty: Optional parameter. Penalty for omitting a specified heading. The penalty corresponds to the accepted time
            delay in seconds in comparison to the route without a heading.
            Default 120.
        :type heading_penalty: int

        :param pass_through: Optional parameter. If true u-turns are avoided at via-points with regard to the heading_penalty.
            Default False.
        :type pass_through: bool

        :param block_area: Optional parameter. Block road access via a point with the format
            latitude,longitude or an area defined by a circle lat,lon,radius or a rectangle lat1,lon1,lat2,lon2.
        :type block_area: str

        :param avoid: Optional semicolon separated parameter. Specify which road classes you would like to avoid
            (currently only supported for motor vehicles like car). Possible values are ferry, motorway, toll, tunnel and ford.
        :type avoid: list of str

        :param algorithm: Optional parameter. round_trip or alternative_route.
        :type algorithm: str

        :param round_trip_distance: If algorithm=round_trip this parameter configures approximative length of the resulting round trip.
            Default 10000.
        :type round_trip_distance: int

        :param round_trip_seed: If algorithm=round_trip this parameter introduces randomness if e.g. the first try wasn't good.
            Default 0.
        :type round_trip_seed: int

        :param alternative_route_max_paths: If algorithm=alternative_route this parameter sets the number of maximum paths
            which should be calculated. Increasing can lead to worse alternatives.
            Default 2.
        :type alternative_route_max_paths: int

        :param alternative_route_max_weight_factor: If algorithm=alternative_route this parameter sets the factor by which the alternatives
            routes can be longer than the optimal route. Increasing can lead to worse alternatives.
            Default 1.4.
        :type alternative_route_max_weight_factor: float

        :param alternative_route_max_share_factor: If algorithm=alternative_route this parameter specifies how much alternatives
            routes can have maximum in common with the optimal route. Increasing can lead to worse alternatives.
            Default 0.6.
        :type alternative_route_max_share_factor: float

        :param dry_run: Print URL and parameters without sending the request.
        :param dry_run: bool

        :returns: One or multiple route(s) from provided coordinates and restrictions.
        :rtype: :class:`routingpy.direction.Direction` or :class:`routingpy.direction.Directions`
        """

        params = [('vehicle', profile)]

        for coordinate in locations:
            coord_latlng = reversed(
                [convert._format_float(f) for f in coordinate])
            params.append(("point", ",".join(coord_latlng)))

        if self.key is not None:
            params.append(("key", self.key))

        if format is not None:
            params.append(("type", format))

        if optimize is not None:
            params.append(("optimize", convert._convert_bool(optimize)))

        if instructions is not None:
            params.append(("instructions",
                           convert._convert_bool(instructions)))

        if locale is not None:
            params.append(("locale", locale))

        if elevation is not None:
            params.append(("elevation", convert._convert_bool(elevation)))

        if points_encoded is not None:
            params.append(("points_encoded",
                           convert._convert_bool(points_encoded)))

        if calc_points is not None:
            params.append(("calc_points", convert._convert_bool(calc_points)))

        if debug is not None:
            params.append(("debug", convert._convert_bool(debug)))

        if point_hint is not None:
            params.append(("point_hint", convert._convert_bool(point_hint)))

        ### all below params will only work if ch is disabled

        if details is not None:
            params.extend([("details", detail) for detail in details])

        if ch_disable is not None:
            params.append(("ch.disable", convert._convert_bool(ch_disable)))

        if weighting is not None:
            params.append(("weighting", weighting))

        if heading is not None:
            params.append(("heading", convert._delimit_list(heading)))

        if heading_penalty is not None:
            params.append(("heading_penalty", heading_penalty))

        if pass_through is not None:
            params.append(("pass_through",
                           convert._convert_bool(pass_through)))

        if block_area is not None:
            params.append(("block_area", block_area))

        if avoid is not None:
            params.append(("avoid", convert._delimit_list(avoid, ';')))

        if algorithm is not None:

            params.append(('algorithm', algorithm))

            if algorithm == 'round_trip':

                if round_trip_distance is not None:
                    params.append(("round_trip.distance", round_trip_distance))

                if round_trip_seed is not None:
                    params.append(("round_trip.seed", round_trip_seed))

            if algorithm == 'alternative_route':

                if alternative_route_max_paths is not None:
                    params.append(("alternative_route.max_paths",
                                   alternative_route_max_paths))

                if alternative_route_max_weight_factor is not None:
                    params.append(("alternative_route.max_weight_factor",
                                   alternative_route_max_weight_factor))

                if alternative_route_max_share_factor:
                    params.append(("alternative_route_max_share_factor",
                                   alternative_route_max_share_factor))

        return self._parse_directions_json(
            self._request('/route', get_params=params, dry_run=dry_run),
            algorithm, elevation)

    @staticmethod
    def _parse_directions_json(response, algorithm, elevation):
        if response is None:  # pragma: no cover
            if algorithm == 'alternative_route':
                return Directions()
            else:
                return Direction()

        if algorithm == 'alternative_route':
            routes = []
            for route in response['paths']:
                geometry = [
                    list(reversed(coord)) for coord in utils.decode_polyline5(
                        route['points'], elevation)
                ]
                routes.append(
                    Direction(
                        geometry=geometry,
                        duration=int(route['time'] / 1000),
                        distance=int(route['distance']),
                        raw=route))
            return Directions(routes, response)
        else:
            geometry = [
                list(reversed(coord)) for coord in utils.decode_polyline5(
                    response['paths'][0]['points'], elevation)
            ]
            return Direction(
                geometry=geometry,
                duration=int(response['paths'][0]['time'] / 1000),
                distance=int(response['paths'][0]['distance']),
                raw=response)

    def isochrones(self,
                   locations,
                   profile,
                   intervals,
                   buckets=1,
                   interval_type=None,
                   reverse_flow=None,
                   debug=None,
                   dry_run=None):
        """Gets isochrones or equidistants for a range of time/distance values around a given set of coordinates.

        For mroe details visit https://docs.graphhopper.com/#tag/Isochrone-API.

        :param locations: One coordinate pair denoting the location.
        :type locations: tuple of float or list of float

        :param profile: Specifies the mode of transport.
            One of bike, car, foot or
            https://graphhopper.com/api/1/docs/supported-vehicle-profiles/Default.
            Default "car".
        :type profile: str

        :param intervals: Maximum range to calculate distances/durations for. You can also specify
            the ``buckets`` variable to break the single value into more isochrones. For compatibility reasons,
            this parameter is expressed as list. In meters or seconds.
        :type intervals: list of int or tuple of int

        :param interval_type: Set ``time`` for isochrones or ``distance`` for equidistants.
            Default 'time'.
        :type interval_type: str

        :param buckets: For how many sub intervals an additional polygon should be calculated.
            Default 1.
        :type buckets: int

        :param reverse_flow: If false the flow goes from point to the polygon,
            if true the flow goes from the polygon "inside" to the point.
            Default False.
        :param reverse_flow: bool

        :param debug: If true, the output will be formatted.
            Default False
        :type debug: bool

        :param dry_run: Print URL and parameters without sending the request.
        :param dry_run: bool

        :returns: An isochrone with the specified range.
        :rtype: :class:`routingpy.isochrone.Isochrones`
        """

        params = [
            ('vehicle', profile),
        ]

        if convert._is_list(intervals):
            if interval_type in (None, 'time'):
                params.append(('time_limit', intervals[0]))
            elif interval_type == 'distance':
                params.append(('distance_limit', intervals[0]))
        else:
            raise TypeError(
                "Parameter range={} must be of type list or tuple".format(
                    range))

        center = [convert._format_float(f) for f in locations]
        center.reverse()
        params.append(("point", ",".join(center)))

        if self.key is not None:
            params.append(("key", self.key))

        if buckets is not None:
            params.append(('buckets', buckets))

        if reverse_flow is not None:
            params.append(('reverse_flow',
                           convert._convert_bool(reverse_flow)))

        if debug is not None:
            params.append(('debug', convert._convert_bool(debug)))

        return self._parse_isochrone_json(
            self._request("/isochrone", get_params=params, dry_run=dry_run),
            intervals[0], buckets, center)

    @staticmethod
    def _parse_isochrone_json(response, max_range, buckets, center):
        if response is None:  # pragma: no cover
            return Isochrones()

        isochrones = []
        for index, polygon in enumerate(response["polygons"]):
            #print(index, buckets, max_range, int(max_range * (index+1 / buckets)))
            isochrones.append(
                Isochrone(
                    geometry=[
                        l[:2] for l in polygon['geometry']['coordinates'][0]
                    ],  # takes in elevation for some reason
                    interval=int(max_range * (
                        (polygon['properties']['bucket'] + 1) / buckets)),
                    center=center,
                ))

        return Isochrones(isochrones, response)

    def matrix(self,
               locations,
               profile,
               sources=None,
               destinations=None,
               out_array=['times', 'distances'],
               debug=None,
               dry_run=None):
        """ Gets travel distance and time for a matrix of origins and destinations.

        For more details visit https://docs.graphhopper.com/#tag/Matrix-API.

        :param locations: Specifiy multiple points for which the weight-, route-, time- or distance-matrix should be calculated.
            In this case the starts are identical to the destinations.
            If there are N points, then NxN entries will be calculated.
            The order of the point parameter is important. Specify at least three points.
            Cannot be used together with from_point or to_point. Is a string with the format latitude,longitude.
        :type locations: list of list or tuple of tuple or list of tuple or tuple of list

        :param profile: Specifies the mode of transport.
            One of bike, car, foot or
            https://graphhopper.com/api/1/docs/supported-vehicle-profiles/Default.
            Default "car".
        :type profile: str

        :param sources: The starting points for the routes.
            Specifies an index referring to locations.
        :type sources: list of int

        :param destinations: The destination points for the routes. Specifies an index referring to locations.
        :type destinations: list of int

        :param out_array: Specifies which arrays should be included in the response. Specify one or more of the following
            options 'weights', 'times', 'distances'.
            The units of the entries of distances are meters, of times are seconds and of weights is arbitrary and it can differ
            for different vehicles or versions of this API.
            Default ["times", "distance"].
        :type out_array: list of str

        :param dry_run: Print URL and parameters without sending the request.
        :param dry_run: bool

        :returns: A matrix from the specified sources and destinations.
        :rtype: :class:`routingpy.matrix.Matrix`
        """
        params = [('vehicle', profile)]

        if self.key is not None:
            params.append(("key", self.key))

        if sources is None and destinations is None:
            locations = (reversed([convert._format_float(f) for f in coord])
                         for coord in locations)
            params.extend([('point', ",".join(coord)) for coord in locations])

        else:
            sources_out = locations
            destinations_out = locations
            try:
                sources_out = []
                for idx in sources:
                    sources_out.append(locations[idx])
            except IndexError:
                raise IndexError(
                    "Parameter sources out of locations range at index {}.".
                    format(idx))
            except TypeError:
                # Raised when sources == None
                pass
            try:
                destinations_out = []
                for idx in destinations:
                    destinations_out.append(locations[idx])
            except IndexError:
                raise IndexError(
                    "Parameter destinations out of locations range at index {}."
                    .format(idx))
            except TypeError:
                # Raised when destinations == None
                pass

            sources_out = (reversed([convert._format_float(f) for f in coord])
                           for coord in sources_out)
            params.extend(
                [("from_point", ",".join(coord)) for coord in sources_out])

            destinations_out = (reversed(
                [convert._format_float(f) for f in coord])
                                for coord in destinations_out)
            params.extend(
                [("to_point", ",".join(coord)) for coord in destinations_out])

        if out_array is not None:
            for e in out_array:
                params.append(("out_array", e))

        if debug is not None:
            params.append(('debug', convert._convert_bool(debug)))

        return self._parse_matrix_json(
            self._request('/matrix', get_params=params, dry_run=dry_run), )

    @staticmethod
    def _parse_matrix_json(response):
        if response is None:  # pragma: no cover
            return Matrix()
        durations = response.get('times')
        distances = response.get('distances')

        return Matrix(durations=durations, distances=distances, raw=response)
