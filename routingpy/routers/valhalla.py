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
import re
import json


class Valhalla(Router):
    """Performs requests to the ORS API services."""

    def __init__(self, base_url, user_agent=None, timeout=None,
                 retry_timeout=None, requests_kwargs=None, retry_over_query_limit=False):
        """
        Initializes a Valhalla client.

        :param key: ORS API key. Required if https://api.openrouteservice.org is used.
        :type key: str

        :param base_url: The base URL for the request. Defaults to the ORS API
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

        super(Valhalla, self).__init__(base_url, user_agent, timeout, retry_timeout, requests_kwargs, retry_over_query_limit)

    def directions(self, coordinates, profile, types=None, headings=None, heading_tolerances=None,
                   minimum_reachabilities=None, radiuses=None, rank_candidates=None, options=None, units=None,
                   language=None, directions_type=None, avoid_locations=None, date_time=None, id=None, dry_run=None):
        """Get directions between an origin point and a destination point.

        For more information, visit https://openrouteservice.org/documentation/.

        :param coordinates: The coordinates tuple the route should be calculated
            from in order of visit. One coordinate pair takes the form [Longitude, Latitude].
        :type coordinates: list, tuple of coordinates lists/tuples

        :param profile: Specifies the mode of transport to use when calculating
            directions. One of ["auto", "auto_shorter", "bicycle", "bus", "hov", "motor_scooter",
            "motorcycle", "multimodal", "pedestrian".
        :type profile: str

        :param types: Type of location. One of ['break', 'through']. A break is a stop, so the first
            and last locations must be of type break. A through location is one that the route path travels
            through, and is useful to force a route to go through location. The path is not allowed to
            reverse direction at the through locations. If no type is provided, the type is assumed to be a break.
            The order has to correspond to ``coordinates`` and be of the same length.
            More info at: https://github.com/valhalla/valhalla/blob/master/docs/api/turn-by-turn/api-reference.md#locations
        :type types: list/tuple of str

        :param headings: Preferred direction of travel for the start from the location. The heading is indicated
            in degrees from north in a clockwise direction, where north is 0°, east is 90°,
            south is 180°, and west is 270°.
        :type headings: list/tuple of int

        :param heading_tolerances: How close in degrees a given street's angle must be in order for it
            to be considered as in the same direction of the heading parameter. The default value is 60 degrees.
        :type heading_tolerances: list/tuple of int

        :param minimum_reachabilities: Minimum number of nodes (intersections) reachable for a given edge (road between
            intersections) to consider that edge as belonging to a connected region. When correlating this
            location to the route network, try to find candidates who are reachable from this many or more
            nodes (intersections). If a given candidate edge reaches less than this number of nodes its considered
            to be a disconnected island and we'll search for more candidates until we find at least one that
            isn't considered a disconnected island. If this value is larger than the configured service limit
            it will be clamped to that limit. The default is a minimum of 50 reachable nodes.
        :type minimum_reachabilities: list/tuple of int

        :param radiuses: The number of meters about this input location within which edges (roads between intersections)
            will be considered as candidates for said location. When correlating this location to the route network,
            try to only return results within this distance (meters) from this location. If there are no candidates
            within this distance it will return the closest candidate within reason. If this value is larger than
            the configured service limit it will be clamped to that limit. The default is 0 meters.
        :type radiuses: list/tuple of int

        :param rank_candidates: Whether or not to rank the edge candidates for this location. The ranking is used
            as a penalty within the routing algorithm so that some edges will be penalized more heavily than others.
            If true candidates will be ranked according to their distance from the input and various other attributes.
            If false the candidates will all be treated as equal which should lead to routes that are just the most
            optimal path with emphasis about which edges were selected.
        :type rank_candidates: list/tuple of bool

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
        :type avoid_locations: list/tuple of coordinates lists/tuples

        :param date_time: This is the local date and time at the location. Field ``type``: 0: Current departure time,
            1: Specified departure time. Field ``value```: the date and time is specified
            in ISO 8601 format (YYYY-MM-DDThh:mm), local time.
            E.g. date_time = {type: 0, value: 2019-03-03T08:06:23}
        :type date_time: datetime.datetime() or str

        :param id: Name your route request. If id is specified, the naming will be sent thru to the response.
        :type id: str

        :param dry_run: Print URL and parameters without sending the request.
        :param dry_run: bool

        :returns: raw JSON response
        :rtype: dict
        """

        # Build the locations object in a common function
        locations = self._build_locations(coordinates, types=types, headings=headings,
                                          heading_tolerances=heading_tolerances, minimum_reachabilities=minimum_reachabilities,
                                          radiuses=radiuses, rank_candidates=rank_candidates)

        params = {
            'locations': locations,
            'costing': profile
        }

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
                params['directions_options']['directions_type'] = directions_type

        if avoid_locations:
            params['avoid_locations'] = [{"lat": coord[1], "lon": coord[0]} for coord in coordinates]

        if date_time:
            params['date_time'] = date_time

        if id:
            params['id'] = id

        return self._request("/route", get_params={'json': json.dumps(params)}, post_json=params, dry_run=dry_run)

    def isochrones(self, coordinates, profile, range, colors=None, polygons=None, denoise=None, generalize=None, types=None,
                   headings=None, heading_tolerances=None, street_names=None,
                   minimum_reachabilities=None, radiuses=None, rank_candidates=None, options=None, units=None,
                   language=None, directions_type=None, avoid_locations=None, date_time=None, id=None, dry_run=None):
        """Gets isochrones or equidistants for a range of time/distance values around a given set of coordinates.

        For more information, visit https://openrouteservice.org/documentation/.

        :param coordinates: One pair of lng/lat values. Takes the form [Longitude, Latitude].
        :type coordinates: list/tuple

        :param profile: Specifies the mode of transport to use when calculating
            directions. One of ["auto", "bicycle", "multimodal", "pedestrian".
        :type profile: str

        :param range: Time ranges to calculate isochrones for. Up to 4 ranges are possible. In seconds.
        :type range: list of int

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

        :param types: Type of location, either break or through. A break is a stop, so the first
            and last locations must be of type break. A through location is one that the route path travels
            through, and is useful to force a route to go through location. The path is not allowed to
            reverse direction at the through locations. If no type is provided, the type is assumed to be a break.

            The order has to correspond to ``coordinates`` and be of the same length.

            More info at: https://github.com/valhalla/valhalla/blob/master/docs/api/turn-by-turn/api-reference.md#locations
        :type types: list/tuple of str

        :param headings: Preferred direction of travel for the start from the location. The heading is indicated
            in degrees from north in a clockwise direction, where north is 0°, east is 90°,
            south is 180°, and west is 270°.
        :type headings: list/tuple of int

        :param heading_tolerances: How close in degrees a given street's angle must be in order for it
            to be considered as in the same direction of the heading parameter. The default value is 60 degrees.
        :type heading_tolerances: list/tuple of int

        :param street_names: Street name. The street name may be used to assist finding the correct routing
            location at the specified latitude, longitude. This is not currently implemented.
        :type street_names: list/tuple of str

        :param minimum_reachabilities: Minimum number of nodes (intersections) reachable for a given edge (road between
            intersections) to consider that edge as belonging to a connected region. When correlating this
            location to the route network, try to find candidates who are reachable from this many or more
            nodes (intersections). If a given candidate edge reaches less than this number of nodes its considered
            to be a disconnected island and we'll search for more candidates until we find at least one that
            isn't considered a disconnected island. If this value is larger than the configured service limit
            it will be clamped to that limit. The default is a minimum of 50 reachable nodes.
        :type minimum_reachabilities: list/tuple of int

        :param radiuses: The number of meters about this input location within which edges (roads between intersections)
            will be considered as candidates for said location. When correlating this location to the route network,
            try to only return results within this distance (meters) from this location. If there are no candidates
            within this distance it will return the closest candidate within reason. If this value is larger than
            the configured service limit it will be clamped to that limit. The default is 0 meters.
        :type radiuses: list/tuple of int

        :param rank_candidates: Whether or not to rank the edge candidates for this location. The ranking is used
            as a penalty within the routing algorithm so that some edges will be penalized more heavily than others.
            If true candidates will be ranked according to their distance from the input and various other attributes.
            If false the candidates will all be treated as equal which should lead to routes that are just the most
            optimal path with emphasis about which edges were selected.
        :type rank_candidates: list/tuple of bool

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
        :type avoid_locations: list/tuple of coordinates lists/tuples

        :param date_time: This is the local date and time at the location. Field ``type``: 0: Current departure time,
            1: Specified departure time. Field ``value```: the date and time is specified
            in format YYYY-MM-DDThh:mm, local time.

            E.g. date_time = {type: 0, value: 2019-03-03T08:06}
        :type date_time: datetime.datetime() or str

        :param id: Name your route request. If id is specified, the naming will be sent thru to the response.
        :type id: str

        :param dry_run: Print URL and parameters without sending the request.
        :param dry_run: bool

        :returns: raw JSON response
        :rtype: dict
        """

        # Build the locations object in a common function
        locations = self._build_locations(coordinates, types=types, headings=headings, heading_tolerances=heading_tolerances,
                                          street_names=street_names, minimum_reachabilities=minimum_reachabilities,
                                          radiuses=radiuses, rank_candidates=rank_candidates)

        params = {
            "locations": locations,
            "costing": profile,
            "contours": range,
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

        if date_time:
            params['date_time'] = date_time

        if id:
            params['id'] = id

        return self._request("/v2/isochrones/" + profile + '/geojson', get_params={}, post_json=params, dry_run=dry_run)

    def distance_matrix(self, coordinates, profile, sources=None, destinations=None, metrics=None,
                        resolve_locations=None, units=None, dry_run=None):
        """ Gets travel distance and time for a matrix of origins and destinations.

            :param coordinates: One or more pairs of lng/lat values.
            :type coordinates: a single location, or a list of locations, where a
                location is a list or tuple of lng,lat values

            :param profile: Specifies the mode of transport to use when calculating
                directions. One of ["driving-car", "driving-hgv", "foot-walking",
                "foot-hiking", "cycling-regular", "cycling-road", "cycling-mountain",
                "cycling-electric",]. Default "driving-car".
            :type profile: str

            :param sources: A list of indices that refer to the list of locations
                (starting with 0). If not passed, all indices are considered.
            :type sources: list or tuple

            :param destinations: A list of indices that refer to the list of locations
                (starting with 0). If not passed, all indices are considered.
            :type destinations: list or tuple

            :param metrics: Specifies a list of returned metrics. One or more of ["distance",
                "duration"]. Default ['duration'].
            :type metrics: list of str

            :param resolve_locations: Specifies whether given locations are resolved or
                not. If set 'true', every element in destinations and sources will
                contain the name element that identifies the name of the closest street.
                Default False.
            :type resolve_locations: bool

            :param units: Specifies the unit system to use when displaying results.
                One of ["m", "km", "m"]. Default "m".
            :type units: str

            :param dry_run: Print URL and parameters without sending the request.
            :param dry_run: bool

            :returns: raw JSON response
            :rtype: dict
            """

        params = {
            "locations": coordinates,
            "profile": profile
        }

        if sources:
            params['sources'] = sources

        if destinations:
            params['destinations'] = destinations

        if metrics:
            params["metrics"] = metrics

        if resolve_locations is not None:
            params["resolve_locations"] = resolve_locations

        if units:
            params["units"] = units

        return self._request("/v2/matrix/" + profile + '/json', get_params={}, post_json=params, dry_run=dry_run)

    def _build_locations(self, coordinates, **kwargs):

        # {VAR_NAME: Valhalla_Param_Name}
        _LOCATIONS_MAPPING = {
            'types': 'type',
            'headings': 'heading',
            'heading_tolerances': 'heading_tolerance',
            'street_names': 'street',
            'minimum_reachabilities': 'minimum_reachability',
            'radiuses': 'radius',
            'rank_candidates': 'rank_candidates'
        }

        locations = [{"lat": coord[1], "lon": coord[0]} for coord in coordinates]

        def append_locations(arg, name):
            if len(arg) == len(coordinates):
                for d, v in zip(locations, arg):
                    d.update({_LOCATIONS_MAPPING[name]: v})
            else:
                raise ValueError("{} needs to be the same length as coordinates".format(name))

        for k, v in kwargs.items():
            if kwargs.get(k, None):
                append_locations(v, k)

        return locations
