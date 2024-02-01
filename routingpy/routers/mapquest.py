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
from ..direction import Direction

class MapQuest:
    """Performs requests to the MapQuest API."""

    _base_url = "https://www.mapquestapi.com/directions/v2/route"

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
        Initializes a MapQuest client.

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
        ambiguities: Optional[str] = None,
        outFormat: Optional[str] = None,
        unit: Optional[str] = None,
        routeType: Optional[str] = None,
        avoidTimedConditions: Optional[str] = None,
        doReverseGeocode: Optional[str] = None,
        narrativeType: Optional[str] = None,
        enhancedNarrative: Optional[str] = None,
        maxLinkId: Optional[str] = None,
        locale: Optional[str] = None,
        avoids: Optional[str] = None,
        disallows: Optional[str] = None,
        prefers: Optional[str] = None,
        mustAvoidLinkIds: Optional[str] = None,
        tryAvoidLinkIds: Optional[str] = None,
        stateBoundaryDisplay: Optional[str] = None,
        countryBoundaryDisplay: Optional[str] = None,
        sideOfStreetDisplay: Optional[str] = None,
        destinationManeuverDisplay: Optional[str] = None,
        fullShape: Optional[str] = None,
        shapeFormat: Optional[str] = None,
        inShapeFormat: Optional[str] = None,
        outShapeFormat: Optional[str] = None,
        generalize: Optional[str] = None,
        cyclingRoadFactor: Optional[str] = None,
        roadGradeStrategy: Optional[str] = None,
        drivingStyle: Optional[str] = None,
        highwayEfficiency: Optional[str] = None,
        manMaps: Optional[str] = None,
        walkingSpeed: Optional[str] = None,
        timeType: Optional[str] = None,
        dateType: Optional[str] = None,
        date: Optional[str] = None,
        localTime: Optional[str] = None,
        isoLocal: Optional[str] = None,
        toleranceBefore: Optional[str] = None,
        toleranceAfter: Optional[str] = None,
        useTraffic: Optional[str] = None,
        dry_run: Optional[bool] = None
    ):
        """
        Get directions between an origin point and a destination point.

        For more information, visit https://developer.mapquest.com/documentation/directions-api/route/get
        """

        params = {}

        """
        The API Key, which is needed to make requests to MapQuest services.	
        """
        params["key"] = self.key

        origin, destination = locations[0], locations[-1]
        if isinstance(origin, (list, tuple)):
            """
            The starting location of a Route Request.
            """
            params["from"] = convert.delimit_list(origin)
        
        if isinstance(destination, (list, tuple)):
            """
            The ending location of a Route Request.
            """
            params["to"] = convert.delimit_list(destination)

        if ambiguities:
            """
            Use this parameter to set the strategy for resolving ambiguous location names.
                - ignore: the Routing Service will simply use the first location found for an address.
                - check:  the Routing Service will return a full list of the possible location matches in the collections attribute of the response.
            Default: ignore
            """
            params["ambiguities"] = ambiguities
        
        if outFormat:
            """
            Specifies the format of the response. Must be one of the following, if supplied:
                - json
                - xml
            Default: json
            """
            params["outFormat"] = outFormat
        
        if unit:
            """
            Specifies the type of units to use when calculating distance. Acceptable values are:
                - m: Miles
                - k: Kilometers
            Default: m
            """
            params["unit"] = unit

        if routeType:
            """
            Specifies the type of route wanted. Acceptable values are:
                - fastest: Quickest drive time route.
                - shortest: Shortest driving distance route.
                - pedestrian: Walking route; Avoids limited access roads; Ignores turn restrictions.
                - bicycle: Will only use roads on which bicycling is appropriate.
            Default: fastest
            """
            params["routeType"] = routeType

        if avoidTimedConditions:
            """
            Avoids using timed conditions such as Timed Turn Restrictions, Timed Access Roads, HOV Roads, and Seasonal Closures. Please Note: This flag should NOT be used if the Date/Time Routing Options are used.
                - false: No penalties will be set and the timed conditions can be utilized when generating a route.
                - true: Penalties will be set and the timed conditions will be avoided when generating a route.
            Default: false
            """
            params["avoidTimedConditions"] = avoidTimedConditions
        
        if doReverseGeocode:
            """
            If this flag is set, no reverse geocoding will be done on input locations.
                - false: Input latitude/longitude will be used without any modification.
                - true: Even if exact latitude/longitude are given as input locations, a reverse geocode call will be performed to determine city/state/zipcode/etc.
            Default: true
            """
            params["doReverseGeocode"] = doReverseGeocode
        
        if narrativeType:
            """
            Specifies the type of narrative to generate.
                - none: No narrative is generated
                - text: Standard text narrative
                - html: Adds some HTML tags to the standard text
                - microformat: Uses HTML span tags with class attributes to allow parts of the narrative to be easily styled via CSS. Explanation
            Default: text
            """
            params["narrativeType"] = narrativeType
              
        if enhancedNarrative:
            """
            This option will generate an enhanced narrative for Route & Alternate Route Services. This will encompass Intersection Counts, Previous Intersection, and Next Intersection/Gone Too Far advice.
                - false: No intersection counts, previous intersection, or Next Intersection/Gone Too Far advice will be displayed.
                - true: Intersection counts, previous intersection, and Next Intersection/Gone Too Far advice can be displayed when available.
            Default: false
            """
            params["enhancedNarrative"] = enhancedNarrative
        
        if maxLinkId:
            """
            The maximum number of Link IDs to return for each maneuver. If zero, no link ID data is returned.
            Default: 0
            """
            params["maxLinkId"] = maxLinkId

        if locale:
            """
            Examples of commonly used locale parameter values. Input can be any supported ISO 639-1 code.
            Default: en_US
            """
            params["locale"] = locale

        if avoids:
            """
            Attribute flags of roads to try to avoid. The available attribute flags depend on the data set. This does not guarantee roads with these attributes will be avoided if alternate route paths are too lengthy, or not possible, or roads that contain these attributes are very short.
            Available choices:
                - Limited Access
                - Toll Road
                - Ferry
                - Unpaved
                - Approximate Seasonal Closure
                - Country Border Crossing
                - Bridge
                - Tunnel
            """
            params["avoids"] = avoids
        
        if disallows:
            """
            Attribute flags of roads to disallow. The available attribute flags depend on the data set. This guarantees roads with these attributes will not be allowed as part of the route.
            Available choices:
                - Limited Access
                - Toll Road
                - Ferry
                - Unpaved
                - Approximate Seasonal Closure
                - Country Border Crossing
                - Bridge
                - Tunnel
            """
            params["disallows"] = disallows

        if prefers:
            """
            Attribute flags of roads to try to prefer. The available attribute flags depend on the data set.
            Available choices:
                - highway
            """
            params["prefers"] = prefers

        if mustAvoidLinkIds:
            """
            Link IDs of roads to absolutely avoid. May cause some routes to fail. Multiple Link IDs should be comma-separated.
            """
            params["mustAvoidLinkIds"] = mustAvoidLinkIds

        if tryAvoidLinkIds:
            """
            Link IDs of roads to try to avoid during route calculation. Does not guarantee these roads will be avoided if alternate route paths are too lengthy or not possible. Multiple Link IDs should be comma-separated.
            """
            params["tryAvoidLinkIds"] = tryAvoidLinkIds

        if stateBoundaryDisplay:
            """
            State boundary display option.
                - true: State boundary crossings will be displayed in narrative.
                - false: State boundary crossings will not be displayed in narrative.
            """    
            params["stateBoundaryDisplay"] = stateBoundaryDisplay

        if countryBoundaryDisplay:
            """
            Country boundary display option.
                - true: Country boundary crossings are displayed in narrative.
                - false: Country boundary crossings are not displayed in narrative.
            """
            params["countryBoundaryDisplay"] = countryBoundaryDisplay

        if sideOfStreetDisplay:
            """
            Side of street display option.
                - true: Side of street is displayed in narrative.
                - false: Side of street is not displayed in narrative.
            """
            params["sideOfStreetDisplay"] = sideOfStreetDisplay

        if destinationManeuverDisplay:
            """
            The "End at" destination maneuver display option.
                - true: the "End at" destination maneuver is displayed in narrative.
                - false: the "End at" destination maneuver is not displayed in narrative.
            """
            params["destinationManeuverDisplay"] = destinationManeuverDisplay

        if fullShape:
            """
            Returns all shapes (no generalization or clipping). This option overrides any mapState or generalize options.
                - true: all shape points will be returned
                - false: returned shape points depend on mapState or generalizeoptions
            Default: false
            """
            params["fullShape"] = fullShape

        if shapeFormat:
            """
            This option applies to both input and output (raw, cmp, cmp6) and overrides inShapeFormat and outShapeFormat.
            Shape format options.
                - raw: shape is represented as float pairs.
                - cmp: shape is represented as a compressed path string with 5 digits of precision.
                - cmp6: Same as for cmp, but uses 6 digits of precision.
            """
            params["shapeFormat"] = shapeFormat

        if inShapeFormat:
            """
            Input shape format options.
                - raw: shape is represented as float pairs.
                - cmp: shape is represented as a compressed path string with 5 digits of precision.
                - cmp6: Same as for cmp, but uses 6 digits of precision.
            """
            params["inShapeFormat"] = inShapeFormat

        if outShapeFormat:
            """
            Output shape format options.
                - raw: shape is represented as float pairs.
                - cmp: shape is represented as a compressed path string with 5 digits of precision.
                - cmp6: Same as for cmp, but uses 6 digits of precision.
            """
            params["outShapeFormat"] = outShapeFormat

        if generalize:
            """
            If there is no mapState and fullShape = false, then the specified generalization factor will be used to generalize the shape.
            If the generalize parameter is 0, then no shape simplification will be done and all shape points will be returned.
            If the generalize parameter is > 0, it will be used as the tolerance distance (in meters) in the Douglas-Peucker Algorithm for line simplification.
            Higher values of generalize will result in fewer points in the final route shape.
            """
            params["generalize"] = generalize

        if cyclingRoadFactor:
            """
            Sets the cycling road favoring factor. A value of < 1 favors cycling on non-bike lane roads. Values are clamped to the range 0.1 to 100.0.
            Default: 1.0
            """
            params["cyclingRoadFactor"] = cyclingRoadFactor

        if roadGradeStrategy:
            """
            Specifies the road grade avoidance strategies to be used for each leg. This parameter is only for bicycle routes.
                - DEFAULT_STRATEGY: No road grade strategy will be used.
                - AVOID_UP_HILL: Avoid uphill road grades.
                - AVOID_DOWN_HILL: Avoid downhill road grades.
                - AVOID_ALL_HILLS: Avoid all hill road grades.
                - FAVOR_UP_HILL: Favor uphill road grades.
                - FAVOR_DOWN_HILL: Favor downhill road grades.
                - FAVOR_ALL_HILLS: Favor all hill road grades.
            Default: DEFAULT_STRATEGY
            """
            params["roadGradeStrategy"] = roadGradeStrategy

        if drivingStyle:
            """
            Driving style to be used when calculating fuel usage.
                - 1 or cautious: Assume a cautious driving style.
                - 2 or normal: Assume a normal driving style. This is the default.
                - 3 or aggressive: Assume an aggressive driving style.
            """
            params["drivingStyle"] = drivingStyle

        if highwayEfficiency:
            """
            This is the fuel efficiency of your vehicle, given as miles per gallon (mpg). Valid range is 0 - 235 mpg. If a value is entered that is less than the minimum range, then 0 will be used. If a value is entered that is greater than the maximum range, then 235 will be used.
            """
            params["highwayEfficiency"] = highwayEfficiency
        
        if manMaps:
            """
            Maneuver maps display option.
                - true: A small staticmap is displayed per maneuver with the route shape of that maneuver. The route response will return a mapUrl. See mapUrl in the Route Response section for a detailed description.
                - false: A small staticmap is not displayed per maneuver.
            Default = true
            """
            params["manMaps"] = manMaps
        
        if walkingSpeed:
            """
            This is the speed (in miles per hour as default and it does adhere to the unit specifier) allowed for the pedestrian routeType. This is used for computing expected route times for walking routes.
            The default is 2.5 miles per hour.
            """
            params["walkingSpeed"] = walkingSpeed
        
        if timeType:
            """
            Specifies the time type to use. Acceptable values are:
                - 0: None (No date/time options will be used)
                - 1: Current (Uses the current date/time when generating a route.)
                - 2: Start At (May specify a specific date/time or day of the week to use when generating a route.)
                - 3: Arrive By (May specify a specific date/time or day of the week to use when generating a route.)
            Default: 0
            """
            params["timeType"] = timeType
        
        if dateType:
            """
            Specifies the date type to use. If timeType is 0 or 1, this option will be ignored. Acceptable values are:
                - 0: Specific Date & Time
                - 1: Sunday
                - 2: Monday
                - 3: Tuesday
                - 4: Wednesday
                - 5: Thursday
                - 6: Friday
                - 7: Saturday
            Default: 0
            """
            params["dateType"] = dateType
        
        if date:
            """
            The format for date is MM/DD/YYYY. If timeType is 0 or 1, or if dateType is 1-7, this option will be ignored.
            If dateType is 0 and isoLocal is null, this parameter must be used. MM specifies the month of year. Acceptable values are:
                01 - January
                02 - February
                03 - March
                04 - April
                05 - May
                06 - June
                07 - July
                08 - August
                09 - September
                10 - October
                11 - November
                12 - December
            DD specifies the day of the month.
            Acceptable values are 01-31. YYYY specifies the year.
            Values need to be entered in YYYY format. Default date value is the current date.
            NOTE: The user has the choice of entering date/time in the ISO 8601 format YYYY-MM-DDThh:mm or as a calendar date (MM/DD/YYYY) and local time (hh:mm) by using the date and localTime fields, respectively.
            """
            params["date"] = date

        if localTime:
            """
            If timeType is 0 or 1, this option will be ignored.
            If dateType is 0 and isoLocal is null, this parameter must be used.
            If dateType is 1-7, this paramater can be used to set a specific time of day to generate a route.
            Values need to be entered in hh:mm format. Default localTime value is the current time.
            NOTE: The user has the choice of entering date/time in the ISO 8601 format YYYY-MM-DDThh:mm or as a calendar date (MM/DD/YYYY) and local time (hh:mm) by using the date and localTime fields, respectively.
            """
            params["localTime"] = localTime

        if isoLocal:
            """
            If timeType is 0 or 1, or if dateType is 1-7, this option will be ignored.
            If dateType is 0, this is an optional parameter.
            The user has the choice of entering date/time in the ISO 8601 format YYYY-MM-DDThh:mm or may enter as individual parameters by using the month, day, year, and localTime fields that are listed below.
            Default: current date and time.
            """
            params["isoLocal"] = isoLocal

        if toleranceBefore:
            """
            If timeType is 0, 1, or 2, this option will be ignored. Otherwise, if timeType is 3, this is an optional parameter.
            Values need to be entered in mm format.
            Sets the minutes before the specified arrive time to accept. Default toleranceBefore value is 15 mins.
            """
            params["toleranceBefore"] = toleranceBefore
        
        if toleranceAfter:
            """
            If timeType is 0, 1, or 2, this option will be ignored. Otherwise, if timeType is 3, this is an optional parameter.
            Values need to be entered in mm format.
            Sets the minutes after the specified arrive time to allow. Default toleranceBefore value is 0.
            """
            params["toleranceAfter"] = toleranceAfter

        if useTraffic:
            """
            If set to true, will use historical and realtime traffic speeds (depending on route time and availability of data) to influence the route.
            NOTE: If this option is set to true, the timeType option must be set to something other than "0" (i.e., not "None").
            Default = false
            """
            params["useTraffic"] = useTraffic       

        return self.parse_direction_json(self.client._request(self._base_url, get_params=params, dry_run=dry_run), fullShape)

    @staticmethod
    def parse_direction_json(response, fullShape):
        if response is None:  # pragma: no cover
            return Direction()

        distance = int(response["route"]["distance"])
        distance = round(distance * 1000) # From Km to m
        duration = int(response["route"]["realTime"])
        if fullShape:
            if fullShape == "true":
                geometry = response["route"]["shape"]["shapePoints"]
                return Direction(geometry=geometry, duration=duration, distance=distance, raw=response)
        else:
            return Direction(duration=duration, distance=distance, raw=response)