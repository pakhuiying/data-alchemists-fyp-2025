car_trips_example = [
    {
        "car_trip_id": 1,
        "start_area_code": "TM",
        "start_lat": 1.3347624,
        "start_lon": 103.9787666,
        "start_node_id": 25451915,
        "start_region_code": "ER",
        "end_area_code": "RV",
        "end_lat": 1.2959214532978,
        "end_lon": 103.839648207666,
        "end_node_id": 74389915,
        "end_region_code": "CR",
        "5kph_total_duration": 846.094561834224,
        "10kph_total_duration": 846.094561834224,
        "20kph_total_duration": 846.094561834224,
        "45kph_total_duration": 846.094561834224,
        "72kph_total_duration": 846.094561834224,
        "81kph_total_duration": 846.094561834224,
        "90kph_total_duration": 846.094561834224,
    },
    {
        "car_trip_id": 2,
        "start_area_code": "TM",
        "start_lat": 1.3347624,
        "start_lon": 103.9787666,
        "start_node_id": 25451915,
        "start_region_code": "ER",
        "end_area_code": "CC",
        "end_lat": 1.38455185352078,
        "end_lon": 103.780567652147,
        "end_node_id": 158014842,
        "end_region_code": "NR",
        "5kph_total_duration": 1328.11506274635,
        "10kph_total_duration": 1328.11506274635,
        "20kph_total_duration": 1328.11506274635,
        "45kph_total_duration": 1328.11506274635,
        "72kph_total_duration": 1328.11506274635,
        "81kph_total_duration": 1328.11506274635,
        "90kph_total_duration": 1328.11506274635,
    }
]
car_trips_detailed_example = [
    {
        "detour_comparison": {
            "10kph": {"detour_route_time_sec": 5785.010106395435, "difference_sec": 1687.8525970813926, "flooded_route_time_sec": 4097.157509314043},
            "20kph": {"detour_route_time_sec": 2892.5050531977176, "difference_sec": 894.7545701234731, "flooded_route_time_sec": 1997.7504830742446},
            "45kph": {"detour_route_time_sec": 1285.5578014212076, "difference_sec": 454.14455514685096, "flooded_route_time_sec": 831.4132462743567},
            "5kph": {"detour_route_time_sec": 11570.02021279087, "difference_sec": 3274.0486509972325, "flooded_route_time_sec": 8295.971561793638},
            "72kph": {"detour_route_time_sec": 803.4736258882548, "difference_sec": 321.9615506538645, "flooded_route_time_sec": 481.5120752343903},
            "81kph": {"detour_route_time_sec": 714.1987785673376, "difference_sec": 297.4832164884967, "flooded_route_time_sec": 416.71556207884095},
            "90kph": {"detour_route_time_sec": 642.7789007106038, "difference_sec": 277.90054915620226, "flooded_route_time_sec": 364.87835155440155}
        },
        "detour_route_geometry": [[1.2976481, 103.8532709], [1.2978206, 103.8534083]],
        "detour_total_travel_time_seconds": {"10kph": 5785.010106395435, "20kph": 2892.5050531977176, "45kph": 1285.5578014212076, "5kph": 11570.02021279087, "72kph": 803.4736258882548, "81kph": 714.1987785673376, "90kph": 642.7789007106038},
        "flooded_segments": [
            {
                "geometry": "LINESTRING (103.8419805 1.3114891, 103.8416957 1.3116266)",
                "length_m": 717.9183136101102,
                "road_name": "Bukit Timah Road",
                "travel_time_seconds": {"10kph": 258.4505928996397, "10kph_delay": 229.73386035523527}
            }
        ],
        "has_detour": True,
        "normal_travel_time_seconds": {"10kph": 3283.905163989614, "20kph": 1641.952581994807},
        "overall_route_status": "flooded",
        "route_geometry": [[1.2976481, 103.8532709], [1.2978206, 103.8534083]]
    }
]