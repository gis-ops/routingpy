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
import datetime
import random

from routingpy.optimization import Job, Vehicle

PARAM_POINT = [8.34234, 48.23424]
PARAM_LINE = [[8.688641, 49.420577], [8.680916, 49.415776]]
PARAM_LINE_MULTI = [[8.688641, 49.420577], [8.680916, 49.415776], [8.780916, 49.445776]]
PARAM_POLY = [[[8.688641, 49.420577], [8.680916, 49.415776]]]

PARAM_INT_BIG = 500
PARAM_INT_SMALL = 50

PARAM_STRING = random.choice("abcdefghijklmnopqrstuvwxyz")

PARAM_GEOJSON_POINT = {"type": "Point", "coordinates": PARAM_POINT}
PARAM_GEOJSON_LINE = {"type": "LineString", "coordinates": PARAM_LINE}
PARAM_GEOJSON_POLY = {"type": "Polygon", "coordinates": PARAM_POLY}

ENDPOINTS_RESPONSES = {
    "valhalla": {
        "directions": {
            "trip": {
                "legs": [
                    {
                        "shape": "}wpulAvkxblCtJpGu}@hrCkAvDsAdEm@xBkAvDeK`\\ssAthE{iAjpDyiAlpD",
                        "summary": {"length": 100, "time": 100},
                    },
                    {
                        "shape": "}wpulAvkxblCtJpGu}@hrCkAvDsAdEm@xBkAvDeK`\\ssAthE{iAjpD",
                        "summary": {"length": 50, "time": 50},
                    },
                ]
            }
        },
        "isochrones": {
            "type": "FeatureCollection",
            "bbox": [8.688474, 8.681829, 49.42577, 49.420176],
            "features": [
                {
                    "type": "Feature",
                    "properties": {
                        "group_index": 0,
                        "value": 100,
                        "center": [8.684162488752957, 49.4230724075398],
                    },
                    "geometry": {
                        "coordinates": [
                            [[8.684544, 49.423295], [8.684665, 49.423101], [8.684706, 49.423036]]
                        ],
                        "type": "Polygon",
                    },
                },
                {
                    "type": "Feature",
                    "properties": {
                        "group_index": 0,
                        "value": 100,
                        "center": [8.684162488752957, 49.4230724075398],
                    },
                    "geometry": {
                        "coordinates": [
                            [[8.684544, 49.423295], [8.684665, 49.423101], [8.684706, 49.423036]]
                        ],
                        "type": "Polygon",
                    },
                },
            ],
        },
        "matrix": {
            "sources_to_targets": [
                [{"distance": 0, "time": 0}, {"distance": 100, "time": 100}],
                [{"distance": 100, "time": 100}, {"distance": 0, "time": 0}],
            ]
        },
        "expansion": {
            "properties": {"algorithm": "unidirectional_dijkstra"},
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "MultiLineString",
                        "coordinates": [
                            [[0.00027, -0.00017], [0.00027, 0.0]],
                            [[0.00027, -0.00017], [0.00027, -0.00035]],
                            [[0.00027, -0.00035], [0.00027, -0.00017]],
                            [[0.00027, 0.0], [0.00027, -0.00017]],
                            [[0.00027, -0.00017], [0.00053, -0.00017]],
                            [[0.00027, -0.00017], [0.0, -0.00017]],
                            [[0.0, -0.00017], [0.00027, -0.00017]],
                            [[0.00053, -0.00017], [0.0008, -0.00017]],
                            [[0.0008, -0.00017], [0.00053, -0.00017]],
                            [[0.00053, -0.00017], [0.00027, -0.00017]],
                            [[0.00053, -0.00017], [0.0008, 0.0]],
                        ],
                    },
                    "properties": {
                        "distances": [20, 20, 40, 40, 30, 30, 60, 60, 90, 120, 80],
                        "durations": [0, 0, 29, 29, 1, 1, 30, 2, 31, 33, 5],
                        "costs": [0, 0, 1, 1, 1, 1, 2, 2, 3, 4, 11],
                    },
                }
            ],
        },
        "trace_attributes": {
            "shape": "qekg}Aq|hqOhIvcBjHo@`]iCFnBbCSh@AlACz@CTCdCvc@vCnl@j@`PjAnTDp@HlBLrBBZpB`b@lBb]~AfZx@`MxWeEDv@FnAFzALz@f@Gt@GzPniBPrC|@Od@MvLgDdWmGjG{C~@v@TpB^?t@CjBMj@I@}@L]RQhAcAxCr@nCx@nCN~UpHrEv@rSrEbZhGFbV",
            "matched_points": [
                {
                    "distance_from_trace_point": 20.547,
                    "edge_index": 0,
                    "type": "matched",
                    "distance_along_edge": 0.000,
                    "lat": 49.420393,
                    "lon": 8.688601,
                },
                {
                    "distance_from_trace_point": 1.403,
                    "edge_index": 41,
                    "type": "matched",
                    "distance_along_edge": 0.435,
                    "lat": 49.415789,
                    "lon": 8.680916,
                },
            ],
            "edges": [
                {
                    "end_node": {
                        "transition_time": 0.000,
                        "fork": False,
                        "type": "street_intersection",
                        "admin_index": 0,
                        "elapsed_time": 83.294,
                        "time_zone": "Europe/Berlin",
                        "intersecting_edges": [
                            {
                                "road_class": "residential",
                                "use": "road",
                                "begin_heading": 353,
                                "to_edge_name_consistency": True,
                                "from_edge_name_consistency": False,
                                "driveability": "both",
                                "cyclability": "both",
                                "walkability": "both",
                            }
                        ],
                    },
                    "length": 0.118,
                    "speed": 5,
                    "road_class": "residential",
                    "begin_heading": 261,
                    "end_heading": 261,
                    "weighted_grade": 0.000,
                    "mean_elevation": 116,
                    "max_downward_grade": None,
                    "bicycle_network": 0,
                    "lane_count": 1,
                    "max_upward_grade": None,
                    "sidewalk": "both",
                    "density": 7,
                    "cycle_lane": "none",
                    "speed_limit": 30,
                    "truck_route": False,
                    "way_id": 25325392,
                    "pedestrian_type": "foot",
                    "end_shape_index": 1,
                    "id": 4649811837074,
                    "travel_mode": "pedestrian",
                    "surface": "paved_smooth",
                    "bridge": False,
                    "roundabout": False,
                    "drive_on_right": True,
                    "names": ["Roonstraße"],
                    "shoulder": False,
                    "sac_scale": 0,
                    "internal_intersection": False,
                    "tunnel": False,
                    "unpaved": False,
                    "use": "road",
                    "toll": False,
                    "traversability": "both",
                    "begin_shape_index": 0,
                },
                {
                    "end_node": {
                        "transition_time": 0.000,
                        "fork": False,
                        "type": "street_intersection",
                        "admin_index": 0,
                        "elapsed_time": 92.294,
                        "time_zone": "Europe/Berlin",
                        "intersecting_edges": [
                            {
                                "road_class": "service_other",
                                "use": "footway",
                                "begin_heading": 265,
                                "to_edge_name_consistency": False,
                                "from_edge_name_consistency": False,
                                "walkability": "both",
                            }
                        ],
                    },
                    "length": 0.017,
                    "speed": 7,
                    "road_class": "residential",
                    "begin_heading": 174,
                    "end_heading": 174,
                    "weighted_grade": -6.667,
                    "mean_elevation": 116,
                    "max_downward_grade": None,
                    "bicycle_network": 0,
                    "lane_count": 1,
                    "max_upward_grade": None,
                    "sidewalk": "both",
                    "density": 7,
                    "cycle_lane": "none",
                    "speed_limit": 30,
                    "truck_route": False,
                    "way_id": 52977975,
                    "pedestrian_type": "foot",
                    "end_shape_index": 2,
                    "id": 985500090514,
                    "travel_mode": "pedestrian",
                    "surface": "paved_smooth",
                    "bridge": False,
                    "roundabout": False,
                    "drive_on_right": True,
                    "names": ["Werderplatz"],
                    "shoulder": False,
                    "sac_scale": 0,
                    "internal_intersection": False,
                    "tunnel": False,
                    "unpaved": False,
                    "use": "road",
                    "toll": False,
                    "traversability": "both",
                    "begin_shape_index": 1,
                },
                {
                    "end_node": {
                        "transition_time": 0.000,
                        "fork": False,
                        "type": "street_intersection",
                        "admin_index": 0,
                        "elapsed_time": 130.412,
                        "time_zone": "Europe/Berlin",
                        "intersecting_edges": [
                            {
                                "road_class": "residential",
                                "use": "road",
                                "begin_heading": 173,
                                "to_edge_name_consistency": False,
                                "from_edge_name_consistency": True,
                                "driveability": "forward",
                                "cyclability": "forward",
                                "walkability": "both",
                            }
                        ],
                    },
                    "length": 0.054,
                    "speed": 5,
                    "road_class": "residential",
                    "begin_heading": 175,
                    "end_heading": 175,
                    "weighted_grade": 0.000,
                    "mean_elevation": 116,
                    "max_downward_grade": None,
                    "bicycle_network": 0,
                    "lane_count": 1,
                    "max_upward_grade": None,
                    "sidewalk": "both",
                    "density": 7,
                    "cycle_lane": "none",
                    "speed_limit": 30,
                    "truck_route": False,
                    "way_id": 52977975,
                    "pedestrian_type": "foot",
                    "end_shape_index": 3,
                    "id": 986070515858,
                    "travel_mode": "pedestrian",
                    "surface": "paved_smooth",
                    "bridge": False,
                    "roundabout": False,
                    "drive_on_right": True,
                    "names": ["Werderplatz"],
                    "shoulder": False,
                    "sac_scale": 0,
                    "internal_intersection": False,
                    "tunnel": False,
                    "unpaved": False,
                    "use": "road",
                    "toll": False,
                    "traversability": "both",
                    "begin_shape_index": 2,
                },
            ],
        },
    },
    "osrm": {
        "directions_geojson": {
            "routes": [
                {
                    "geometry": {"coordinates": [[8.681495, 49.41461], [8.681445, 49.415755]]},
                    "duration": 100,
                    "distance": 100,
                }
            ]
        },
        "directions_polyline": {
            "routes": [
                {
                    "geometry": "qmbjHspkr@kCmCpE{T~M|@|QcRvC}OjCgD~F~@~I~SjLxqAjT||@lDde@aBhh@uUbuAmJpPod@|c@iWhQoSt_@}Hx]oTfNqNWqQeKilAa]hByx@DiCvDd@dNxJ[zMl[eCfKlBn[rUb]z]pGoGbHtY|j@xw@jKnFfd@~IdhEpyFm@rGpInKyAhDuDuE",
                    "duration": 100,
                    "distance": 100,
                }
            ]
        },
        "directions_polyline6": {
            "routes": [
                {
                    "geometry": "wpan|A}n|`O{j@yk@v`AuyE~tCfRx|De~Dln@khDhj@as@doAnR~lBhqEtdCxzXvtExjRvu@t|Ju]z{K}aFd|YiqBrnDkvJrpJ_rF|uDalEhfIibB`sHavEjwCgzCyFayDkxBadWykHf`@_aQ|@cj@rx@rJjvCduBgGtsCb{Gsh@lyBla@f|GhaFxkHvsHttAatAhzAliGvvLnwPtzBriAjsJhmBvz}@jhmAoMnuA`iBb|Bi[bt@}w@ebA",
                    "duration": 100,
                    "distance": 100,
                }
            ]
        },
        "matrix": {"durations": [[1, 2, 3], [4, 5, 6]], "distances": [[1, 2, 3], [4, 5, 6]]},
    },
    "mapbox_osrm": {
        "directions": {
            "routes": [
                {
                    "geometry": {"coordinates": [[8.681495, 49.41461], [8.681445, 49.415755]]},
                    "duration": 100,
                    "distance": 100,
                }
            ]
        },
        "isochrones": {
            "type": "FeatureCollection",
            "bbox": [8.688474, 8.681829, 49.42577, 49.420176],
            "features": [
                {
                    "type": "Feature",
                    "properties": {
                        "group_index": 0,
                        "value": 100,
                        "center": [8.684162488752957, 49.4230724075398],
                    },
                    "geometry": {
                        "coordinates": [
                            [[8.684544, 49.423295], [8.684665, 49.423101], [8.684706, 49.423036]]
                        ],
                        "type": "Polygon",
                    },
                },
                {
                    "type": "Feature",
                    "properties": {
                        "group_index": 0,
                        "value": 100,
                        "center": [8.684162488752957, 49.4230724075398],
                    },
                    "geometry": {
                        "coordinates": [
                            [[8.684544, 49.423295], [8.684665, 49.423101], [8.684706, 49.423036]]
                        ],
                        "type": "Polygon",
                    },
                },
            ],
        },
        "matrix": {"distances": [[1, 2, 3], [4, 5, 6]], "durations": [[1, 2, 3], [4, 5, 6]]},
    },
    "google": {
        "directions": {
            "routes": [
                {
                    "legs": [
                        {
                            "distance": {"value": 541359},
                            "duration": {"value": 19448},
                            "steps": [
                                {
                                    "distance": {"value": 280},
                                    "duration": {"value": 67},
                                    "polyline": {
                                        "points": "ayotGvy_sMV]t@_APk@DOFW@O@OAwADiE?k@Hq@@UHuG@s@@{@DiIDsFDkG@aIAa@?WAUASGe@Im@EYEOCOO_@Kk@Ie@Oe@GWKUMWwAoCmDmGwB}D_AgBoAaCqCaGuA_D}@_BIS]m@KQMUy@}AwAgCk@cAiB_D{AsCcBwCmAsBm@aAoAuBeB{Bm@sAe@mAMa@Qi@Uy@e@eB[eAIUOm@u@iCi@eCaA}DcAyCy@qB{EiIMU"
                                    },
                                },
                                {
                                    "distance": {"value": 2493},
                                    "duration": {"value": 511},
                                    "polyline": {
                                        "points": "ayotGvy_sMV]t@_APk@DOFW@O@OAwADiE?k@Hq@@UHuG@s@@{@DiIDsFDkG@aIAa@?WAUASGe@Im@EYEOCOO_@Kk@Ie@Oe@GWKUMWwAoCmDmGwB}D_AgBoAaCqCaGuA_D}@_BIS]m@KQMUy@}AwAgCk@cAiB_D{AsCcBwCmAsBm@aAoAuBeB{Bm@sAe@mAMa@Qi@Uy@e@eB[eAIUOm@u@iCi@eCaA}DcAyCy@qB{EiIMU"
                                    },
                                },
                            ],
                        }
                    ]
                }
            ],
            "status": "OK",
        },
        "matrix": {
            "rows": [
                {
                    "elements": [
                        {
                            "distance": {"text": "225 mi", "value": 361957},
                            "duration": {"text": "3 hours 50 mins", "value": 13813},
                        }
                    ]
                }
            ]
        },
    },
    "ors": {
        "directions": {
            "json": {
                "routes": [
                    {
                        "summary": {"distance": 850.5, "duration": 191.4},
                        "geometry": "ihrlHir~s@cFFcAKeB_@_B]g@IUAQB]PaCr@y@cJeBXe@qJ_@kH??",
                    }
                ]
            },
            "geojson": {
                "type": "FeatureCollection",
                "features": [
                    {
                        "type": "Feature",
                        "geometry": {
                            "coordinates": [[8.681495, 49.41461], [8.681445, 49.415755]],
                            "type": "LineString",
                        },
                        "properties": {"summary": {"distance": 850.5, "duration": 191.4}},
                    }
                ],
            },
        },
        "isochrones": {
            "type": "FeatureCollection",
            "bbox": [8.688474, 8.681829, 49.42577, 49.420176],
            "features": [
                {
                    "type": "Feature",
                    "properties": {
                        "group_index": 0,
                        "value": 100,
                        "center": [8.684162488752957, 49.4230724075398],
                    },
                    "geometry": {
                        "coordinates": [
                            [[8.684544, 49.423295], [8.684665, 49.423101], [8.684706, 49.423036]]
                        ],
                        "type": "Polygon",
                    },
                },
                {
                    "type": "Feature",
                    "properties": {
                        "group_index": 0,
                        "value": 200,
                        "center": [8.684162488752957, 49.4230724075398],
                    },
                    "geometry": {
                        "coordinates": [
                            [[8.683974, 49.423982], [8.684035, 49.423627], [8.685104, 49.422131]]
                        ],
                        "type": "Polygon",
                    },
                },
                {
                    "type": "Feature",
                    "properties": {
                        "group_index": 0,
                        "value": 300,
                        "center": [8.684162488752957, 49.4230724075398],
                    },
                    "geometry": {
                        "coordinates": [
                            [[8.68261, 49.423744], [8.682671, 49.423389], [8.683764, 49.421902]]
                        ],
                        "type": "Polygon",
                    },
                },
                {
                    "type": "Feature",
                    "properties": {
                        "group_index": 0,
                        "value": 400,
                        "center": [8.684162488752957, 49.4230724075398],
                    },
                    "geometry": {
                        "coordinates": [
                            [[8.681829, 49.424426], [8.682416, 49.421699], [8.686179, 49.420176]]
                        ],
                        "type": "Polygon",
                    },
                },
            ],
        },
        "matrix": {
            "durations": [[7900.34], [0], [136841.92], [483295.5]],
            "distances": [[125414.58], [0], [2383943.25], [10037064]],
        },
    },
    "graphhopper": {
        "directions": {
            "paths": [
                {"distance": 15239.553, "time": 2349463, "points": "korlHun~s@inUAiBP"},
                {"distance": 15239.553, "time": 2349463, "points": "korlHun~s@inUAiBP"},
                {"distance": 15239.553, "time": 2349463, "points": "korlHun~s@inUAiBP"},
            ]
        },
        "isochrones": {
            "polygons": [
                {
                    "type": "Feature",
                    "properties": {"bucket": 0},
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [
                            [
                                [8.345841896068496, 48.23514181901086, 1.0],
                                [8.340545650732793, 48.23651784814562, 1.5],
                                [8.340935036709944, 48.23593307068795, 1.5],
                            ]
                        ],
                    },
                },
                {
                    "type": "Feature",
                    "properties": {"bucket": 1},
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [
                            [
                                [8.345999848380682, 48.23155678581201, 2.0],
                                [8.348431345412836, 48.234402721399135, 2.0],
                                [8.348099422039823, 48.23458791489723, 2.0],
                            ]
                        ],
                    },
                },
                {
                    "type": "Feature",
                    "properties": {"bucket": 2},
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [
                            [
                                [8.349068835729408, 48.2354851976518, 2.5],
                                [8.34836307396443, 48.23601708826144],
                                [8.342155162442218, 48.23711268388732, 2.5],
                            ]
                        ],
                    },
                },
            ]
        },
        "matrix": {
            "distances": [[0, 1181, 13965], [1075, 0, 14059], [14120, 13766, 0]],
            "times": [[0, 255, 2122], [242, 0, 2094], [2144, 2021, 0]],
            "weights": [[0.0, 272.99, 2331.526], [258.115, 0.0, 2305.121], [2356.307, 2225.083, 0.0]],
        },
    },
    "heremaps": {
        "directions": {
            "response": {
                "route": [
                    {
                        "shape": ["8.6841352,49.4161567,560.0", "8.683039,49.4174594,560.0"],
                        "summary": {
                            "distance": 27084,
                            "trafficTime": 2830,
                            "baseTime": 2830,
                            "travelTime": 2830,
                        },
                    },
                    {
                        "shape": ["8.6841352,49.4161567,560.0", "8.683039,49.4174594,560.0"],
                        "summary": {
                            "distance": 27084,
                            "trafficTime": 2830,
                            "baseTime": 2830,
                            "travelTime": 2830,
                        },
                    },
                    {
                        "shape": ["8.6841352,49.4161567,560.0", "8.683039,49.4174594,560.0"],
                        "summary": {
                            "distance": 27084,
                            "trafficTime": 2830,
                            "baseTime": 2830,
                            "travelTime": 2830,
                        },
                    },
                ]
            }
        },
        "isochrones": {
            "response": {
                "center": {"latitude": 8.3423399, "longitude": 48.23424},
                "isoline": [
                    {
                        "range": 1000,
                        "component": [
                            {"id": 0, "shape": ["8.3724403,48.2271481", "8.3729553,48.2272339"]}
                        ],
                    },
                    {
                        "range": 2000,
                        "component": [
                            {"id": 0, "shape": ["8.3724403,48.2271481", "8.3729553,48.2272339"]}
                        ],
                    },
                    {
                        "range": 3000,
                        "component": [
                            {"id": 0, "shape": ["8.3724403,48.2271481", "8.3729553,48.2272339"]}
                        ],
                    },
                ],
                "start": {
                    "linkId": "+1141790171",
                    "mappedPosition": {"latitude": 8.3658099, "longitude": 48.2353663},
                    "originalPosition": {"latitude": 8.3423399, "longitude": 48.23424},
                },
            }
        },
        "matrix": {
            "response": {
                "matrixEntry": [
                    {
                        "startIndex": 0,
                        "destinationIndex": 0,
                        "summary": {"distance": 1398, "travelTime": 82, "costFactor": 82},
                    },
                    {
                        "startIndex": 1,
                        "destinationIndex": 0,
                        "summary": {"distance": 1188, "travelTime": 69, "costFactor": 69},
                    },
                    {"startIndex": 1, "destinationIndex": 0, "status": "failed"},
                ]
            }
        },
    },
    "vroom": {
        "optimization": {
            "code": 0,
            "summary": {
                "cost": 4097,
                "routes": 2,
                "unassigned": 0,
                "setup": 0,
                "service": 0,
                "duration": 4097,
                "waiting_time": 0,
                "priority": 0,
                "distance": 43547,
                "violations": [],
                "computing_times": {"loading": 3, "solving": 0, "routing": 3},
            },
            "unassigned": [],
            "routes": [
                {
                    "vehicle": 0,
                    "cost": 0,
                    "setup": 0,
                    "service": 0,
                    "duration": 0,
                    "waiting_time": 0,
                    "priority": 0,
                    "distance": 0,
                    "steps": [
                        {
                            "type": "start",
                            "location": [8.688641, 49.420577],
                            "setup": 0,
                            "service": 0,
                            "waiting_time": 0,
                            "arrival": 0,
                            "duration": 0,
                            "violations": [],
                            "distance": 0,
                        },
                        {
                            "type": "job",
                            "location": [8.688641, 49.420577],
                            "id": 0,
                            "setup": 0,
                            "service": 0,
                            "waiting_time": 0,
                            "job": 0,
                            "arrival": 0,
                            "duration": 0,
                            "violations": [],
                            "distance": 0,
                        },
                        {
                            "type": "end",
                            "location": [8.688641, 49.420577],
                            "setup": 0,
                            "service": 0,
                            "waiting_time": 0,
                            "arrival": 0,
                            "duration": 0,
                            "violations": [],
                            "distance": 0,
                        },
                    ],
                    "violations": [],
                    "geometry": "olslHi_`t@????",
                },
                {
                    "vehicle": 1,
                    "cost": 4097,
                    "setup": 0,
                    "service": 0,
                    "duration": 4097,
                    "waiting_time": 0,
                    "priority": 0,
                    "distance": 43547,
                    "steps": [
                        {
                            "type": "start",
                            "location": [8.680916, 49.415776],
                            "setup": 0,
                            "service": 0,
                            "waiting_time": 0,
                            "arrival": 0,
                            "duration": 0,
                            "violations": [],
                            "distance": 0,
                        },
                        {
                            "type": "job",
                            "location": [8.780916, 49.445776],
                            "id": 2,
                            "setup": 0,
                            "service": 0,
                            "waiting_time": 0,
                            "job": 2,
                            "arrival": 2043,
                            "duration": 2043,
                            "violations": [],
                            "distance": 21683,
                        },
                        {
                            "type": "job",
                            "location": [8.680916, 49.415776],
                            "id": 1,
                            "setup": 0,
                            "service": 0,
                            "waiting_time": 0,
                            "job": 1,
                            "arrival": 4097,
                            "duration": 4097,
                            "violations": [],
                            "distance": 43547,
                        },
                        {
                            "type": "end",
                            "location": [8.680916, 49.415776],
                            "setup": 0,
                            "service": 0,
                            "waiting_time": 0,
                            "arrival": 4097,
                            "duration": 4097,
                            "violations": [],
                            "distance": 43547,
                        },
                    ],
                    "violations": [],
                    "geometry": "korlHwn~s@AgBB_FBuF?_KC{DE{EIyJCyBCsCGmE?E?A?I?CE{Ej@ElBGlACJ?pCED?NB?K@OB_@NoBZyD@S@S?Y@I@E?W?E?E@E@G@CBEGg@CSAO?W?w@BoGA]?[Ae@AUEy@QgCKgAWuBQoAAQMsACSKu@QeA[sBGc@QsBWeCEk@Ce@I{@O_BScBGk@I{@Iu@Ac@Ca@[kKCc@AS?KCk@Ek@G_ACo@Cg@Ac@CiAKiFEoBAe@E_BAGOkDGgAEk@QmAOgAIi@Mc@COEKCK?CKc@Os@CMGU_@mBIe@[_B_@wBi@yDk@uFKu@CSQkAO_ACSIWEMGOM[[q@]y@i@kAs@oA_AyA[e@c@s@S_@OWMWGOCIGUGUCKEQKc@Ki@UoAO_AGc@Ea@Iy@Gu@Es@GcAE_AEu@Ai@Ci@Ac@AaAC_C?g@@o@@k@JmBHgATwBNmA\\aC@MlAsGJm@BMH_@DQd@uB\\uAl@qCv@sDvAoHZoBVuBR}An@}Fh@cFNyA`@iETkDLmCFkD?cDKkEIgBIsAQoBGy@a@oEW{CSqCKcBI}ACw@Cs@EkD?q@?Y@cA@i@@aAJwCNcCHeAJ}ARkBD_@TgBHm@@GF]p@eEBOx@}ENiAF]Hq@T}BFu@JyAHqB@WDqBDiBJ_EBq@J{CLgBN{Bf@oEJw@RcBFe@BS\\_CVgBPgALi@Rw@HSTi@LWJUHKNURUlDsCfBoAh@a@z@i@rAu@vAw@~@e@HEl@[VM|BoAbJwE`CaAzB}@~@[j@Oz@SjAOfAIpAMhCBn@BdAH~@H\\DdARn@H|BZvFv@jFv@jALp@DfABz@IdAYf@Ud@W\\WZYLOPUPWZg@Xk@Rg@L_@J]Ja@H_@Hg@He@BYBWDa@FmA@qA?w@C{@Cq@G_AK}@Ee@AISkBo@iFWkBy@aIwB}SE_@MeBMkBEiBE{BAaC?kA@g@@Y?QBWDYBWF[Z_BD[DSD]D[B]Du@FeABQ@SBUBQHa@FYZcABIj@kBJ]J]DUDSDWBQD_@@SBa@BiADkC@w@@]B_@Bi@B]Dk@Fs@NaAR{A@CHi@Pw@^iBF]DI@G@M?O?K?MCOBCBE@E@G?G?EAGLULS@E?OBIBGFSF]Di@Fm@Ba@Bc@DaB@g@?m@AME}CEyAA_A?k@?_@@c@@c@@]Dm@Ba@De@D_@D]VyAHm@N}@NcAFm@Dc@De@Ba@B}@@E@u@@c@?c@Ao@Ai@Cc@Ei@Ea@?EIk@QoA[_BMk@Qi@a@oA[w@gAoBiAgBs@aAY_@kBuB_A}@cB{AoBaB{AeA}AcAcCwA{CgBqBuA_Ak@o@[]M]Ka@KUGq@Ks@G}@IsCUuCYi@Ig@Im@Mq@Mi@S_@MWMk@We@WeAu@g@_@q@i@s@w@e@q@a@q@S_@Q_@M[IYO_@Oi@S}@GWAKKm@Ks@Ei@Gm@GcBA_A?o@@c@?]Bi@Bc@Di@Fu@Fg@Jq@l@_EHq@z@qIFc@DW@EP{@H_@F]Fw@D[Ba@HkB@gACYIaAK_@Mm@E]CWAUY?k@Ek@A{@Fw@^YJMHKLMRKTMTCFc@~@a@dA]hA[rAY`BMzBCXGRq@vACHAH?H?dAXdKHxE@pA@`A?n@Cx@MbAQx@Yz@Wr@oAxBgCpE{D|H]`AM`AIr@Ct@?z@F~@nAjHx@hE^fD@pDQhFYnH]`L[~HKdCYdD_AbECPy@dCO^}@fBgA~AcAjAu@j@_@Na@B_@E]Mm@c@k@c@q@YYGWCq@Ao@B_BFkBDqBEu@Fs@Pu@ZgAj@y@X}AXyARu@J_@?_@C_@IyAi@oCqAoEqCoCgCwDcCu@a@uI}EgAq@eAg@i@SSEa@@_@?aBF]Ai@MiAc@w@Gk@Dm@PQHy@f@uAv@OHs@|@a@r@Q`@Kd@Kv@Gf@ARIxACfACXGVf@XPLFJDLAh@KZMb@Mh@QnAU`B[fBQl@QZmAfAk@`@@JuB`IqBzIM`@OTc@`@Yb@I\\I`@CXFNc@h@c@j@c@`AyAjDaAjDOd@Sp@c@xAMxAEnAI|DWhG_@fCMhAQzAUvASrAEf@EXIx@Cx@E~@G^EPITOTUXOHKBKAMDUPW^QTUZMNQPOJSHUDi@BcAC{@Ew@Cs@?}@Be@Bc@BUDm@Jg@P_@Z_@Xc@Vk@P[HZIj@Qb@W^Y^[f@Ql@KTEb@Cd@C|@Cr@?v@Bz@DbABh@CTERINKPQLOT[PUV_@TQLEJ@JCNITYNUHUDQF_@D_ABy@Hy@DYDg@RsATwAP{ALiA^gCViGH}DDoALyAb@yARq@Ne@`AkDxAkDb@aAb@k@b@i@`CaDl@{@Tc@Nc@~@}BlAqC`@s@^g@t@eAn@{AVo@Tw@VcBHuAAcACcAAeAFwB@WAU@i@EMGKQMg@YFWBYBgAHyA@SFg@Jw@Je@Pa@`@s@r@}@NItAw@x@g@PIl@Qj@Ev@FhAb@h@L\\@`BG^?`@ARDh@RdAf@fAp@tI|Et@`@vDbCnCfCnEpCnCpAxAh@^H^B^?t@KxAS|AYx@YfAk@t@[r@Qt@GpBDjBE~AGn@Cp@@VBXFp@Xj@b@l@b@\\L^D`@C^Ot@k@bAkAfA_B|@gBN_@x@eCBQ~@cEXeDJeCZ_I\\aLXoHPiFAqD_@gDy@iEoAkHG_A?{@Bu@Hs@LaA\\aAzD}HfCqEnAyBVs@X{@Py@LcABy@?o@AaAAqAIyEYeK?eA?I@IBIp@wAFSBYL{BXaBZsA\\iA`@eAb@_ABGLUJULSJMLIXKv@_@z@Gj@@j@DX?@TBVD\\Ll@J^H`ABXAfAIjBC`@EZGv@G\\I^Qz@ADEVGb@{@pIIp@m@~DKp@Gf@Gt@Eh@Cb@Ch@?\\Ab@?n@@~@FbBFl@Dh@Jr@Jl@@JFVR|@Nh@N^HXLZP^R^`@p@d@p@r@v@p@h@f@^dAt@d@Vj@VVL^Lh@Rp@Ll@Lf@Hh@HtCXrCT|@Hr@Fp@JTF`@J\\J\\Ln@Z~@j@pBtAzCfBbCvA|AbAzAdAnB`BbBzA~@|@jBtBX^r@`AhAfBfAnBZv@`@nAPh@Lj@Z~APnAHj@?DD`@Dh@Bb@@h@@n@?b@Ab@At@ADC|@C`@Ed@Eb@Gl@ObAO|@Il@WxAE\\E^Ed@C`@El@A\\Ab@Ab@?^?j@@~@DxAD|C@L?l@Af@E`BCb@C`@Gl@Eh@G\\GRCFCHIDMRORCCCAE?C?E@CBCDADAB?@AF?D?F@F@D@DBBBBD@B@DP@R?V?RG\\_@hBQv@Ih@ABSzAO`AGr@Ej@C\\Ch@C^A\\Av@EjCChAC`@ARE^CPEVERETK\\K\\k@jBCH[bAGXI`@CPCTARCPGdAEt@C\\EZE\\EREZ[~AGZCVEXCV?PAXAf@?jA@`CDzBDhBLjBLdBD^vB|Sx@`IVjBn@hFRjB@HDd@J|@F~@Bp@Bz@?v@ApAGlAE`@CVCXId@If@I^K`@K\\M^Sf@Yj@[f@QVQTMN[X]Ve@Vg@TeAX{@HgACq@EkAMkFw@wFw@}B[o@IeAS]E_AIeAIo@CiCCqALgAHkAN{@Rk@N_AZ{B|@aC`AcJvE}BnAWLm@ZID_Ad@wAv@sAt@{@h@i@`@gBnAmDrCSTOTIJKTMVUh@IRSv@Mh@QfAWfB]~BCRGd@SbBKv@g@nEOzBMfBKzCCp@K~DEhBEpBAVIpBKxAGt@U|BIp@G\\OhAy@|ECNq@dEG\\AFIl@UfBE^SjBK|AIdAObCKvCA`AAh@AbA?X?p@DjDBr@Bv@H|AJbBRpCVzC`@nEFx@PnBHrAHfBJjE?bDGjDMlCUjDa@hEOxAi@bFo@|FS|AWtB[nBwAnHw@rDm@pC]tAe@tBEPI^CLKl@mArGAL]`COlAUvBIfAKlBAj@An@?f@B~B@`A@b@Bh@@h@Dt@D~@FbADr@Ft@Hx@D`@Fb@N~@TnAJh@Jb@DPBJFTFTBHFNLVNVR^b@r@Zd@~@xAr@nAh@jA\\x@Zp@LZFNDLHVBRN~@PjABRJt@j@tFh@xD^vBZ~AHd@^lBFTBLNr@Jb@?BBJDJBNLb@Hh@NfAPlADj@FfANjD@FD~A@d@DnBJhFBhA@b@Bf@Bn@F~@Dj@Bj@?J@RBb@ZjKB`@@b@Ht@Hz@Fj@RbBN~AHz@Bd@Dj@VdCPrBFb@ZrBPdAJt@BRLrA@PPnAVtBJfAPfCDx@@T@d@?Z@\\CnG?v@?V@NBRFf@@H@P@J?J@^LxFDbC?\\?F@vA@~@?p@@n@?X@dA?J?HAL?L?N?v@@n@@fA@`@@`ADzABjBH`AHhAbAxG@NDn@@TDlA@TFrADnADrADp@?NDv@DpAHhB@ZD~@Dt@Gh@AJQ`AUQO@oCbBs@f@aA]kBs@eFJ@fB??",
                },
            ],
        }
    },
}

ENDPOINTS_QUERIES = {
    "google": {
        "directions": {
            "profile": "driving",
            "locations": PARAM_LINE_MULTI,
            "alternatives": True,
            "avoid": ["tolls", "ferries"],
            "optimize": False,
            "language": "de",
            "region": "de",
            "units": "metrics",
            "arrival_time": 1567512000,
            "traffic_model": "optimistic",
            "transit_mode": ["bus", "rail"],
            "transit_routing_preference": "less_walking",
        },
        "matrix": {
            "profile": "driving",
            "locations": PARAM_LINE_MULTI,
            "avoid": ["tolls", "ferries"],
            "language": "de",
            "region": "de",
            "units": "metrics",
            "arrival_time": 1567512000,
            "traffic_model": "optimistic",
            "transit_mode": ["bus", "rail"],
            "transit_routing_preference": "less_walking",
        },
    },
    "osrm": {
        "directions": {
            "profile": "driving",
            "locations": PARAM_LINE_MULTI,
            "radiuses": [PARAM_INT_BIG, PARAM_INT_BIG, PARAM_INT_BIG],
            "bearings": [[PARAM_INT_SMALL, PARAM_INT_SMALL]] * 3,
            "alternatives": True,
            "steps": True,
            "annotations": True,
            "geometries": "geojson",
            "overview": "simplified",
            "continue_straight": True,
        },
        "matrix": {
            "profile": "walking",
            "locations": PARAM_LINE_MULTI,
            "radiuses": [PARAM_INT_BIG, PARAM_INT_BIG, PARAM_INT_BIG],
            "bearings": [[PARAM_INT_SMALL, PARAM_INT_SMALL]] * 3,
            "annotations": ["distance", "duration"],
        },
    },
    "mapbox_osrm": {
        "directions": {
            "locations": PARAM_LINE_MULTI,
            "profile": "driving",
            "radiuses": [PARAM_INT_BIG, PARAM_INT_BIG, PARAM_INT_BIG],
            "bearings": [[PARAM_INT_SMALL, PARAM_INT_SMALL]] * 3,
            "alternatives": 3,
            "steps": True,
            "annotations": ["duration", "distance", "speed"],
            "geometries": "geojson",
            "overview": "simplified",
            "continue_straight": True,
            "exclude": "motorway",
            "approaches": ["curb"] * 3,
            "banner_instructions": True,
            "language": "de",
            "roundabout_exits": True,
            "voice_instructions": True,
            "voice_units": "metric",
            "waypoint_names": ["a", "b", "c"],
            "waypoint_targets": PARAM_LINE_MULTI,
        },
        "isochrones": {
            "locations": PARAM_POINT,
            "profile": "driving",
            "intervals": [600, 1200],
            "contours_colors": ["ff0000", "00FF00"],
            "polygons": True,
            "generalize": 0.5,
            "denoise": 0.1,
        },
        "matrix": {
            "locations": PARAM_LINE_MULTI,
            "profile": "driving",
            "annotations": ["distance", "duration"],
            "fallback_speed": PARAM_INT_SMALL,
        },
    },
    "heremaps": {
        "directions": {
            "locations": PARAM_LINE_MULTI,
            "profile": "truck",
            "request_id": 101,
            "avoid_areas": [
                [(8.688641, 49.420577), (8.680916, 49.415776)],
                [(8.780916, 49.445776), (8.780916, 49.445776)],
            ],
            "avoid_links": [-53623477],
            "avoid_seasonal_closures": True,
            "avoid_turns": "difficult",
            "exclude_zones": [510, 511],
            "exclude_zone_types": ["vignette", "congestionPricing"],
            "exclude_countries": ["AUT", "CHE"],
            "departure": datetime.datetime(2021, 3, 29, 3, 0).isoformat(),
            "alternatives": 3,
            "metric_system": "metric",
            "view_bounds": [(8.688641, 49.420577), (8.680916, 49.415776)],
            "resolution": {"viewresolution": 300, "snapresolution": 300},
            "instruction_format": "text",
            "language": "en-us",
            "json_attributes": 9,
            "route_attributes": [
                "waypoints",
                "summary",
                "summaryByCountry",
                "shape",
                "boundingBox",
                "legs",
                "notes",
                "lines",
                "routeId",
                "groups",
                "tickets",
                "incidents",
                "zones",
            ],
            "leg_attributes": ["maneuvers", "waypoint", "length", "travelTime"],
            "maneuver_attributes": ["position", "length", "travelTime"],
            "link_attributes": ["shape", "speedLimit"],
            "generalization_tolerances": [0.1, 0.01],
            "vehicle_type": "diesel,5.5",
            "license_plate": "lastcharacter:5",
            "max_number_of_changes": 5,
            "combine_change": False,
            "truck_type": "truck",
            "trailers_count": 3,
            "shipped_hazardous_goods": ["gas", "flammable"],
            "limited_weight": 10,
            "weight_per_axle": 100,
            "height": 20,
            "width": 10,
            "length": 10,
            "truck_restriction_penalty": "soft",
            "return_elevation": True,
            "consumption_model": "default",
            "speed_profile": "fast",
        },
        "matrix": {
            "locations": [[8.688641, 49.420577], [8.680916, 49.415776], [8.780916, 49.445776]],
            "sources": [0, 1],
            "destinations": [2],
            "profile": "car",
            "summary_attributes": ["traveltime", "costfactor"],
            "truck_type": "truck",
            "trailers_count": 3,
            "shipped_hazardous_goods": ["gas", "flammable"],
            "limited_weight": 10,
            "weight_per_axle": 100,
            "height": 20,
            "width": 10,
            "length": 10,
        },
        "isochrones": {
            "locations": PARAM_POINT,
            "intervals": [1000, 2000, 3000],
            "interval_type": "distance",
            "profile": "car",
            "center_type": "start",
            "request_id": 101,
            "single_component": False,
            "quality": 1,
        },
    },
    "graphhopper": {
        "directions": {
            "locations": PARAM_LINE_MULTI,
            "profile": "car",
            "elevation": True,
            "points_encoded": True,
            "format": "json",
            "instructions": False,
            "locale": "en",
            "calc_points": False,
            "optimize": True,
            "debug": True,
            "point_hint": ["OSM Street", "Graphhopper Lane", "Routing Broadway"],
            "snap_prevention": ["trunk", "ferry"],
            "curb_side": ["any", "right"],
            "turn_costs": True,
            "details": ["tolls", "time"],
            "ch_disable": True,
            "weighting": "short_fastest",
            "heading": [PARAM_INT_SMALL, PARAM_INT_SMALL, PARAM_INT_SMALL],
            "heading_penalty": 100,
            "pass_through": True,
            "block_area": ",".join(list(map(str, reversed(PARAM_POINT)))),
            "avoid": ["tunnel", "ford"],
            "algorithm": "alternative_route",
            "round_trip_distance": 10000,
            "round_trip_seed": 3,
            "alternative_route_max_paths": 2,
            "alternative_route_max_weight_factor": 1.7,
            "alternative_route_max_share_factor": 0.7,
        },
        "matrix": {
            "locations": PARAM_LINE_MULTI,
            "profile": "car",
            "out_array": ["weights", "times", "distances"],
            "debug": True,
        },
        "isochrones": {
            "locations": PARAM_POINT,
            "profile": "car",
            "intervals": [1000],
            "buckets": 5,
            "reverse_flow": True,
            "debug": False,
        },
    },
    "valhalla": {
        "directions": {
            "locations": PARAM_LINE_MULTI,
            "options": {
                "maneuver_penalty": PARAM_INT_SMALL,
                "toll_booth_cost": PARAM_INT_SMALL,
                "country_crossing_penalty": PARAM_INT_SMALL,
            },
            "profile": "auto",
            "preference": "shortest",
            "units": "mi",
            "directions_type": "none",
            "avoid_locations": PARAM_POINT,
            "avoid_polygons": PARAM_POLY,
            "date_time": {"type": 1, "value": "2021-03-03T08:06"},
            "language": "pirate",
            "instructions": False,
            "id": "wacko",
            "somerandom": "option",
        },
        "isochrones": {
            "locations": PARAM_POINT,
            "options": {
                "maneuver_penalty": PARAM_INT_SMALL,
                "toll_booth_cost": PARAM_INT_SMALL,
                "country_crossing_penalty": PARAM_INT_SMALL,
            },
            "profile": "auto",
            "id": "wacko",
            "preference": "fastest",
            "intervals": [600, 1200],
            "colors": ["ff0000", "00FF00"],
            "polygons": True,
            "avoid_locations": PARAM_POINT,
            "generalize": 0.5,
            "denoise": 0.1,
            "date_time": {"type": 1, "value": "2021-03-03T08:06"},
        },
        "matrix": {
            "locations": PARAM_LINE_MULTI,
            "options": {
                "maneuver_penalty": PARAM_INT_SMALL,
                "toll_booth_cost": PARAM_INT_SMALL,
                "country_crossing_penalty": PARAM_INT_SMALL,
            },
            "avoid_locations": PARAM_POINT,
            "profile": "auto",
            "units": "mi",
            "id": "wacko",
        },
        "expansion": {
            "expansion_properties": ["distances", "durations", "costs"],
            "intervals": [60],
            "locations": [(0.00026949361342338066, -0.00017966240895360996)],
            "profile": "auto",
        },
        "trace_attributes": {
            "locations": PARAM_LINE_MULTI,
            "profile": "pedestrian",
            "shape_match": "map_snap",
            "filters": ["edge.id", "matched.type"],
            "filters_action": "exclude",
            "options": {
                "maneuver_penalty": PARAM_INT_SMALL,
                "toll_booth_cost": PARAM_INT_SMALL,
                "country_crossing_penalty": PARAM_INT_SMALL,
            },
        },
    },
    "ors": {
        "directions": {
            "locations": PARAM_LINE,
            "profile": "driving-car",
            "preference": "fastest",
            "units": "mi",
            "language": "en",
            "geometry": "true",
            "geometry_simplify": "False",
            "instructions": "False",
            "instructions_format": "html",
            "roundabout_exits": "true",
            "attributes": ["avgspeed"],
            "radiuses": [PARAM_INT_SMALL] * 2,
            "bearings": [[PARAM_INT_SMALL, PARAM_INT_SMALL]] * 2,
            "elevation": "true",
            "extra_info": ["roadaccessrestrictions"],
            "options": {"avoid_features": ["highways", "tollways"]},
        },
        "isochrones": {
            "locations": PARAM_POINT,
            "profile": "cycling-regular",
            "interval_type": "distance",
            "intervals": [PARAM_INT_BIG],
            "units": "m",
            "location_type": "destination",
            "attributes": ["area", "reachfactor"],
        },
        "matrix": {
            "locations": PARAM_LINE,
            "sources": [1],
            "destinations": [0],
            "profile": "driving-car",
            "metrics": ["duration", "distance"],
            "resolve_locations": "true",
            "units": "mi",
        },
    },
    "vroom": {
        "optimization": {
            "jobs": [Job(id=ix, location=location) for ix, location in enumerate(PARAM_LINE_MULTI)],
            "vehicles": [
                Vehicle(id=ix, start=location, end=location) for ix, location in enumerate(PARAM_LINE)
            ],
        }
    },
}

ENDPOINTS_EXPECTED = {
    "valhalla": {
        "directions": {
            "locations": [
                {"lat": 49.420577, "lon": 8.688641},
                {"lat": 49.415776, "lon": 8.680916},
                {"lat": 49.445776, "lon": 8.780916},
            ],
            "costing": "auto",
            "costing_options": {
                "auto": {
                    "maneuver_penalty": 50,
                    "toll_booth_cost": 50,
                    "country_crossing_penalty": 50,
                    "shortest": True,
                }
            },
            "directions_options": {"units": "mi", "language": "pirate", "directions_type": "none"},
            "avoid_locations": [{"lon": 8.34234, "lat": 48.23424}],
            "avoid_polygons": PARAM_POLY,
            "date_time": {"type": 1, "value": "2021-03-03T08:06"},
            "id": "wacko",
            "narrative": False,
            "somerandom": "option",
        },
        "isochrones": {
            "locations": [{"lat": PARAM_POINT[1], "lon": PARAM_POINT[0]}],
            "costing": "auto",
            "costing_options": {
                "auto": {"maneuver_penalty": 50, "toll_booth_cost": 50, "country_crossing_penalty": 50}
            },
            "contours": [{"time": 10, "color": "ff0000"}, {"time": 20, "color": "00FF00"}],
            "avoid_locations": [{"lon": 8.34234, "lat": 48.23424}],
            "date_time": {"type": 1, "value": "2021-03-03T08:06"},
            "id": "wacko",
            "denoise": 0.1,
            "polygons": True,
            "generalize": 0.5,
        },
        "matrix": {
            "sources": [
                {"lat": 49.420577, "lon": 8.688641},
                {"lat": 49.415776, "lon": 8.680916},
                {"lat": 49.445776, "lon": 8.780916},
            ],
            "targets": [
                {"lat": 49.420577, "lon": 8.688641},
                {"lat": 49.415776, "lon": 8.680916},
                {"lat": 49.445776, "lon": 8.780916},
            ],
            "costing": "auto",
            "costing_options": {
                "auto": {"maneuver_penalty": 50, "toll_booth_cost": 50, "country_crossing_penalty": 50}
            },
            "avoid_locations": [{"lon": 8.34234, "lat": 48.23424}],
            "id": "wacko",
            "units": "mi",
        },
        "expansion": {
            "expansion_properties": ["distances", "durations", "costs"],
            "contours": [{"time": 1.0}],
            "locations": [{"lon": 0.00026949361342338066, "lat": -0.00017966240895360996}],
            "costing": "auto",
            "action": "isochrone",
        },
        "trace_attributes": {
            "shape": [
                {"lat": 49.420577, "lon": 8.688641},
                {"lat": 49.415776, "lon": 8.680916},
                {"lat": 49.445776, "lon": 8.780916},
            ],
            "costing": "pedestrian",
            "shape_match": "map_snap",
            "filters": {"attributes": ["edge.id", "matched.type"]},
            "action": "exclude",
            "costing_options": {
                "pedestrian": {
                    "maneuver_penalty": PARAM_INT_SMALL,
                    "toll_booth_cost": PARAM_INT_SMALL,
                    "country_crossing_penalty": PARAM_INT_SMALL,
                }
            },
        },
    },
}

ENDPOINTS_ERROR_RESPONSES = {
    "google": {
        "ZERO_RESULTS": {
            "available_travel_modes": ["DRIVING", "WALKING", "BICYCLING"],
            "geocoded_waypoints": [{}, {}],
            "routes": [],
            "status": "ZERO_RESULTS",
        },
        "UNKNOWN_ERROR": {
            "available_travel_modes": ["DRIVING", "WALKING", "BICYCLING"],
            "geocoded_waypoints": [{}, {}],
            "routes": [],
            "status": "UNKNOWN_ERROR",
        },
    }
}
