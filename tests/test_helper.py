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

ENDPOINT_DICT = {
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
            "directions_options": {
                "units": "mi",
                "language": "pirate",
                "directions_type": "none"
            },
            "avoid_locations": [
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
                    "lat": 49.420577,
                    "lon": 8.688641,
                    "type": "break",
                    "heading": 50,
                    "heading_tolerance": 50,
                    "minimum_reachability": 50,
                    "radius": 50,
                    "rank_candidates": True
                }
            ],
            "costing": "auto",
            "contours": {
                "time": 600,
                "color": 'ff0000'
            },
            "date_time": {
                "type": 1,
                "value": "2019-03-03T08:06"
            },
            "id": "wacko",
            "polygons": True,
            "generalize": 0.65,

        }
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
