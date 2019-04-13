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
import random
import datetime

PARAM_POINT = [8.34234, 48.23424]
PARAM_LINE = [[8.688641, 49.420577], [8.680916, 49.415776]]
PARAM_LINE_MULTI = [[8.688641, 49.420577], [8.680916, 49.415776],
                    [8.780916, 49.445776]]
PARAM_POLY = [[[8.688641, 49.420577], [8.680916, 49.415776]]]

PARAM_INT_BIG = 500
PARAM_INT_SMALL = 50

PARAM_STRING = random.choice('abcdefghijklmnopqrstuvwxyz')

PARAM_GEOJSON_POINT = {'type': 'Point', 'coordinates': PARAM_POINT}
PARAM_GEOJSON_LINE = {'type': 'LineString', 'coordinates': PARAM_LINE}
PARAM_GEOJSON_POLY = {'type': 'Polygon', 'coordinates': PARAM_POLY}

ENDPOINTS_RESPONSES = {
    'valhalla': {
        'directions': {
            "trip": {
                'legs':
                [{
                    "shape":
                    '}wpulAvkxblCtJpGu}@hrCkAvDsAdEm@xBkAvDeK`\\ssAthE{iAjpDyiAlpD',
                    "summary": {
                        'length': 100,
                        "time": 100
                    }
                },
                 {
                     "shape":
                     '}wpulAvkxblCtJpGu}@hrCkAvDsAdEm@xBkAvDeK`\\ssAthE{iAjpD',
                     "summary": {
                         'length': 50,
                         "time": 50
                     }
                 }]
            }
        },
        "isochrones": {
            "type":
            "FeatureCollection",
            "bbox": [8.688474, 8.681829, 49.42577, 49.420176],
            "features": [
                {
                    "type": "Feature",
                    "properties": {
                        "group_index": 0,
                        "value": 100,
                        "center": [8.684162488752957, 49.4230724075398]
                    },
                    "geometry": {
                        "coordinates": [[[8.684544, 49.423295],
                                         [8.684665, 49.423101],
                                         [8.684706, 49.423036]]],
                        "type":
                        "Polygon"
                    }
                },
                {
                    "type": "Feature",
                    "properties": {
                        "group_index": 0,
                        "value": 100,
                        "center": [8.684162488752957, 49.4230724075398]
                    },
                    "geometry": {
                        "coordinates": [[[8.684544, 49.423295],
                                         [8.684665, 49.423101],
                                         [8.684706, 49.423036]]],
                        "type":
                        "Polygon"
                    }
                },
            ]
        },
        "matrix": {
            'sources_to_targets': [[{
                "distance": 0,
                "time": 0
            }, {
                "distance": 100,
                "time": 100
            }], [{
                "distance": 100,
                "time": 100
            }, {
                "distance": 0,
                "time": 0
            }]]
        }
    },
    'osrm': {
        'directions_geojson': {
            'routes': [{
                "geometry": {
                    "coordinates": [[8.681495, 49.41461],
                                    [8.681445, 49.415755]]
                },
                "duration": 100,
                "distance": 100
            }]
        },
        'directions_polyline': {
            'routes': [{
                "geometry":
                'qmbjHspkr@kCmCpE{T~M|@|QcRvC}OjCgD~F~@~I~SjLxqAjT||@lDde@aBhh@uUbuAmJpPod@|c@iWhQoSt_@}Hx]oTfNqNWqQeKilAa]hByx@DiCvDd@dNxJ[zMl[eCfKlBn[rUb]z]pGoGbHtY|j@xw@jKnFfd@~IdhEpyFm@rGpInKyAhDuDuE',
                "duration": 100,
                "distance": 100
            }]
        },
        'directions_polyline6': {
            'routes': [{
                "geometry":
                'wpan|A}n|`O{j@yk@v`AuyE~tCfRx|De~Dln@khDhj@as@doAnR~lBhqEtdCxzXvtExjRvu@t|Ju]z{K}aFd|YiqBrnDkvJrpJ_rF|uDalEhfIibB`sHavEjwCgzCyFayDkxBadWykHf`@_aQ|@cj@rx@rJjvCduBgGtsCb{Gsh@lyBla@f|GhaFxkHvsHttAatAhzAliGvvLnwPtzBriAjsJhmBvz}@jhmAoMnuA`iBb|Bi[bt@}w@ebA',
                "duration": 100,
                "distance": 100
            }]
        },
        "matrix": {
            "durations": [[1, 2, 3], [4, 5, 6]]
        }
    },
    'mapbox_osrm': {
        'directions': {
            'routes': [{
                "geometry": {
                    "coordinates": [[8.681495, 49.41461],
                                    [8.681445, 49.415755]]
                },
                "duration": 100,
                "distance": 100
            }]
        },
        "isochrones": {
            "type":
            "FeatureCollection",
            "bbox": [8.688474, 8.681829, 49.42577, 49.420176],
            "features": [
                {
                    "type": "Feature",
                    "properties": {
                        "group_index": 0,
                        "value": 100,
                        "center": [8.684162488752957, 49.4230724075398]
                    },
                    "geometry": {
                        "coordinates": [[[8.684544, 49.423295],
                                         [8.684665, 49.423101],
                                         [8.684706, 49.423036]]],
                        "type":
                        "Polygon"
                    }
                },
                {
                    "type": "Feature",
                    "properties": {
                        "group_index": 0,
                        "value": 100,
                        "center": [8.684162488752957, 49.4230724075398]
                    },
                    "geometry": {
                        "coordinates": [[[8.684544, 49.423295],
                                         [8.684665, 49.423101],
                                         [8.684706, 49.423036]]],
                        "type":
                        "Polygon"
                    }
                },
            ]
        },
        "matrix": {
            "distances": [[1, 2, 3], [4, 5, 6]],
            "durations": [[1, 2, 3], [4, 5, 6]]
        }
    },
    'google': {
        "directions": {
            "routes": [{
                "legs": [{
                    "distance": {
                        "value": 541359
                    },
                    "duration": {
                        "value": 19448
                    },
                    "steps": [
                        {
                            "distance": {
                                "value": 280
                            },
                            "duration": {
                                "value": 67
                            },
                            "polyline": {
                                "points":
                                "ayotGvy_sMV]t@_APk@DOFW@O@OAwADiE?k@Hq@@UHuG@s@@{@DiIDsFDkG@aIAa@?WAUASGe@Im@EYEOCOO_@Kk@Ie@Oe@GWKUMWwAoCmDmGwB}D_AgBoAaCqCaGuA_D}@_BIS]m@KQMUy@}AwAgCk@cAiB_D{AsCcBwCmAsBm@aAoAuBeB{Bm@sAe@mAMa@Qi@Uy@e@eB[eAIUOm@u@iCi@eCaA}DcAyCy@qB{EiIMU"
                            },
                        },
                        {
                            "distance": {
                                "value": 2493
                            },
                            "duration": {
                                "value": 511
                            },
                            "polyline": {
                                "points":
                                "ayotGvy_sMV]t@_APk@DOFW@O@OAwADiE?k@Hq@@UHuG@s@@{@DiIDsFDkG@aIAa@?WAUASGe@Im@EYEOCOO_@Kk@Ie@Oe@GWKUMWwAoCmDmGwB}D_AgBoAaCqCaGuA_D}@_BIS]m@KQMUy@}AwAgCk@cAiB_D{AsCcBwCmAsBm@aAoAuBeB{Bm@sAe@mAMa@Qi@Uy@e@eB[eAIUOm@u@iCi@eCaA}DcAyCy@qB{EiIMU"
                            },
                        }
                    ]
                }]
            }]
        },
        'matrix': {
            "rows": [{
                "elements": [{
                    "distance": {
                        "text": "225 mi",
                        "value": 361957
                    },
                    "duration": {
                        "text": "3 hours 50 mins",
                        "value": 13813
                    }
                }]
            }]
        }
    },
    'ors': {
        'directions': {
            "json": {
                "routes": [{
                    "summary": {
                        "distance": 850.5,
                        "duration": 191.4
                    },
                    "geometry":
                    "ihrlHir~s@cFFcAKeB_@_B]g@IUAQB]PaCr@y@cJeBXe@qJ_@kH??"
                }]
            },
            "geojson": {
                "type":
                "FeatureCollection",
                "features": [{
                    "type": "Feature",
                    "geometry": {
                        "coordinates": [[8.681495, 49.41461],
                                        [8.681445, 49.415755]],
                        "type":
                        "LineString"
                    },
                    "properties": {
                        "summary": {
                            "distance": 850.5,
                            "duration": 191.4
                        }
                    },
                }]
            }
        },
        "isochrones": {
            "type":
            "FeatureCollection",
            "bbox": [8.688474, 8.681829, 49.42577, 49.420176],
            "features": [{
                "type": "Feature",
                "properties": {
                    "group_index": 0,
                    "value": 100,
                    "center": [8.684162488752957, 49.4230724075398]
                },
                "geometry": {
                    "coordinates": [[[8.684544, 49.423295],
                                     [8.684665, 49.423101],
                                     [8.684706, 49.423036]]],
                    "type":
                    "Polygon"
                }
            },
                         {
                             "type": "Feature",
                             "properties": {
                                 "group_index": 0,
                                 "value": 200,
                                 "center":
                                 [8.684162488752957, 49.4230724075398]
                             },
                             "geometry": {
                                 "coordinates": [[[8.683974, 49.423982],
                                                  [8.684035, 49.423627],
                                                  [8.685104, 49.422131]]],
                                 "type":
                                 "Polygon"
                             }
                         },
                         {
                             "type": "Feature",
                             "properties": {
                                 "group_index": 0,
                                 "value": 300,
                                 "center":
                                 [8.684162488752957, 49.4230724075398]
                             },
                             "geometry": {
                                 "coordinates": [[[8.68261, 49.423744],
                                                  [8.682671, 49.423389],
                                                  [8.683764, 49.421902]]],
                                 "type":
                                 "Polygon"
                             }
                         },
                         {
                             "type": "Feature",
                             "properties": {
                                 "group_index": 0,
                                 "value": 400,
                                 "center":
                                 [8.684162488752957, 49.4230724075398]
                             },
                             "geometry": {
                                 "coordinates": [[[8.681829, 49.424426],
                                                  [8.682416, 49.421699],
                                                  [8.686179, 49.420176]]],
                                 "type":
                                 "Polygon"
                             }
                         }]
        },
        "matrix": {
            "durations": [[7900.34], [0], [136841.92], [483295.5]],
            "distances": [[125414.58], [0], [2383943.25], [10037064]]
        }
    },
    'graphhopper': {
        'directions': {
            "paths": [{
                "distance": 15239.553,
                "time": 2349463,
                "points": "korlHun~s@inUAiBP"
            },
                      {
                          "distance": 15239.553,
                          "time": 2349463,
                          "points": "korlHun~s@inUAiBP"
                      },
                      {
                          "distance": 15239.553,
                          "time": 2349463,
                          "points": "korlHun~s@inUAiBP"
                      }]
        },
        'isochrones': {
            "polygons": [
                {
                    "type": "Feature",
                    "geometry": {
                        "type":
                        "Polygon",
                        "coordinates":
                        [[[8.345841896068496, 48.23514181901086, 1.0],
                          [8.340545650732793, 48.23651784814562, 1.5],
                          [8.340935036709944, 48.23593307068795, 1.5]]]
                    }
                },
                {
                    "type": "Feature",
                    "geometry": {
                        "type":
                        "Polygon",
                        "coordinates":
                        [[[8.345999848380682, 48.23155678581201, 2.0],
                          [8.348431345412836, 48.234402721399135, 2.0],
                          [8.348099422039823, 48.23458791489723, 2.0]]]
                    }
                },
                {
                    "type": "Feature",
                    "geometry": {
                        "type":
                        "Polygon",
                        "coordinates":
                        [[[8.349068835729408, 48.2354851976518, 2.5],
                          [8.34836307396443, 48.23601708826144],
                          [8.342155162442218, 48.23711268388732, 2.5]]]
                    }
                }
            ]
        },
        'matrix': {
            "distances": [[0, 1181, 13965], [1075, 0, 14059],
                          [14120, 13766, 0]],
            "times": [[0, 255, 2122], [242, 0, 2094], [2144, 2019, 0]],
            "weights": [[0.0, 272.99, 2331.526], [258.115, 0.0, 2305.121],
                        [2356.307, 2225.083, 0.0]]
        }
    },
    'heremaps': {
        'directions': {
            'response': {
                'route': [{
                    'shape': [
                        '8.6841352,49.4161567,560.0',
                        '8.683039,49.4174594,560.0'
                    ],
                    'summary': {
                        'distance': 27084,
                        'trafficTime': 2830,
                        'baseTime': 2830,
                        'travelTime': 2830
                    }
                },
                          {
                              'shape': [
                                  '8.6841352,49.4161567,560.0',
                                  '8.683039,49.4174594,560.0'
                              ],
                              'summary': {
                                  'distance': 27084,
                                  'trafficTime': 2830,
                                  'baseTime': 2830,
                                  'travelTime': 2830
                              }
                          },
                          {
                              'shape': [
                                  '8.6841352,49.4161567,560.0',
                                  '8.683039,49.4174594,560.0'
                              ],
                              'summary': {
                                  'distance': 27084,
                                  'trafficTime': 2830,
                                  'baseTime': 2830,
                                  'travelTime': 2830
                              }
                          }]
            }
        },
        'isochrones': {
            'response': {
                'center': {
                    'latitude': 8.3423399,
                    'longitude': 48.23424
                },
                'isoline': [{
                    'range':
                    1000,
                    'component': [{
                        'id':
                        0,
                        'shape':
                        ['8.3724403,48.2271481', '8.3729553,48.2272339']
                    }]
                },
                            {
                                'range':
                                2000,
                                'component': [{
                                    'id':
                                    0,
                                    'shape': [
                                        '8.3724403,48.2271481',
                                        '8.3729553,48.2272339'
                                    ]
                                }]
                            },
                            {
                                'range':
                                3000,
                                'component': [{
                                    'id':
                                    0,
                                    'shape': [
                                        '8.3724403,48.2271481',
                                        '8.3729553,48.2272339'
                                    ]
                                }]
                            }],
                'start': {
                    'linkId': '+1141790171',
                    'mappedPosition': {
                        'latitude': 8.3658099,
                        'longitude': 48.2353663
                    },
                    'originalPosition': {
                        'latitude': 8.3423399,
                        'longitude': 48.23424
                    }
                }
            }
        },
        'matrix': {
            "response": {
                "matrixEntry": [
                    {
                        "startIndex": 0,
                        "destinationIndex": 0,
                        "summary": {
                            "distance": 1398,
                            "travelTime": 82,
                            "costFactor": 82
                        }
                    },
                    {
                        "startIndex": 1,
                        "destinationIndex": 0,
                        "summary": {
                            "distance": 1188,
                            "travelTime": 69,
                            "costFactor": 69
                        }
                    },
                ]
            }
        }
    }
}

ENDPOINTS_QUERIES = {
    'google': {
        'directions': {
            'locations': PARAM_LINE_MULTI,
            'profile': 'driving',
            'alternatives': True,
            'avoid': ['tolls', 'ferries'],
            'optimize': False,
            'language': 'de',
            'region': 'de',
            'units': 'metrics',
            'arrival_time': 1567512000,
            'traffic_model': 'optimistic',
            'transit_mode': ['bus', 'rail'],
            'transit_routing_preference': 'less_walking'
        },
        'matrix': {
            'locations': PARAM_LINE_MULTI,
            'profile': 'driving',
            'avoid': ['tolls', 'ferries'],
            'language': 'de',
            'region': 'de',
            'units': 'metrics',
            'arrival_time': 1567512000,
            'traffic_model': 'optimistic',
            'transit_mode': ['bus', 'rail'],
            'transit_routing_preference': 'less_walking'
        }
    },
    'osrm': {
        'directions': {
            'locations': PARAM_LINE_MULTI,
            'profile': 'car',
            'radiuses': [PARAM_INT_BIG, PARAM_INT_BIG, PARAM_INT_BIG],
            'bearings': [[PARAM_INT_SMALL, PARAM_INT_SMALL]] * 3,
            'alternatives': True,
            'steps': True,
            'annotations': True,
            'geometries': 'geojson',
            'overview': 'simplified',
            'continue_straight': True
        },
        'matrix': {
            'locations': PARAM_LINE_MULTI,
            'profile': 'car',
            'radiuses': [PARAM_INT_BIG, PARAM_INT_BIG, PARAM_INT_BIG],
            'bearings': [[PARAM_INT_SMALL, PARAM_INT_SMALL]] * 3,
        }
    },
    'mapbox_osrm': {
        'directions': {
            'locations': PARAM_LINE_MULTI,
            'profile': 'driving',
            'radiuses': [PARAM_INT_BIG, PARAM_INT_BIG, PARAM_INT_BIG],
            'bearings': [[PARAM_INT_SMALL, PARAM_INT_SMALL]] * 3,
            'alternatives': 3,
            'steps': True,
            'annotations': ['duration', 'distance', 'speed'],
            'geometries': 'geojson',
            'overview': 'simplified',
            'continue_straight': True,
            'exclude': 'motorway',
            'approaches': ['curb'] * 3,
            'banner_instructions': True,
            'language': 'de',
            'roundabout_exits': True,
            'voice_instructions': True,
            'voice_units': 'metric',
            'waypoint_names': ['a', 'b', 'c'],
            'waypoint_targets': PARAM_LINE_MULTI
        },
        'isochrones': {
            'locations': PARAM_POINT,
            'profile': 'mapbox/driving',
            'intervals': [600, 1200],
            'contours_colors': ['ff0000', '00FF00'],
            'polygons': True,
            'generalize': 0.5,
            'denoise': 0.1,
        },
        'matrix': {
            'locations': PARAM_LINE_MULTI,
            'profile': 'driving',
            'annotations': ['distance', 'duration'],
            'fallback_speed': PARAM_INT_SMALL
        }
    },
    'heremaps': {
        'directions': {
            'locations':
            PARAM_LINE_MULTI,
            'profile':
            'truck;fastest',
            'request_id':
            101,
            'avoid_areas': [[(8.688641, 49.420577), (8.680916, 49.415776)],
                            [(8.780916, 49.445776), (8.780916, 49.445776)]],
            'avoid_links': [-53623477],
            'avoid_seasonal_closures':
            True,
            'avoid_turns':
            'difficult',
            'exclude_zones': [510, 511],
            'exclude_zone_types': ['vignette', 'congestionPricing'],
            'exclude_countries': ['AUT', 'CHE'],
            'departure':
            datetime.datetime(2019, 3, 29, 3, 0).isoformat(),
            'alternatives':
            3,
            'metric_system':
            'metric',
            'view_bounds': [(8.688641, 49.420577), (8.680916, 49.415776)],
            'resolution': {
                'viewresolution': 300,
                'snapresolution': 300
            },
            'instruction_format':
            'text',
            'language':
            'en-us',
            'json_attributes':
            9,
            'route_attributes': [
                'waypoints', 'summary', 'summaryByCountry', 'shape',
                'boundingBox', 'legs', 'notes', 'lines', 'routeId', 'groups',
                'tickets', 'incidents', 'zones'
            ],
            'leg_attributes':
            ['maneuvers', 'waypoint', 'length', 'travelTime'],
            'maneuver_attributes': ['position', 'length', 'travelTime'],
            'link_attributes': ['shape', 'speedLimit'],
            'generalization_tolerances': [0.1, 0.01],
            'vehicle_type':
            'diesel,5.5',
            'license_plate':
            'lastcharacter:5',
            'max_number_of_changes':
            5,
            'combine_change':
            False,
            'truck_type':
            'truck',
            'trailers_count':
            3,
            'shipped_hazardous_goods': ['gas', 'flammable'],
            'limited_weight':
            10,
            'weight_per_axle':
            100,
            'height':
            20,
            'width':
            10,
            'length':
            10,
            'truck_restriction_penalty':
            'soft',
            'return_elevation':
            True,
            'consumption_model':
            'default',
            'speed_profile':
            'fast',
        },
        'matrix': {
            'locations': [[8.688641, 49.420577], [8.680916, 49.415776],
                          [8.780916, 49.445776]],
            'sources': [0, 1],
            'destinations': [2],
            'profile':
            'car;fastest',
            'summary_attributes': ['traveltime', 'costfactor'],
            'truck_type':
            'truck',
            'trailers_count':
            3,
            'shipped_hazardous_goods': ['gas', 'flammable'],
            'limited_weight':
            10,
            'weight_per_axle':
            100,
            'height':
            20,
            'width':
            10,
            'length':
            10,
        },
        'isochrones': {
            'locations': PARAM_POINT,
            'intervals': [1000, 2000, 3000],
            'interval_type': 'distance',
            'profile': 'car;fastest',
            'center_type': 'start',
            'request_id': 101,
            'single_component': False,
            'quality': 1
        }
    },
    'graphhopper': {
        'directions': {
            'locations': PARAM_LINE_MULTI,
            'profile': 'car',
            'elevation': True,
            'points_encoded': True,
            'format': 'json',
            'instructions': False,
            'locale': 'en',
            'calc_points': False,
            'optimize': True,
            'debug': True,
            'point_hint': False,
            'details': ['tolls', 'time'],
            'ch_disable': True,
            'weighting': 'short_fastest',
            'heading': [PARAM_INT_SMALL, PARAM_INT_SMALL, PARAM_INT_SMALL],
            'heading_penalty': 100,
            'pass_through': True,
            'block_area': ','.join(list(map(str, reversed(PARAM_POINT)))),
            'avoid': ['tunnel', 'ford'],
            'algorithm': 'alternative_route',
            'round_trip_distance': 10000,
            'round_trip_seed': 3,
            'alternative_route_max_paths': 2,
            'alternative_route_max_weight_factor': 1.7,
            'alternative_route_max_share_factor': 0.7
        },
        'matrix': {
            'locations': PARAM_LINE_MULTI,
            'profile': 'car',
            'out_array': ['weights', 'times', 'distances'],
            'debug': True
        },
        'isochrones': {
            'locations': PARAM_POINT,
            'profile': 'car',
            'intervals': [1000],
            'interval_type': None,
            'buckets': 5,
            'reverse_flow': True,
            'debug': False
        }
    },
    'valhalla': {
        'directions': {
            'locations': PARAM_LINE_MULTI,
            'options': {
                'maneuver_penalty': PARAM_INT_SMALL,
                'toll_booth_cost': PARAM_INT_SMALL,
                'country_crossing_penalty': PARAM_INT_SMALL
            },
            'profile': 'auto',
            'units': 'mi',
            'directions_type': 'none',
            'avoid_locations': PARAM_POINT,
            'date_time': {
                'type': 1,
                'value': '2019-03-03T08:06'
            },
            'language': 'pirate',
            'id': 'wacko'
        },
        'isochrones': {
            'locations': PARAM_POINT,
            'options': {
                'maneuver_penalty': PARAM_INT_SMALL,
                'toll_booth_cost': PARAM_INT_SMALL,
                'country_crossing_penalty': PARAM_INT_SMALL
            },
            'profile': 'auto',
            'id': 'wacko',
            'intervals': [600, 1200],
            'colors': ['ff0000', '00FF00'],
            'polygons': True,
            'avoid_locations': PARAM_POINT,
            'generalize': 0.5,
            'denoise': 0.1,
            'date_time': {
                'type': 1,
                'value': '2019-03-03T08:06'
            },
        },
        'matrix': {
            'locations': PARAM_LINE_MULTI,
            'options': {
                'maneuver_penalty': PARAM_INT_SMALL,
                'toll_booth_cost': PARAM_INT_SMALL,
                'country_crossing_penalty': PARAM_INT_SMALL
            },
            'avoid_locations': PARAM_POINT,
            'profile': 'auto',
            'units': 'mi',
            'id': 'wacko'
        },
    },
    'ors': {
        'directions': {
            'locations': PARAM_LINE,
            'profile': 'driving-car',
            'preference': 'fastest',
            'units': 'mi',
            'language': 'en',
            'geometry': 'true',
            'geometry_simplify': 'false',
            'instructions': 'false',
            'instructions_format': 'html',
            'roundabout_exits': 'true',
            'attributes': ['avgspeed'],
            'radiuses': [PARAM_INT_SMALL] * 2,
            'bearings': [[PARAM_INT_SMALL, PARAM_INT_SMALL]] * 2,
            'elevation': 'true',
            'extra_info': ['roadaccessrestrictions'],
            'options': {
                'avoid_features': ['highways', 'tollways']
            }
        },
        'isochrones': {
            'locations': PARAM_POINT,
            'profile': 'cycling-regular',
            'interval_type': 'distance',
            'intervals': [PARAM_INT_BIG],
            'units': 'm',
            'location_type': 'destination',
            'attributes': ['area', 'reachfactor']
        },
        'matrix': {
            'locations': PARAM_LINE,
            'sources': [1],
            'destinations': [0],
            'profile': 'driving-car',
            'metrics': ['duration', 'distance'],
            'resolve_locations': 'true',
            'units': 'mi',
        }
    }
}

ENDPOINTS_EXPECTED = {
    'valhalla': {
        'directions': {
            'locations': [
                {
                    'lat': 49.420577,
                    'lon': 8.688641
                },
                {
                    'lat': 49.415776,
                    'lon': 8.680916
                },
                {
                    'lat': 49.445776,
                    'lon': 8.780916
                },
            ],
            'costing':
            'auto',
            'costing_options': {
                'auto': {
                    'maneuver_penalty': 50,
                    'toll_booth_cost': 50,
                    'country_crossing_penalty': 50
                }
            },
            'directions_options': {
                'units': 'mi',
                'language': 'pirate',
                'directions_type': 'none'
            },
            'avoid_locations': [{
                'lon': 8.34234,
                'lat': 48.23424
            }],
            'date_time': {
                'type': 1,
                'value': '2019-03-03T08:06'
            },
            'id':
            'wacko'
        },
        'isochrones': {
            'locations': [{
                'lat': PARAM_POINT[1],
                'lon': PARAM_POINT[0]
            }],
            'costing':
            'auto',
            'costing_options': {
                'auto': {
                    'maneuver_penalty': 50,
                    'toll_booth_cost': 50,
                    'country_crossing_penalty': 50
                }
            },
            'contours': [{
                'time': 10,
                'color': 'ff0000'
            }, {
                'time': 20,
                'color': '00FF00'
            }],
            'avoid_locations': [{
                'lon': 8.34234,
                'lat': 48.23424
            }],
            'date_time': {
                'type': 1,
                'value': '2019-03-03T08:06'
            },
            'id':
            'wacko',
            'denoise':
            0.1,
            'polygons':
            True,
            'generalize':
            0.5,
        },
        'matrix': {
            'sources': [
                {
                    'lat': 49.420577,
                    'lon': 8.688641
                },
                {
                    'lat': 49.415776,
                    'lon': 8.680916
                },
                {
                    'lat': 49.445776,
                    'lon': 8.780916
                },
            ],
            'targets': [
                {
                    'lat': 49.420577,
                    'lon': 8.688641
                },
                {
                    'lat': 49.415776,
                    'lon': 8.680916
                },
                {
                    'lat': 49.445776,
                    'lon': 8.780916
                },
            ],
            'costing':
            'auto',
            'costing_options': {
                'auto': {
                    'maneuver_penalty': 50,
                    'toll_booth_cost': 50,
                    'country_crossing_penalty': 50
                }
            },
            'avoid_locations': [{
                'lon': 8.34234,
                'lat': 48.23424
            }],
            'id':
            'wacko',
            'units':
            'mi'
        },
    },
}
