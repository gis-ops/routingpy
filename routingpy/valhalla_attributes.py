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
:class:`Expansion` returns expansion results.
"""
from enum import Enum
from typing import List, Optional, Tuple, Union

from routingpy.utils import decode_polyline6


class MatchDiscontinuity(str, Enum):
    BEGIN = "begin"
    END = "end"
    NONE = ""


class MatchType(str, Enum):
    UNMATCHED = "unmatched"
    MATCHED = "matched"
    INTERPOLATED = "interpolated"
    NONE = ""


class Traversability(str, Enum):
    FORWARD = "forward"
    BACKWARD = "backward"
    BOTH = "both"
    NONE = ""


class DrivingSide(str, Enum):
    RIGHT = "right"
    LEFT = "left"
    NONE = ""


class Sidewalk(str, Enum):
    RIGHT = "right"
    LEFT = "left"
    BOTH = "both"
    NONE = ""


class Surface(str, Enum):
    PAVED_SMOOTH = "paved_smooth"
    PAVED = "paved"
    PAVED_ROUGH = "paved_rough"
    COMPACTED = "compacted"
    DIRT = "dirt"
    GRAVEL = "gravel"
    PATH = "path"
    IMPASSABLE = "impassable"
    NONE = ""


class RoadClass(str, Enum):
    MOTORWAY = "motorway"
    TRUCK = "trunk"
    PRIMARY = "primary"
    SECONDARY = "secondary"
    TERTIARY = "tertiary"
    UNCLASSIFIED = "unclassified"
    RESIDENTIAL = "residential"
    SERVICE_OTHER = "service_other"
    NONE = ""


class Use(str, Enum):
    TRAM = "tram"
    ROAD = "road"
    RAMP = "ramp"
    TURN_CHANNEL = "turn_channel"
    TRACK = "track"
    DRIVEWAY = "driveway"
    ALLEY = "alley"
    PARKING_AISLE = "parking_aisle"
    EMERGENCY_ACCESS = "emergency_access"
    DRIVE_TROUGH = "drive_through"
    CULDESAC = "culdesac"
    CYCLEWAY = "cycleway"
    MOUNTAIN_BIKE = "mountain_bike"
    SIDEWALK = "sidewalk"
    FOOTWAY = "footway"
    STEPS = "steps"
    OTHER = "other"
    RAIL_FERRY = "rail-ferry"
    FERRY = "ferry"
    RAIL = "rail"
    BUS = "bus"
    RAIL_CONNECTION = "rail_connection"
    BUS_CONNECTION = "bus_connnection"
    TRANSIT_CONNECTION = "transit_connection"
    NONE = ""


class MatchedEdge:
    """
    Contains a parsed single line string and its attributes, if specified in the request.
    Access via properties ``geometry``, ``distances`` ``durations``, ``costs``, ``edge_ids``, ``statuses``.
    """

    def __init__(self, edge: dict, coords: List[List[float]]):
        self._geometry = coords
        self._traversability: Optional[Traversability] = (
            Traversability(edge.get("traversability", "")) or None
        )
        self._toll: Optional[bool] = edge.get("toll")
        self._use: Optional[Use] = Use(edge.get("use")) or None
        self._tunnel: Optional[bool] = edge.get("tunnel")
        self._names: Optional[List[str]] = edge.get("names")

        driving_side = edge.get("drive_on_right")
        if driving_side is True:
            self._driving_side = DrivingSide("right")
        elif driving_side is False:
            self._driving_side = DrivingSide("right")
        else:
            self._driving_side = None

        self._roundabout: Optional[bool] = edge.get("roundabout")
        self._bridge: Optional[bool] = edge.get("bridge")
        self._surface: Optional[Surface] = Surface(edge.get("surface", "")) or None
        self._edge_id: Optional[int] = edge.get("id")
        self._osm_way_id: Optional[int] = edge.get("way_id")
        self._speed_limit = edge.get("speed_limit")
        self._cycle_lane = edge.get("cycle_lane")
        self._sidewalk = Sidewalk(edge.get("sidewalk")) or None
        self._lane_count: Optional[int] = edge.get("lane_count")
        self._mean_elevation: Optional[int] = edge.get("mean_elevation")
        self._weighted_grade: Optional[int] = edge.get("weighted_grade")
        self._road_class: Optional[RoadClass] = RoadClass(edge.get("road_class", "")) or None
        self._speed: Optional[int] = edge.get("speed")
        self._length: Optional[int] = edge.get("length")

    @property
    def geometry(self) -> List[List[float]]:
        """
        The geometry of the edge as [[lon1, lat1], [lon2, lat2]] list.
        """
        return self._geometry

    @property
    def traversability(self) -> Optional[Traversability]:
        """
        The traversability of the edge, one of :class:`Traversability`.
        """
        return self._traversability

    @property
    def toll(self) -> Optional[bool]:
        """
        Is this a toll road?
        """
        return self._toll

    @property
    def use(self) -> Optional[Use]:
        """
        The Use of this edge as :class:`Use`.
        """
        return self._use

    @property
    def tunnel(self) -> Optional[bool]:
        """
        Is this part of a tunnel?
        """
        return self._tunnel

    @property
    def names(self) -> Optional[List[str]]:
        """
        Returns the list of names and aliases.
        """
        return self._names

    @property
    def driving_side(self) -> Optional[DrivingSide]:
        """
        Returns the :class:`DrivingSide` of the road.
        """
        return self._driving_side

    @property
    def roundabout(self) -> Optional[bool]:
        """
        Is this part of a roundabout?
        """
        return self._roundabout

    @property
    def bridge(self) -> Optional[bool]:
        """
        Is this part of a bridge?
        """
        return self._bridge

    @property
    def surface(self) -> Optional[Surface]:
        """
        Returns the :class:`Surface` value for this road.
        """
        return self._surface

    @property
    def edge_id(self) -> Optional[int]:
        """
        Returns the edge's GraphId?
        """
        return self._edge_id

    @property
    def osm_way_id(self) -> Optional[int]:
        """
        Returns the way's OSM ID.
        """
        return self._osm_way_id

    @property
    def speed_limit(self) -> Optional[int]:
        """
        The legal speed limit, if available
        """
        return self._speed_limit

    @property
    def cycle_lane(self) -> Optional[str]:
        """
        Returns the type (if any) of bicycle lane along this edge.
        """
        return self._cycle_lane

    @property
    def sidewalk(self) -> Optional[Sidewalk]:
        """
        Returns the :class:`Sidewalk` value for this road.
        """
        return self._sidewalk

    @property
    def lane_count(self) -> Optional[int]:
        """
        How many lanes does this road have?
        """
        return self._lane_count

    @property
    def mean_elevation(self) -> Optional[int]:
        """
        The mean elevation of this edge in meters.
        """
        return self._mean_elevation

    @property
    def weighted_grade(self) -> Optional[float]:
        """
        The weighted grade factor. Valhalla manufactures a weighted_grade from elevation data.
        It is a measure used for hill avoidance in routing - sort of a relative energy use along
        an edge. But since an edge in Valhalla can possibly go up and down over several hills it
        might not equate to what most folks think of as grade.
        """
        return self._weighted_grade

    @property
    def road_class(self) -> Optional[RoadClass]:
        """
        Returns the :class:`RoadClass` of this edge.
        """
        return self._road_class

    @property
    def speed(self) -> Optional[int]:
        """
        Returns the actual speed of the edge, as used by Valhalla.
        """
        return self._speed

    @property
    def length(self) -> Optional[int]:
        """
        The length of this edge in meters.
        """
        return self._length

    def __repr__(self):  # pragma: no cover
        return "Edge({})".format(", ".join([f"{k[1:]}: {v}" for k, v in vars(self).items() if v]))


class MatchedPoint:
    """
    A single matched point
    """

    def __init__(self, point: dict):
        self._geometry: List[float] = [point["lon"], point["lat"]]
        self._match_type = MatchType(point.get("type", "")) or None
        self._dist_along_edge: Optional[float] = point.get("distance_along_edge")
        self._dist_from_input: Optional[int] = point.get("distance_from_trace_point")
        self._edge_index: Optional[int] = point.get("distance_along_edge")
        self._discontinuity: Optional[MatchDiscontinuity] = None
        if point.get("begin_route_discontinuity"):
            self._discontinuity = MatchDiscontinuity("begin")
        elif point.get("end_route_discontinuity"):
            self._discontinuity = MatchDiscontinuity("end")

    @property
    def geometry(self) -> Union[Tuple[float, float], List[float]]:
        """
        The geometry of the point as [lon1, lat1] list.
        """
        return self._geometry

    @property
    def match_type(self) -> MatchType:
        """
        Returns the match type.
        """
        return self._match_type

    @property
    def distance_along_edge(self) -> Optional[float]:
        """
        Returns the relative distance along the matched edge. E.g. if the point
        projects to the center of an edge, the return value will be 0.5.
        """
        return self._dist_along_edge

    @property
    def distance_from_input(self) -> Optional[int]:
        """
        Returns the distance of the matched point from the corresponding input location.
        """
        return self._dist_from_input

    @property
    def edge_index(self) -> Optional[int]:
        """
        Returns the edge index.
        """
        return self._edge_index

    @property
    def discontinuity(self) -> Optional[MatchDiscontinuity]:
        """
        Returns the :class:`MatchDiscontinuity` status.
        """
        return self._discontinuity


class MatchedResults:
    """
    Contains a list of :class:`Expansion`, which can be iterated over or accessed by index. The property ¸`raw`` contains
    the complete raw response of the expansion request.
    """

    def __init__(self, response: Optional[dict] = None):
        self._edges: List[MatchedEdge] = list()
        self._points: List[MatchedPoint] = list()
        self._raw = response

        if not response:
            return

        geometry = decode_polyline6(response["shape"])
        # fill the edges
        for edge in response["edges"]:
            coords: List[List[float]] = geometry[
                response.get("begin_shape_index")
                or 0 : (response.get("end_shape_index") or (len(geometry) - 1)) + 1
            ]
            self._edges.append(MatchedEdge(edge, coords))

        # and the nodes
        for pt in response["matched_points"]:
            self._points.append(MatchedPoint(pt))

    @property
    def raw(self) -> Optional[dict]:
        """
        Returns the trace_attribute's raw, unparsed response. For details, consult the documentation
         at https://valhalla.readthedocs.io/en/latest/api/map-matching/api-reference/.

        :rtype: dict or None
        """
        return self._raw

    @property
    def matched_edges(self) -> Optional[List[MatchedEdge]]:
        """Returns the list of :class:`MatchedEdge`"""
        return self._edges

    @property
    def matched_points(self) -> Optional[List[MatchedPoint]]:
        """Returns the list of :class:`MatchedEdge`"""
        return self._points

    def __repr__(self):  # pragma: no cover
        if len(self._edges) < 10 and len(self._points) < 10:
            return "Expansions({}, {}, {})".format(self._edges, self._points, self.raw)
        else:
            return "Expansions({}, ..., {}; {}, ..., {})".format(
                ", ".join([str(e) for e in self._edges[:3]]),
                ", ".join(str(e) for e in self._edges[-3:]),
                ", ".join([str(e) for e in self._points[:3]]),
                ", ".join(str(e) for e in self._points[-3:]),
            )
