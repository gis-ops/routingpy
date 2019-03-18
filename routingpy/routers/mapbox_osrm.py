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


class MapBoxOSRM(Router):
    """Performs requests to the OSRM API services."""

    _base_url = 'https://api.mapbox.com'

    def __init__(self, api_key, user_agent=None, timeout=None,
                 retry_timeout=None, requests_kwargs=None, retry_over_query_limit=False):
        """
        Initializes an OSRM client.

        :param key: ORS API key. Required if https://api.openrouteservice.org is used.
        :type key: str

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

        self.api_key = api_key

        super(MapBoxOSRM, self).__init__(self._base_url, user_agent, timeout, retry_timeout, requests_kwargs, retry_over_query_limit)

    def directions(self, coordinates, profile, radiuses=None, bearings=None, alternatives=None, steps=None,
                   continue_straight=None, annotations=None, geometries=None, overview=None, exclude=None,
                   approaches=None, banner_instructions=None, language=None, roundabout_exits=None,
                   voice_instructions=None, voice_units=None, waypoint_names=None, waypoint_targets=None, dry_run=None):
        """Get directions between an origin point and a destination point.

        For more information, visit http://project-osrm.org/docs/v5.5.1/api/#route-service.

        :param coordinates: The coordinates tuple the route should be calculated
            from in order of visit.
        :type coordinates: list, tuple

        :param profile: Specifies the mode of transport to use when calculating
            directions. One of ["driving-traffic", "driving", "walking", "cycling"].
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

        :param alternatives: Search for alternative routes and return as well. A result cannot be guaranteed.
            Default false.
        :type alternatives: bool

        :param steps: Return route steps for each route leg. Default false.
        :type steps: bool

        :param continue_straight: Forces the route to keep going straight at waypoints constraining
            uturns there even if it would be faster. Default value depends on the profile.
        :type continue_straight: bool

        :param annotations: Returns additional metadata for each coordinate along the route geometry.
            One of [duration, distance, speed, congestion].
        :type annotations: list of str

        :param geometries: Returned route geometry format (influences overview and per step). One of ["polyline",
            "polyline6", "geojson". Default polyline.
        :type geometries: str

        :param overview: Add overview geometry either full, simplified according to highest zoom level
            it could be display on, or not at all. One of ["simplified", "full", "false", False]. Default simplified.
        :type overview: str

        :param exclude: Exclude certain road types from routing. One of ['toll', 'motorway', 'ferry'] if profile=driving*.
            'ferry' for profile=cycling. None for profile=walking. Default none.
        :type exclude: str

        :param approaches: Indicating the side of the road from which to approach waypoint
            in a requested route. One of ["unrestricted", "curb"]. unrestricted: route can arrive at the waypoint from
            either side of the road. curb: route will arrive at the waypoint on the driving_side of the region. If provided,
            the number of approaches must be the same as the number of waypoints.
            Default unrestricted.
        :type approaches: list of str

        :param banner_instructions: Whether to return banner objects associated with the route steps. Default False.
        :type banner_instructions: bool

        :param language: The language of returned turn-by-turn text instructions. Default is en.
            See the full list here of supported languages here:
            https://docs.mapbox.com/api/navigation/#instructions-languages
        :type language: str

        :param roundabout_exits: Whether to emit instructions at roundabout exits or not.
            Without this parameter, roundabout maneuvers are given as a single instruction that includes both entering
            and exiting the roundabout. With roundabout_exits=true, this maneuver becomes two instructions, one for
            entering the roundabout and one for exiting it. Default false.
        :type roundabout_exits: bool

        :param voice_instructions: Whether to return SSML marked-up text for voice guidance along the route or not.
            Default false.
        :type voice_instructions: bool

        :param voice_units: Specify which type of units to return in the text for voice instructions. One of
            ["imperial", "metric"]. Default imperial.
        :type voice_units: str

        :param waypoint_names: List of custom names for entries in the list of coordinates,
            used for the arrival instruction in banners and voice instructions. Values can be any string, and the
            total number of all characters cannot exceed 500. If provided, the list of waypoint_names must be the
            same length as the list of coordinates. The first value in the list corresponds to the route origin, not the first
            destination.
        :type waypoint_names: list of str

        :param waypoint_targets: List of coordinate pairs used to specify drop-off locations that are distinct from the
            locations specified in coordinates. If this parameter is provided, the Directions API will compute the side
            of the street, left or right, for each target based on the waypoint_targets and the driving direction. The
            maneuver.modifier, banner and voice instructions will be updated with the computed side of street. The
            number of waypoint_targets must be the same as the number of coordinates.
        :type waypoint_targets: list of lists of float

        :param dry_run: Print URL and parameters without sending the request.
        :param dry_run: bool

        :returns: raw JSON response
        :rtype: dict
        """

        coords = convert._delimit_list([convert._delimit_list([convert._format_float(f) for f in pair]) for pair in coordinates], ';')

        params = {
            'coordinates': coords
        }

        if radiuses:
            params["radiuses"] = convert._delimit_list(radiuses, ';')

        if bearings:
            params["bearings"] = convert._delimit_list([convert._delimit_list(pair) for pair in bearings], ';')

        if alternatives is not None:
            params["alternatives"] = convert._convert_bool(alternatives)

        if steps is not None:
            params["steps"] = convert._convert_bool(steps)

        if continue_straight is not None:
            params["continue_straight"] = convert._convert_bool(continue_straight)

        if annotations is not None:
            params["annotations"] = convert._delimit_list(annotations)

        if geometries:
            params["geometries"] = geometries

        if overview is not None:
            params["overview"] = convert._convert_bool(overview)

        if exclude is not None:
            params['exclude'] = exclude

        if approaches:
            params['approaches'] = ';' + convert._delimit_list(approaches, ';')

        if banner_instructions:
            params['banner_instuctions'] = convert._convert_bool(banner_instructions)

        if language:
            params['language'] = language

        if roundabout_exits:
            params['roundabout_exits'] = convert._convert_bool(roundabout_exits)

        if voice_instructions:
            params['voide_instructions'] = convert._convert_bool(voice_instructions)

        if voice_units:
            params['voice_units'] = voice_units

        if waypoint_names:
            params['waypoint_names'] = convert._delimit_list(waypoint_names, ';')

        if waypoint_targets:
            params['waypoint_targets'] = ';' + convert._delimit_list([convert._delimit_list([convert._format_float(f) for f in pair]) for pair in waypoint_targets], ';')

        get_params = {'access_token': self.api_key} if self.api_key else {}

        return self._request("/directions/v5/mapbox/" + profile, get_params=get_params, post_params=params, dry_run=dry_run)

    def isochrones(self):
        raise NotImplementedError

    def distance_matrix(self, coordinates, profile, annotations=None, fallback_speed=None, sources=None,
                        destinations=None, dry_run=None):
        """
        Gets travel distance and time for a matrix of origins and destinations.

        For more information visit http://project-osrm.org/docs/v5.5.1/api/#table-service.

        :param coordinates: The coordinates tuple the route should be calculated
            from in order of visit.
        :type coordinates: list, tuple

        :param profile: Specifies the mode of transport to use when calculating
            directions. One of ["car", "bike", "foot"].
        :type profile: str

        :param annotations: Used to specify the resulting matrices. One or more of ["duration", "distance"]. Default
            ["duration"]
        :type annotations: list of str

        :param fallback_speed: 	By default, if there is no possible route between two points, the Matrix API sets the
            resulting matrix element to null. To circumvent this behavior, set the fallback_speed parameter to a
            value greater than 0 in kilometers per hour. The Matrix API will replace a null value with a straight-line
            estimate between the source and destination based on the provided speed value.
        :type fallback_speed: int

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

        coords = convert._delimit_list([convert._delimit_list([convert._format_float(f) for f in pair]) for pair in coordinates], ';')

        params = {
            'access_token': self.api_key
        }

        if sources:
            params['sources'] = convert._delimit_list(sources, ';')

        if destinations:
            params['destinations'] = convert._delimit_list(destinations, ';')

        if annotations:
            params['annotations'] = convert._delimit_list(annotations)

        if fallback_speed:
            params['fallback_speed'] = str(fallback_speed)

        return self._request("/directions-matrix/v1/mapbox/" + profile + '/' + coords, get_params=params, dry_run=dry_run)
