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

from .base import Router
from routingpy import convert

from operator import itemgetter


class Google(Router):
    """Performs requests to the Google API services."""

    _base_url = "https://maps.googleapis.com/maps/api"

    def __init__(self, api_key, user_agent=None, timeout=None,
                 retry_timeout=None, requests_kwargs={}, retry_over_query_limit=False):

        """
        Initializes a Google client.

        :param key: API key.
        :type key: str

        :param user_agent: User Agent to be used when requesting. Can be globally set in routingpy.options.
            Default 'routingpy.<version string>'.
        :type user_agent: str

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

        self.key = api_key

        super(Google, self).__init__(self._base_url, user_agent, timeout, retry_timeout, requests_kwargs,
                                     retry_over_query_limit)

    class WayPoint(object):
        """
        Optionally construct a waypoint from this class with additional attributes, such as via.
        """
        def __init__(self, position, waypoint_type='coords', stopover=True):
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

            waypoint = ''
            if self.waypoint_type == 'coords':
                waypoint += convert._delimit_list(list(reversed(self.position)))
            elif self.waypoint_type == 'place_id':
                waypoint += self.waypoint_type + ':' + self.position
            elif self.waypoint_type == 'enc':
                waypoint += self.waypoint_type + ':' + self.position + ':'
            else:
                raise ValueError("waypoint_type only supports enc, place_id, coords")

            if not self.stopover:
                waypoint = 'via:' + waypoint

            return waypoint

    def directions(self, coordinates, profile, alternatives=None, avoid=None, optimize=None, language=None,
                   region=None, units=None, arrival_time=None, departure_time=None, traffic_model=None,
                   transit_mode=None, transit_routing_preference=None, dry_run=None):
        """Get directions between an origin point and a destination point.

        For more information, visit https://developers.google.com/maps/documentation/directions/intro.

        :param coordinates: The coordinates tuple the route should be calculated
            from in order of visit. Can be a list/tuple of [lon, lat], a list/tuple of address strings, Google's
            Place ID's or a combination of these. Note, the first and last location have to be specified as [lon, lat].
            Optionally, specify ``optimize=true`` for via waypoint optimization.
        :type coordinates: list, tuple of lists/tuples of float or str

        :param profile: The vehicle for which the route should be calculated.
            Default "driving". One of ['driving', 'walking', 'bicycling', 'transit'].
        :type profile: str

        :param alternatives: Specifies whether more than one route should be returned.
            Only available for requests without intermediate waypoints. Default False.
        :type alternatives: bool

        :param avoid: Indicates that the calculated route(s) should avoid the indicated features. One or more of
            ['tolls', 'highways', 'ferries', 'indoor']. Default None.
        :param avoid: list of str

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
        :param dry_run: bool

        :returns: raw JSON response
        :rtype: dict
        """

        params = {
            'profile': profile
        }

        origin, destination = coordinates[0], coordinates[-1]
        if isinstance(origin, (list, tuple)):
            params['origin'] = convert._delimit_list(list(reversed(origin)))
        elif isinstance(origin, self.WayPoint):
            raise TypeError("The first and last coordinates must be list/tuple of [lon, lat]")

        if isinstance(destination, (list, tuple)):
            params['destination'] = convert._delimit_list(list(reversed(destination)))
        elif isinstance(origin, self.WayPoint):
            print('bla')
            raise TypeError("The first and last coordinates must be list/tuple of [lon, lat]")

        if len(coordinates) > 2:
            waypoints = []
            s = slice(1, -1)
            for coord in coordinates[s]:
                if isinstance(coord, (list, tuple)):
                    waypoints.append(convert._delimit_list(list(reversed(coord))))
                elif isinstance(coord, self.WayPoint):
                    waypoints.append(coord.make_waypoint())
            if optimize:
                waypoints.insert(0, 'optimize:true')

            params['waypoints'] = convert._delimit_list(waypoints, '|')

        if self.key is not None:
            params["key"] = self.key

        if alternatives is not None:
            params['alternatives'] = convert._convert_bool(alternatives)

        if avoid:
            params['avoid'] = convert._delimit_list(avoid, '|')

        if language:
            params['language'] = language

        if region:
            params['region'] = region

        if units:
            params['units'] = units

        if arrival_time and departure_time:
            raise ValueError("Specify either arrival_time or departure_time.")

        if arrival_time:
            params['arrival_time'] = str(arrival_time)

        if departure_time:
            params['departure_time'] = str(departure_time)

        if traffic_model:
            params['traffic_model'] = traffic_model

        if transit_mode:
            params['transit_mode'] = convert._delimit_list(transit_mode, '|')

        if transit_routing_preference:
            params['transit_routing_preference'] = transit_routing_preference

        return self._request('/directions/json', get_params=params, dry_run=dry_run)

    def isochrones(self):
        raise NotImplementedError

    def distance_matrix(self, coordinates, profile, sources=None, destinations=None, avoid=None, language=None,
                   region=None, units=None, arrival_time=None, departure_time=None, traffic_model=None,
                   transit_mode=None, transit_routing_preference=None, dry_run=None):
        """ Gets travel distance and time for a matrix of origins and destinations.

        :param coordinates: Specifiy multiple points for which the weight-, route-, time- or distance-matrix should be calculated.
            In this case the starts are identical to the destinations.
            If there are N points, then NxN entries will be calculated.
            The order of the point parameter is important. Specify at least three points.
            Cannot be used together with from_point or to_point. Is a string with the format latitude,longitude.
        :type coordinates: list, tuple

        :param profile: Specifies the mode of transport.
            One of bike, car, foot or
            https://graphhopper.com/api/1/docs/supported-vehicle-profiles/Default.
            Default "car".
        :type profile: str

        :param sources: The starting points for the routes.
            Specifies an index referring to coordinates.
        :type sources: list

        :param destinations: The destination points for the routes. Specifies an index referring to coordinates.
        :type destinations: list

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
        :param dry_run: bool

        :returns: raw JSON response
        :rtype: dict
        """
        params = {
            'profile': profile
        }

        waypoints = []
        for coord in coordinates:
            if isinstance(coord, (list, tuple)):
                waypoints.append(convert._delimit_list(list(reversed(coord))))
            elif isinstance(coord, self.WayPoint):
                waypoints.append(coord.make_waypoint())

        sources_coords = waypoints
        if sources is not None:
            sources_coords = itemgetter(*sources)(sources_coords)
            if not isinstance(sources_coords, (list, tuple)):
                sources_coords = [sources_coords]
        params['origins'] = convert._delimit_list(sources_coords, '|')

        destinations_coords = waypoints
        if destinations is not None:
            destinations_coords = itemgetter(*destinations)(destinations_coords)
            if not isinstance(destinations_coords, (list, tuple)):
                destinations_coords = [destinations_coords]
        params['destinations'] = convert._delimit_list(destinations_coords, '|')

        if self.key is not None:
            params["key"] = self.key

        if avoid:
            params['avoid'] = convert._delimit_list(avoid, '|')

        if language:
            params['language'] = language

        if region:
            params['region'] = region

        if units:
            params['units'] = units

        if arrival_time:
            params['arrival_time'] = str(arrival_time)

        if departure_time:
            params['departure_time'] = str(departure_time)

        if traffic_model:
            params['traffic_model'] = traffic_model

        if transit_mode:
            params['transit_mode'] = convert._delimit_list(transit_mode, '|')

        if transit_routing_preference:
            params['transit_routing_preference'] = transit_routing_preference

        return self._request('/distancematrix/json', get_params=params, dry_run=dry_run)

