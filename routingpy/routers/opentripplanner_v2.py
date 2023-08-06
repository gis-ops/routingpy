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
import abc
import datetime
from typing import List, Optional

from .. import convert, utils
from ..client_base import DEFAULT
from ..client_default import Client
from ..direction import Direction, Directions
from ..isochrone import Isochrone, Isochrones
from ..raster import Raster


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
        client: abc.ABCMeta = Client,
        **client_kwargs,
    ):
        """
        Initializes an OpenTripPlannerV2 client.

        :param base_url: The base URL for the request. Defaults to localhost. Should not have a
            trailing slash.
        :param user_agent: User Agent to be used when requesting.
            Default :attr:`routingpy.routers.options.default_user_agent`.
        :param timeout: Combined connect and read timeout for HTTP requests, in seconds.
            Specify ``None`` for no timeout.
            Default :attr:`routingpy.routers.options.default_timeout`.
        :param retry_timeout: Timeout across multiple retriable requests, in seconds.
            Default :attr:`routingpy.routers.options.default_retry_timeout`.
        :param retry_over_query_limit: If True, client will not raise an exception on HTTP 429,
            but instead jitter a sleeping timer to pause between requests until HTTP 200 or
            retry_timeout is reached.
            Default :attr:`routingpy.routers.options.default_retry_over_query_limit`.
        :param skip_api_error: Continue with batch processing if a
            :class:`routingpy.exceptions.RouterApiError` is encountered (e.g. no route found).
            If False, processing will discontinue and raise an error.
            Default :attr:`routingpy.routers.options.default_skip_api_error`.
        :param client: A client class for request handling. Needs to be derived from
            :class:`routingpy.client_base.BaseClient`
        :param client_kwargs: Additional arguments passed to the client, such as headers or proxies.
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
        profile: Optional[str],
        date_time: Optional[datetime.datetime] = datetime.datetime.now(datetime.timezone.utc),
        date_time_type: Optional[str] = "depart_at",
        num_itineraries: Optional[int] = 3,
        dry_run: Optional[bool] = None,
    ):
        """
        Get directions between an origin point and a destination point.

        :param locations: List of coordinates for departure and arrival points as
            [[lon,lat], [lon,lat]].
        :param profile: Comma-separated list of transportation modes that the user is willing to
            use.
        :param date_time: Departure date and time (timezone aware). The default value is now (UTC).
        :param date_time_type: One of ["depart_at", "arrive_by"].. Default "depart_at".
        :param num_itineraries: The maximum number of itineraries to return. Default value: 3.
        :param dry_run: Print URL and parameters without sending the request.

        :returns: One or multiple route(s) from provided coordinates and restrictions.
        :rtype: :class:`routingpy.direction.Direction` or :class:`routingpy.direction.Directions`
        """
        transport_modes = [{"mode": mode} for mode in profile.strip().split(",")]
        query = f"""
            {{
                plan(
                    date: "{ date_time.date().strftime("%Y-%m-%d") }"
                    time: "{ date_time.time().strftime("%H:%M:%S") }"
                    from: {{lat: {locations[0][1]}, lon: {locations[0][0]}}}
                    to: {{lat: {locations[1][1]}, lon: {locations[1][0]}}}
                    transportModes: {str(transport_modes).replace("'", "")}
                    numItineraries: {num_itineraries}
                    arriveBy: {"true" if date_time_type == "depart_at" else "false"}
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
            departure_datetime = convert.timestamp_to_tz_datetime(itinerary["startTime"], "UTC")
            arrival_datetime = convert.timestamp_to_tz_datetime(itinerary["endTime"], "UTC")
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
        profile: str,
        intervals: List[int],
        interval_type: Optional[str] = None,
        date_time: Optional[datetime.datetime] = datetime.datetime.now(datetime.timezone.utc),
        date_time_type: Optional[str] = None,
        arrive_by: Optional[bool] = False,
        dry_run: Optional[bool] = None,
    ):
        """Gets isochrones for a range of time values around a given set of coordinates.

        :param locations: Origin of the search as [lon,lat].
        :param profile: Comma-separated list of transportation modes that the user is willing to use.
        :param intervals: Time ranges to calculate isochrones for. In seconds or meters, depending on `interval_type`.
        :param interval_type: Only for compatibility. This isn't used, only 'time' is allowed.
        :param date_time: Departure date and time (timezone aware). The default value is now (UTC).
        :param date_time_type: Only for compatibility. This isn't used, only "depart_at" isochrones are allowed.
        :arrive_by: Set to False when searching from the location and True when searching to the
            location. Default value: False.
        :param dry_run: Print URL and parameters without sending the request.

        :returns: An isochrone with the specified range.
        :rtype: :class:`routingpy.isochrone.Isochrones`
        """
        params = [
            ("location", convert.delimit_list(reversed(locations), ",")),
            ("time", date_time.isoformat()),
            ("modes", profile),
            ("arriveBy", "true" if arrive_by else "false"),
        ]
        for cutoff in intervals:
            params.append(("cutoff", convert.seconds_to_iso8601(cutoff)))

        response = self.client._request(
            "/otp/traveltime/isochrone",
            get_params=params,
            dry_run=dry_run,
        )
        return self.parse_isochrones_response(response)

    @staticmethod
    def parse_isochrones_response(response):
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
        profile: Optional[str],
        date_time: Optional[datetime.datetime] = datetime.datetime.now(datetime.timezone.utc),
        date_time_type: Optional[str] = None,
        cutoff: Optional[int] = 3600,
        dry_run: Optional[bool] = None,
    ):
        """Get raster for a time value around a given set of coordinates.

        :param locations: Origin of the search as [lon,lat].
        :type locations: list of float

        :param profile: Comma-separated list of transportation modes that the user is willing to
            use.
        :param date_time: Date and time of departure or arrival. Default value: current datetime.
        :param date_time_type: One of ["depart_at", "arrive_by"].. Default "depart_at".
        :param cutoff: The maximum travel duration in seconds. The default value is one hour.
        :param dry_run: Print URL and parameters without sending the request.

        :returns: A raster with the specified range.
        :rtype: :class:`routingpy.raster.Raster`
        """
        params = [
            ("location", convert.delimit_list(reversed(locations), ",")),
            ("time", date_time.isoformat()),
            ("modes", profile),
            ("arriveBy", "true" if date_time_type == "arrive_by" else "false"),
            ("cutoff", convert.seconds_to_iso8601(cutoff)),
        ]
        response = self.client._request(
            "/otp/traveltime/surface",
            get_params=params,
            dry_run=dry_run,
        )
        return self.parse_rasters_response(response, cutoff)

    @staticmethod
    def parse_rasters_response(response, max_travel_time):
        if response is None:  # pragma: no cover
            return Raster()

        return Raster(image=response, max_travel_time=max_travel_time)

    def matrix(self):  # pragma: no cover
        raise NotImplementedError
