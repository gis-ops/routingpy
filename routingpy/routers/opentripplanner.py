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
from datetime import datetime
from typing import List, Union, Optional

from routingpy.client_default import Client
from routingpy.exceptions import RouterApiError
from routingpy.isochrone import Isochrone, Isochrones


class OpenTripPlanner:
    def __init__(
        self,
        base_url: str,
        client=Client,
        router_id="default",
        **client_kwargs,
    ):
        """
        Initializes a OpenTripPlanner client.

        Additional keyword arguments are derived from :class:`routingpy.base.BaseClient`:

        user_agent: User Agent to be used when requesting.
            Default :attr:`routingpy.routers.options.default_user_agent`.

        timeout: Combined connect and read timeout for HTTP requests, in
            seconds. Specify ``None`` for no timeout. Default :attr:`routingpy.routers.options.default_timeout`.

        retry_timeout: Timeout across multiple retriable requests, in
            seconds.  Default :attr:`routingpy.routers.options.default_retry_timeout`.

        retry_over_query_limit: If True, client will not raise an exception
            on HTTP 429, but instead jitter a sleeping timer to pause between
            requests until HTTP 200 or retry_timeout is reached.
            Default :attr:`routingpy.routers.options.default_retry_over_query_limit`.

        skip_api_error: Continue with batch processing if a :class:`routingpy.exceptions.RouterApiError` is
            encountered (e.g. no route found). If False, processing will discontinue and raise an error.
            Default :attr:`routingpy.routers.options.default_skip_api_error`.

        :param router_id: The registered router ID. Default 'default'.
        :param base_url: The base URL for the request. Defaults to the ORS API
            server. Should not have a trailing slash.
        :param client: A client class for request handling. Needs to be derived from :class:`routingpy.base.BaseClient`
        :param **client_kwargs: Additional arguments passed to the client, see description.
        """

        self.router_id = router_id
        self.client = client(
            base_url,
            **client_kwargs,
        )

    def isochrones(
        self,
        locations: List[float],
        intervals: List[int],
        profiles: Optional[Union[str, List[str]]] = None,
        date_time: datetime = None,
        arrive_by: bool = False,  # TODO: check whether param makes sense (if so, keep in mind that toPlace must be specified)
        bike_speed: Optional[float] = None,
        max_time_sec: Optional[int] = None,
        walk_speed: Optional[float] = None,
        transfer_penalty: Optional[int] = None,
        wheelchair: bool = None,
        max_walk_distance: Optional[float] = None,
        min_transfer_time: Optional[int] = None,
        dry_run: bool = None,
    ) -> Isochrones:

        get_params = self.get_isochrone_params(
            locations,
            profiles,
            intervals,
            date_time,
            arrive_by,
            bike_speed,
            max_time_sec,
            walk_speed,
            transfer_penalty,
            wheelchair,
            max_walk_distance,
            min_transfer_time,
        )

        return self.parse_isochrone_json(
            self.client._request(
                f"/otp/routers/{self.router_id}/isochrone", get_params=get_params, dry_run=dry_run
            ),
            intervals,
            locations,
        )

    @staticmethod
    def get_isochrone_params(
        locations,
        profile,
        intervals,
        date_time,
        arrive_by,
        bike_speed,
        max_time_sec,
        walk_speed,
        transfer_penalty,
        wheelchair,
        max_walk_distance,
        min_transfer_time,
    ):
        locations = list(reversed(locations))

        params = [
            ("fromPlace", locations),
            ("toPlace", locations),
            *[("cutoffSec", interval) for interval in intervals],
        ]

        if profile:
            profiles = profile if isinstance(profile, str) else ",".join(profile)
            params.append(("mode", profiles))
        if date_time:
            params.append(("date", date_time.strftime("%m-%d-%Y")))
            params.append(("time", date_time.strftime("%I:%m%p")))
        if arrive_by:
            params.append(("arriveBy", arrive_by))
        if bike_speed:
            params.append(("bikeSpeed", bike_speed))
        if max_time_sec:
            params.append(("maxTimeSec", max_time_sec))
        if walk_speed:
            params.append(("walkSpeed", walk_speed))
        if transfer_penalty:
            params.append(("transferPenalty", transfer_penalty))
        if wheelchair:
            params.append(("wheelchair", wheelchair))
        if max_walk_distance:
            params.append(("maxWalkDistance", max_walk_distance))
        if min_transfer_time:
            params.append(("minTransferTime", min_transfer_time))

        return params

    @staticmethod
    def parse_isochrone_json(response, intervals, locations):
        if response is None:
            return Isochrones()

        isochrones = []
        for idx, feature in enumerate(response["features"]):
            # some queries give a 200, but don't have any features
            if not feature["geometry"]:
                raise RouterApiError(400, "No isochrone found for profile and parameters")

            isochrones.append(
                Isochrone(
                    geometry=feature["geometry"]["coordinates"],
                    interval=intervals[idx],
                    center=locations,
                )
            )

        return Isochrones(isochrones, "Polygon", response)
