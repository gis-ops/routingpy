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
"""
Core client functionality, common across all API requests.
"""

from typing import List, Union, Sequence, Optional  # noqa: F401

from ..client_base import DEFAULT
from ..client_default import Client
from .. import utils
from ..direction import Direction
from ..expansion import Expansions, Edge
from ..isochrone import Isochrone, Isochrones
from ..matrix import Matrix

from operator import itemgetter


class Valhalla:
    """Performs requests to a Valhalla instance."""

    def __init__(
        self,
        base_url,
        api_key=None,
        user_agent=None,
        timeout=DEFAULT,
        retry_timeout=None,
        retry_over_query_limit=False,
        skip_api_error=None,
        client=Client,
        **client_kwargs
    ):
        """
        Initializes a Valhalla client.

        :param api_key: Mapbox API key. Required if base_url='https://api.mapbox.com/valhalla/v1'.
        :type api_key: str

        :param base_url: The base URL for the request. Defaults to the ORS API
            server. Should not have a trailing slash.
        :type base_url: str

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
            Default :attr:`routingpy.routers.options.default_retry_over_query_limit`.
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

        self.api_key = api_key

        self.client = client(
            base_url,
            user_agent,
            timeout,
            retry_timeout,
            retry_over_query_limit,
            skip_api_error,
            **client_kwargs
        )

    class Waypoint(object):
        """
        Constructs a waypoint with additional information or constraints.

        Refer to Valhalla's documentation for details: https://github.com/valhalla/valhalla/blob/master/docs/api/turn-by-turn/api-reference.md#locations

        Use ``kwargs`` to specify options, make sure the value is proper for each option.

        Example:

        >>> waypoint = Valhalla.WayPoint(position=[8.15315, 52.53151], type='through', heading=120, heading_tolerance=10, minimum_reachability=10, radius=400)
        >>> route = Valhalla('http://localhost').directions(locations=[[[8.58232, 51.57234]], waypoint, [7.15315, 53.632415]])
        """

        def __init__(self, position, **kwargs):
            self._position = position
            self._kwargs = kwargs

        def _make_waypoint(self):

            waypoint = {"lon": self._position[0], "lat": self._position[1]}
            for k, v in self._kwargs.items():
                waypoint[k] = v

            return waypoint

    def directions(
        self,
        locations,
        profile,
        preference=None,
        options=None,
        units=None,
        language=None,
        directions_type=None,
        avoid_locations=None,
        avoid_polygons=None,
        date_time=None,
        id=None,
        dry_run=None,
        **kwargs
    ):
        """Get directions between an origin point and a destination point.

        For more information, visit https://github.com/valhalla/valhalla/blob/master/docs/api/turn-by-turn/api-reference.md.

        Use ``kwargs`` for any missing ``directions`` request options.

        :param Union[List[List[float]]|List[Valhalla.Waypoint]] locations: The coordinates tuple the route should be calculated
            from in order of visit. Can be a list/tuple of [lon, lat] or :class:`Valhalla.WayPoint` instance or
            a combination of both.

        :param str profile: Specifies the mode of transport to use when calculating
            directions. One of ["auto", "auto_shorter" (deprecated), "bicycle", "bus", "hov", "motor_scooter",
            "motorcycle", "multimodal", "pedestrian".

        :param str preference: Convenience argument to set the cost metric, one of ['shortest', 'fastest']. Note,
            that shortest is not guaranteed to be absolute shortest for motor vehicle profiles. It's called ``preference``
            to be inline with the already existing parameter in the ORS adapter.

        :param dict options: Profiles can have several options that can be adjusted to develop the route path,
            as well as for estimating time along the path. Only specify the actual options dict, the profile
            will be filled automatically. For more information, visit:
            https://github.com/valhalla/valhalla/blob/master/docs/api/turn-by-turn/api-reference.md#costing-options

        :param str units: Distance units for output. One of ['mi', 'km']. Default km.

        :param str language: The language of the narration instructions based on the IETF BCP 47 language tag string.
            One of ['ca', 'cs', 'de', 'en', 'pirate', 'es', 'fr', 'hi', 'it', 'pt', 'ru', 'sl', 'sv']. Default 'en'.

        :param str directions_type: 'none': no instructions are returned. 'maneuvers': only maneuvers are returned.
            'instructions': maneuvers with instructions are returned. Default 'instructions'.

        :param Union[List[List[float]]|List[Valhalla.Waypoint]] avoid_locations: A set of locations to exclude or avoid within a route.
            Specified as a list of coordinates, similar to coordinates object.

        :param List[List[List[float]]] avoid_polygons: One or multiple exterior rings of polygons in the form of nested
            JSON arrays, e.g. [[[lon1, lat1], [lon2,lat2]],[[lon1,lat1],[lon2,lat2]]]. Roads intersecting these rings
            will be avoided during path finding. If you only need to avoid a few specific roads, it's much more
            efficient to use avoid_locations. Valhalla will close open rings (i.e. copy the first coordingate to the
            last position).

        :param dict date_time: This is the local date and time at the location. Field ``type``: 0: Current departure time,
            1: Specified departure time. Field ``value```: the date and time is specified
            in ISO 8601 format (YYYY-MM-DDThh:mm), local time.
            E.g. date_time = {type: 0, value: 2021-03-03T08:06:23}

        :param Union[str|int|float] id: Name your route request. If id is specified, the naming will be sent thru to the response.

        :param bool dry_run: Print URL and parameters without sending the request.

        :returns: A route from provided coordinates and restrictions.
        :rtype: :class:`routingpy.direction.Direction`
        """

        params = self.get_direction_params(
            locations,
            profile,
            preference,
            options,
            units,
            language,
            directions_type,
            avoid_locations,
            avoid_polygons,
            date_time,
            id,
        )

        get_params = {"access_token": self.api_key} if self.api_key else {}

        return self._parse_direction_json(
            self.client._request("/route", get_params=get_params, post_params=params, dry_run=dry_run),
            units,
        )

    @staticmethod
    def get_direction_params(
        locations,
        profile,
        preference=None,
        options=None,
        units=None,
        language=None,
        directions_type=None,
        avoid_locations=None,
        avoid_polygons=None,
        date_time=None,
        id=None,
    ):
        params = dict(costing=profile)

        params["locations"] = Valhalla._build_locations(locations)

        if options or preference:
            params["costing_options"] = dict()
            profile = profile if profile not in ("multimodal", "transit") else "transit"
            params["costing_options"][profile] = dict()
            if options:
                params["costing_options"][profile] = options
            if preference == "shortest":
                params["costing_options"][profile]["shortest"] = True

        if any((units, language, directions_type)):
            params["directions_options"] = dict()
            if units:
                params["directions_options"]["units"] = units
            if language:
                params["directions_options"]["language"] = language
            if directions_type:
                params["directions_options"]["directions_type"] = directions_type

        if avoid_locations:
            params["avoid_locations"] = Valhalla._build_locations(avoid_locations)

        if avoid_polygons:
            params["avoid_polygons"] = avoid_polygons

        if date_time:
            params["date_time"] = date_time

        if id:
            params["id"] = id

        return params

    @staticmethod
    def _parse_direction_json(response, units):
        if response is None:  # pragma: no cover
            return Direction()

        geometry, duration, distance = [], 0, 0
        for leg in response["trip"]["legs"]:
            geometry.extend(utils.decode_polyline6(leg["shape"]))
            duration += leg["summary"]["time"]

            factor = 0.621371 if units == "mi" else 1
            distance += int(leg["summary"]["length"] * 1000 * factor)

        return Direction(geometry=geometry, duration=int(duration), distance=int(distance), raw=response)

    def isochrones(  # noqa: C901
        self,
        locations,
        profile,
        intervals,
        interval_type=None,
        colors=None,
        polygons=None,
        denoise=None,
        generalize=None,
        preference=None,
        options=None,
        units=None,
        language=None,
        directions_type=None,
        avoid_locations=None,
        avoid_polygons=None,
        date_time=None,
        show_locations=None,
        id=None,
        dry_run=None,
    ):
        """Gets isochrones or equidistants for a range of time values around a given set of coordinates.

        For more information, visit https://github.com/valhalla/valhalla/blob/master/docs/api/isochrone/api-reference.md.

        Use ``kwargs`` for any missing ``isochrones`` request options.

        :param locations: One pair of lng/lat values. Takes the form [Longitude, Latitude].
        :type locations: list of float

        :param profile: Specifies the mode of transport to use when calculating
            directions. One of ["auto", "bicycle", "multimodal", "pedestrian".
        :type profile: str

        :param intervals: Time ranges to calculate isochrones for. In seconds or meters, depending on `interval_type`.
        :type intervals: list of int

        :param interval_type: Set 'time' for isochrones or 'distance' for equidistants.
            Default 'time'.
        :type interval_type: str

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

        :param str preference: Convenience argument to set the cost metric, one of ['shortest', 'fastest']. Note,
            that shortest is not guaranteed to be absolute shortest for motor vehicle profiles. It's called ``preference``
            to be inline with the already existing parameter in the ORS adapter.

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
        :type avoid_locations: list of list

        :param List[List[List[float]]] avoid_polygons: One or multiple exterior rings of polygons in the form of nested
            JSON arrays, e.g. [[[lon1, lat1], [lon2,lat2]],[[lon1,lat1],[lon2,lat2]]]. Roads intersecting these rings
            will be avoided during path finding. If you only need to avoid a few specific roads, it's much more
            efficient to use avoid_locations. Valhalla will close open rings (i.e. copy the first coordingate to the
            last position).

        :param date_time: This is the local date and time at the location. Field ``type``: 0: Current departure time,
            1: Specified departure time. Field ``value```: the date and time is specified
            in format YYYY-MM-DDThh:mm, local time.

            E.g. date_time = {type: 0, value: 2021-03-03T08:06}
        :type date_time: dict

        :param id: Name your route request. If id is specified, the naming will be sent thru to the response.
        :type id: str

        :param dry_run: Print URL and parameters without sending the request.
        :param dry_run: bool

        :returns: An isochrone with the specified range.
        :rtype: :class:`routingpy.isochrone.Isochrones`
        """

        params = self.get_isochrone_params(
            locations,
            profile,
            intervals,
            interval_type,
            colors,
            polygons,
            denoise,
            generalize,
            preference,
            options,
            avoid_locations,
            avoid_polygons,
            date_time,
            show_locations,
            id,
        )

        get_params = {"access_token": self.api_key} if self.api_key else {}
        return self._parse_isochrone_json(
            self.client._request(
                "/isochrone", get_params=get_params, post_params=params, dry_run=dry_run
            ),
            intervals,
            locations,
        )

    @staticmethod  # noqa: C901
    def get_isochrone_params(  # noqa: C901
        locations,
        profile,
        intervals,
        interval_type=None,
        colors=None,
        polygons=None,
        denoise=None,
        generalize=None,
        preference=None,
        options=None,
        avoid_locations=None,
        avoid_polygons=None,
        date_time=None,
        show_locations=None,
        id=None,
    ):
        contours = []
        for idx, r in enumerate(intervals):
            key = "time"
            value = r / 60
            if interval_type == "distance":
                key = "distance"
                value = r / 1000

            d = {key: value}
            if colors:
                try:
                    d.update(color=colors[idx])
                except IndexError:
                    raise IndexError("Colors object must have same length as Range object.")
            contours.append(d)

        params = {
            "locations": Valhalla._build_locations(locations),
            "costing": profile,
            "contours": contours,
        }

        if options:
            params["costing_options"] = dict()
            profile = profile if profile != "multimodal" else "transit"
            params["costing_options"][profile] = dict()
            if options:
                params["costing_options"][profile] = options
            if preference == "shortest":
                params["costing_options"][profile]["shortest"] = True

        if polygons is not None:
            params["polygons"] = polygons

        if denoise:
            params["denoise"] = denoise

        if generalize:
            params["generalize"] = generalize

        if avoid_locations:
            params["avoid_locations"] = Valhalla._build_locations(avoid_locations)

        if avoid_polygons:
            params["avoid_polygons"] = avoid_polygons

        if date_time:
            params["date_time"] = date_time

        if show_locations is not None:
            params["show_locations"] = show_locations

        if id:
            params["id"] = id

        return params

    @staticmethod
    def _parse_isochrone_json(response, intervals, locations):
        if response is None:  # pragma: no cover
            return Isochrones()

        isochrones = []
        for idx, feature in enumerate(reversed(response["features"])):
            if feature["geometry"]["type"] in ("LineString", "Polygon"):
                isochrones.append(
                    Isochrone(
                        geometry=feature["geometry"]["coordinates"],
                        interval=intervals[idx],
                        center=locations,
                    )
                )

        return Isochrones(isochrones, response)

    def matrix(
        self,
        locations,
        profile,
        sources=None,
        destinations=None,
        preference=None,
        options=None,
        avoid_locations=None,
        avoid_polygons=None,
        units=None,
        id=None,
        dry_run=None,
    ):
        """
        Gets travel distance and time for a matrix of origins and destinations.

        For more information, visit https://github.com/valhalla/valhalla/blob/master/docs/api/matrix/api-reference.md.

        Use ``kwargs`` for any missing ``matrix`` request options.

        :param locations: Multiple pairs of lng/lat values.
        :type locations: list of list

        :param profile: Specifies the mode of transport to use when calculating
            matrices. One of ["auto", "bicycle", "multimodal", "pedestrian".
        :type profile: str

        :param sources: A list of indices that refer to the list of locations
            (starting with 0). If not passed, all indices are considered.
        :type sources: list of int

        :param destinations: A list of indices that refer to the list of locations
            (starting with 0). If not passed, all indices are considered.
        :type destinations: list of int

        :param str preference: Convenience argument to set the cost metric, one of ['shortest', 'fastest']. Note,
            that shortest is not guaranteed to be absolute shortest for motor vehicle profiles. It's called ``preference``
            to be inline with the already existing parameter in the ORS adapter.

        :param options: Profiles can have several options that can be adjusted to develop the route path,
            as well as for estimating time along the path. Only specify the actual options dict, the profile
            will be filled automatically. For more information, visit:
            https://github.com/valhalla/valhalla/blob/master/docs/api/turn-by-turn/api-reference.md#costing-options
        :type options: dict

        :param avoid_locations: A set of locations to exclude or avoid within a route.
            Specified as a list of coordinates, similar to coordinates object.
        :type avoid_locations: list of list

        :param List[List[List[float]]] avoid_polygons: One or multiple exterior rings of polygons in the form of nested
            JSON arrays, e.g. [[[lon1, lat1], [lon2,lat2]],[[lon1,lat1],[lon2,lat2]]]. Roads intersecting these rings
            will be avoided during path finding. If you only need to avoid a few specific roads, it's much more
            efficient to use avoid_locations. Valhalla will close open rings (i.e. copy the first coordingate to the
            last position).

        :param units: Distance units for output. One of ['mi', 'km']. Default km.
        :type units: str

        :param id: Name your route request. If id is specified, the naming will be sent through to the response.
        :type id: str

        :param dry_run: Print URL and parameters without sending the request.
        :param dry_run: bool

        :returns: A matrix from the specified sources and destinations.
        :rtype: :class:`routingpy.matrix.Matrix`
        """

        params = self.get_matrix_params(
            locations,
            profile,
            sources,
            destinations,
            preference,
            options,
            avoid_locations,
            avoid_polygons,
            units,
            id,
        )

        get_params = {"access_token": self.api_key} if self.api_key else {}

        return self._parse_matrix_json(
            self.client._request(
                "/sources_to_targets", get_params=get_params, post_params=params, dry_run=dry_run
            ),
            units,
        )

    @staticmethod
    def get_matrix_params(
        locations,
        profile,
        sources=None,
        destinations=None,
        preference=None,
        options=None,
        avoid_locations=None,
        avoid_polygons=None,
        units=None,
        id=None,
    ):
        params = {
            "costing": profile,
        }

        locations = Valhalla._build_locations(locations)

        sources_coords = locations
        if sources is not None:
            sources_coords = itemgetter(*sources)(sources_coords)
            if isinstance(sources_coords, dict):
                sources_coords = [sources_coords]
        params["sources"] = sources_coords

        dest_coords = locations
        if destinations is not None:
            dest_coords = itemgetter(*destinations)(dest_coords)
            if isinstance(dest_coords, dict):
                dest_coords = [dest_coords]
        params["targets"] = dest_coords

        if options:
            params["costing_options"] = dict()
            profile = profile if profile != "multimodal" else "transit"
            params["costing_options"][profile] = dict()
            if options:
                params["costing_options"][profile] = options
            if preference == "shortest":
                params["costing_options"][profile]["shortest"] = True

        if avoid_locations:
            params["avoid_locations"] = Valhalla._build_locations(avoid_locations)

        if avoid_polygons:
            params["avoid_polygons"] = avoid_polygons

        if units:
            params["units"] = units

        if id:
            params["id"] = id

        return params

    @staticmethod
    def _parse_matrix_json(response, units):
        if response is None:  # pragma: no cover
            return Matrix()

        factor = 0.621371 if units == "mi" else 1
        durations = [
            [destination["time"] for destination in origin] for origin in response["sources_to_targets"]
        ]
        distances = [
            [int(destination["distance"] * 1000 * factor) for destination in origin]
            for origin in response["sources_to_targets"]
        ]

        return Matrix(durations=durations, distances=distances, raw=response)

    def expansion(
        self,
        locations: Sequence[float],
        profile: str,
        intervals: Sequence[int],
        skip_opposites: Optional[bool] = None,
        expansion_properties: Optional[Sequence[str]] = None,
        interval_type: Optional[str] = None,
        options: Optional[dict] = None,
        date_time: Optional[dict] = None,
        id: Optional[str] = None,
        dry_run: Optional[bool] = None,
    ) -> Expansions:
        """Gets the expansion tree for a range of time or distance values around a given coordinate.

        For more information, visit https://valhalla.readthedocs.io/en/latest/api/expansion/api-reference/.

        :param locations: One pair of lng/lat values. Takes the form [Longitude, Latitude].

        :param profile: Specifies the mode of transport to use when calculating
            directions. One of ["auto", "bicycle", "multimodal", "pedestrian".

        :param intervals: Time ranges to calculate isochrones for. In seconds or meters, depending on `interval_type`.

        :param skip_opposites: If set to true the output won't contain an edge's opposing edge. Opposing edges can be thought of as both directions of one road segment. Of the two, we discard the directional edge with higher cost and keep the one with less cost.

        :param expansion_properties: A JSON array of strings of the GeoJSON property keys you'd like to have in the response. One or multiple of "durations", "distances", "costs", "edge_ids", "statuses". Note, that each additional property will increase the output size by minimum ~ 25%.

        :param interval_type: Set 'time' for isochrones or 'distance' for equidistants.
            Default 'time'.

        :param options: Profiles can have several options that can be adjusted to develop the route path,
            as well as for estimating time along the path. Only specify the actual options dict, the profile
            will be filled automatically. For more information, visit:
            https://github.com/valhalla/valhalla/blob/master/docs/api/turn-by-turn/api-reference.md#costing-options

        :param date_time: This is the local date and time at the location. Field ``type``: 0: Current departure time,
            1: Specified departure time. Field ``value```: the date and time is specified
            in format YYYY-MM-DDThh:mm, local time.

            E.g. date_time = {type: 0, value: 2021-03-03T08:06}

        :param id: Name your route request. If id is specified, the naming will be sent thru to the response.

        :param dry_run: Print URL and parameters without sending the request.

        :returns: An expansions object consisting of single line strings and their attributes (if specified).
        """

        get_params = {"access_token": self.api_key} if self.api_key else {}
        params = self.get_expansion_params(
            locations,
            profile,
            intervals,
            skip_opposites,
            expansion_properties,
            interval_type,
            options,
            date_time,
            id,
        )
        return self._parse_expansion_json(
            self.client._request(
                "/expansion", get_params=get_params, post_params=params, dry_run=dry_run
            ),
            locations,
            expansion_properties,
        )

    @classmethod
    def get_expansion_params(
        cls,
        locations,
        profile,
        intervals,
        skip_opposites=None,
        expansion_properties=None,
        interval_type=None,
        options=None,
        date_time=None,
        id=None,
    ):
        params = cls.get_isochrone_params(
            locations,
            profile,
            intervals,
            interval_type,
            options=options,
            date_time=date_time,
            id=id,
        )
        params["action"] = "isochrone"
        if skip_opposites:
            params["skip_opposites"] = skip_opposites
        if expansion_properties:
            params["expansion_properties"] = expansion_properties
        return params

    @staticmethod
    def _parse_expansion_json(response, locations, expansion_properties):
        if response is None:  # pragma: no cover
            return Expansions()

        expansions = []
        for idx, line in enumerate(response["features"][0]["geometry"]["coordinates"]):
            properties = {}
            if expansion_properties:
                for expansion_prop in expansion_properties:
                    properties[expansion_prop] = response["features"][0]["properties"][expansion_prop][
                        idx
                    ]
            expansions.append(Edge(geometry=line, **properties))

        return Expansions(expansions, locations, response)

    @staticmethod
    def _build_locations(coordinates):
        """Build the locations object for all methods"""

        locations = []

        # Isochrones only support one coordinate tuple, so check for type of first element
        if isinstance(coordinates[0], (list, tuple, Valhalla.Waypoint)):
            for idx, coord in enumerate(coordinates):
                if isinstance(coord, (list, tuple)):
                    locations.append({"lon": coord[0], "lat": coord[1]}),
                elif isinstance(coord, Valhalla.Waypoint):
                    locations.append(coord._make_waypoint())
                else:
                    raise TypeError(
                        "Location type {} at index {} is not supported: {}".format(
                            type(coord), idx, coord
                        )
                    )
        elif isinstance(coordinates[0], float):
            locations.append({"lon": coordinates[0], "lat": coordinates[1]})

        return locations
