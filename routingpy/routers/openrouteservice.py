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

from ..client_base import DEFAULT
from ..client_default import Client
from .. import utils
from ..direction import Direction, Directions
from ..isochrone import Isochrone, Isochrones
from ..matrix import Matrix


class ORS:
    """Performs requests to the ORS API services."""

    _DEFAULT_BASE_URL = "https://api.openrouteservice.org"

    def __init__(
        self,
        api_key=None,
        base_url=_DEFAULT_BASE_URL,
        user_agent=None,
        timeout=DEFAULT,
        retry_timeout=None,
        retry_over_query_limit=False,
        skip_api_error=None,
        client=Client,
        **client_kwargs
    ):
        """
        Initializes an openrouteservice client.

        :param api_key: ORS API key. Required if https://api.openrouteservice.org is used.
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

        if base_url == self._DEFAULT_BASE_URL and api_key is None:
            raise KeyError("API key must be specified.")

        client_kwargs = client_kwargs or {}
        headers = client_kwargs.get("headers") or {}
        headers.update({"Authorization": api_key})
        client_kwargs.update({"headers": headers})

        self.client = client(
            base_url,
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
        format="geojson",
        preference=None,
        alternative_routes=None,
        units=None,
        language=None,
        geometry=None,
        geometry_simplify=None,
        instructions=None,
        instructions_format=None,
        roundabout_exits=None,
        attributes=None,
        radiuses=None,
        maneuvers=None,
        bearings=None,
        continue_straight=None,
        elevation=None,
        extra_info=None,
        suppress_warnings=None,
        options=None,
        dry_run=None,
    ):
        """Get directions between an origin point and a destination point.

        For more information, visit https://openrouteservice.org/dev/#/api-docs/v2/directions/{profile}/post

        :param locations: The coordinates tuple the route should be calculated
            from in order of visit.
        :type locations: list of list

        :param profile: Specifies the mode of transport to use when calculating
            directions. One of ["driving-car", "driving-hgv", "foot-walking",
            "foot-hiking", "cycling-regular", "cycling-road",
            "cycling-mountain", "cycling-electric",]. Default "driving-car".
        :type profile: str

        :param format: Specifies the response format. One of ['json', 'geojson']. Default "json".
            Geometry format for "json" is Google's encodedpolyline.
        :type format: str

        :param preference: Specifies the routing preference. One of ["fastest, "shortest",
            "recommended"]. Default fastest.
        :type preference: str

        :param alternative_routes: Specifies whether alternative routes are computed, and parameters
            for the algorithm determining suitable alternatives. Must contain "share_factor", "target_count"
            and "weight_factor".
        :type alternative_routes: dict

        :param units: Specifies the distance unit. One of ["m", "km", "mi"]. Default "m".
        :type units: str

        :param language: Language for routing instructions. One of ["en", "de", "cn",
            "es", "ru", "dk", "fr", "it", "nl", "br", "se", "tr", "gr"].
        :type language: str

        :param geometry: Specifies whether geometry should be returned. Default True.
        :type geometry: bool

        :param geometry_simplify: Specifies whether to simplify the geometry.
            Default False.
        :type geometry_simplify: bool

        :param instructions: Specifies whether to return turn-by-turn instructions.
            Default True.
        :type instructions: bool

        :param instructions_format: Specifies the the output format for instructions.
            One of ["text", "html"]. Default "text".
        :type instructions_format: str

        :param roundabout_exits: Provides bearings of the entrance and all passed
            roundabout exits. Adds the 'exit_bearings' array to the 'step' object
            in the response. Default False.
        :type roundabout_exits: bool

        :param attributes: Returns route attributes on ["avgspeed", "detourfactor", "percentage"].
            Must be a list of strings. Default None.
        :type attributes: list of str

        :param maneuvers: Specifies whether the maneuver object is included into the step object or not. Default: False.
        :type maneuvers: bool

        :param radiuses: A list of maximum distances (measured in
            meters) that limit the search of nearby road segments to every given waypoint.
            The values must be greater than 0, the value of -1 specifies no limit in
            the search. The number of radiuses must correspond to the number of waypoints.
            Default 50 km (ORS backend).
        :type radiuses: list of int

        :param bearings: Specifies a list of pairs (bearings and
            deviations) to filter the segments of the road network a waypoint can
            snap to. For example bearings=[[45,10],[120,20]]. Each pair is a
            comma-separated list that can consist of one or two float values, where
            the first value is the bearing and the second one is the allowed deviation
            from the bearing. The bearing can take values between 0 and 360 clockwise
            from true north. If the deviation is not set, then the default value of
            100 degrees is used. The number of pairs must correspond to the number
            of waypoints. Setting optimized=false is mandatory for this feature to
            work for all profiles. The number of bearings corresponds to the length
            of waypoints-1 or waypoints. If the bearing information for the last waypoint
            is given, then this will control the sector from which the destination
            waypoint may be reached.
        :type bearings: list of list

        :param continue_straight: Forces the route to keep going straight at waypoints not
            restricting u-turns even if u-turns would be faster. Default False.
        :type continue_straight: bool

        :param elevation: Specifies whether to return elevation values for points.
            Default False.
        :type elevation: bool

        :param extra_info: Returns additional information on ["steepness", "suitability",
            "surface", "waycategory", "waytype", "tollways", "traildifficulty", "roadaccessrestrictions"].
            Must be a list of strings. Default None.
        :type extra_info: list of str

        :param suppress_warnings: Tells the system to not return any warning messages in extra_info.
        :type suppress_warnings: bool

        :param options: Refer to https://openrouteservice.org/dev/#/api-docs/v2/directions/{profile}/geojson/post for
            detailed documentation. Construct your own dict() options object and paste it to your code.
        :type options: dict

        :param dry_run: Print URL and parameters without sending the request.
        :type dry_run: bool

        :returns: A route from provided coordinates and restrictions.
        :rtype: :class:`routingpy.direction.Direction`

        """

        params = {"coordinates": locations}

        if preference:
            params["preference"] = preference

        if alternative_routes:
            if not isinstance(alternative_routes, dict):
                raise TypeError("alternative_routes must be a dict.")
            if not all(
                [
                    key in alternative_routes.keys()
                    for key in ["share_factor", "target_count", "weight_factor"]
                ]
            ):
                raise ValueError(
                    "alternative_routes needs 'share_factor', 'target_count', 'weight_factor' keys"
                )
            params["alternative_routes"] = alternative_routes

        if units:
            params["units"] = units

        if language:
            params["language"] = language

        if geometry is not None:
            params["geometry"] = geometry

        if geometry_simplify is not None:
            params["geometry_simplify"] = geometry_simplify

        if instructions is not None:
            params["instructions"] = instructions

        if instructions_format:
            params["instructions_format"] = instructions_format

        if roundabout_exits is not None:
            params["roundabout_exits"] = roundabout_exits

        if attributes:
            params["attributes"] = attributes

        if radiuses:
            params["radiuses"] = radiuses

        if maneuvers is not None:
            params["maneuvers"] = maneuvers

        if bearings:
            params["bearings"] = bearings

        if continue_straight is not None:
            params["continue_straight"] = continue_straight

        if elevation is not None:
            params["elevation"] = elevation

        if extra_info:
            params["extra_info"] = extra_info

        if suppress_warnings is not None:
            params["suppress_warnings"] = suppress_warnings

        if options:
            if profile == "driving-hgv" and options.get("profile_params"):
                if options["profile_params"].get("restrictions") and not options.get("vehicle_type"):
                    raise ValueError(
                        "ORS: options.vehicle_type must be specified for driving-hgv if restrictions are set."
                    )
            params["options"] = options

        return self._parse_direction_json(
            self.client._request(
                "/v2/directions/" + profile + "/" + format,
                get_params={},
                post_params=params,
                dry_run=dry_run,
            ),
            format,
            units,
            alternative_routes,
        )

    @staticmethod
    def _parse_direction_json(response, format, units, alternative_routes):
        if response is None:  # pragma: no cover
            return Direction()

        units_factor = 1
        if units == "mi":
            units_factor = 0.621371 * 1000
        elif units == "km":
            units_factor = 1000

        if format == "geojson":
            if alternative_routes:
                routes = []
                for route in response["features"]:
                    routes.append(
                        Direction(
                            geometry=route["geometry"]["coordinates"],
                            distance=int(route["properties"]["summary"]["distance"]),
                            duration=int(route["properties"]["summary"]["duration"]),
                            raw=route,
                        )
                    )
                return Directions(routes, response)
            else:
                geometry = response["features"][0]["geometry"]["coordinates"]
                duration = int(response["features"][0]["properties"]["summary"]["duration"])
                distance = int(response["features"][0]["properties"]["summary"]["distance"])
                return Direction(geometry=geometry, duration=duration, distance=distance, raw=response)
        elif format == "json":
            if alternative_routes:
                routes = []
                for route in response["routes"]:
                    geometry = [
                        list(reversed(coord)) for coord in utils.decode_polyline5(route["geometry"])
                    ]
                    routes.append(
                        Direction(
                            geometry=geometry,
                            distance=int(route["summary"]["distance"]),
                            duration=int(route["summary"]["duration"] * units_factor),
                            raw=route,
                        )
                    )
                return Directions(routes, response)
            else:
                geometry = utils.decode_polyline5(response["routes"][0]["geometry"])
                duration = int(response["routes"][0]["summary"]["duration"])
                distance = int(response["routes"][0]["summary"]["distance"] * units_factor)

                return Direction(geometry=geometry, duration=duration, distance=distance, raw=response)

    def isochrones(
        self,
        locations,
        profile,
        intervals,
        interval_type=None,
        units=None,
        location_type=None,
        smoothing=None,
        attributes=None,
        intersections=None,
        dry_run=None,
    ):
        """Gets isochrones or equidistants for a range of time/distance values around a given set of coordinates.

        :param locations: One pair of lng/lat values.
        :type locations: list of float

        :param profile: Specifies the mode of transport to use when calculating
            directions. One of ["driving-car", "driving-hgv", "foot-walking",
            "foot-hiking", "cycling-regular", "cycling-safe", "cycling-mountain",
            "cycling-electric",]. Default "driving-car".
        :type profile: str

        :param interval_type: Set 'time' for isochrones or 'distance' for equidistants.
            Default 'time'.
        :type interval_type: str

        :param intervals: Ranges to calculate distances/durations for. This can be
            a list of multiple ranges, e.g. [600, 1200, 1400]. In meters or seconds.
        :type intervals: list of int

        :param units: Specifies the unit system to use when displaying results.
            One of ["m", "km", "m"]. Default "m".
        :type units: str

        :param location_type: 'start' treats the location(s) as starting point,
            'destination' as goal. Default 'start'.
        :type location_type: str

        :param smoothing: Applies a level of generalisation to the isochrone polygons generated.
            Value between 0 and 1, whereas a value closer to 1 will result in a more generalised shape.
        :type smoothing: float

        :param attributes: 'area' returns the area of each polygon in its feature
            properties. 'reachfactor' returns a reachability score between 0 and 1.
            'total_pop' returns population statistics from https://ghsl.jrc.ec.europa.eu/about.php.
            One or more of ['area', 'reachfactor', 'total_pop']. Default 'area'.
        :type attributes: list of str

        :param intersections: Write smth.
        :type intersections: bool

        :param dry_run: Print URL and parameters without sending the request.
        :param dry_run: bool

        :returns: An isochrone with the specified range.
        :rtype: :class:`routingpy.isochrone.Isochrones`
        """

        params = {
            "locations": [locations],
            "profile": profile,
            "range": intervals,
        }

        if interval_type:
            params["range_type"] = interval_type

        if units:
            params["units"] = units

        if location_type:
            params["location_type"] = location_type

        if smoothing:
            params["smoothing"] = smoothing

        if attributes:
            params["attributes"] = attributes

        if intersections:
            params["intersections"] = intersections

        return self._parse_isochrone_json(
            self.client._request(
                "/v2/isochrones/" + profile + "/geojson",
                get_params={},
                post_params=params,
                dry_run=dry_run,
            )
        )

    @staticmethod
    def _parse_isochrone_json(response):
        if response is None:  # pragma: no cover
            return Isochrones()

        isochrones = []
        for idx, isochrone in enumerate(response["features"]):
            isochrones.append(
                Isochrone(
                    geometry=isochrone["geometry"]["coordinates"][0],
                    interval=isochrone["properties"]["value"],
                    center=isochrone["properties"]["center"],
                )
            )

        return Isochrones(isochrones=isochrones, raw=response)

    def matrix(
        self,
        locations,
        profile,
        sources=None,
        destinations=None,
        metrics=None,
        resolve_locations=None,
        units=None,
        dry_run=None,
    ):
        """Gets travel distance and time for a matrix of origins and destinations.

        :param locations: Two or more pairs of lng/lat values.
        :type locations: list of list

        :param profile: Specifies the mode of transport to use when calculating
            directions. One of ["driving-car", "driving-hgv", "foot-walking",
            "foot-hiking", "cycling-regular", "cycling-road", "cycling-mountain",
            "cycling-electric",]. Default "driving-car".
        :type profile: str

        :param sources: A list of indices that refer to the list of locations
            (starting with 0). If not passed, all indices are considered.
        :type sources: list of int

        :param destinations: A list of indices that refer to the list of locations
            (starting with 0). If not passed, all indices are considered.
        :type destinations: list of int

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

        :returns: A matrix from the specified sources and destinations.
        :rtype: :class:`routingpy.matrix.Matrix`
        """

        params = {"locations": locations, "profile": profile}

        if sources:
            params["sources"] = sources

        if destinations:
            params["destinations"] = destinations

        if metrics:
            params["metrics"] = metrics

        if resolve_locations is not None:
            params["resolve_locations"] = resolve_locations

        if units:
            params["units"] = units

        return self._parse_matrix_json(
            self.client._request(
                "/v2/matrix/" + profile + "/json", get_params={}, post_params=params, dry_run=dry_run
            )
        )

    @staticmethod
    def _parse_matrix_json(response):
        if response is None:  # pragma: no cover
            return Matrix()
        durations = response.get("durations")
        distances = response.get("distances")
        return Matrix(durations=durations, distances=distances, raw=response)
