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
from .. import convert
from ..direction import Direction, Directions
from ..isochrone import Isochrones, Isochrone
from ..matrix import Matrix

from operator import itemgetter


class HereMaps:
    """Performs requests to the HERE Maps API services."""

    def __init__(
        self,
        app_id=None,
        app_code=None,
        user_agent=None,
        timeout=DEFAULT,
        retry_timeout=None,
        retry_over_query_limit=False,
        skip_api_error=None,
        api_key=None,
        client=Client,
        **client_kwargs
    ):
        """
        Initializes a HERE Maps client.

        :param app_id: HERE Maps app id.
        :type app_id: str

        :param app_code: HERE Maps app code.
        :type app_code: str

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

        if app_id is None and app_code is None and api_key is None:
            raise KeyError("HERE Maps app_id and app_code, or api_key must be specified.")
        if (app_id is not None or app_code is not None) and api_key is not None:
            raise KeyError(
                "Either HERE Maps app_id and app_code, or api_key can be specified, not both."
            )

        self.app_code = app_code
        self.app_id = app_id
        self.api_key = api_key

        if self.api_key:
            self.auth = {"apikey": self.api_key}
        else:
            self.auth = {"app_id": self.app_id, "app_code": self.app_code}

        self.client = client(
            "",
            user_agent,
            timeout,
            retry_timeout,
            retry_over_query_limit,
            skip_api_error,
            **client_kwargs
        )

    class Waypoint(object):
        """
        Constructs a waypoint with additional information.
        https://developer.here.com/documentation/routing/topics/resource-param-type-waypoint.html

        Example:

        >>> waypoint = HereMaps.Waypoint(position=[8.15315, 52.53151], waypoint_type='passThrough', stopover_duration=120, transit_radius=500)
        >>> route = HereMaps(api_key).directions(locations=[[[8.58232, 51.57234]], waypoint, [7.15315, 53.632415]])
        """

        def __init__(
            self,
            position,
            waypoint_type=None,
            stopover_duration=None,
            transit_radius="",
            user_label="",
            heading="",
        ):
            """
            :param position: Indicates that the parameter contains a geographical position.
            :type position: list

            :param waypoint_type: 180 degree turns are allowed for ``stopOver`` but not for ``passThrough``.
                Waypoints defined through a drag-n-drop action should be marked as passThrough.
                PassThrough waypoints will not appear in the list of maneuvers.
            :type waypoint_type: str

            :param stopover_duration: Stopover delay in seconds.
                Impacts time-aware calculations. Ignored for passThrough.
            :type stopover_duration: int

            :param transit_radius: Matching Links are selected within the
                specified TransitRadius, in meters.
                For example to drive past a city without necessarily going into the
                city center you can specify the coordinates of the center and a
                TransitRadius of 5000m.
            :type transit_radius: int

            :param user_label: Custom label identifying this waypoint.
            :type user_label: str

            :param heading: Heading in degrees starting at true north and continuing
                clockwise around the compass.
                North is 0 degrees, East is 90 degrees, South is 180 degrees,
                and West is 270 degrees.
            :type heading: int
            """

            self.position = position
            self.waypoint_type = waypoint_type
            self.stopover_duration = stopover_duration
            self.transit_radius = str(transit_radius)
            self.user_label = user_label
            self.heading = str(heading)

        def _make_waypoint(self):

            here_waypoint = ["geo"]
            if self.waypoint_type is not None and self.stopover_duration is not None:
                here_waypoint.append(
                    convert.delimit_list([self.waypoint_type, self.stopover_duration], ",")
                )
            elif self.waypoint_type is not None:
                here_waypoint.append(self.waypoint_type)

            position = convert.delimit_list(
                [convert.format_float(f) for f in list(reversed(self.position))], ","
            )
            position += ";" + self.transit_radius
            position += ";" + self.user_label
            position += ";" + self.heading
            here_waypoint.append(position)
            return convert.delimit_list(here_waypoint, "!")

    class RoutingMode(object):
        """
        Optionally construct the routing profile from this class with additional attributes.
        https://developer.here.com/documentation/routing/topics/resource-param-type-routing-mode.html

        Example

        >>> profile = HereMaps.RoutingMode(mode_type='shortest', mode_transport_type='truck', mode_traffic=True, features={'motorway': -2})
        >>> route = HereMaps(api_key).directions(locations=location_list, profile=profile)

        """

        def __init__(
            self, mode_type="fastest", mode_transport_type="car", mode_traffic=None, features=None
        ):
            """
            :param mode_type: RoutingType relevant to calculation.
            :type mode_type: str

            :param mode_transport_type: Specify which mode of transport to calculate the route for.
            :type mode_transport_type: str

            :param mode_traffic: Specify whether to optimize a route for traffic.
            :type mode_traffic: bool

            :param features: Route feature weightings to be applied when calculating
                the route. As many as required.
            :type features: dict
            """

            self.mode_type = mode_type
            self.mode_transport_type = mode_transport_type
            self.mode_traffic = mode_traffic
            self.features = features

        def make_routing_mode(self):

            routing_mode = []
            routing_mode.append(self.mode_type)
            routing_mode.append(self.mode_transport_type)

            if self.mode_traffic is not None:
                routing_mode.append("traffic:" + self.mode_traffic)

            if self.features is not None:
                get_features = []
                for f, w in self.features.items():
                    get_features.append(convert.delimit_list([f, str(w)], ":"))
                routing_mode.append(convert.delimit_list(get_features, ","))
            return convert.delimit_list(routing_mode, ";")

    def directions(  # noqa: C901
        self,
        locations,
        profile,
        mode_type="fastest",
        format="json",
        request_id=None,
        avoid_areas=None,
        avoid_links=None,
        avoid_seasonal_closures=None,
        avoid_turns=None,
        allowed_zones=None,
        exclude_zones=None,
        exclude_zone_types=None,
        exclude_countries=None,
        arrival=None,
        departure=None,
        alternatives=None,
        metric_system=None,
        view_bounds=None,
        resolution=None,
        instruction_format=None,
        language=None,
        json_attributes=None,
        json_callback=None,
        representation=None,
        route_attributes=["waypoints", "summary", "shape", "boundingBox", "legs"],
        leg_attributes=None,
        maneuver_attributes=None,
        link_attributes=None,
        line_attributes=None,
        generalization_tolerances=None,
        vehicle_type=None,
        license_plate=None,
        max_number_of_changes=None,
        avoid_transport_types=None,
        walk_time_multiplier=None,
        walk_speed=None,
        walk_radius=None,
        combine_change=None,
        truck_type=None,
        trailers_count=None,
        shipped_hazardous_goods=None,
        limited_weight=None,
        weight_per_axle=None,
        height=None,
        width=None,
        length=None,
        tunnel_category=None,
        truck_restriction_penalty=None,
        return_elevation=None,
        consumption_model=None,
        custom_consumption_details=None,
        speed_profile=None,
        dry_run=None,
        **directions_kwargs
    ):
        """Get directions between an origin point and a destination point.

        Use ``direction_kwargs`` for any missing ``directions`` request options.

        For more information, https://developer.here.com/documentation/routing/topics/resource-calculate-route.html.

        :param locations: The coordinates tuple the route should be calculated
            from in order of visit. Can be a list/tuple of [lon, lat] or :class:`HereMaps.Waypoint` instance or a
            combination of those. For further explanation, see
            https://developer.here.com/documentation/routing/topics/resource-param-type-waypoint.html
        :type locations: list of list or list of :class:`HereMaps.Waypoint`

        :param profile: Specifies the routing mode of transport and further options.
            Can be a str and one of [car, pedestrian, carHOV, publicTransport, publicTransportTimeTable, truck, bicycle]
            or :class:`HereMaps.RoutingMode`.
            https://developer.here.com/documentation/routing/topics/resource-param-type-routing-mode.html
        :type profile: str or :class:`HereMaps.RoutingMode`

        :param mode_type: RoutingType relevant to calculation. One of [fastest, shortest, balanced]. Default fastest.
            https://developer.here.com/documentation/routing/topics/resource-param-type-routing-mode.html#ariaid-title2
        :type mode_type: str

        :param format: Currently only "json" supported.
        :type format: str

        :param request_id: Clients may pass in an arbitrary string to trace request
            processing through the system. The RequestId is mirrored in the MetaInfo
            element of the response structure.
        :type request_id: str

        :param avoid_areas: Areas which the route must not cross. Array of BoundingBox.
            Example with 2 bounding boxes
            https://developer.here.com/documentation/routing/topics/resource-param-type-bounding-box.html
        :type avoid_areas: list of list of list

        :param avoid_links: Links which the route must not cross. The list of LinkIdTypes.
        :type avoid_areas: list of str

        :param avoid_seasonal_closures: The optional avoid seasonal closures boolean
            flag can be specified to avoid usage of seasonally closed links.
            Examples of seasonally closed links are roads that may be closed during the
            winter due to weather conditions or ferries that may be out of operation
            for the season (based on past closure dates).
        :type avoid_seasonal_closures: bool

        :param avoid_turns: List of turn types that the route should avoid.
            Defaults to empty list.
            https://developer.here.com/documentation/routing/topics/resource-type-enumerations.html
        :type avoid_turns: str

        :param allowed_zones: Identifiers of zones where routing engine should
            not take zone restrictions into account (for example in case of a
            special permission to access a restricted environmental zone).
            https://developer.here.com/documentation/routing/topics/resource-get-routing-zones.html
        :type allowed_zones: list of int

        :param exclude_zones: Identifiers of zones which the route must not cross
            under any circumstances.
            https://developer.here.com/documentation/routing/topics/resource-get-routing-zones.html
        :type exclude_zones: list of int

        :param exclude_zone_types: List of zone types which the route must not
            cross under any circumstances.
            https://developer.here.com/documentation/routing/topics/resource-type-enumerations.html
            #resource-type-enumerations__enum-routing-zone-type-type
        :type exclude_zone_types: list of str

        :param exclude_countries: Countries that must be excluded from route calculation.
        :type exclude_zone_types: list of str

        :param departure: Time when travel is expected to start. Traffic speed and
            incidents are taken into account
            when calculating the route (note that in case of a past
            departure time the historical traffic is limited to one year).
            You can use now to specify the current time. Specify either departure
            or arrival, not both. When the optional timezone offset is not
            specified, the time is assumed to be the local.
            Formatted as iso time, e.g. 2018-07-04T17:00:00+02.
        :type departure: str

        :param arrival: Time when travel is expected to end. Specify either
            departure or arrival, not both.
            When the optional timezone offset is not specified, the time is assumed to be the local.
            Formatted as iso time, e.g. 2018-07-04T17:00:00+02.
        :type arrival: str

        :param alternatives: Maximum number of alternative routes that will be
            calculated and returned. Alternative routes can be unavailable, thus
            they are not guaranteed to be returned. If at least one via point is used
            in a route request, returning alternative routes is not supported.
            0 stands for "no alternative routes", i.e. only best route is returned.
        :type alternatives: int

        :param metric_system: Defines the measurement system used in instruction text.
            When imperial is selected, units used are based on the language specified
            in the request. Defaults to metric when not specified.
        :type metric_system: str

        :param view_bounds: If the view bounds are given in the request then only
            route shape points which fit into these bounds will be returned.
            The route shape beyond the view bounds is reduced to the points which
            are referenced by links, legs or maneuvers.
        :type view_bounds: list or tuple

        :param resolution: Specifies the resolution of the view and a possible snap
            resolution in meters per pixel in the response. You must specify a whole, positive integer.
            If you specify only one value, then this value defines the view resolution only.
            You can use snap resolution to adjust waypoint links to the resolution of the client display.
            e.g. {'viewresolution': 300,'snapresolution': 300}
        :type resolution: dict

        :param instruction_format: Defines the representation format of the maneuver's instruction text. Html or txt.
        :type instruction_format: str

        :param language: A list of languages for all textual information,
            the first supported language is used. If there are no matching supported
            languages the response is an error. Defaults to en-us.
            https://developer.here.com/documentation/routing/topics/resource-param-type-languages.html#languages
        :type language: str

        :param json_attributes: Flag to control JSON output. Combine parameters
            by adding their values.
            https://developer.here.com/documentation/routing/topics/resource-param-type-json-representation.html
        :type json_attributes: int

        :param json_callback: Name of a user-defined function used to wrap the JSON response.
        :type json_callback: str

        :param representation: Define which elements are included in the response
            as part of the data representation
            of the route.
            https://developer.here.com/documentation/routing/topics/resource-param-type-route-representation-options.html#type-route-represenation-mode
        :type representation: list of str

        :param route_attributes: Define which attributes are included in the
            response as part of the data representation of the route. Defaults to
            waypoints, summary, legs and additionally lines if publicTransport or
            publicTransportTimeTable mode is used.
            https://developer.here.com/documentation/routing/topics/resource-param-type-route-representation-options.html#type-route-attribute
        :type route_attributes: list of str

        :param leg_attributes: Define which attributes are included in the response
            as part of the data representation
            of the route legs. Defaults to maneuvers, waypoint, length, travelTime.
            https://developer.here.com/documentation/routing/topics/resource-param-type-route-representation-options.html#type-route-leg-attribute
        :type leg_attributes: list of str

        :param maneuver_attributes: Define which attributes are included in the
            response as part of the data
            representation of the route maneuvers. Defaults to position, length, travelTime.
            https://developer.here.com/documentation/routing/topics/resource-param-type-route-representation-options.html#type-maneuver-attribute
        :type maneuver_attributes: list of str

        :param link_attributes: Define which attributes are included in the response
            as part of the data representation of the route links. Defaults to shape, speedLimit.
            https://developer.here.com/documentation/routing/topics/resource-param-type-route-representation-options.html#type-route-link-attribute
        :type link_attributes: list of str

        :param line_attributes: Sequence of attribute keys of the fields that are
            included in public transport line elements. If not specified,
            defaults to lineForeground, lineBackground.
            https://developer.here.com/documentation/routing/topics/resource-param-type-route-representation-options.html#type-public-transport-line-attribute
        :type line_attributes: list of str

        :param generalization_tolerances: Specifies the desired tolerances for
            generalizations of the base route geometry. Tolerances are given in
            degrees of longitude or latitude on a spherical approximation of the Earth.
            One meter is approximately equal to 0:00001 degrees at typical latitudes.
        :type generalization_tolerances: list of float

        :param param vehicle_type: Specifies type of vehicle engine and average
            fuel consumption, which can be used to estimate CO2 emission for
            the route summary.
            https://developer.here.com/documentation/routing/topics/resource-param-type-vehicle-type.html
        :type vehicle_type: str

        :param param license_plate: Specifies fragments of vehicle's license plate number.
            The lastcharacter is currently the only supported fragment type.
            The license plate parameter enables evaluation of license plate
            based vehicle restrictions like odd/even scheme in Indonesia.
        :type license_plate: str

        :param max_number_of_changes: Restricts number of changes in a public
            transport route to a given value. The parameter does not filter resulting
            alternatives. Instead, it affects route calculation so that only
            routes containing at most the given number of changes are considered.
            The provided value must be between 0 and 10.
        :type max_number_of_changes: int

        :param avoid_transport_types: Public transport types that shall not be included
            in the response route. Please refer to Enumeration Types for a list of supported values.
            https://developer.here.com/documentation/routing/topics/resource-type-enumerations.html
        :type avoid_transport_types: list of str

        :param walk_time_multiplier: Allows to prefer or avoid public transport
            routes with longer walking distances. A value > 1.0 means a slower
            walking speed and will prefer routes with less walking distance.
            The provided value must be between 0.01 and 100.
        :type walk_time_multiplier: float

        :param walk_speed: Specifies speed which will be used by a service as a
            walking speed for pedestrian routing (meters per second).
            This parameter affects pedestrian, publicTransport and publicTransportTimetable modes.
            The provided value must be between 0.5 and 2.
        :type walk_speed: float

        :param walk_radius: Allows the user to specify a maximum distance to the
            start and end stations of a public transit route. Only valid for
            publicTransport and publicTransportTimetable routes.
            The provided value must be between 0 and 6000.
        :type walk_radius: int

        :param combine_change: Enables the change maneuver in the route response,
            which indicates a public transit line change. In the absence of this
            maneuver, each line change is represented with a pair of subsequent enter
            and leave maneuvers. We recommend enabling combineChange behavior wherever
            possible, to simplify client-side development.
        :type combine_change: bool

        :param truck_type: Truck routing only, specifies the vehicle type. Defaults to truck.
        :type truck_type: str

        :param trailers_count: Truck routing only, specifies number of trailers
            pulled by a vehicle. The provided value must be between 0 and 4.
            Defaults to 0.
        :type trailers_count: int

        :param shipped_hazardous_goods: Truck routing only, list of hazardous
            materials in the vehicle. Please refer to the enumeration type
            HazardousGoodTypeType for available values.
            Note the value allhazardousGoods does not apply to the request parameter.
            https://developer.here.com/documentation/routing/topics/resource-type-enumerations.html#resource-type-enumerations__enum-hazardous-good-type-type
        :type shipped_hazardous_goods: list of str

        :param limited_weight: Truck routing only, vehicle weight including
            trailers and shipped goods, in tons. The provided value must be between 0 and 1000.
        :type limited_weight: int

        :param weight_per_axle: Truck routing only, vehicle weight per axle in
            tons. The provided value must be between 0 and 1000.
        :type limited_weight: int

        :param height: Truck routing only, vehicle height in meters.
            The provided value must be between 0 and 50.
        :type height: int

        :param width: Truck routing only, vehicle width in meters.
            The provided value must be between 0 and 50.
        :type width: int

        :param length: Truck routing only, vehicle length in meters.
            The provided value must be between 0 and 300.
        :type length: int

        :param tunnel_category: Truck routing only, specifies the tunnel category
            to restrict certain route links. The route will pass only through tunnels
            of a less strict category.
        :type tunnel_category: list of str

        :param truck_restriction_penalty: Truck routing only, specifies the
            penalty type on violated truck restrictions. Defaults to strict.
            Refer to the enumeration type TruckRestrictionPenaltyType for
            details on available values.
            https://developer.here.com/documentation/routing/topics/resource-type-enumerations.html#resource-type-enumerations__enum-truck-restriction-penalty-type
        :type truck_restriction_penalty: str

        :param return_elevation: If set to true, all shapes inside routing response
            will consist of 3 values instead of 2. Third value will be elevation.
            If there are no elevation data available for given shape point,
            elevation will be interpolated from surrounding points. In case
            there is no elevation data available for any of the shape points,
            elevation will be 0.0. If jsonattributes=32, elevation cannot be returned.
        :type return_elevation: bool

        :param consumption_model: If you request information on consumption,
            you must provide a consumption model. The possible values are default
            and standard. When you specify the value standard, you must provide
            additional information in the query parameter customconsumptiondetails
        :type consumption_model: str

        :param custom_consumption_details: Provides vehicle specific information
            for use in the consumption model. This information can include such
            things as the amount of energy consumed while travelling at a given speed.
            https://developer.here.com/documentation/routing/topics/resource-param-type-custom-consumption-details.html#type-standard
        :type custom_consumption_details: str

        :param speed_profile: Specifies the speed profile variant for a given routing mode.
            The speed profile affects travel time estimation as well as roads evaluation
            when computing the fastest route. Note that computed routes might differ depending on a used profile.
            https://developer.here.com/documentation/routing/topics/resource-param-type-speed-profile-type.html
        :type speed_profile: str

        :param dry_run: Print URL and parameters without sending the request.
        :param dry_run: bool

        :returns: One or multiple route(s) from provided coordinates and restrictions.
        :rtype: :class:`routingpy.direction.Direction` or :class:`routingpy.direction.Directions`
        """

        self.client.base_url = (
            "https://route.api.here.com/routing/7.2"
            if self.api_key is None
            else "https://route.ls.hereapi.com/routing/7.2"
        )

        params = self.auth.copy()

        locations = self._build_locations(locations)

        for idx, wp in enumerate(locations):
            wp_index = "waypoint" + str(idx)
            params[wp_index] = wp

        if isinstance(profile, str):
            params["mode"] = mode_type + ";" + profile
        elif isinstance(profile, self.RoutingMode):
            params["mode"] = profile.make_routing_mode()

        if request_id is not None:
            params["requestId"] = request_id

        if avoid_areas is not None:
            params["avoidAreas"] = convert.delimit_list(
                [
                    convert.delimit_list(
                        [
                            convert.delimit_list(
                                [convert.format_float(f) for f in list(reversed(pair))], ","
                            )
                            for pair in bounding_box
                        ],
                        ";",
                    )
                    for bounding_box in avoid_areas
                ],
                "!",
            )

        if avoid_links is not None:
            params["avoidLinks"] = convert.delimit_list(avoid_links, ",")

        if avoid_seasonal_closures is not None:
            params["avoidSeasonalClosures"] = convert.convert_bool(avoid_seasonal_closures)

        if avoid_turns is not None:
            params["avoidTurns"] = avoid_turns

        if allowed_zones is not None:
            params["allowedZones"] = convert.delimit_list(allowed_zones, ",")

        if exclude_zones is not None:
            params["excludeZones"] = convert.delimit_list(exclude_zones, ",")

        if exclude_zone_types is not None:
            params["excludeZoneTypes"] = convert.delimit_list(exclude_zone_types, ",")

        if exclude_countries is not None:
            params["excludeCountries"] = convert.delimit_list(exclude_countries, ",")

        if departure is not None:
            params["departure"] = departure
        elif arrival is not None:
            params["arrival"] = arrival

        if alternatives is not None:
            params["alternatives"] = alternatives

        if metric_system is not None:
            params["metricSystem"] = metric_system

        if view_bounds is not None:
            params["viewBounds"] = convert.delimit_list(
                [
                    convert.delimit_list([convert.format_float(f) for f in list(reversed(pair))], ",")
                    for pair in view_bounds
                ],
                ";",
            )

        if resolution is not None:
            params["resolution"] = str(resolution["viewresolution"])
            if "snapresolution" in resolution:
                params["resolution"] += ":" + str(resolution["snapresolution"])

        if instruction_format is not None:
            params["instructionFormat"] = instruction_format

        if json_attributes is not None:
            params["jsonAttributes"] = json_attributes

        if json_callback is not None:
            params["jsonCallback"] = json_callback

        if representation is not None:
            params["representation"] = convert.delimit_list(representation, ",")

        if route_attributes is not None:
            params["routeAttributes"] = convert.delimit_list(route_attributes, ",")

        if leg_attributes is not None:
            params["legAttributes"] = convert.delimit_list(leg_attributes, ",")

        if maneuver_attributes is not None:
            params["maneuverAttributes"] = convert.delimit_list(maneuver_attributes, ",")

        if link_attributes is not None:
            params["linkAttributes"] = convert.delimit_list(link_attributes, ",")

        if line_attributes is not None:
            params["lineAttributes"] = convert.delimit_list(line_attributes, ",")

        if generalization_tolerances is not None:
            params["generalizationTolerances"] = convert.delimit_list(generalization_tolerances, ",")

        if vehicle_type is not None:
            params["vehicleType"] = vehicle_type

        if license_plate is not None:
            params["licensePlate"] = license_plate

        if max_number_of_changes is not None:
            params["maxNumberOfChanges"] = max_number_of_changes

        if avoid_transport_types is not None:
            params["avoidTransportTypes"] = convert.delimit_list(avoid_transport_types, ",")

        if walk_time_multiplier is not None:
            params["walkTimeMultiplier"] = walk_time_multiplier

        if walk_speed is not None:
            params["walkSpeed"] = walk_speed

        if walk_radius is not None:
            params["walkRadius"] = walk_radius

        if combine_change is not None:
            params["combineChange"] = convert.convert_bool(combine_change)

        if truck_type is not None:
            params["truckType"] = truck_type

        if trailers_count is not None:
            params["trailersCount"] = trailers_count

        if shipped_hazardous_goods is not None:
            params["shippedHazardousGoods"] = convert.delimit_list(shipped_hazardous_goods, ",")

        if limited_weight is not None:
            params["limitedWeight"] = limited_weight

        if weight_per_axle is not None:
            params["weightPerAxle"] = weight_per_axle

        if height is not None:
            params["height"] = height

        if width is not None:
            params["width"] = width

        if length is not None:
            params["length"] = length

        if tunnel_category is not None:
            params["tunnelCategory"] = convert.delimit_list(tunnel_category, ",")

        if truck_restriction_penalty is not None:
            params["truckRestrictionPenalty"] = truck_restriction_penalty

        if return_elevation is not None:
            params["returnElevation"] = convert.convert_bool(return_elevation)

        if consumption_model is not None:
            params["consumptionModel"] = consumption_model

        if custom_consumption_details is not None:
            params["customConsumptionDetails"] = custom_consumption_details

        if speed_profile is not None:
            params["speedProfile"] = speed_profile

        params.update(directions_kwargs)

        return self._parse_direction_json(
            self.client._request(
                convert.delimit_list(["/calculateroute", format], "."),
                get_params=params,
                dry_run=dry_run,
            ),
            alternatives=alternatives,
        )

    @staticmethod
    def _parse_direction_json(response, alternatives):
        if response is None:  # pragma: no cover
            if alternatives:
                return Directions()
            else:
                return Direction()

        if alternatives is not None and alternatives > 1:
            routes = []
            for route in response["response"]["route"]:
                routes.append(
                    Direction(
                        geometry=[
                            list(reversed(list((map(float, coordinates.split(","))))))
                            for coordinates in route["shape"]
                        ],
                        duration=int(route["summary"]["baseTime"]),
                        distance=int(route["summary"]["distance"]),
                        raw=route,
                    )
                )

            return Directions(directions=routes, raw=response)

        else:
            geometry = [
                list(reversed(list(map(float, coordinates.split(",")))))
                for coordinates in response["response"]["route"][0].get("shape")
            ]
            duration = int(response["response"]["route"][0]["summary"].get("baseTime"))
            distance = int(response["response"]["route"][0]["summary"].get("distance"))

            return Direction(geometry=geometry, duration=duration, distance=distance, raw=response)

    def isochrones(  # noqa: C901
        self,
        locations,
        profile,
        intervals,
        mode_type="fastest",
        interval_type="time",
        format="json",
        center_type="start",
        request_id=None,
        arrival=None,
        departure=None,
        single_component=None,
        resolution=None,
        max_points=None,
        quality=None,
        json_attributes=None,
        json_callback=None,
        truck_type=None,
        trailers_count=None,
        shipped_hazardous_goods=None,
        limited_weight=None,
        weight_per_axle=None,
        height=None,
        width=None,
        length=None,
        tunnel_category=None,
        consumption_model=None,
        custom_consumption_details=None,
        speed_profile=None,
        dry_run=None,
        **isochrones_kwargs
    ):
        """Gets isochrones or equidistants for a range of time/distance values around a given set of coordinates.

        Use ``isochrones_kwargs`` for any missing ``isochrones`` request options.

        For more information, https://developer.here.com/documentation/routing/topics/resource-calculate-isoline.html.

        :param locations: One pair of lng/lat values.
        :type locations: list of float

        :param profile: Specifies the routing mode of transport and further options.
            Can be a str or :class:`HereMaps.RoutingMode`
            https://developer.here.com/documentation/routing/topics/resource-param-type-routing-mode.html
        :type profile: str or :class:`HereMaps.RoutingMode`

        :param intervals: Range of isoline. Several comma separated values can be specified.
            The unit is defined by parameter rangetype.
        :type ranges: list of int

        :param mode_type: RoutingType relevant to calculation. One of [fastest, shortest, balanced]. Default fastest.
            https://developer.here.com/documentation/routing/topics/resource-param-type-routing-mode.html#ariaid-title2
        :type mode_type: str

        :param interval_type: Specifies type of range. Possible values are distance,
            time, consumption. For distance the unit is meters. For time the unit is seconds.
            For consumption it is defined by consumption model
        :type range_type: str

        :param format: Currently only "json" supported.
        :type format: str

        :param center_type: If 'start' then the isoline will cover all roads which
            can be reached from this point within given range.
            It cannot be used in combination with destination parameter.
            If 'destination' Center of the isoline request. Isoline will cover all
            roads from which this point can be reached within given range.
            It cannot be used in combination with start parameter.
        :type center_type: str

        :param departure: Time when travel is expected to start. Traffic speed and
            incidents are taken into account
            when calculating the route (note that in case of a past
            departure time the historical traffic is limited to one year).
            You can use now to specify the current time. Specify either departure
            or arrival, not both. When the optional timezone offset is not
            specified, the time is assumed to be the local.
            Formatted as iso time, e.g. 2018-07-04T17:00:00+02.
        :type departure: str

        :param arrival: Time when travel is expected to end. Specify either
            departure or arrival, not both.
            When the optional timezone offset is not specified, the time is
            assumed to be the local.
            Formatted as iso time, e.g. 2018-07-04T17:00:00+02.
        :type arrival: str

        :param single_component: If set to true the isoline service will always
            return single polygon, instead of creating a separate polygon
            for each ferry separated island. Default value is false.
        :type single_component: bool

        :param resolution: Allows to specify level of detail needed for the
            isoline polygon. Unit is meters per pixel. Higher resolution may
            cause increased response time from the service.
        :type resolution: int

        :param max_points: Allows to limit amount of points in the returned
            isoline. If isoline consists of multiple components, sum of points from
            all components is considered. Each component will have at least 2 points,
            so it is possible that more points than maxpoints value will be returned.
            This is in case when 2 * number of components is higher than maxpoints.
            Enlarging number of maxpoints may cause increased response time from the service.
        :type max_points: int

        :param quality: Allows to reduce the quality of the isoline in favor
            of the response time. Allowed values are 1, 2, 3.
            Default value is 1 and it is the best quality.
        :type quality: int

        :param json_attributes: Flag to control JSON output.
            Combine parameters by adding their values.
            https://developer.here.com/documentation/routing/topics/resource-param-type-json-representation.html
        :type json_attributes: int

        :param truck_type: Truck routing only, specifies the vehicle type. Defaults to truck.
        :type truck_type: str

        :param trailers_count: Truck routing only, specifies number of trailers
            pulled by a vehicle. The provided value must be between 0 and 4. Defaults to 0.
        :type trailers_count: int

        :param shipped_hazardous_goods: Truck routing only, list of hazardous
            materials in the vehicle. Please refer to the enumeration type
            HazardousGoodTypeType for available values.
            Note the value allhazardousGoods does not apply to the request parameter.
            https://developer.here.com/documentation/routing/topics/resource-type-enumerations.html#resource-type-enumerations__enum-hazardous-good-type-type
        :type shipped_hazardous_goods: list of str

        :param limited_weight: Truck routing only, vehicle weight including
            trailers and shipped goods, in tons. The provided value must be between 0 and 1000.
        :type limited_weight: int

        :param weight_per_axle: Truck routing only, vehicle weight per axle in tons.
            The provided value must be between 0 and 1000.
        :type limited_weight: int

        :param height: Truck routing only, vehicle height in meters.
            The provided value must be between 0 and 50.
        :type height: int

        :param width: Truck routing only, vehicle width in meters.
            The provided value must be between 0 and 50.
        :type width: int

        :param length: Truck routing only, vehicle length in meters.
            The provided value must be between 0 and 300.
        :type length: int

        :param tunnel_category: Truck routing only, specifies the tunnel category to
            restrict certain route links. The route will pass only through tunnels of a less strict category.
        :type tunnel_category: list of str

        :param consumption_model: If you request information on consumption, you must
            provide a consumption model. The possible values are default and standard.
            When you specify the value standard, you must provide additional
            information in the query parameter custom consumption details
        :type consumption_model: str

        :param custom_consumption_details: Provides vehicle specific information
            for use in the consumption model. This information can include such
            things as the amount of energy consumed while travelling at a given speed.
            https://developer.here.com/documentation/routing/topics/resource-param-type-custom-consumption-details.html#type-standard
        :type custom_consumption_details: str

        :param speed_profile: Specifies the speed profile variant for a given
            routing mode. The speed profile affects travel time estimation as
            well as roads evaluation when computing the fastest route.
            Note that computed routes might differ depending on a used profile.
            https://developer.here.com/documentation/routing/topics/resource-param-type-speed-profile-type.html
        :type speed_profile: str

        :param dry_run: Print URL and parameters without sending the request.
        :param dry_run: bool

        :returns: raw JSON response
        :rtype: dict
        """

        self.client.base_url = (
            "https://isoline.route.api.here.com/routing/7.2"
            if self.api_key is None
            else "https://isoline.route.ls.hereapi.com/routing/7.2"
        )

        params = self.auth.copy()

        params[center_type] = self._build_locations(locations)[0]

        if isinstance(profile, str):
            params["mode"] = mode_type + ";" + profile
        elif isinstance(profile, self.RoutingMode):
            params["mode"] = profile.make_routing_mode()

        if intervals is not None:
            params["range"] = convert.delimit_list(intervals, ",")

        if interval_type is not None:
            params["rangeType"] = interval_type

        if departure is not None:
            params["departure"] = departure
        elif arrival is not None:
            params["arrival"] = arrival

        if single_component is not None:
            params["singleComponent"] = convert.convert_bool(single_component)

        if max_points is not None:
            params["maxPoints"] = max_points

        if quality is not None:
            params["quality"] = quality

        if json_attributes is not None:
            params["jsonAttributes"] = json_attributes

        if json_callback is not None:
            params["jsonCallback"] = json_callback

        if truck_type is not None:
            params["truckType"] = truck_type

        if trailers_count is not None:
            params["trailersCount"] = trailers_count

        if shipped_hazardous_goods is not None:
            params["shippedHazardousGoods"] = convert.delimit_list(shipped_hazardous_goods, ",")

        if limited_weight is not None:
            params["limitedWeight"] = limited_weight

        if weight_per_axle is not None:
            params["weightPerAxle"] = weight_per_axle

        if height is not None:
            params["height"] = height

        if width is not None:
            params["width"] = width

        if length is not None:
            params["length"] = length

        if tunnel_category is not None:
            params["tunnelCategory"] = convert.delimit_list(tunnel_category, ",")

        if consumption_model is not None:
            params["consumptionModel"] = consumption_model

        if custom_consumption_details is not None:
            params["customConsumptionDetails"] = custom_consumption_details

        if speed_profile is not None:
            params["speedProfile"] = speed_profile

        params.update(isochrones_kwargs)

        return self._parse_isochrone_json(
            self.client._request(
                convert.delimit_list(["/calculateisoline", format], "."),
                get_params=params,
                dry_run=dry_run,
            ),
            intervals,
        )

    @staticmethod
    def _parse_isochrone_json(response, intervals):
        if response is None:  # pragma: no cover
            return Isochrones()

        geometries = []
        for idx, isochrones in enumerate(response["response"]["isoline"]):
            range_polygons = []
            if "component" in isochrones:
                for component in isochrones["component"]:
                    if "shape" in component:
                        coordinates_list = []
                        for coordinates in component["shape"]:
                            coords = [float(f) for f in coordinates.split(",")]
                            coordinates_list.append(list(reversed(coords)))
                        range_polygons.append(coordinates_list)

            geometries.append(
                Isochrone(
                    geometry=range_polygons,
                    interval=intervals[idx],
                    center=list(response["response"]["start"]["mappedPosition"].values()),
                )
            )

        return Isochrones(isochrones=geometries, raw=response)

    def matrix(  # noqa: C901
        self,
        locations,
        profile,
        format="json",
        mode_type="fastest",
        sources=None,
        destinations=None,
        search_range=None,
        avoid_areas=None,
        avoid_links=None,
        avoid_turns=None,
        exclude_countries=None,
        departure=None,
        matrix_attributes=None,
        summary_attributes=["traveltime", "costfactor", "distance"],
        truck_type=None,
        trailers_count=None,
        shipped_hazardous_goods=None,
        limited_weight=None,
        weight_per_axle=None,
        height=None,
        width=None,
        length=None,
        tunnel_category=None,
        speed_profile=None,
        dry_run=None,
        **matrix_kwargs
    ):
        """Gets travel distance and time for a matrix of origins and destinations.

        Use ``matrix_kwargs`` for any missing ``matrix`` request options.

        :param locations: The coordinates tuple the route should be calculated
            from in order of visit. Can be a list/tuple of [lon, lat] or :class:`HereMaps.Waypoint` instance or a
            combination of those. For further explanation, see
            https://developer.here.com/documentation/routing/topics/resource-param-type-waypoint.html
        :type locations: list of list or list of :class:`HereMaps.Waypoint`

        :param profile: Specifies the routing mode of transport and further options.
            Can be a str or :class:`HereMaps.RoutingMode`
            https://developer.here.com/documentation/routing/topics/resource-param-type-routing-mode.html
        :type profile: str or :class:`HereMaps.RoutingMode`

        :param mode_type: RoutingType relevant to calculation. One of [fastest, shortest, balanced]. Default fastest.
            https://developer.here.com/documentation/routing/topics/resource-param-type-routing-mode.html#ariaid-title2
        :type mode_type: str

        :param sources: The starting points for the matrix.
            Specifies an index referring to coordinates.
        :type sources: list of int

        :param destinations: The destination points for the routes.
            Specifies an index referring to coordinates.
        :type destinations: list of int

        :param search_range: Defines the maximum search range for destination
            waypoints, in meters. This parameter is especially useful for optimizing
            matrix calculation where the maximum desired effective distance is known
            in advance. Destination waypoints with a longer effective distance than
            specified by searchRange will be skipped. The parameter is optional.
            In pedestrian mode the default search range is 20 km.
            If parameter is omitted in other modes, no range limit will apply.
        :type search_range: int

        :param avoid_areas: Areas which the route must not cross.
            Array of BoundingBox. Example with 2 bounding boxes
            https://developer.here.com/documentation/routing/topics/resource-param-type-bounding-box.html
        :type avoid_areas: list of list of list

        :param avoid_links: Links which the route must not cross.
          The list of LinkIdTypes.
        :type avoid_areas: list of string

        :param avoid_turns: List of turn types that the route should avoid. Defaults to empty list.
          https://developer.here.com/documentation/routing/topics/resource-type-enumerations.html
        :type avoid_turns: str

        :param exclude_countries: Countries that must be excluded from route calculation.
        :type exclude_countries: list of str

        :param departure: Time when travel is expected to start. Traffic speed and
            incidents are taken into account
            when calculating the route (note that in case of a past
            departure time the historical traffic is limited to one year).
            You can use now to specify the current time. Specify either departure
            or arrival, not both. When the optional timezone offset is not
            specified, the time is assumed to be the local.
            Formatted as iso time, e.g. 2018-07-04T17:00:00+02.
        :type departure: str

        :param matrix_attributes: Defines which attributes are included in the
          response as part of the data representation of the route matrix entries.
          Defaults to indices and summary.
          https://developer.here.com/documentation/routing/topics/resource-calculate-matrix.html#resource-calculate-matrix__matrix-route-attribute-type
        :type matrix_attributes: list of str

        :param summary_attributes: Defines which attributes are included in
            the response as part of the data representation of the matrix
            entries summaries. Defaults to costfactor.
            https://developer.here.com/documentation/routing/topics/resource-calculate-matrix.html#resource-calculate-matrix__matrix-route-summary-attribute-type
        :type matrix_attributes: list of str

        :param truck_type: Truck routing only, specifies the vehicle type.
            Defaults to truck.
        :type truck_type: str

        :param trailers_count: Truck routing only, specifies number of
            trailers pulled by a vehicle. The provided value must be between 0 and 4.
            Defaults to 0.
        :type trailers_count: int

        :param shipped_hazardous_goods: Truck routing only, list of hazardous
            materials in the vehicle. Please refer to the enumeration type
            HazardousGoodTypeType for available values. Note the value
            allhazardousGoods does not apply to the request parameter.
            https://developer.here.com/documentation/routing/topics/resource-type-enumerations.html#resource-type-enumerations__enum-hazardous-good-type-type
        :type shipped_hazardous_goods: list of str

        :param limited_weight: Truck routing only, vehicle weight including
            trailers and shipped goods, in tons. The provided value must be
            between 0 and 1000.
        :type limited_weight: int

        :param weight_per_axle: Truck routing only, vehicle weight per axle
            in tons. The provided value must be between 0 and 1000.
        :type limited_weight: int

        :param height: Truck routing only, vehicle height in meters. The
            provided value must be between 0 and 50.
        :type height: int

        :param width: Truck routing only, vehicle width in meters.
            The provided value must be between 0 and 50.
        :type width: int

        :param length: Truck routing only, vehicle length in meters.
            The provided value must be between 0 and 300.
        :type length: int

        :param tunnel_category: Truck routing only, specifies the tunnel
            category to restrict certain route links. The route will pass
            only through tunnels of a less strict category.
        :type tunnel_category: list of str

        :param speed_profile: Specifies the speed profile variant for a given
            routing mode. The speed profile affects travel time estimation as
            well as roads evaluation when computing the fastest route.
            Note that computed routes might differ depending on a used profile.
            https://developer.here.com/documentation/routing/topics/resource-param-type-speed-profile-type.html
        :type speed_profile: str

        :param dry_run: Print URL and parameters without sending the request.
        :param dry_run: bool

        :returns: raw JSON response
        :rtype: dict
        """
        self.client.base_url = (
            "https://matrix.route.api.here.com/routing/7.2"
            if self.api_key is None
            else "https://matrix.route.ls.hereapi.com/routing/7.2"
        )

        params = self.auth.copy()

        locations = self._build_locations(locations)

        sources_coords = locations
        if sources is not None:
            sources_coords = itemgetter(*sources)(sources_coords)
            if isinstance(sources_coords, str):
                sources_coords = [sources_coords]
        for i, location in enumerate(sources_coords):
            params["start" + str(i)] = location

        dest_coords = locations
        if destinations is not None:
            dest_coords = itemgetter(*destinations)(dest_coords)
            if isinstance(dest_coords, str):
                dest_coords = [dest_coords]
        for i, location in enumerate(dest_coords):
            params["destination" + str(i)] = location

        if isinstance(profile, str):
            params["mode"] = mode_type + ";" + profile
        elif isinstance(profile, self.RoutingMode):
            params["mode"] = profile.make_routing_mode()

        if search_range is not None:
            params["searchRange"] = search_range

        if avoid_areas is not None:
            params["avoidAreas"] = convert.delimit_list(
                [
                    convert.delimit_list(
                        [
                            convert.delimit_list(
                                [convert.format_float(f) for f in list(reversed(pair))], ","
                            )
                            for pair in bounding_box
                        ],
                        ";",
                    )
                    for bounding_box in avoid_areas
                ],
                "!",
            )

        if avoid_links is not None:
            params["avoidLinks"] = convert.delimit_list(avoid_links, ",")

        if avoid_turns is not None:
            params["avoidTurns"] = avoid_turns

        if exclude_countries is not None:
            params["excludeCountries"] = convert.delimit_list(exclude_countries, ",")

        if departure is not None:
            params["departure"] = departure.isoformat()

        if matrix_attributes is not None:
            params["matrixAttributes"] = convert.delimit_list(matrix_attributes, ",")

        if summary_attributes is not None:
            params["summaryAttributes"] = convert.delimit_list(summary_attributes, ",")

        if truck_type is not None:
            params["truckType"] = truck_type

        if trailers_count is not None:
            params["trailersCount"] = trailers_count

        if shipped_hazardous_goods is not None:
            params["shippedHazardousGoods"] = convert.delimit_list(shipped_hazardous_goods, ",")

        if limited_weight is not None:
            params["limitedWeight"] = limited_weight

        if weight_per_axle is not None:
            params["weightPerAxle"] = weight_per_axle

        if height is not None:
            params["height"] = height

        if width is not None:
            params["width"] = width

        if length is not None:
            params["length"] = length

        if tunnel_category is not None:
            params["tunnelCategory"] = convert.delimit_list(tunnel_category, ",")

        if speed_profile is not None:
            params["speedProfile"] = speed_profile

        params.update(matrix_kwargs)

        return self._parse_matrix_json(
            self.client._request(
                convert.delimit_list(["/calculatematrix", format], "."),
                get_params=params,
                dry_run=dry_run,
            )
        )

    @staticmethod
    def _parse_matrix_json(response):
        if response is None:  # pragma: no cover
            return Matrix()

        durations = []
        distances = []
        index_durations = []
        index_distances = []

        next_ = None
        mtx_objects = response["response"]["matrixEntry"]
        length = len(mtx_objects)
        for index, obj in enumerate(mtx_objects):
            if index < (length - 1):
                next_ = mtx_objects[index + 1]

            if "travelTime" in obj["summary"]:
                index_durations.append(obj["summary"]["travelTime"])
            else:
                index_durations.append(obj["summary"]["costfactor"])

            if "distance" in obj["summary"]:
                index_distances.append(obj["summary"]["distance"])

            if next_["startIndex"] > obj["startIndex"]:
                durations.append(index_durations)
                distances.append(index_distances)
                index_durations = []
                index_distances = []

        durations.append(index_durations)
        distances.append(index_distances)

        return Matrix(durations=durations, distances=distances, raw=response)

    def _build_locations(self, coordinates, matrix=False):
        """Build the locations object for all methods"""

        locations = []

        # Directions and matrix calls which are lists of list
        if isinstance(coordinates[0], (list, tuple, self.Waypoint)):

            for idx, coord in enumerate(coordinates):
                if isinstance(locations, self.Waypoint):
                    locations.append(locations._make_waypoint())
                elif isinstance(locations, (list, tuple)):
                    wp = "geo!" + convert.delimit_list(
                        [convert.format_float(f) for f in list(reversed(coord))], ","
                    )
                    locations.append(wp)
                else:
                    raise TypeError(
                        "Location type {} at index {} is not supported: {}".format(
                            type(coord), idx, coord
                        )
                    )

        # Isochrones
        elif isinstance(coordinates[0], float):
            center = "geo!" + convert.delimit_list(
                [convert.format_float(f) for f in list(reversed(coordinates))], ","
            )
            locations.append(center)
        # Isochrones using waypoint class
        elif isinstance(coordinates, self.Waypoint):
            locations.append(coordinates._make_waypoint())

        return locations
