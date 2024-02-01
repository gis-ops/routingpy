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

class ArcGIS:
    """Performs requests to the ArcGIS API."""

    _base_url = "https://route.arcgis.com/arcgis/rest/services/World/Route/NAServer/Route_World/solve"

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
        Initializes a ArcGIS client.

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
        f: str,
        travelMode: Optional[str] = None,
        startTime: Optional[str] = None,
        startTimeIsUTC: Optional[str] = None,
        timeWindowsAreUTC: Optional[str] = None,
        findBestSequence: Optional[str] = None,
        preserveFirstStop: Optional[str] = None,
        preserveLastStop: Optional[str] = None,
        useTimeWindows: Optional[str] = None,
        restrictUTurns: Optional[str] = None,
        useHierarchy: Optional[str] = None,
        impedanceAttributeName: Optional[str] = None,
        accumulateAttributeNames: Optional[str] = None,
        restrictionAttributeNames: Optional[str] = None,
        attributeParameterValues: Optional[str] = None,
        barriers: Optional[str] = None,
        polylineBarriers: Optional[str] = None,
        polygonBarriers: Optional[str] = None,
        returnDirections: Optional[str] = None,
        directionsLanguage: Optional[str] = None,
        directionsOutputType: Optional[str] = None,
        directionsStyleName: Optional[str] = None,
        directionsLengthUnits: Optional[str] = None,
        returnRoutes: Optional[str] = None,
        directionsTimeAttributeName: Optional[str] = None,
        outputLines: Optional[str] = None,
        returnStops: Optional[str] = None,
        returnBarriers: Optional[str] = None,
        returnPolylineBarriers: Optional[str] = None,
        returnPolygonBarriers: Optional[str] = None,
        returnTraversedEdges: Optional[str] = None,
        returnTraversedJunctions: Optional[str] = None,
        returnTraversedTurns: Optional[str] = None,
        ignoreInvalidLocations: Optional[str] = None,
        outSR: Optional[str] = None,
        outputGeometryPrecision: Optional[str] = None,
        outputGeometryPrecisionUnits: Optional[str] = None,
        geometryPrecision: Optional[str] = None,
        geometryPrecisionM: Optional[str] = None,
        preserveObjectID: Optional[str] = None,
        returnEmptyResults: Optional[str] = None,
        locateSettings: Optional[str] = None,
        dry_run: Optional[bool] = None
    ):
        """
        Get directions between an origin point and a destination point.

        For more information, visit https://developers.arcgis.com/rest/network/api-reference/route-synchronous-service.htm
        """

        params = {}

        """
        The API Key, which is needed to make requests to the ArcGIS services.	
        """
        params["token"] = self.key

        if len(locations) > 2:
            s = ""
            for l in locations:
                if len(s) == 0:
                    s = convert.delimit_list(list(reversed(l)))
                else:
                    s = s + ";" + convert.delimit_list(list(reversed(l)))
            params["stops"] = s
        else:
            origin, destination = locations[0], locations[-1]
            if isinstance(origin, (list, tuple)) and isinstance(destination, (list, tuple)) :
                params["stops"] = convert.delimit_list(list(reversed(origin)))+";"+convert.delimit_list(list(reversed(destination)))

        """
        Specify the response format.
        Values: json, pjson
        """
        params["f"] = f
        
        if travelMode:
            """
            Choose the mode of transportation for the analysis.
            """
            params["travelMode"] = travelMode
        
        if startTime:
            """
            Indicate the time at which travel begins from the input stops. You can also specify a value of now, to set the depart time to the current time.
            """
            params["startTime"] = startTime

        if startTimeIsUTC:
            """
            Specify the time zone or zones of the startTime parameter.
            The default value is false.
            Values: true, false
            """
            params["startTimeIsUTC"] = startTimeIsUTC

        if timeWindowsAreUTC:
            """
            Specify whether the TimeWindowStart and TimeWindowEnd attribute values on stops are specified in coordinated universal time (UTC) or geographically local time.
            The default value is false.
            Values: true, false
            """
            params["timeWindowsAreUTC"] = timeWindowsAreUTC
        
        if findBestSequence:
            """
            Specify whether the service should reorder stops to find the optimized route.
            The default value is false.
            Values: true, false
            """
            params["findBestSequence"] = findBestSequence
        
        if preserveFirstStop:
            """
            Indicate whether the service should keep the first stop fixed when reordering the stops. This parameter is required only if the findBestSequence parameter value is set to true.
            The default value is true.
            Values: true, false
            """
            params["preserveFirstStop"] = preserveFirstStop
              
        if preserveLastStop:
            """
            Indicate whether the service should keep the last stop fixed when reordering the stops. This parameter is required only if the findBestSequence parameter value is set to true.
            The default value is true.
            Values: true, false
            """
            params["preserveLastStop"] = preserveLastStop
        
        if useTimeWindows:
            """
            Indicate whether the service should consider time windows specified on the stops when finding the best route.
            The default value is false.
            Values: true, false
            """
            params["useTimeWindows"] = useTimeWindows

        if restrictUTurns:
            """
            Restrict or permit the route from making U-turns at junctions.
            The default value is esriNFSBAtDeadEndsAndIntersections.
            Values: esriNFSBAtDeadEndsAndIntersections | esriNFSBAllowBacktrack | esriNFSBAtDeadEndsOnly | esriNFSBNoBacktrack
            """
            params["restrictUTurns"] = restrictUTurns

        if useHierarchy:
            """
            Specify whether hierarchy should be used when finding the shortest paths.
            The default value is true.
            Values: true | false
            """
            params["useHierarchy"] = useHierarchy
        
        if impedanceAttributeName:
            """
            Specify the impedance.
            The default value is TravelTime.
            Values: TravelTime | Minutes | TruckTravelTime | TruckMinutes | WalkTime | Miles | Kilometers
            """
            params["impedanceAttributeName"] = impedanceAttributeName

        if accumulateAttributeNames:
            """
            Specify whether the service should accumulate values other than the value specified for impedanceAttributeName. The parameter value should be specified as a comma-separated list of names. The parameter values are the same as the impedanceAttributeName parameter.
            Values: TravelTime | Minutes | TruckTravelTime | TruckMinutes | WalkTime | Miles | Kilometers
            """
            params["accumulateAttributeNames"] = accumulateAttributeNames

        if restrictionAttributeNames:
            """
            Specify the restrictions that should be honored by the service. 
            """
            params["restrictionAttributeNames"] = restrictionAttributeNames
            
        if attributeParameterValues:
            """
            Specify additional values required by an attribute or restriction.
            """
            params["attributeParameterValues"] = attributeParameterValues

        if barriers:
            """
            Specify one or more points that act as temporary restrictions or represent additional time or distance that may be required to travel on the underlying streets.
            """
            params["barriers"] = barriers

        if polylineBarriers:
            """
            Specify one or more lines that prohibit travel anywhere the lines intersect the streets.
            """    
            params["polylineBarriers"] = polylineBarriers

        if polygonBarriers:
            """
            Specify polygons that either prohibit travel or proportionately scale the time or distance required to travel on the streets intersected by the polygons.
            """
            params["polygonBarriers"] = polygonBarriers

        if returnDirections:
            """
            Specify whether the service should generate driving directions for each route.
            The default value is true.
            Values: true | false
            """
            params["returnDirections"] = returnDirections

        if directionsLanguage:
            """
            Specify the language to be used when generating driving directions. This parameter is required only when the returnDirections parameter is set to true.
            The default value is en.
            """
            params["directionsLanguage"] = directionsLanguage

        if directionsOutputType:
            """
            Define the content and verbosity of the driving directions. This parameter is required only when the returnDirections parameter is set to true.
            The default value is esriDOTStandard.
            Values: esriDOTStandard | esriDOTComplete | esriDOTCompleteNoEvents | esriDOTInstructionsOnly | esriDOTStandard | esriDOTSummaryOnly | esriDOTFeatureSets
            """
            params["directionsOutputType"] = directionsOutputType

        if directionsStyleName:
            """
            Specify the name of the formatting style for the directions. This parameter is required only when the returnDirections parameter is set to true.
            The default value is NA Desktop.
            Values: NA Desktop | NA Navigation | NA Campus
            """
            params["directionsStyleName"] = directionsStyleName

        if directionsLengthUnits:
            """
            Indicate the units for displaying travel distance in the driving directions. This parameter is required only when the returnDirections parameter is set to true.
            The default value is esriNAUMiles.
            Values: esriNAUMiles | esriNAUFeet | esriNAUKilometers | esriNAUMeters | esriNAUNauticalMiles | esriNAUYards
            """
            params["directionsLengthUnits"] = directionsLengthUnits

        if returnRoutes:
            """
            Specify whether the service should return routes.
            The default value is true.
            Values: true | false
            """
            params["returnRoutes"] = returnRoutes

        if directionsTimeAttributeName:
            """
            Indicate a time-based impedance attribute to display the duration of a maneuver.
            The default value is TravelTime.
            Values: TravelTime | Minutes | TruckTravelTime | TruckMinutes | WalkTime
            """
            params["directionsTimeAttributeName"] = directionsTimeAttributeName

        if outputLines:
            """
            Specify the type of route features that are output by the service.
            The default value is esriNAOutputLineTrueShape.
            Values: esriNAOutputLineTrueShape | esriNAOutputLineTrueShapeWithMeasure | esriNAOutputLineStraight | esriNAOutputLineNone
            """
            params["outputLines"] = outputLines

        if returnStops:
            """
            Specify whether stops will be returned by the service.
            The default value is false.
            Values: true | false
            """
            params["returnStops"] = returnStops

        if returnBarriers:
            """
            Specify whether barriers will be returned by the service.
            The default value is false.
            Values: true | false
            """
            params["returnBarriers"] = returnBarriers

        if returnPolylineBarriers:
            """
            Specify whether polyline barriers will be returned by the service.
            The default value is false.
            Values: true | false
            """
            params["returnPolylineBarriers"] = returnPolylineBarriers
        
        if returnPolygonBarriers:
            """
            Specify whether polygon barriers will be returned by the service.
            The default value is false.
            Values: true | false
            """
            params["returnPolygonBarriers"] = returnPolygonBarriers
        
        if returnTraversedEdges:
            """
            Specify whether traversed edges will be returned by the service. The default value is false.
            Values: true | false
            When this parameter is set to true, the traversed edges are available in the traversedEdges property of the JSON response.
            """
            params["returnTraversedEdges"] = returnTraversedEdges
        
        if returnTraversedJunctions:
            """
            Specify whether traversed junctions will be returned by the service. The default value is false.
            Values: true | false
            When this parameter is set to true, the traversed junctions are available in the traversedJunctions property of the JSON response.
            """
            params["returnTraversedJunctions"] = returnTraversedJunctions
        
        if returnTraversedTurns:
            """
            Specify whether traversed turns will be returned by the service. The default value is false.
            Values: true | false
            When this parameter is set to true, the traversed turns are available in the traversedTurns property of the JSON response.
            """
            params["returnTraversedTurns"] = returnTraversedTurns
        
        if ignoreInvalidLocations:
            """
            Specify whether invalid input locations should be ignored when finding the best solution.
            The default value is true.
            Values: true | false
            """
            params["ignoreInvalidLocations"] = ignoreInvalidLocations

        if outSR:
            """
            Specify the spatial reference of the geometries.
            """
            params["outSR"] = outSR

        if outputGeometryPrecision:
            """
            Specify by how much you want to simplify the route geometry.
            The default value is 10.
            """
            params["outputGeometryPrecision"] = outputGeometryPrecision

        if outputGeometryPrecisionUnits:
            """
            Specify the units for the value specified for the outputGeometryPrecision parameter.
            The default value is esriMeters.
            Values: esriMeters | esriCentimeters | esriDecimalDegrees | esriDecimeters | esriFeet | esriInches | esriKilometers | esriMiles | esriMillimeters | esriNauticalMiles | esriPoints | esriYards
            """
            params["outputGeometryPrecisionUnits"] = outputGeometryPrecisionUnits
        
        if geometryPrecision:
            """
            Specify the number of decimal places in the response geometries returned by solve operation. This applies to x- and y-values only (not m- or z-values).
            """
            params["geometryPrecision"] = geometryPrecision

        if geometryPrecisionM:
            """
            Specify the number of decimal places in the response geometries returned by solve operation. This applies to m-value only (not x-, y,- or z-values).
            """
            params["geometryPrecisionM"] = geometryPrecisionM

        if preserveObjectID:
            """
            Specify whether the object IDs from the input locations should be preserved when the input locations are returned as output.
            The default value is false.
            Values: true | false
            """
            params["preserveObjectID"] = preserveObjectID

        if returnEmptyResults:
            """
            Specify whether the service will return empty results instead of the error property when the request fails.
            Values: true | false
            The default value is false.
            """
            params["returnEmptyResults"] = returnEmptyResults

        if locateSettings:
            """
            Specify settings that affect how inputs are located.
            """
            params["locateSettings"] = locateSettings              

        return self.parse_direction_json(self.client._request(self._base_url, get_params=params, dry_run=dry_run), outputLines)

    @staticmethod
    def parse_direction_json(response, outputLines):
        if response is None:  # pragma: no cover
            return Direction()

        distance = response["routes"]["features"][0]["attributes"]["Total_Kilometers"]
        distance = round(distance * 1000) # From Km to m
        duration = response["routes"]["features"][0]["attributes"]["Total_TravelTime"]
        duration = round(duration * 60) # From minutes to seconds
        if outputLines:
            if outputLines == "esriNAOutputLineTrueShape":
                geometry = response["routes"]["features"][0]["geometry"]["paths"][0]
                return Direction(geometry=geometry, duration=duration, distance=distance, raw=response)
        else:
            return Direction(duration=duration, distance=distance, raw=response)