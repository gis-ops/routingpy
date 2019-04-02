# -*- coding: utf-8 -*-
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

ENDPOINTS_QUERIES = {
    'google': {
        'directions': {
            'coordinates': PARAM_LINE_MULTI,
            'profile': 'driving',
            'alternatives': True,
            'avoid': ["tolls", "ferries"],
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
            'coordinates': PARAM_LINE_MULTI,
            'profile': 'driving',
            'avoid': ["tolls", "ferries"],
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
            'coordinates': PARAM_LINE_MULTI,
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
            'coordinates': PARAM_LINE_MULTI,
            'profile': 'car',
            'radiuses': [PARAM_INT_BIG, PARAM_INT_BIG, PARAM_INT_BIG],
            'bearings': [[PARAM_INT_SMALL, PARAM_INT_SMALL]] * 3,
        }
    },
    'mapbox_osrm': {
        'directions': {
            'coordinates': PARAM_LINE_MULTI,
            'profile': 'driving',
            'radiuses': [PARAM_INT_BIG, PARAM_INT_BIG, PARAM_INT_BIG],
            'bearings': [[PARAM_INT_SMALL, PARAM_INT_SMALL]] * 3,
            'alternatives': True,
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
        'matrix': {
            'coordinates': PARAM_LINE_MULTI,
            'profile': 'driving',
            'annotations': ['distance', 'duration'],
            'fallback_speed': PARAM_INT_SMALL
        }
    },
    'heremaps': {
        'directions': {
            'coordinates':
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
            datetime.datetime(2019, 3, 29, 3, 0),
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
            'coordinates': [[8.688641, 49.420577], [8.680916, 49.415776],
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
            'coordinates': PARAM_POINT,
            'ranges': [1000, 2000, 3000],
            'range_type': 'distance',
            'profile': 'car;fastest',
            'center_type': 'start',
            'request_id': 101,
            'single_component': False,
            'quality': 1
        }
    },
    'graphhopper': {
        'directions': {
            'coordinates': PARAM_LINE_MULTI,
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
            'block_area': ",".join(list(map(str, reversed(PARAM_POINT)))),
            'avoid': ['tunnel', 'ford'],
            'algorithm': 'alternative_route',
            'round_trip_distance': 10000,
            'round_trip_seed': 3,
            'alternative_route_max_paths': 2,
            'alternative_route_max_weight_factor': 1.7,
            'alternative_route_max_share_factor': 0.7
        },
        'matrix': {
            'coordinates': PARAM_LINE_MULTI,
            'profile': 'car',
            'out_array': ['weights', 'times', 'distance'],
            'debug': True
        },
        'isochrones': {
            'coordinates': PARAM_POINT,
            'profile': 'car',
            'distance_limit': 1000,
            'time_limit': 1000,
            'buckets': 5,
            'reverse_flow': True,
            'debug': False
        }
    },
    'valhalla': {
        'directions': {
            'coordinates': PARAM_LINE_MULTI,
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
            'coordinates': PARAM_POINT,
            'options': {
                'maneuver_penalty': PARAM_INT_SMALL,
                'toll_booth_cost': PARAM_INT_SMALL,
                'country_crossing_penalty': PARAM_INT_SMALL
            },
            'profile': 'auto',
            'id': 'wacko',
            'range': [600, 1200],
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
            'coordinates': PARAM_LINE_MULTI,
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
            'coordinates': PARAM_LINE,
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
            'coordinates': PARAM_LINE,
            'profile': 'cycling-regular',
            'range_type': 'distance',
            'range': [PARAM_INT_BIG],
            'units': 'm',
            'location_type': 'destination',
            'attributes': ['area', 'reachfactor'],
            'interval': [PARAM_INT_SMALL]
        },
        'matrix': {
            'coordinates': PARAM_LINE,
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
    'mapbox_osrm': {
        'directions': {
            'alternatives':
            'true',
            'annotations':
            'duration,distance,speed',
            'approaches':
            ';curb;curb;curb',
            'banner_instuctions':
            'true',
            'bearings':
            '50,50;50,50;50,50',
            'continue_straight':
            'true',
            'coordinates':
            '8.688641,49.420577;8.680916,49.415776;8.780916,49.445776',
            'exclude':
            'motorway',
            'geometries':
            'geojson',
            'language':
            'de',
            'overview':
            'simplified',
            'radiuses':
            '500;500;500',
            'roundabout_exits':
            'true',
            'steps':
            'true',
            'voice_units':
            'metric',
            'voide_instructions':
            'true',
            'waypoint_names':
            'a;b;c',
            'waypoint_targets':
            ';8.688641,49.420577;8.680916,49.415776;8.780916,49.445776'
        }
    },
    'valhalla': {
        'directions': {
            "locations": [
                {
                    "lat": 49.420577,
                    "lon": 8.688641
                },
                {
                    "lat": 49.415776,
                    "lon": 8.680916
                },
                {
                    "lat": 49.445776,
                    "lon": 8.780916
                },
            ],
            "costing":
            "auto",
            "costing_options": {
                "auto": {
                    "maneuver_penalty": 50,
                    "toll_booth_cost": 50,
                    "country_crossing_penalty": 50
                }
            },
            "directions_options": {
                "units": "mi",
                "language": "pirate",
                "directions_type": "none"
            },
            "avoid_locations": [{
                "lon": 8.34234,
                "lat": 48.23424
            }],
            "date_time": {
                "type": 1,
                "value": "2019-03-03T08:06"
            },
            "id":
            "wacko"
        },
        'isochrones': {
            "locations": [{
                "lat": PARAM_POINT[1],
                "lon": PARAM_POINT[0]
            }],
            "costing":
            "auto",
            "costing_options": {
                "auto": {
                    "maneuver_penalty": 50,
                    "toll_booth_cost": 50,
                    "country_crossing_penalty": 50
                }
            },
            "contours": [{
                "time": 10,
                "color": 'ff0000'
            }, {
                "time": 20,
                "color": "00FF00"
            }],
            "avoid_locations": [{
                "lon": 8.34234,
                "lat": 48.23424
            }],
            "date_time": {
                "type": 1,
                "value": "2019-03-03T08:06"
            },
            "id":
            "wacko",
            "denoise":
            0.1,
            "polygons":
            True,
            "generalize":
            0.5,
        },
        'matrix': {
            "sources": [
                {
                    "lat": 49.420577,
                    "lon": 8.688641
                },
                {
                    "lat": 49.415776,
                    "lon": 8.680916
                },
                {
                    "lat": 49.445776,
                    "lon": 8.780916
                },
            ],
            "targets": [
                {
                    "lat": 49.420577,
                    "lon": 8.688641
                },
                {
                    "lat": 49.415776,
                    "lon": 8.680916
                },
                {
                    "lat": 49.445776,
                    "lon": 8.780916
                },
            ],
            "costing":
            "auto",
            "costing_options": {
                "auto": {
                    "maneuver_penalty": 50,
                    "toll_booth_cost": 50,
                    "country_crossing_penalty": 50
                }
            },
            "avoid_locations": [{
                "lon": 8.34234,
                "lat": 48.23424
            }],
            "id":
            "wacko",
            "units":
            'mi'
        },
    },
}
