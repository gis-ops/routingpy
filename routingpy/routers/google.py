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

from ..client_base import DEFAULT
from ..client_default import Client
from .. import convert, utils
from ..direction import Directions, Direction
from ..matrix import Matrix
from ..exceptions import RouterApiError, RouterServerError, OverQueryLimit

from operator import itemgetter

STATUS_CODES = {
    "NOT_FOUND": {
        "code": 404,
        "message": "At least one of the locations specified in the request's origin, destination, or waypoints could not be geocoded.",
    },
    "ZERO_RESULTS": {
        "code": 404,
        "message": "No route could be found between the origin and destination.",
    },
    "MAX_WAYPOINTS_EXCEEDED": {
        "code": 413,
        "message": "Too many waypoints were provided in the request. The maximum is 25 excluding the origin and destination points.",
    },
    "MAX_ROUTE_LENGTH_EXCEEDED": {
        "code": 413,
        "message": "The requested route is too long and cannot be processed.",
    },
    "INVALID_REQUEST": {
        "code": 400,
        "message": "The provided request is invalid. Please check your parameters or parameter values.",
    },
    "OVER_DAILY_LIMIT": {
        "code": 429,
        "message": "This may be caused by an invalid API key, or billing issues.",
    },
    "OVER_QUERY_LIMIT": {
        "code": 429,
        "message": "The service has received too many requests from your application within the allowed time period.",
    },
    "REQUEST_DENIED": {
        "code": 403,
        "message": "The service denied use of the directions service by your application.",
    },
    "UNKNOWN_ERROR": {
        "code": 503,
        "message": "The directions request could not be processed due to a server error. The request may succeed if you try again.",
    },
}


class Google:
    """Performs requests to the Google API services."""

    _base_url = "https://maps.googleapis.com/maps/api"

    def __init__(
        self,
        api_key,
        user_agent=None,
        timeout=DEFAULT,
        retry_timeout=None,
        retry_over_query_limit=True,
        skip_api_error=None,
        client=Client,
        **client_kwargs
    ):
        """
        Initializes a Google client.

        :param api_key: API key.
        :type api_key: str

        :param user_agent: User Agent to be used when requesting.
            Default :attr:`routingpy.routers.options.default_user_agent`.
        :type user_agent: str

        :param timeout: Combined connect and read timeout for HTTP requests, in
            seconds. Specify ``None`` for no timeout. Default :attr:`routingpy.routers.options.default_timeout`.
        :type timeout: int or None

        :param retry_timeout: Timeout across multiple retriable requests, in
            seconds.  Default :attr:`routingpy.routers.options.default_retry_timeout`.
        :type retry_timeout: int

        :param retry_over_query_limit: If True, client will not raise an exception
            on HTTP 429, but instead jitter a sleeping timer to pause between
            requests until HTTP 200 or retry_timeout is reached.
            Default :attr:`routingpy.routers.options.default_over_query_limit`.
        :type retry_over_query_limit: bool

        :param skip_api_error: Continue with batch processing if a :class:`routingpy.exceptions.RouterApiError` is
            encountered (e.g. no route found). If False, processing will discontinue and raise an error.
            Default :attr:`routingpy.routers.options.default_skip_api_error`.
        :type skip_api_error: bool

        :param client: A client class for request handling. Needs to be derived from :class:`routingpy.base.BaseClient`
        :type client: abc.ABCMeta

        :param **client_kwargs: Additional arguments passed to the client, such as headers or proxies.
        :type **client_kwargs: dict
        """

        self.key = api_key

        self.client = client(
            self._base_url,
            user_agent,
            timeout,
            retry_timeout,
            retry_over_query_limit,
            skip_api_error,
            **client_kwargs
        )

    class WayPoint(object):
        """
        TODO: make the WayPoint class and its parameters appear in Sphinx. True for Valhalla as well.

        Optionally construct a waypoint from this class with additional attributes.

        Example:

        >>> waypoint = Google.WayPoint(position=[8.15315, 52.53151], waypoint_type='coords', stopover=False)
        >>> route = Google(api_key).directions(locations=[[[8.58232, 51.57234]], waypoint, [7.15315, 53.632415]])
        """

        def __init__(self, position, waypoint_type="coords", stopover=True):
            """
            Constructs a waypoint with additional information, such as via or encoded lines.

            :param position: Coordinates in [long, lat] order.
            :type position: list/tuple of float

            :param waypoint_type: The type of information provided. One of ['place_id', 'enc', 'coords']. Default 'coords'.
            :type waypoint_type: str

            :param stopover: If True, the waypoint will be used to add an additional leg to the journey. If False,
                it's only used as a via waypoint. Not supported for first and last waypoint. Default True.
            :type stopover: bool
            """

            self.position = position
            self.waypoint_type = waypoint_type
            self.stopover = stopover

        def make_waypoint(self):

            waypoint = ""
            if self.waypoint_type == "coords":
                waypoint += convert.delimit_list(list(reversed(self.position)))
            elif self.waypoint_type == "place_id":
                waypoint += self.waypoint_type + ":" + self.position
            elif self.waypoint_type == "enc":
                waypoint += self.waypoint_type + ":" + self.position + ":"
            else:
                raise ValueError("waypoint_type only supports enc, place_id, coords")

            if not self.stopover:
                waypoint = "via:" + waypoint

            return waypoint

    def directions(  # noqa: C901
        self,
        locations,
        profile,
        alternatives=None,
        avoid=None,
        optimize=None,
        language=None,
        region=None,
        units=None,
        arrival_time=None,
        departure_time=None,
        traffic_model=None,
        transit_mode=None,
        transit_routing_preference=None,
        dry_run=None,
    ):
        """Get directions between an origin point and a destination point.

        For more information, visit https://developers.google.com/maps/documentation/directions/intro.

        :param locations: The coordinates tuple the route should be calculated
            from in order of visit. Can be a list/tuple of [lon, lat], a list/tuple of address strings, Google's
            Place ID's, a :class:`Google.WayPoint` instance or a combination of these. Note, the first and last location have to be specified as [lon, lat].
            Optionally, specify ``optimize=true`` for via waypoint optimization.
        :type locations: list of list or list of :class:`Google.WayPoint`

        :param profile: The vehicle for which the route should be calculated.
            Default "driving". One of ['driving', 'walking', 'bicycling', 'transit'].
        :type profile: str

        :param alternatives: Specifies whether more than one route should be returned.
            Only available for requests without intermediate waypoints. Default False.
        :type alternatives: bool

        :param avoid: Indicates that the calculated route(s) should avoid the indicated features. One or more of
            ['tolls', 'highways', 'ferries', 'indoor']. Default None.
        :type avoid: list of str

        :param optimize: Optimize the given order of via waypoints (i.e. between first and last location). Default False.
        :type optimize: bool

        :param language: Language for routing instructions. The locale of the resulting turn instructions. Visit
            https://developers.google.com/maps/faq#languagesupport for options.
        :type language: str

        :param region: Specifies the region code, specified as a ccTLD ("top-level domain") two-character value.
            See https://developers.google.com/maps/documentation/directions/intro#RegionBiasing.
        :type region: str

        :param units: Specifies the unit system to use when displaying results. One of ['metric', 'imperial'].
        :type units: str

        :param arrival_time: Specifies the desired time of arrival for transit directions, in seconds since midnight,
            January 1, 1970 UTC. Incompatible with departure_time.
        :type arrival_time: int

        :param departure_time: Specifies the desired time of departure. You can specify the time as an integer in
            seconds since midnight, January 1, 1970 UTC.

        :param traffic_model: Specifies the assumptions to use when calculating time in traffic. One of ['best_guess',
            'pessimistic', 'optimistic'. See https://developers.google.com/maps/documentation/directions/intro#optional-parameters
            for details.
        :type traffic_model: str

        :param transit_mode: Specifies one or more preferred modes of transit. One or more of ['bus', 'subway', 'train',
            'tram', 'rail'].
        :type transit_mode: list/tuple of str

        :param transit_routing_preference: Specifies preferences for transit routes. Using this parameter, you can bias
            the options returned, rather than accepting the default best route chosen by the API. One of ['less_walking',
            'fewer_transfers'].
        :type transit_routing_preference: str

        :param dry_run: Print URL and parameters without sending the request.
        :type dry_run: bool

        :returns: One or multiple route(s) from provided coordinates and restrictions.
        :rtype: :class:`routingpy.direction.Direction` or :class:`routingpy.direction.Directions`
        """

        params = {"mode": profile}

        origin, destination = locations[0], locations[-1]
        if isinstance(origin, (list, tuple)):
            params["origin"] = convert.delimit_list(list(reversed(origin)))
        elif isinstance(origin, self.WayPoint):
            raise TypeError("The first and last locations must be list/tuple of [lon, lat]")

        if isinstance(destination, (list, tuple)):
            params["destination"] = convert.delimit_list(list(reversed(destination)))
        elif isinstance(origin, self.WayPoint):
            raise TypeError("The first and last locations must be list/tuple of [lon, lat]")

        if len(locations) > 2:
            waypoints = []
            s = slice(1, -1)
            for coord in locations[s]:
                if isinstance(coord, (list, tuple)):
                    waypoints.append(convert.delimit_list(list(reversed(coord))))
                elif isinstance(coord, self.WayPoint):
                    waypoints.append(coord.make_waypoint())
            if optimize:
                waypoints.insert(0, "optimize:true")

            params["waypoints"] = convert.delimit_list(waypoints, "|")

        if self.key is not None:
            params["key"] = self.key

        if alternatives is not None:
            params["alternatives"] = convert.convert_bool(alternatives)

        if avoid:
            params["avoid"] = convert.delimit_list(avoid, "|")

        if language:
            params["language"] = language

        if region:
            params["region"] = region

        if units:
            params["units"] = units

        if arrival_time and departure_time:
            raise ValueError("Specify either arrival_time or departure_time.")

        if arrival_time:
            params["arrival_time"] = str(arrival_time)

        if departure_time:
            params["departure_time"] = str(departure_time)

        if traffic_model:
            params["traffic_model"] = traffic_model

        if transit_mode:
            params["transit_mode"] = convert.delimit_list(transit_mode, "|")

        if transit_routing_preference:
            params["transit_routing_preference"] = transit_routing_preference

        return self._parse_direction_json(
            self.client._request("/directions/json", get_params=params, dry_run=dry_run), alternatives
        )

    @staticmethod
    def _parse_direction_json(response, alternatives):
        if response is None:  # pragma: no cover
            if alternatives:
                return Directions()
            else:
                return Direction()

        status = response["status"]

        if status in STATUS_CODES.keys():
            if status == "UNKNOWN_ERROR":
                error = RouterServerError

            elif status in ["OVER_QUERY_LIMIT", "OVER_DAILY_LIMIT"]:
                error = OverQueryLimit

            else:
                error = RouterApiError

            raise error(STATUS_CODES[status]["code"], STATUS_CODES[status]["message"])

        if alternatives:
            routes = []
            for route in response["routes"]:
                geometry = []
                duration, distance = 0, 0
                for leg in route["legs"]:
                    duration += leg["duration"]["value"]
                    distance += leg["distance"]["value"]
                    for step in leg["steps"]:
                        geometry.extend(utils.decode_polyline5(step["polyline"]["points"]))

                routes.append(
                    Direction(
                        geometry=geometry, duration=int(duration), distance=int(distance), raw=route
                    )
                )
            return Directions(routes, response)
        else:
            geometry = []
            duration, distance = 0, 0
            for leg in response["routes"][0]["legs"]:
                duration = int(leg["duration"]["value"])
                distance = int(leg["distance"]["value"])
                for step in leg["steps"]:
                    geometry.extend(
                        [
                            list(reversed(coords))
                            for coords in utils.decode_polyline5(step["polyline"]["points"])
                        ]
                    )
            return Direction(geometry=geometry, duration=duration, distance=distance, raw=response)

    def isochrones(self):  # pragma: no cover
        raise NotImplementedError

    def matrix(  # noqa: C901
        self,
        locations,
        profile,
        sources=None,
        destinations=None,
        avoid=None,
        language=None,
        region=None,
        units=None,
        arrival_time=None,
        departure_time=None,
        traffic_model=None,
        transit_mode=None,
        transit_routing_preference=None,
        dry_run=None,
    ):
        """Gets travel distance and time for a matrix of origins and destinations.

        :param locations: Two or more pairs of lng/lat values.
        :type locations: list of list

        :param profile: The vehicle for which the route should be calculated.
            Default "driving". One of ['driving', 'walking', 'bicycling', 'transit'].
        :type profile: str

        :param sources: A list of indices that refer to the list of locations
            (starting with 0). If not passed, all indices are considered.
        :type sources: list or tuple

        :param destinations: A list of indices that refer to the list of locations
            (starting with 0). If not passed, all indices are considered.
        :type destinations: list or tuple

        :param avoid: Indicates that the calculated route(s) should avoid the indicated features. One or more of
            ['tolls', 'highways', 'ferries', 'indoor']. Default None.
        :param avoid: list of str

        :param language: Language for routing instructions. The locale of the resulting turn instructions. Visit
            https://developers.google.com/maps/faq#languagesupport for options.
        :type language: str

        :param region: Specifies the region code, specified as a ccTLD ("top-level domain") two-character value.
            See https://developers.google.com/maps/documentation/directions/intro#RegionBiasing.
        :type region: str

        :param units: Specifies the unit system to use when displaying results. One of ['metric', 'imperial'].
        :type units: str

        :param arrival_time: Specifies the desired time of arrival for transit directions, in seconds since midnight,
            January 1, 1970 UTC. Incompatible with departure_time.
        :type arrival_time: int

        :param departure_time: Specifies the desired time of departure. You can specify the time as an integer in
            seconds since midnight, January 1, 1970 UTC.
        :type departure_time: int

        :param traffic_model: Specifies the assumptions to use when calculating time in traffic. One of ['best_guess',
            'pessimistic', 'optimistic'. See https://developers.google.com/maps/documentation/directions/intro#optional-parameters
            for details.
        :type traffic_model: str

        :param transit_mode: Specifies one or more preferred modes of transit. One or more of ['bus', 'subway', 'train',
            'tram', 'rail'].
        :type transit_mode: list of str or tuple of str

        :param transit_routing_preference: Specifies preferences for transit routes. Using this parameter, you can bias
            the options returned, rather than accepting the default best route chosen by the API. One of ['less_walking',
            'fewer_transfers'].
        :type transit_routing_preference: str

        :param dry_run: Print URL and parameters without sending the request.
        :param dry_run: bool

        :returns: A matrix from the specified sources and destinations.
        :rtype: :class:`routingpy.matrix.Matrix`
        """
        params = {"mode": profile}

        waypoints = []
        for coord in locations:
            if isinstance(coord, (list, tuple)):
                waypoints.append(convert.delimit_list(list(reversed(coord))))
            elif isinstance(coord, self.WayPoint):
                waypoints.append(coord.make_waypoint())

        sources_coords = waypoints
        if sources is not None:
            sources_coords = itemgetter(*sources)(sources_coords)
            if not isinstance(sources_coords, (list, tuple)):
                sources_coords = [sources_coords]
        params["origins"] = convert.delimit_list(sources_coords, "|")

        destinations_coords = waypoints
        if destinations is not None:
            destinations_coords = itemgetter(*destinations)(destinations_coords)
            if not isinstance(destinations_coords, (list, tuple)):
                destinations_coords = [destinations_coords]
        params["destinations"] = convert.delimit_list(destinations_coords, "|")

        if self.key is not None:
            params["key"] = self.key

        if avoid:
            params["avoid"] = convert.delimit_list(avoid, "|")

        if language:
            params["language"] = language

        if region:
            params["region"] = region

        if units:
            params["units"] = units

        if arrival_time:
            params["arrival_time"] = str(arrival_time)

        if departure_time:
            params["departure_time"] = str(departure_time)

        if traffic_model:
            params["traffic_model"] = traffic_model

        if transit_mode:
            params["transit_mode"] = convert.delimit_list(transit_mode, "|")

        if transit_routing_preference:
            params["transit_routing_preference"] = transit_routing_preference

        return self._parse_matrix_json(
            self.client._request("/distancematrix/json", get_params=params, dry_run=dry_run)
        )

    @staticmethod
    def _parse_matrix_json(response):
        if response is None:  # pragma: no cover
            return Matrix()

        durations = [
            [destination["duration"]["value"] for destination in origin["elements"]]
            for origin in response["rows"]
        ]
        distances = [
            [destination["distance"]["value"] for destination in origin["elements"]]
            for origin in response["rows"]
        ]

        return Matrix(durations, distances, response)
