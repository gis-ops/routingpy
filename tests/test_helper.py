# -*- coding: utf-8 -*-
import random

PARAM_POINT = [8.34234, 48.23424]
PARAM_LINE = [[8.688641, 49.420577], [8.680916, 49.415776]]
PARAM_LINE_MULTI = [[8.688641, 49.420577], [8.680916, 49.415776], [8.780916, 49.445776]]
PARAM_POLY = [[[8.688641, 49.420577], [8.680916, 49.415776]]]

PARAM_INT_BIG = 500
PARAM_INT_SMALL = 50

PARAM_STRING = random.choice('abcdefghijklmnopqrstuvwxyz')

PARAM_GEOJSON_POINT = {'type': 'Point', 'coordinates': PARAM_POINT}
PARAM_GEOJSON_LINE = {'type': 'LineString', 'coordinates': PARAM_LINE}
PARAM_GEOJSON_POLY = {'type': 'Polygon', 'coordinates': PARAM_POLY}

ENDPOINTS_QUERIES = {
    'graphhopper': {
        'directions': {
            'coordinates': PARAM_LINE_MULTI,
            'profile': 'car',
            'elevation': True, 
            'points_encoded': True,
            'avoid': 'motorway;toll', 
            'format': 'json',
            'instructions': False
        },
        'matrix': {
            'coordinates': PARAM_LINE_MULTI,
            'profile': 'car',
            'sources': [0,1], 
            'destinations': [2], 
            'out_array': ['weights', 'times', 'distance']
        },
        'isochrones': {
            'coordinates': PARAM_POINT,
            'profile': 'car'
        }
    },
    'valhalla': {
        'directions': {
            'coordinates': PARAM_LINE_MULTI,
            'types': ['break', 'through', 'break'],
            'headings': [PARAM_INT_SMALL] * 3,
            'heading_tolerances': [PARAM_INT_SMALL] * 3,
            'minimum_reachabilities': [PARAM_INT_SMALL] * 3,
            'radiuses': [PARAM_INT_SMALL] * 3,
            'rank_candidates': [True, False, True],
            'options': {
                'maneuver_penalty': PARAM_INT_SMALL,
                'toll_booth_cost': PARAM_INT_SMALL,
                'country_crossing_penalty': PARAM_INT_SMALL
            },
            'profile': 'auto',
            'units': 'mi',
            'directions_type': 'none',
            'avoid_locations': PARAM_POINT,
            'date_time': {'type': 1, 'value': '2019-03-03T08:06'},
            'language': 'pirate',
            'id': 'wacko'
        },
        'isochrones': {
            'coordinates': PARAM_POINT,
            'types': ['break'],
            'headings': [PARAM_INT_SMALL],
            'heading_tolerances': [PARAM_INT_SMALL],
            'minimum_reachabilities': [PARAM_INT_SMALL],
            'radiuses': [PARAM_INT_SMALL],
            'rank_candidates': [True],
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
            'date_time': {'type': 1, 'value': '2019-03-03T08:06'},
        },
        'matrix': {
            'coordinates': PARAM_LINE_MULTI,
            'types': ['break', 'through', 'break'],
            'headings': [PARAM_INT_SMALL] * 3,
            'heading_tolerances': [PARAM_INT_SMALL] * 3,
            'minimum_reachabilities': [PARAM_INT_SMALL] * 3,
            'radiuses': [PARAM_INT_SMALL] * 3,
            'rank_candidates': [True, False, True],
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
    }
}

ENDPOINTS_EXPECTED = {
    'valhalla': {
        'directions': {
            "locations": [
                {
                    "lat": 49.420577,
                    "lon": 8.688641,
                    "type": "break",
                    "heading": 50,
                    "heading_tolerance": 50,
                    "minimum_reachability": 50,
                    "radius": 50,
                    "rank_candidates": True
                },
                {
                    "lat": 49.415776,
                    "lon": 8.680916,
                    "type": "through",
                    "heading": 50,
                    "heading_tolerance": 50,
                    "minimum_reachability": 50,
                    "radius": 50,
                    "rank_candidates": False
                },
                {
                    "lat": 49.445776,
                    "lon": 8.780916,
                    "type": "break",
                    "heading": 50,
                    "heading_tolerance": 50,
                    "minimum_reachability": 50,
                    "radius": 50,
                    "rank_candidates": True
                },
            ],
            "costing": "auto",
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
            "avoid_locations": [
                {
                    "lon": 8.34234,
                    "lat": 48.23424
                }
            ],
            "date_time": {
                "type": 1,
                "value": "2019-03-03T08:06"
            },
            "id": "wacko"
        },
        'isochrones': {
            "locations": [
                {
                    "lat": PARAM_POINT[1],
                    "lon": PARAM_POINT[0],
                    "type": "break",
                    "heading": 50,
                    "heading_tolerance": 50,
                    "minimum_reachability": 50,
                    "radius": 50,
                    "rank_candidates": True
                }
            ],
            "costing": "auto",
            "costing_options": {
                "auto": {
                    "maneuver_penalty": 50,
                    "toll_booth_cost": 50,
                    "country_crossing_penalty": 50
                }
            },
            "contours": [
                {
                    "time": 10,
                    "color": 'ff0000'
                },
                {
                    "time": 20,
                    "color": "00FF00"
                }
            ],
            "avoid_locations": [
                {
                    "lon": 8.34234,
                    "lat": 48.23424
                }
            ],
            "date_time": {
                "type": 1,
                "value": "2019-03-03T08:06"
            },
            "id": "wacko",
            "denoise": 0.1,
            "polygons": True,
            "generalize": 0.5,
        },
        'matrix': {
            "sources": [
                {
                    "lat": 49.420577,
                    "lon": 8.688641,
                    "type": "break",
                    "heading": 50,
                    "heading_tolerance": 50,
                    "minimum_reachability": 50,
                    "radius": 50,
                    "rank_candidates": True
                },
                {
                    "lat": 49.415776,
                    "lon": 8.680916,
                    "type": "through",
                    "heading": 50,
                    "heading_tolerance": 50,
                    "minimum_reachability": 50,
                    "radius": 50,
                    "rank_candidates": False
                },
                {
                    "lat": 49.445776,
                    "lon": 8.780916,
                    "type": "break",
                    "heading": 50,
                    "heading_tolerance": 50,
                    "minimum_reachability": 50,
                    "radius": 50,
                    "rank_candidates": True
                },
            ],
            "targets": [
                {
                    "lat": 49.420577,
                    "lon": 8.688641,
                    "type": "break",
                    "heading": 50,
                    "heading_tolerance": 50,
                    "minimum_reachability": 50,
                    "radius": 50,
                    "rank_candidates": True
                },
                {
                    "lat": 49.415776,
                    "lon": 8.680916,
                    "type": "through",
                    "heading": 50,
                    "heading_tolerance": 50,
                    "minimum_reachability": 50,
                    "radius": 50,
                    "rank_candidates": False
                },
                {
                    "lat": 49.445776,
                    "lon": 8.780916,
                    "type": "break",
                    "heading": 50,
                    "heading_tolerance": 50,
                    "minimum_reachability": 50,
                    "radius": 50,
                    "rank_candidates": True
                },
            ],
            "costing": "auto",
            "costing_options": {
                "auto": {
                    "maneuver_penalty": 50,
                    "toll_booth_cost": 50,
                    "country_crossing_penalty": 50
                }
            },
            "avoid_locations": [
                {
                    "lon": 8.34234,
                    "lat": 48.23424
                }
            ],
            "id": "wacko",
            "units": 'mi'
        },
    },
    'ors': {
        'directions': {
            'coordinates': PARAM_LINE,
            'profile': 'driving-car',
            'preference': 'fastest',
            'format': 'geojson',
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
            'optimized': 'false',
            'options': {
                'avoid_features': [
                    'highways',
                    'tollways'
                ]
            }
        },
        'isochrones': {
            'locations': PARAM_LINE,
             'profile': 'cycling-regular',
             'range_type': 'distance',
             'range': [PARAM_INT_BIG],
             'units': 'm',
             'location_type': 'destination',
             'attributes': ['area', 'reachfactor'],
             'interval': [PARAM_INT_SMALL]
         },
        'matrix': {
            'locations': PARAM_LINE,
             'sources': [1],
             'destinations': [0],
             'profile': 'driving-car',
             'metrics': ['duration', 'distance'],
             'resolve_locations': 'true',
             'units': 'mi',
             'optimized': 'false'
        }
    }
}
