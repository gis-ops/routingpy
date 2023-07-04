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
from typing import List, Optional, Union  # noqa: F401

from .. import convert, utils
from ..client_base import DEFAULT
from ..client_default import Client
from ..direction import Direction, Directions
from ..isochrone import Isochrone, Isochrones


class OpenTripPlannerV2:
    """Performs requests over OpenTripPlannerV2 GraphQL API."""

    _DEFAULT_BASE_URL = "http://localhost:8080"

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = _DEFAULT_BASE_URL,
        user_agent: Optional[str] = None,
        timeout: Optional[int] = DEFAULT,
        retry_timeout: Optional[int] = None,
        retry_over_query_limit: Optional[bool] = False,
        skip_api_error: Optional[bool] = None,
        client=Client,
        **client_kwargs,
    ):
        """
        Initializes an OpenTripPlannerV2 client.

        :param api_key: NOT USED, only for compatibility with other providers.

        :param base_url: The base URL for the request. Defaults to localhost. Should not have a
            trailing slash.
        :type base_url: str

        :param user_agent: User Agent to be used when requesting.
            Default :attr:`routingpy.routers.options.default_user_agent`.
        :type user_agent: str

        :param timeout: Combined connect and read timeout for HTTP requests, in seconds.
            Specify ``None`` for no timeout.
            Default :attr:`routingpy.routers.options.default_timeout`.
        :type timeout: int or None

        :param retry_timeout: Timeout across multiple retriable requests, in seconds.
            Default :attr:`routingpy.routers.options.default_retry_timeout`.
        :type retry_timeout: int

        :param retry_over_query_limit: If True, client will not raise an exception on HTTP 429,
            but instead jitter a sleeping timer to pause between requests until HTTP 200 or
            retry_timeout is reached.
            Default :attr:`routingpy.routers.options.default_retry_over_query_limit`.
        :type retry_over_query_limit: bool

        :param skip_api_error: Continue with batch processing if a
            :class:`routingpy.exceptions.RouterApiError` is encountered (e.g. no route found).
            If False, processing will discontinue and raise an error.
            Default :attr:`routingpy.routers.options.default_skip_api_error`.
        :type skip_api_error: bool

        :param client: A client class for request handling. Needs to be derived from
            :class:`routingpy.client_base.BaseClient`
        :type client: abc.ABCMeta

        :param client_kwargs: Additional arguments passed to the client, such as headers or proxies.
        :type client_kwargs: dict
        """

        self.client = client(
            base_url,
            user_agent,
            timeout,
            retry_timeout,
            retry_over_query_limit,
            skip_api_error,
            **client_kwargs,
        )

    def directions(
        self,
        locations: List[List[float]],
        profile: str,
        num_itineraries: Optional[int] = 1,
        dry_run: Optional[bool] = None,
    ):
        """
        Get directions between an origin point and a destination point.

        :param locations: The coordinates tuple the route should be calculated from in order of
            visit.
        :type locations: list of list

        :param profile: Specifies the mode of transport to use when calculating directions. Possible
            values are "CAR", "BICYCLE", "TRANSIT", "WALK". For more profiles, see
            OpenTripPlannerV2's GraphiQL documentation.
        :type profile: str

        :param num_itineraries: The maximum number of itineraries to be returned. Default 1.
        :type num_itineraries: int

        :param dry_run: Print URL and parameters without sending the request.
        :type dry_run: bool

        :returns: One or multiple route(s) from provided coordinates and restrictions.
        :rtype: :class:`routingpy.direction.Direction` or :class:`routingpy.direction.Directions`
        """
        query = f"""
            {{
                plan(
                    from: {{lat: {locations[0][1]}, lon: {locations[0][0]}}}
                    to: {{lat: {locations[1][1]}, lon: {locations[1][0]}}}
                    transportModes: [{{mode: {profile}}}]
                    numItineraries: {num_itineraries}
                ) {{
                    itineraries {{
                        duration
                        legs {{
                            duration
                            distance
                            legGeometry {{
                                points
                            }}
                        }}
                    }}
                }}
            }}
        """
        params = {"query": query}
        response = self.client._request(
            "/otp/routers/default/index/graphql", post_params=params, dry_run=dry_run
        )
        return self._parse_directions_response(response, num_itineraries)

    def _parse_directions_response(self, response, num_itineraries):
        routes = []
        for itinerary in response["data"]["plan"]["itineraries"]:
            geometry, distance = self._parse_legs(itinerary["legs"])
            routes.append(
                Direction(
                    geometry=geometry,
                    duration=int(itinerary["duration"]),
                    distance=distance,
                    raw=itinerary,
                )
            )

        if num_itineraries > 1:
            return Directions(routes, raw=response)

        elif routes:
            return routes[0]

        else:
            return Direction()

    def _parse_legs(self, legs):
        distance = 0
        geometry = []
        for leg in legs:
            points = utils.decode_polyline5(leg["legGeometry"]["points"])
            geometry.extend(points)
            distance += int(leg["distance"])

        return geometry, distance

    def isochrones(
        self,
        locations: List[float],
        profile: str,
        intervals: List[int],
        location_type: Optional[str] = "start",
        dry_run: Optional[bool] = None,
    ):
        """Gets isochrones for a range of time values around a given set of coordinates.

        :param locations: One pair of lng/lat values.
        :type locations: list of float

        :param profile: Specifies the mode of transport to use when calculating directions. Possible
            values are "CAR", "BICYCLE", "TRANSIT", "WALK". For more profiles, see OpenTripPlannerV2's
            GraphiQL documentation.
        :type profile: str

        :param intervals: Ranges to calculate distances/durations for. This can be a list of
            multiple ranges, e.g. [600, 1200, 1400]. In seconds.
        :type intervals: list of int

        :param location_type: 'start' treats the location(s) as starting point, 'destination' as
            goal. Default 'start'.
        :type location_type: str

        :param dry_run: Print URL and parameters without sending the request.
        :param dry_run: bool

        :returns: An isochrone with the specified range.
        :rtype: :class:`routingpy.isochrone.Isochrones`
        """
        params = [
            ("location", convert.delimit_list(reversed(locations), ",")),
            ("mode", profile),
            ("arriveBy", "false" if location_type == "start" else "true"),
        ]
        for interval in intervals:
            params.append(("cutoff", convert.seconds_to_iso8601(interval)))

        response = self.client._request("/otp/traveltime/isochrone", get_params=params, dry_run=dry_run)
        return self._parse_isochrones_response(response)

    def _parse_isochrones_response(self, response):
        if response is None:  # pragma: no cover
            return Isochrones()

        isochrones = []
        for feature in response["features"]:
            isochrones.append(
                Isochrone(
                    geometry=feature["geometry"]["coordinates"][0],
                    interval=feature["properties"]["time"],
                    interval_type="time",
                )
            )

        return Isochrones(isochrones=isochrones, raw=response)

    def matrix(self):  # pragma: no cover
        raise NotImplementedError
