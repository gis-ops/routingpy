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
import datetime
from typing import List, Optional

from .. import convert, utils
from ..client_base import DEFAULT
from ..client_default import Client
from ..direction import Direction, Directions
from ..isochrone import Isochrone, Isochrones
from ..raster import Raster
from ..utils import timestamp_to_utc_datetime


class OpenTripPlannerV2:
    """Performs requests over OpenTripPlannerV2 GraphQL API."""

    _DEFAULT_BASE_URL = "http://localhost:8080"

    def __init__(
        self,
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
        profile: Optional[str] = "WALK,TRANSIT",
        date: Optional[datetime.date] = datetime.datetime.now().date(),
        time: Optional[datetime.time] = datetime.datetime.now().time(),
        arrive_by: Optional[bool] = False,
        num_itineraries: Optional[int] = 3,
        dry_run: Optional[bool] = None,
    ):
        """
        Get directions between an origin point and a destination point.

        :param locations: List of coordinates for departure and arrival points as
            [[lon,lat], [lon,lat]].
        :type locations: list of list of float

        :param profile: Comma-separated list of transportation modes that the user is willing to
            use. Default: "WALK,TRANSIT"
        :type profile: str

        :param date: Date of departure or arrival. Default value: current date.
        :type date: datetime.date

        :param time: Time of departure or arrival. Default value: current time.
        :type time: datetime.time

        :arrive_by: Whether the itinerary should depart at the specified time (False), or arrive to
            the destination at the specified time (True). Default value: False.
        :type arrive_by: bool

        :param num_itineraries: The maximum number of itineraries to return. Default value: 3.
        :type num_itineraries: int

        :param dry_run: Print URL and parameters without sending the request.
        :type dry_run: bool

        :returns: One or multiple route(s) from provided coordinates and restrictions.
        :rtype: :class:`routingpy.direction.Direction` or :class:`routingpy.direction.Directions`
        """
        transport_modes = [{"mode": mode} for mode in profile.strip().split(",")]
        query = f"""
            {{
                plan(
                    date: "{ date.strftime("%Y-%m-%d") }"
                    time: "{ time.strftime("%H:%M:%S") }"
                    from: {{lat: {locations[0][1]}, lon: {locations[0][0]}}}
                    to: {{lat: {locations[1][1]}, lon: {locations[1][0]}}}
                    transportModes: {str(transport_modes).replace("'", "")}
                    numItineraries: {num_itineraries}
                    arriveBy: {"true" if arrive_by else "false"}
                ) {{
                    itineraries {{
                        duration
                        startTime
                        endTime
                        legs {{
                            startTime
                            endTime
                            duration
                            distance
                            mode
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
        return self.parse_directions_response(response, num_itineraries)

    @staticmethod
    def parse_directions_response(response, num_itineraries):
        if response is None:  # pragma: no cover
            return Directions() if num_itineraries > 1 else Direction()

        directions = []
        for itinerary in response["data"]["plan"]["itineraries"]:
            distance, geometry = OpenTripPlannerV2._parse_legs(itinerary["legs"])
            departure_datetime = timestamp_to_utc_datetime(itinerary["startTime"])
            arrival_datetime = timestamp_to_utc_datetime(itinerary["endTime"])
            directions.append(
                Direction(
                    geometry=geometry,
                    duration=int(itinerary["duration"]),
                    distance=distance,
                    departure_datetime=departure_datetime,
                    arrival_datetime=arrival_datetime,
                    raw=itinerary,
                )
            )

        if num_itineraries > 1:
            return Directions(directions, raw=response)

        elif directions:
            return directions[0]

    @staticmethod
    def _parse_legs(legs):
        distance = 0
        geometry = []
        for leg in legs:
            points = utils.decode_polyline5(leg["legGeometry"]["points"])
            geometry.extend(list(reversed(points)))
            distance += int(leg["distance"])

        return distance, geometry

    def isochrones(
        self,
        locations: List[float],
        profile: Optional[str] = "WALK,TRANSIT",
        time: Optional[datetime.datetime] = datetime.datetime.now(datetime.timezone.utc),
        cutoffs: Optional[List[int]] = [3600],
        arrive_by: Optional[bool] = False,
        dry_run: Optional[bool] = None,
    ):
        """Gets isochrones for a range of time values around a given set of coordinates.

        :param locations: Origin of the search as [lon,lat].
        :type locations: list of float

        :param profile: Comma-separated list of transportation modes that the user is willing to
            use. Default: "WALK,TRANSIT"
        :type profile: str

        :time: Departure date and time (timezone aware). The default value is now (UTC).
        :type time: datetime.datetime

        :cutoff: The maximum travel duration in seconds. The default value is one hour.

        :arrive_by: Set to False when searching from the location and True when searching to the
            location. Default value: False.
        :type arrive_by: bool

        :param dry_run: Print URL and parameters without sending the request.
        :param dry_run: bool

        :returns: An isochrone with the specified range.
        :rtype: :class:`routingpy.isochrone.Isochrones`
        """
        params = [
            ("location", convert.delimit_list(reversed(locations), ",")),
            ("time", time.isoformat()),
            ("modes", profile),
            ("arriveBy", "true" if arrive_by else "false"),
        ]
        for cutoff in cutoffs:
            params.append(("cutoff", convert.seconds_to_iso8601(cutoff)))

        response = self.client._request(
            "/otp/traveltime/isochrone",
            get_params=params,
            dry_run=dry_run,
        )
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

    def raster(
        self,
        locations: List[float],
        profile: Optional[str] = "WALK,TRANSIT",
        time: Optional[datetime.datetime] = datetime.datetime.now(),
        cutoff: Optional[int] = 3600,
        arrive_by: Optional[bool] = False,
        dry_run: Optional[bool] = None,
    ):
        """Get raster for a time value around a given set of coordinates.

        :param locations: Origin of the search as [lon,lat].
        :type locations: list of float

        :param profile: Comma-separated list of transportation modes that the user is willing to
            use. Default: "WALK,TRANSIT"
        :type profile: str

        :time: Departure date and time (timezone aware). The default value is now (UTC).
        :type time: datetime.datetime

        :cutoff: The maximum travel duration in seconds. The default value is one hour.

        :arrive_by: Set to False when searching from the location and True when searching to the
            location. Default value: False.
        :type arrive_by: bool

        :param dry_run: Print URL and parameters without sending the request.
        :param dry_run: bool

        :returns: A raster with the specified range.
        :rtype: :class:`routingpy.raster.Raster`
        """
        params = [
            ("location", convert.delimit_list(reversed(locations), ",")),
            ("time", time.isoformat()),
            ("modes", profile),
            ("arriveBy", "true" if arrive_by else "false"),
            ("cutoff", convert.seconds_to_iso8601(cutoff)),
        ]
        response = self.client._request(
            "/otp/traveltime/surface",
            get_params=params,
            dry_run=dry_run,
        )
        return self._parse_rasters_response(response, cutoff)

    def _parse_rasters_response(self, response, max_travel_time):
        if response is None:  # pragma: no cover
            return Raster()

        return Raster(image=response, max_travel_time=max_travel_time)

    def matrix(self):  # pragma: no cover
        raise NotImplementedError
