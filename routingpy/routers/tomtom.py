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
from ..direction import Direction, Directions

class TomTom:
    """Performs requests to the TomTom API."""

    _base_url = "https://api.tomtom.com/routing/1/calculateRoute/"

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
        Initializes a TomTom client.

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
        maxAlternatives: Optional[str] = None,
        instructionsType: Optional[str] = None,
        language: Optional[str] = None,
        computeBestOrder: Optional[str] = None,
        routeRepresentation: Optional[str] = None,
        computeTravelTimeFor: Optional[str] = None,
        vehicleHeading: Optional[str] = None,
        sectionType: Optional[str] = None,
        report: Optional[str] = None,
        departAt: Optional[str] = None,
        arriveAt: Optional[str] = None,
        routeType: Optional[str] = None,
        traffic: Optional[str] = None,
        avoid: Optional[str] = None,
        travelMode: Optional[str] = None,
        hilliness: Optional[str] = None,
        windingness: Optional[str] = None,
        vehicleMaxSpeed: Optional[str] = None,
        vehicleWeight: Optional[str] = None,
        vehicleAxleWeight: Optional[str] = None,
        vehicleNumberOfAxles: Optional[str] = None,
        vehicleLength: Optional[str] = None,
        vehicleWidth: Optional[str] = None,
        vehicleHeight: Optional[str] = None,
        vehicleCommercial: Optional[str] = None,
        roadGradeStrategy: Optional[str] = None,
        vehicleLoadType: Optional[str] = None,
        vehicleAdrTunnelRestrictionCode: Optional[str] = None,
        vehicleEngineType: Optional[str] = None,
        constantSpeedConsumptionInLitersPerHundredkm: Optional[str] = None,
        currentFuelInLiters: Optional[str] = None,
        auxiliaryPowerInLitersPerHour: Optional[str] = None,
        fuelEnergyDensityInMJoulesPerLiter: Optional[str] = None,
        accelerationEfficiency: Optional[str] = None,
        decelerationEfficiency: Optional[str] = None,
        uphillEfficiency: Optional[str] = None,
        downhillEfficiency: Optional[str] = None,
        consumptionInkWhPerkmAltitudeGain: Optional[str] = None,
        recuperationInkWhPerkmAltitudeLoss: Optional[str] = None,
        constantSpeedConsumptionInkWhPerHundredkm: Optional[str] = None,
        currentChargeInkWh: Optional[str] = None,
        maxChargeInkWh: Optional[str] = None,
        auxiliaryPowerInkW: Optional[str] = None,
        dry_run: Optional[bool] = None
    ):
        """
        Get directions between an origin point and a destination point.

        For more information, visit https://developer.tomtom.com/routing-api/documentation/routing/calculate-route and https://developer.tomtom.com/routing-api/api-explorer
        """

        params = {}

        """
        The API Key, which is needed to make requests to the TomTom services.	
        """
        params["key"] = self.key

        if len(locations) > 2:
            url = ""
            for l in locations:
                if len(url) == 0:
                    url = self._base_url + convert.delimit_list(l)
                url = url + ":" + convert.delimit_list(l)
            url = url + "/json"
        else:
            origin, destination = locations[0], locations[-1]
            if isinstance(origin, (list, tuple)) and isinstance(destination, (list, tuple)):
                url = self._base_url+convert.delimit_list(origin)+":"+convert.delimit_list(destination)+"/json"

        if maxAlternatives:
            """
            Number of alternative routes to be calculated.
            """
            params["maxAlternatives"] = maxAlternatives
        
        if instructionsType:
            """
            If specified, guidance instructions will be returned (if available).
            """
            params["instructionsType"] = instructionsType
        
        if language:
            """
            The language parameter determines the language of the guidance messages.
            """
            params["language"] = language

        if computeBestOrder:
            """
            Re-order the route waypoints to reduce the route length.
            """
            params["computeBestOrder"] = computeBestOrder

        if routeRepresentation:
            """
            Specifies the representation of the set of routes provided as a Response.
            """
            params["routeRepresentation"] = routeRepresentation
        
        if computeTravelTimeFor:
            """
            Specifies whether to return additional travel times using different types of traffic information (none, historic, live) as well as the default best-estimate travel time.
            """
            params["computeTravelTimeFor"] = computeTravelTimeFor
        
        if vehicleHeading:
            """
            The directional heading of the vehicle in degrees. Entered in degrees, measured clockwise from north (so north is 0, east is 90, etc.).
            """
            params["vehicleHeading"] = vehicleHeading
              
        if sectionType:
            """
            Specifies which section types are explicitly reported in the route response. Can be specified multiple times.
                - carTrain, ferry, tunnel or motorway
                - pedestrian
                - tollRoad
                - tollVignette
                - country
                - travelMode
                - traffic
            """
            params["sectionType"] = sectionType
        
        if report:
            """
            Specifies which data should be reported for diagnosis purposes.
            """
            params["report"] = report

        if departAt:
            """
            The date and time of departure from the origin point. Departure times apart from now must be specified as a dateTime.
            """
            params["departAt"] = departAt

        if arriveAt:
            """
            The date and time of arrival at the destination point. It must be specified as a dateTime.
            """
            params["arriveAt"] = arriveAt
        
        if routeType:
            """
            The type of route requested.
            """
            params["routeType"] = routeType

        if traffic:
            """
            Determines whether current traffic is used in route calculations. Note that information on historic road speeds is always used.
            """
            params["traffic"] = traffic

        if avoid:
            """
            Specifies whether the routing engine should try to avoid specific types of road segment when calculating the route. Can be specified multiple times. Possible values:
                - tollRoads
                - motorways
                - ferries
                - unpavedRoads
                - carpools
                - alreadyUsedRoads
            """
            params["avoid"] = avoid

        if travelMode:
            """
            The mode of travel for the requested route.
            """
            params["travelMode"] = travelMode

        if hilliness:
            """
            Degree of hilliness for calculating a thrilling route.
            """    
            params["hilliness"] = hilliness

        if windingness:
            """
            Amount that a thrilling route should wind.
            """
            params["windingness"] = windingness

        if vehicleMaxSpeed:
            """
            Maximum speed of the vehicle in km/hour.
            """
            params["vehicleMaxSpeed"] = vehicleMaxSpeed

        if vehicleWeight:
            """
            Weight of the vehicle in kilograms.
            """
            params["vehicleWeight"] = vehicleWeight

        if vehicleAxleWeight:
            """
            Weight per axle of the vehicle in kg.
            """
            params["vehicleAxleWeight"] = vehicleAxleWeight

        if vehicleNumberOfAxles:
            """
            Number of axles of the vehicle.
            """
            params["vehicleNumberOfAxles"] = vehicleNumberOfAxles

        if vehicleLength:
            """
            Length of the vehicle in meters.
            """
            params["vehicleLength"] = vehicleLength

        if vehicleWidth:
            """
            Width of the vehicle in meters.
            """
            params["vehicleWidth"] = vehicleWidth

        if vehicleHeight:
            """
            Height of the vehicle in meters.
            """
            params["vehicleHeight"] = vehicleHeight

        if vehicleCommercial:
            """
            Indicates that the vehicle is used for commercial purposes. This means it may not be allowed on certain roads.
            """
            params["vehicleCommercial"] = vehicleCommercial

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

        if vehicleLoadType:
            """
            Indicates what kinds of hazardous materials the vehicle is carrying (if any). This means it may not be allowed on certain roads. Use these for routing in the US:
                - USHazmatClass1 Explosives
                - USHazmatClass2 Compressed gas
                - USHazmatClass3 Flammable liquids
                - USHazmatClass4 Flammable solids
                - USHazmatClass5 Oxidizers
                - USHazmatClass6 Poisons
                - USHazmatClass7 Radioactive
                - USHazmatClass8 Corrosives
                - USHazmatClass9 Miscellaneous
            Use these for routing in all other countries:
                - otherHazmatExplosive Explosives
                - otherHazmatGeneral Miscellaneous
                - otherHazmatHarmfulToWater Harmful to water
            vehicleLoadType can be specified multiple times. This parameter is currently only considered for travelMode=truck.
            """
            params["vehicleLoadType"] = vehicleLoadType

        if vehicleAdrTunnelRestrictionCode:
            """
            If vehicleAdrTunnelRestrictionCode is specified, the vehicle is subject to ADR tunnel restrictions.
            """
            params["vehicleAdrTunnelRestrictionCode"] = vehicleAdrTunnelRestrictionCode
        
        if vehicleEngineType:
            """
            Engine type of the vehicle.
            """
            params["vehicleEngineType"] = vehicleEngineType
        
        if constantSpeedConsumptionInLitersPerHundredkm:
            """
            Specifies the speed-dependent component of consumption. Provided as an unordered list of speed/consumption-rate pairs.
            """
            params["constantSpeedConsumptionInLitersPerHundredkm"] = constantSpeedConsumptionInLitersPerHundredkm
        
        if currentFuelInLiters:
            """
            Specifies the current supply of fuel in liters.
            """
            params["currentFuelInLiters"] = currentFuelInLiters
        
        if auxiliaryPowerInLitersPerHour:
            """
            Specifies the amount of fuel consumed for sustaining auxiliary systems of the vehicle, in liters per hour.
            """
            params["auxiliaryPowerInLitersPerHour"] = auxiliaryPowerInLitersPerHour
        
        if fuelEnergyDensityInMJoulesPerLiter:
            """
            Specifies the amount of chemical energy stored in one liter of fuel in megajoules (MJ).
            """
            params["fuelEnergyDensityInMJoulesPerLiter"] = fuelEnergyDensityInMJoulesPerLiter

        if accelerationEfficiency:
            """
            Specifies the efficiency of converting chemical energy stored in fuel to kinetic energy when the vehicle accelerates (i.e. KineticEnergyGained/ChemicalEnergyConsumed).
            """
            params["accelerationEfficiency"] = accelerationEfficiency

        if decelerationEfficiency:
            """
            Specifies the efficiency of converting kinetic energy to saved (not consumed) fuel when the vehicle decelerates (i.e. ChemicalEnergySaved/KineticEnergyLost).
            """
            params["decelerationEfficiency"] = decelerationEfficiency

        if uphillEfficiency:
            """
            Specifies the efficiency of converting chemical energy stored in fuel to potential energy when the vehicle gains elevation (i.e. PotentialEnergyGained/ChemicalEnergyConsumed).
            """
            params["uphillEfficiency"] = uphillEfficiency
        
        if downhillEfficiency:
            """
            Specifies the efficiency of converting potential energy to saved (not consumed) fuel when the vehicle loses elevation (i.e. ChemicalEnergySaved/PotentialEnergyLost).
            """
            params["downhillEfficiency"] = downhillEfficiency

        if consumptionInkWhPerkmAltitudeGain:
            """
            Specifies the electric energy in kWh consumed by the vehicle through gaining 1000 meters of elevation.
            """
            params["consumptionInkWhPerkmAltitudeGain"] = consumptionInkWhPerkmAltitudeGain

        if recuperationInkWhPerkmAltitudeLoss:
            """
            Specifies the electric energy in kWh gained by the vehicle through losing 1000 meters of elevation.
            """
            params["recuperationInkWhPerkmAltitudeLoss"] = recuperationInkWhPerkmAltitudeLoss

        if constantSpeedConsumptionInkWhPerHundredkm:
            """
            Specifies the speed-dependent component of consumption. Provided as an unordered list of speed/consumption-rate pairs.
            """
            params["constantSpeedConsumptionInkWhPerHundredkm"] = constantSpeedConsumptionInkWhPerHundredkm

        if currentChargeInkWh:
            """
            Specifies the current electric energy supply in kilowatt hours (kWh).
            """
            params["currentChargeInkWh"] = currentChargeInkWh

        if maxChargeInkWh:
            """
            Specifies the maximum electric energy supply in kilowatt hours (kWh) that may be stored in the vehicle's battery.
            """
            params["maxChargeInkWh"] = maxChargeInkWh

        if auxiliaryPowerInkW:
            """
            Specifies the amount of power consumed by auxiliary systems, in kilowatts (kW).
            """
            params["auxiliaryPowerInkW"] = auxiliaryPowerInkW                     

        return self.parse_direction_json(self.client._request(url, get_params=params, dry_run=dry_run), traffic, routeRepresentation, maxAlternatives)

    @staticmethod
    def parse_direction_json(response, traffic, routeRepresentation, maxAlternatives):
        if response is None:  # pragma: no cover
            if maxAlternatives:
                if int(maxAlternatives) > 1:
                    return Directions()
            else:
                return Direction()
        
        if maxAlternatives:
            if int(maxAlternatives) > 1:
                # TODO
                pass 
        else:
            distance = response["routes"][0]["summary"]["lengthInMeters"]
            duration = response["routes"][0]["summary"]["travelTimeInSeconds"]
            if traffic:
                if traffic == "true":
                    duration = duration + response["routes"][0]["summary"]["trafficDelayInSeconds"]
            if routeRepresentation:
                if routeRepresentation== "polyline":
                    geometry = []
                    for node in response["routes"][0]["legs"][0]["points"]:
                        lat = node["latitude"]
                        lng = node["longitude"]
                        geometry.append([lat, lng])
                    return Direction(geometry=geometry, duration=duration, distance=distance, raw=response)
            else:
                return Direction(duration=duration, distance=distance, raw=response)