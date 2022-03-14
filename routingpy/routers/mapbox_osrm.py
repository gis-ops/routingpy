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

from ..client_base import DEFAULT
from ..client_default import Client
from .. import convert, utils
from ..direction import Direction, Directions
from ..isochrone import Isochrone, Isochrones
from ..matrix import Matrix


class MapboxOSRM:
    """Performs requests to the OSRM API services."""

    _base_url = "https://api.mapbox.com"

    def __init__(
        self,
        api_key,
        user_agent=None,
        timeout=DEFAULT,
        retry_timeout=None,
        retry_over_query_limit=False,
        skip_api_error=None,
        client=Client,
        **client_kwargs
    ):
        """
        Initializes a Mapbox OSRM client.

        :param api_key: Mapbox API key.
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

        client_kwargs.update({"headers": {"Content-Type": "application/x-www-form-urlencoded"}})

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
        locations,
        profile,
        radiuses=None,
        bearings=None,
        alternatives=None,
        steps=None,
        continue_straight=None,
        annotations=None,
        geometries=None,
        overview=None,
        exclude=None,
        approaches=None,
        banner_instructions=None,
        language=None,
        roundabout_exits=None,
        voice_instructions=None,
        voice_units=None,
        waypoint_names=None,
        waypoint_targets=None,
        dry_run=None,
    ):
        """Get directions between an origin point and a destination point.

        For more information, visit https://docs.mapbox.com/api/navigation/#directions.

        :param locations: The coordinates tuple the route should be calculated
            from in order of visit.
        :type locations: list of list

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
        :type bearings: list of list of int

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
        :type waypoint_targets: list of list of float

        :param dry_run: Print URL and parameters without sending the request.
        :param dry_run: bool

        :returns: One or multiple route(s) from provided coordinates and restrictions.
        :rtype: :class:`routingpy.direction.Direction` or :class:`routingpy.direction.Directions`
        """

        coords = convert.delimit_list(
            [convert.delimit_list([convert.format_float(f) for f in pair]) for pair in locations], ";"
        )

        params = {"coordinates": coords}

        if radiuses:
            params["radiuses"] = convert.delimit_list(radiuses, ";")

        if bearings:
            params["bearings"] = convert.delimit_list(
                [convert.delimit_list(pair) for pair in bearings], ";"
            )

        if alternatives is not None:
            params["alternatives"] = convert.convert_bool(alternatives)

        if steps is not None:
            params["steps"] = convert.convert_bool(steps)

        if continue_straight is not None:
            params["continue_straight"] = convert.convert_bool(continue_straight)

        if annotations is not None:
            params["annotations"] = convert.delimit_list(annotations)

        if geometries:
            params["geometries"] = geometries

        if overview is not None:
            params["overview"] = convert.convert_bool(overview)

        if exclude is not None:
            params["exclude"] = exclude

        if approaches:
            params["approaches"] = ";" + convert.delimit_list(approaches, ";")

        if banner_instructions:
            params["banner_instuctions"] = convert.convert_bool(banner_instructions)

        if language:
            params["language"] = language

        if roundabout_exits:
            params["roundabout_exits"] = convert.convert_bool(roundabout_exits)

        if voice_instructions:
            params["voide_instructions"] = convert.convert_bool(voice_instructions)

        if voice_units:
            params["voice_units"] = voice_units

        if waypoint_names:
            params["waypoint_names"] = convert.delimit_list(waypoint_names, ";")

        if waypoint_targets:
            params["waypoint_targets"] = ";" + convert.delimit_list(
                [
                    convert.delimit_list([convert.format_float(f) for f in pair])
                    for pair in waypoint_targets
                ],
                ";",
            )

        get_params = {"access_token": self.api_key} if self.api_key else {}

        return self._parse_direction_json(
            self.client._request(
                "/directions/v5/mapbox/" + profile,
                get_params=get_params,
                post_params=params,
                dry_run=dry_run,
            ),
            alternatives,
            geometries,
        )

    @staticmethod
    def _parse_direction_json(response, alternatives, geometry_format):
        if response is None:  # pragma: no cover
            if alternatives:
                return Directions()
            else:
                return Direction()

        def _parse_geometry(route_geometry):
            if geometry_format in (None, "polyline"):
                geometry = utils.decode_polyline5(route_geometry, is3d=False)
            elif geometry_format == "polyline6":
                geometry = utils.decode_polyline6(route_geometry, is3d=False)
            elif geometry_format == "geojson":
                geometry = route_geometry["coordinates"]
            else:
                raise ValueError(
                    "OSRM: parameter geometries needs one of ['polyline', 'polyline6', 'geojson']"
                )
            return geometry

        if alternatives:
            routes = []
            for route in response["routes"]:
                routes.append(
                    Direction(
                        geometry=_parse_geometry(route["geometry"]),
                        duration=int(route["duration"]),
                        distance=int(route["distance"]),
                        raw=route,
                    )
                )
            return Directions(routes, response)
        else:
            return Direction(
                geometry=_parse_geometry(response["routes"][0]["geometry"]),
                duration=int(response["routes"][0]["duration"]),
                distance=int(response["routes"][0]["distance"]),
                raw=response,
            )

    def isochrones(
        self,
        locations,
        profile,
        intervals,
        contours_colors=None,
        polygons=None,
        denoise=None,
        generalize=None,
        dry_run=None,
    ):
        """Gets isochrones or equidistants for a range of time values around a given set of coordinates.

        For more information, visit https://github.com/valhalla/valhalla/blob/master/docs/api/isochrone/api-reference.md.

        :param locations: One pair of lng/lat values. Takes the form [Longitude, Latitude].
        :type locations: list of float

        :param profile: Specifies the mode of transport to use when calculating
            directions. One of ["driving", "walking", "cycling".
        :type profile: str

        :param intervals: Time ranges to calculate isochrones for. Up to 4 ranges are possible. In seconds.
        :type intervals: list of int

        :param contours_colors: The color for the output of the contour. Specify it as a Hex value, but without the #, such as
            "color":"ff0000" for red. If no color is specified, the isochrone service will assign a default color to the output.
        :type contours_colors: list of str

        :param polygons: Controls whether polygons or linestrings are returned in GeoJSON geometry. Default False.
        :type polygons: bool

        :param denoise: Can be used to remove smaller contours. In range [0, 1]. A value of 1 will only return the largest contour
            for a given time value. A value of 0.5 drops any contours that are less than half the area of the largest
            contour in the set of contours for that same time value. Default 1.
        :type denoise: float

        :param generalize: A floating point value in meters used as the tolerance for Douglas-Peucker generalization.
            Note: Generalization of contours can lead to self-intersections, as well as intersections of adjacent contours.
        :type generalize: float

        :param dry_run: Print URL and parameters without sending the request.
        :param dry_run: bool

        :returns: An isochrone with the specified range.
        :rtype: :class:`routingpy.isochrone.Isochrones`
        """

        params = {
            "contours_minutes": convert.delimit_list([int(x / 60) for x in sorted(intervals)], ","),
            "access_token": self.api_key,
        }

        locations_string = convert.delimit_list(locations, ",")

        if contours_colors:
            params["contours_colors"] = convert.delimit_list(contours_colors, ",")

        if polygons is not None:
            params["polygons"] = polygons

        if denoise:
            params["denoise"] = denoise

        if generalize:
            params["generalize"] = generalize

        profile = profile.replace("mapbox/", "")

        return self._parse_isochrone_json(
            self.client._request(
                "/isochrone/v1/mapbox/" + profile + "/" + locations_string,
                get_params=params,
                dry_run=dry_run,
            ),
            intervals,
            locations,
        )

    @staticmethod
    def _parse_isochrone_json(response, intervals, locations):
        if response is None:  # pragma: no cover
            return Isochrones()
        return Isochrones(
            [
                Isochrone(
                    geometry=isochrone["geometry"]["coordinates"],
                    interval=intervals[idx],
                    center=locations,
                )
                for idx, isochrone in enumerate(list(reversed(response["features"])))
            ],
            response,
        )

    def matrix(
        self,
        locations,
        profile,
        sources=None,
        destinations=None,
        annotations=None,
        fallback_speed=None,
        dry_run=None,
    ):
        """
        Gets travel distance and time for a matrix of origins and destinations.

        For more information visit https://docs.mapbox.com/api/navigation/#matrix.

        :param locations: The coordinates tuple the route should be calculated
            from in order of visit.
        :type locations: list or tuple

        :param profile: Specifies the mode of transport to use when calculating
            directions. One of ["car", "bike", "foot"].
        :type profile: str

        :param sources: A list of indices that refer to the list of locations
            (starting with 0). If not passed, all indices are considered.
        :type sources: list or tuple

        :param destinations: A list of indices that refer to the list of locations
            (starting with 0). If not passed, all indices are considered.
        :type destinations: list or tuple

        :param annotations: Used to specify the resulting matrices. One or more of ["duration", "distance"]. Default
            ["duration"]
        :type annotations: list of str

        :param fallback_speed: 	By default, if there is no possible route between two points, the Matrix API sets the
            resulting matrix element to null. To circumvent this behavior, set the fallback_speed parameter to a
            value greater than 0 in kilometers per hour. The Matrix API will replace a null value with a straight-line
            estimate between the source and destination based on the provided speed value.
        :type fallback_speed: int

        :param dry_run: Print URL and parameters without sending the request.
        :param dry_run: bool

        :returns: A matrix from the specified sources and destinations.
        :rtype: :class:`routingpy.matrix.Matrix`
        """

        coords = convert.delimit_list(
            [convert.delimit_list([convert.format_float(f) for f in pair]) for pair in locations], ";"
        )

        params = {"access_token": self.api_key}

        if sources:
            params["sources"] = convert.delimit_list(sources, ";")

        if destinations:
            params["destinations"] = convert.delimit_list(destinations, ";")

        if annotations:
            params["annotations"] = convert.delimit_list(annotations)

        if fallback_speed:
            params["fallback_speed"] = str(fallback_speed)

        return self._parse_matrix_json(
            self.client._request(
                "/directions-matrix/v1/mapbox/" + profile + "/" + coords,
                get_params=params,
                dry_run=dry_run,
            )
        )

    @staticmethod
    def _parse_matrix_json(response):
        if response is None:  # pragma: no cover
            return Matrix()

        return Matrix(
            durations=response.get("durations"), distances=response.get("distances"), raw=response
        )
