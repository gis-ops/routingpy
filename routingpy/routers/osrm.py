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
from routingpy import convert


class OSRM(Router):
    """Performs requests to the OSRM API services."""

    _DEFAULT_BASE_URL = 'https://router.project-osrm.org'

    def __init__(self,
                 base_url=_DEFAULT_BASE_URL,
                 user_agent=None,
                 timeout=None,
                 retry_timeout=None,
                 requests_kwargs=None,
                 retry_over_query_limit=False):
        """
        Initializes an OSRM client.

        :param base_url: The base URL for the request. Defaults to the OSRM demo API
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

        :param queries_per_minute: Number of queries per second permitted.
            If the rate limit is reached, the client will sleep for the
            appropriate amount of time before it runs the current query.
            Note, it won't help to initiate another client. This saves you the
            trouble of raised exceptions.
        :type queries_per_minute: int
        """

        super(OSRM,
              self).__init__(base_url, user_agent, timeout, retry_timeout,
                             requests_kwargs, retry_over_query_limit)

    def directions(self,
                   coordinates,
                   profile,
                   radiuses=None,
                   bearings=None,
                   alternatives=None,
                   steps=None,
                   continue_straight=None,
                   annotations=None,
                   geometries=None,
                   overview=None,
                   dry_run=None):
        """Get directions between an origin point and a destination point.

        For more information, visit http://project-osrm.org/docs/v5.5.1/api/#route-service.

        :param coordinates: The coordinates tuple the route should be calculated
            from in order of visit.
        :type coordinates: list, tuple

        :param profile: Specifies the mode of transport to use when calculating
            directions. One of ["car", "bike", "foot"].
        :type profile: str

        :param radiuses: A list of maximum distances (measured in
            meters) that limit the search of nearby road segments to every given waypoint.
            The values must be greater than 0, an empty element signifies to use the backend default
            radius. The number of radiuses must correspond to the number of waypoints.
        :type radiuses: list or tuple

        :param bearings: Specifies a list of pairs (bearings and
            deviations) to filter the segments of the road network a waypoint can
            snap to. For example bearings=[[45,10],[120,20]]. Each pair is a
            comma-separated list that can consist of one or two float values, where
            the first value is the bearing and the second one is the allowed deviation
            from the bearing. The bearing can take values between 0 and 360 clockwise
            from true north. If the deviation is not set, then the default value of
            100 degrees is used. The number of pairs must correspond to the number
            of waypoints.
        :type bearings: list, tuple of int lists/tuples

        :param alternatives: Search for alternative routes. A result cannot be guaranteed. Accepts an integer.
            Default false.
        :type alternatives: bool or int

        :param steps: Return route steps for each route leg. Default false.
        :type steps: bool

        :param continue_straight: Forces the route to keep going straight at waypoints constraining
            uturns there even if it would be faster. Default value depends on the profile.
        :type continue_straight: bool

        :param annotations: Returns additional metadata for each coordinate along the route geometry. Default false.
        :type annotations: bool

        :param geometries: Returned route geometry format (influences overview and per step). One of ["polyline",
            "polyline6", "geojson". Default polyline.
        :type geometries: str

        :param overview: Add overview geometry either full, simplified according to highest zoom level
            it could be display on, or not at all. One of ["simplified", "full", "false", False]. Default simplified.
        :type overview: str

        :param dry_run: Print URL and parameters without sending the request.
        :param dry_run: bool

        :returns: raw JSON response
        :rtype: dict
        """

        coords = convert._delimit_list([
            convert._delimit_list([convert._format_float(f) for f in pair])
            for pair in coordinates
        ], ';')

        params = dict()

        if radiuses:
            params["radiuses"] = convert._delimit_list(radiuses, ';')

        if bearings:
            params["bearings"] = convert._delimit_list(
                [convert._delimit_list(pair) for pair in bearings], ';')

        if alternatives is not None:
            params["alternatives"] = convert._convert_bool(alternatives)

        if steps is not None:
            params["steps"] = convert._convert_bool(steps)

        if continue_straight is not None:
            params["continue_straight"] = convert._convert_bool(
                continue_straight)

        if annotations is not None:
            params["annotations"] = convert._convert_bool(annotations)

        if geometries:
            params["geometries"] = geometries

        if overview is not None:
            params["overview"] = convert._convert_bool(overview)

        return self._request(
            "/route/v1/" + profile + '/' + coords,
            get_params=params,
            dry_run=dry_run)

    def isochrones(self):
        raise NotImplementedError

    def distance_matrix(self,
                        coordinates,
                        profile,
                        radiuses=None,
                        bearings=None,
                        sources=None,
                        destinations=None,
                        dry_run=None):
        """
        Gets travel distance and time for a matrix of origins and destinations.

        For more information visit http://project-osrm.org/docs/v5.5.1/api/#table-service.

        :param coordinates: The coordinates tuple the route should be calculated
            from in order of visit.
        :type coordinates: list, tuple

        :param profile: Specifies the mode of transport to use when calculating
            directions. One of ["car", "bike", "foot"].
        :type profile: str

        :param radiuses: A list of maximum distances (measured in
            meters) that limit the search of nearby road segments to every given waypoint.
            The values must be greater than 0, an empty element signifies to use the backend default
            radius. The number of radiuses must correspond to the number of waypoints.
        :type radiuses: list or tuple

        :param bearings: Specifies a list of pairs (bearings and
            deviations) to filter the segments of the road network a waypoint can
            snap to. For example bearings=[[45,10],[120,20]]. Each pair is a
            comma-separated list that can consist of one or two float values, where
            the first value is the bearing and the second one is the allowed deviation
            from the bearing. The bearing can take values between 0 and 360 clockwise
            from true north. If the deviation is not set, then the default value of
            100 degrees is used. The number of pairs must correspond to the number
            of waypoints.
        :type bearings: list, tuple of int lists/tuples

        :param sources: A list of indices that refer to the list of locations
            (starting with 0). If not passed, all indices are considered.
        :type sources: list or tuple

        :param destinations: A list of indices that refer to the list of locations
            (starting with 0). If not passed, all indices are considered.
        :type destinations: list or tuple

        :param dry_run: Print URL and parameters without sending the request.
        :param dry_run: bool

        :returns: raw JSON response
        :rtype: dict
        """

        coords = convert._delimit_list([
            convert._delimit_list([convert._format_float(f) for f in pair])
            for pair in coordinates
        ], ';')

        params = dict()

        if sources:
            params['sources'] = convert._delimit_list(sources, ';')

        if destinations:
            params['destinations'] = convert._delimit_list(destinations, ';')

        return self._request(
            "/table/v1/" + profile + '/' + coords,
            get_params=params,
            dry_run=dry_run)
