from routingpy import ORS, Graphhopper, HereMaps

#api = ORS(key='5b3ce3597851110001cf624858ff1f9270364f74907d578b80c3c41cc', base_url='https://api.openrouteservice.org', requests_kwargs={})

#routes = api.directions(coordinates=[[8.681495, 49.41461], [8.686507, 49.41943]], profile='driving-car', format='json', dry_run=False)

#print(routes)

# from routingpy import Google

# api = Google(api_key='AIzaSyBibIkPFip29wcE4y4wrZnY_mnwZv_sU8g')

# routes = api.directions(
#     coordinates=[[8.688641, 49.420577], [8.680916, 49.415776],
#                  [8.780916, 49.445776]],
#     profile='car',
#     dry_run=False)

# print(routes.distance)

# from routingpy import Graphhopper

# api = Graphhopper(api_key='78a38b3d-bd4f-4e52-b466-37053a0344fa')

# routes = api.directions(
#     coordinates=[[8.688641, 49.420577], [8.680916, 49.415776],
#                  [8.780916, 49.445776]],
#     elevation=False,
#     # points_encoded=True,
#     profile='car',
#     # avoid=['motorway', 'toll'],
#     format='json',
#     # instructions=False,
#     dry_run=False)

# print(routes.geometry, routes.duration, routes.distance)

# isochrone = api.isochrones(
#     coordinates=[8.34234, 48.23424],
#     range=[200],
#     profile='car',
#     buckets=3,
#     dry_run=True)

# print(isochrone)

# #matrix = api.distance_matrix(coordinates=[[11.588051, 49.932707], [10.747375,50.241935], [11.983337,50.118817]], out_array=['weights', 'times', 'distance'], profile='car', dry_run=False)

# #print(matrix)

# # matrix1 = api.distance_matrix(
# #     coordinates=[[8.688641, 49.420577], [8.680916, 49.415776],
# #                  [8.780916, 49.445776]],
# #     sources=[0, 1],
# #     destinations=[2],
# #     out_array=['weights', 'times', 'distance'],
# #     profile='car',
# #     dry_run=False)
# #matrix1 = api.distance_matrix(coordinates=[[8.688641, 49.420577], [8.680916, 49.415776], [8.780916, 49.445776]], sources=[0,1], out_array=['weights', 'times', 'distance'], profile='car', dry_run=False)

# #print(matrix1)

# from routingpy import HereMaps
# import datetime

here_api = HereMaps(
    app_id='Ssw36q9nNyfx6899yBPK', app_code='L6SDa5v0jzsgRr1yAtMWFw')

# # routes = here_api.directions(
# #     # coordinates=[
# #     #     [8.688641, 49.420577],
# #     #     [8.680916, 49.415776],
# #     #     [8.780916, 49.445776]
# #     # ],
# #     coordinates=[
# #         here_api.WayPoint(
# #             position=(8.688641, 49.420577),
# #             waypoint_type='stopOver',
# #             stopover_duration=30,
# #             transit_radius=200,
# #             heading=180),
# #         here_api.WayPoint(
# #             position=(8.680916, 49.415776),
# #             waypoint_type='passThrough',
# #             user_label='honk',
# #         ),
# #         here_api.WayPoint(position=(8.780916, 49.445776))
# #     ],
# #     profile='car;fastest',
# #     # profile=here_api.RoutingMode(
# #     #     mode_type='fastest',
# #     #     mode_transport_type='car',
# #     #     mode_traffic='enabled',
# #     #     features={
# #     #         "motorway": -2,
# #     #         "tollroad": -1,
# #     #         #"tunnel": 1
# #     #     }),
# #     request_id=101,
# #     avoid_areas=[[(8.688641, 49.420577), (8.680916, 49.415776)],
# #                  [(8.780916, 49.445776), (8.780916, 49.445776)]],
# #     #avoid_links=[-53623477, -536234327, 123],
# #     avoid_seasonal_closures=True,
# #     #avoid_turns='difficult',
# #     allowed_zones=[167772378],
# #     exclude_zones=[510, 511],
# #     exclude_zone_types=['vignette', 'congestionPricing'],
# #     exclude_countries=['AUT', 'CHE'],
# #     departure=datetime.datetime(2019, 3, 29, 3, 0).isoformat(),
# #     #arrival=datetime.datetime(2019, 3, 29, 3, 0).isoformat(),
# #     alternatives=3,
# #     metric_system='metric',
# #     view_bounds=[(8.688641, 49.420577), (8.680916, 49.415776)],
# #     resolution={
# #         'viewresolution': 300,
# #         'snapresolution': 300
# #     },
# #     instruction_format='text',
# #     language='en-us',
# #     route_attributes=[
# #         'waypoints', 'summary', 'summaryByCountry', 'shape', 'boundingBox',
# #         'legs', 'notes', 'lines', 'routeId', 'groups', 'tickets', 'incidents',
# #         'zones'
# #     ],
# #     leg_attributes=['maneuvers', 'waypoint', 'length', 'travelTime'],
# #     maneuver_attributes=['position', 'length', 'travelTime'],
# #     link_attributes=['shape', 'speedLimit'],
# #     dry_run=False)

# #print(routes.__repr__)

# isochrones = here_api.isochrones(
#     # coordinates=
#     #       here_api.WayPoint(
#     #           position=(8.688641, 49.420577)
#     #       )
#     # ,
#     coordinates=[8.34234, 48.23424],
#     ranges=[3000],
#     range_type='distance',
#     profile='car;fastest',
#     #center_type='start',
#     #request_id=101,
#     #single_component=False,
#     #quality=1,
#     dry_run=False
#     #max_points=100,

#     # profile=here_api.RoutingMode(
#     #     mode_type='fastest',
#     #     mode_transport_type='car',
#     #     mode_traffic='enabled',
#     #     features={
#     #         "motorway": -2,
#     #         "tollroad": -1,
#     #         #"tunnel": 1
#     #     }),
#)

#print(isochrones[0].geometry, isochrones[0].center, isochrones[0].range )

ors_api = ORS(
    api_key='5b3ce3597851110001cf624858ff1f9270364f74907d578b80c3c41cc')

isochrones = ors_api.isochrones(
    coordinates=[[8.34234, 48.23424]],
    intervals=[3000],
    interval_type='distance',
    profile='driving-car',
    dry_run=False)

print(isochrones, isochrones[0].geometry, isochrones[0].center,
      isochrones[0].range)

# #print(isochrones.__repr__)
# #print(isochrones.isochrones[2].__repr__)

# matrix = here_api.distance_matrix(
#     coordinates=[[8.688641, 49.420577], [8.680916, 49.415776],
#                  [8.780916, 49.445776]],
#     sources=[0, 1, 2],
#     destinations=[0, 1, 2],
#     profile='car;fastest',
#     summary_attributes=['traveltime', 'costfactor', 'distance'],
#     truck_type='truck',
#     trailers_count=3,
#     shipped_hazardous_goods=['gas', 'flammable'],
#     limited_weight=10,
#     weight_per_axle=100,
#     height=20,
#     width=10,
#     length=10,
#     # coordinates=[
#     #     here_api.WayPoint(
#     #         position=(8.688641, 49.420577),
#     #         waypoint_type='stopOver',
#     #         stopover_duration=30,
#     #         transit_radius=200,
#     #         heading=180),
#     #     here_api.WayPoint(
#     #         position=(8.680916, 49.415776),
#     #         waypoint_type='passThrough',
#     #         user_label='honk',
#     #     ),
#     #     here_api.WayPoint(position=(8.780916, 49.445776))
#     # ],
#     #search_range=10000,
#     dry_run=True

#     # profile=here_api.RoutingMode(
#     #     mode_type='fastest',
#     #     mode_transport_type='car',
#     #     mode_traffic='enabled',
#     #     features={
#     #         "motorway": -2,
#     #         "tollroad": -1,
#     #         #"tunnel": 1
#     #     }),
# )

# # #print(matrix.__repr__)

# routes = here_api.directions(
#     # coordinates=[
#     #     here_api.WayPoint(
#     #         position=(8.688641, 49.420577),
#     #         waypoint_type='stopOver',
#     #         stopover_duration=30,
#     #         transit_radius=200,
#     #         heading=180),
#     #     here_api.WayPoint(
#     #         position=(8.680916, 49.415776),
#     #         waypoint_type='passThrough',
#     #         user_label='honk',
#     #     ),
#     #     here_api.WayPoint(position=(8.780916, 49.445776))
#     # ],
#     # routing_mode=here_api.RoutingMode(
#     #     mode_type='fastest',
#     #     mode_transport_type='car',
#     #     mode_traffic='enabled',
#     #     features={
#     #         "motorway": -2,
#     #         "tollroad": -1,
#     #         "tunnel": 1
#     #     }),
#     # allowed_zones=[167772378],
#     # custom_consumption_details='',
#     # line_attributes=['lineForeground', 'lineBackground'],
#     # walk_time_multiplier=2.0,
#     # walk_speed=1.2,
#     # walk_radius=2000,
#     # representation=[
#     #    'overview', 'display', 'dragNDrop', 'navigation', 'linkPaging',
#     #    'turnByTurn'
#     # ],
#     # tunnel_category=['A'],
#     coordinates=[(8.688641, 49.420577), (8.680916, 49.415776),
#                  (8.780916, 49.445776)],
#     profile='truck;fastest',
#     request_id=101,
#     avoid_areas=[[(8.688641, 49.420577), (8.680916, 49.415776)],
#                  [(8.780916, 49.445776), (8.780916, 49.445776)]],
#     avoid_links=[-53623477],
#     avoid_seasonal_closures=True,
#     avoid_turns='difficult',
#     exclude_zones=[510, 511],
#     exclude_zone_types=['vignette', 'congestionPricing'],
#     exclude_countries=['AUT', 'CHE'],
#     departure=datetime.datetime(2019, 3, 29, 3, 0).isoformat(),
#     alternatives=3,
#     metric_system='metric',
#     view_bounds=[(8.688641, 49.420577), (8.680916, 49.415776)],
#     resolution={
#         'viewresolution': 300,
#         'snapresolution': 300
#     },
#     instruction_format='text',
#     language='en-us',
#     json_attributes=9,
#     route_attributes=[
#         'waypoints', 'summary', 'summaryByCountry', 'shape', 'boundingBox',
#         'legs', 'notes', 'lines', 'routeId', 'groups', 'tickets', 'incidents',
#         'zones'
#     ],
#     leg_attributes=['maneuvers', 'waypoint', 'length', 'travelTime'],
#     maneuver_attributes=['position', 'length', 'travelTime'],
#     link_attributes=['shape', 'speedLimit'],
#     generalization_tolerances=[0.1, 0.01],
#     vehicle_type='diesel,5.5',
#     license_plate='lastcharacter:5',
#     max_number_of_changes=5,
#     combine_change=False,
#     truck_type='truck',
#     trailers_count=3,
#     shipped_hazardous_goods=['gas', 'flammable'],
#     limited_weight=10,
#     weight_per_axle=100,
#     height=20,
#     width=10,
#     length=10,
#     truck_restriction_penalty='soft',
#     return_elevation=True,
#     consumption_model='default',
#     speed_profile='fast',
#     dry_run=False)

# print(routes)
