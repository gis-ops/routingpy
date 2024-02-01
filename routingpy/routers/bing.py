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

from typing import List, Optional

from .. import convert
from ..client_base import DEFAULT
from ..client_default import Client
from ..direction import Direction, Directions

class Bing:
    """Performs requests to the Bing Maps API."""

    _base_url = "http://dev.virtualearth.net/REST/V1/Routes/Driving"

    def __init__(
        self,
        api_key: str,
        user_agent: Optional[str] = None,
        timeout: Optional[int] = DEFAULT,
        retry_timeout: Optional[int] = None,
        retry_over_query_limit=True,
        skip_api_error: Optional[bool] = None,
        client=Client,
        **client_kwargs
    ):
        """
        Initializes a Bing client.

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

        :param client: A client class for request handling. Needs to be derived from :class:`routingpy.client_base.BaseClient`
        :type client: abc.ABCMeta

        :param client_kwargs: Additional arguments passed to the client, such as headers or proxies.
        :type client_kwargs: dict
        """

        self.api_key = api_key

        self.client = client(
            self._base_url,
            user_agent,
            timeout,
            retry_timeout,
            retry_over_query_limit,
            skip_api_error,
            **client_kwargs
        )

    def directions(  # noqa: C901
        self,
        locations: List[List[float]],
        o: Optional[str] = None,
        avoid: Optional[str] = None,
        distanceBeforeFirstTurn: Optional[str] = None,
        heading: Optional[str] = None,
        optimize: Optional[str] = None,
        optimizeWaypoints: Optional[str] = None,
        routeAttributes: Optional[str] = None,
        routePathOutput: Optional[str] = None,
        tolerances: Optional[str] = None,
        distanceUnit: Optional[str] = None,
        dateTime: Optional[str] = None,
        timeType: Optional[str] = None,
        maxSolutions: Optional[str] = None,
        travelMode: Optional[str] = None,
        itineraryGroups: Optional[str] = None,
        dry_run: Optional[bool] = None
    ):
        """
        Get directions between an origin point and a destination point.

        For more information, visit https://learn.microsoft.com/en-us/bingmaps/rest-services/routes/calculate-a-route
        """

        params = {}

        """
        The API Key, which is needed to make requests to the Bing Maps services.	
        """
        params["key"] = self.key

        if len(locations) > 2:
            for i, l in enumerate(locations):
                params["wp."+str(i)] = convert.delimit_list(l)
        else:
            origin, destination = locations[0], locations[-1]
            if isinstance(origin, (list, tuple)):
                params["wp.0"] = convert.delimit_list(origin)
            
            if isinstance(destination, (list, tuple)):
                params["wp.1"] = convert.delimit_list(destination)

        if o:
            """
            A JSON response is provided by default, unless you request a XML response by setting this parameter.
            """
            params["o"] = o

        if avoid:
            """
            Specifies the road types to minimize or avoid when a route is created for the driving travel mode.
            """
            params["avoid"] = avoid
        
        if distanceBeforeFirstTurn:
            """
            Specifies the distance before the first turn is allowed in the route. This option only applies to the driving travel mode.
            """
            params["distanceBeforeFirstTurn"] = distanceBeforeFirstTurn
        
        if heading:
            """
            Specifies the initial heading for the route.
            """
            params["heading"] = heading

        if optimize:
            """
            Specifies what parameters to use to optimize the route.
            """
            params["optimize"] = optimize

        if optimizeWaypoints:
            """
            Instructs the API to rearrange the route waypoints and reduce the route cost specified with the optimize parameter. The route first waypoint wp.0 and last waypoint wp.n order is not changed, their position is considered fixed.
            """
            params["optimizeWaypoints"] = optimizeWaypoints
        
        if routeAttributes:
            """
            Specify to include or exclude parts of the routes response.
            """
            params["routeAttributes"] = routeAttributes
        
        if routePathOutput:
            """
            Specifies whether the response should include information about Point (latitude and longitude) values for the route’s path.
            """
            params["routePathOutput"] = routePathOutput
              
        if tolerances:
            """
            Specifies a series of tolerance values. Each value produces a subset of points that approximates the route that is described by the full set of points.
            This parameter is only valid when the routePathOutput parameter is set to Points.
            """
            params["tolerances"] = tolerances
        
        if distanceUnit:
            """
            The units to use for distance in the response.
            """
            params["distanceUnit"] = distanceUnit

        if dateTime:
            """
            Required when the travel mode is Transit. The dateTime parameter identifies the desired transit time, such as arrival time or departure time. The transit time type is specified by the timeType parameter.
            Optional for Driving. When specified and the route is optimized for timeWithTraffic, predictive traffic data is used to calculate the best route for the specified date time.
            """
            params["dateTime"] = dateTime

        if timeType:
            """
            Required when the travel mode is Transit Specifies how to interpret the date and transit time value that is specified by the dateTime parameter.
            """
            params["timeType"] = timeType
        
        if maxSolutions:
            """
            Specifies the maximum number of transit or driving routes to return.
            """
            params["maxSolutions"] = maxSolutions

        if travelMode:
            """
            The mode of travel for the route.
            """
            params["travelMode"] = travelMode

        if itineraryGroups:
            """
            Specifies whether the response include information about itinerary groups (continuous itinerary items in same mode are usually grouped together).
            """
            params["itineraryGroups"] = itineraryGroups

        return self.parse_direction_json(self.client._request(self._base_url, get_params=params, dry_run=dry_run), optimize, routeAttributes, maxSolutions)

    @staticmethod
    def parse_direction_json(response, optimize, routeAttributes, maxSolutions):
        if response is None:  # pragma: no cover
            if maxSolutions:
                if int(maxSolutions) > 1:
                    return Directions()
            else:
                return Direction()

        if maxSolutions:
            if int(maxSolutions) > 1:
                # TODO
                pass
        else:
            distance = response["resourceSets"][0]["resources"][0]["travelDistance"]
            distance = round(distance * 1000) # From Km to m
            if optimize:
                if optimize == "timeWithTraffic":
                    duration = response["resourceSets"][0]["resources"][0]["travelDurationTraffic"]
            else:
                duration = response["resourceSets"][0]["resources"][0]["travelDuration"]
            if routeAttributes:
                if "routePath" in routeAttributes:
                    geometry = response["resourceSets"][0]["resources"][0]["routePath"]["line"]["coordinates"]
                    return Direction(geometry=geometry, duration=duration, distance=distance, raw=response)
            else:
                return Direction(duration=duration, distance=distance, raw=response)