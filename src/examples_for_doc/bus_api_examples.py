bus_stops_example = [
    {
        "stop_code": "98281",
        "stop_id": "98281",
        "stop_lat": 103.966171624349,
        "stop_lon": 1.35967915316721,
        "stop_name": "Estella Gdns",
        "stop_desc": None,
        "wheelchair_boarding": 1,
        "geom": None,
    },
    {
        "stop_code": "59629",
        "stop_id": "59629",
        "stop_lat": 1.434758706,
        "stop_lon": 103.8439165,
        "stop_name": "Symphony Suites Condo",
        "stop_desc": None,
        "wheelchair_boarding": 1,
        "geom": None,
    },
]

bus_stop_get_example = {
    "stop_code": "98281",
    "stop_id": "98281",
    "stop_lat": 103.966171624349,
    "stop_lon": 1.35967915316721,
    "stop_name": "Estella Gdns",
    "stop_desc": None,
    "wheelchair_boarding": "1",
    "geom": None
}


bus_trips_get_example ={
    "10kmh_total_bus_duration": 240,
    "10kmh_total_duration": 2185,
    "20kmh_total_bus_duration": 212,
    "20kmh_total_duration": 2157,
    "5kmh_total_bus_duration": 303,
    "5kmh_total_duration": 2248,
    "5kmh_total_bus_duration": 303,
    "5kmh_total_duration": 2248,
    "bus_trip_id": 13,
    "end_area_code": "PG",
    "end_geom": None,
    "end_lat": 1.40544909693222,
    "end_lon": 103.908503032429,
    "end_node_id": 2274884501,
    "end_region_code": "NER",
    "filepath": "01012to2274884501.json",
    "non_bus_duration": 1945,
    "non_flooded_total_bus_duration": 203,
    "non_flooded_total_duration": 2148,
    "number_of_busroutes": 1,
    "routeNodeIDs": [
        4738400701, 233432515, 233432542, 595267994, 595268007,
        233432563, 233432607, 233432633, 365302308, 233432671,
        5982556742, 4602210048, 233432705, 233432799, 7043294787,
        233432823, 5166520742, 249392291, 240646599, 249392296,
        240646581, 378619193, 378618810, 240646389, 240646408,
        236310575, 236320394, 2948839129, 229576235, 245396647,
        5243487086, 229576256, 377553457
    ],
    "start_area_code": "RC",
    "start_geom": None,
    "start_lat": 1.29684825487647,
    "start_lon": 103.85253591654,
    "start_node_id": 4748705954,
    "start_region_code": "CR",
    "total_bus_distance": 3388,
    "transfers": 2,
    "transit_time": 1860,
    "waiting_time": 366
}


bus_trip_segment_example = {
    "10kmh_flooded_bus_duration": 240,
    "20kmh_flooded_bus_duration": 212,
    "5kmh_flooded_bus_duration": 303,
    "bus_trip_id": 13,
    "destination_stop_id": "60121",
    "filepath": "01012to2274884501.json",
    "non_flooded_bus_duration": 203,
    "origin_stop_id": "01013",
    "route_id": "133",
    "segment": 1
}

bus_trips_delayed_example = {
    "trips": [
        {
            "bus_trip_id": 5,
            "start_lat": 1.29684825487647,
            "start_lon": 103.85253591654,
            "end_lat": 1.35537955952137,
            "end_lon": 103.887346108709,
            "flooded_total_bus_durations": {
                "10kmh": 240,
                "20kmh": 212,
                "5kmh": 303
            },
            "flooded_total_durations": {
                "10kmh": 2002,
                "20kmh": 1974,
                "5kmh": 2065
            },
            "non_flooded_total_bus_duration": 203,
            "non_flooded_total_duration": 1965,
            "overall_bus_delay": {
                "10kmh": 37,
                "20kmh": 9,
                "5kmh": 100
            },
            "overall_total_delay": {
                "10kmh": 37,
                "20kmh": 9,
                "5kmh": 100
            },
            "segments": [
                {
                    "segment_id": 1,
                    "origin_stop_id": "01013",
                    "destination_stop_id": "60121",
                    "non_flooded_bus_duration": 203,
                    "flooded_durations": {
                        "10kmh": 240,
                        "20kmh": 212,
                        "5kmh": 303
                    },
                    "delays": {
                        "10kmh": 37,
                        "20kmh": 9,
                        "5kmh": 100
                    }
                }
            ]
        }
    ]
}


end_area_codes_example = {
    "Ang Mo Kio": "AM",
    "Bedok": "BD",
    "Bishan": "BS",
    "Boon Lay": "BL",
    "Bukit Batok": "BK",
    "Bukit Merah": "BM",
    "Bukit Panjang": "BP",
    "Bukit Timah": "BT",
    "Changi": "CH",
    "Choa Chu Kang": "CK",
    "Clementi": "CL",
    "Downtown": "DT",
}


get_route_example = {
    "plan": {
        "date": 1763506800000,
        "from": {"lat": 1.3727816, "lon": 103.9482223, "name": "Origin"},
        "itineraries": [
            {
                "duration": 1376,
                "startTime": 1763507169000,
                "legs": [
                    {
                        "mode": "WALK",
                        "distance": 63.11,
                        "duration": 52,
                        "from": {"lat": 1.3727816, "lon": 103.9482223, "name": "Origin"},
                        "to": {"lat": 1.3724107, "lon": 103.9486593, "name": "PASIR RIS STN EXIT B", "stopCode": "77039"}
                    },
                    {
                        "mode": "BUS",
                        "route": "518",
                        "routeId": "518",
                        "distance": 3276.98,
                        "duration": 731,
                        "from": {"name": "PASIR RIS STN EXIT B", "stopCode": "77039"},
                        "to": {"name": "BLK 390/OPP TAMPINES JC", "stopCode": "76239"},
                        "overall_bus_route_status": "clear",
                        "non_flooded_bus_duration": [238],
                        "5kmh_flooded_bus_duration": [238],
                        "10kmh_flooded_bus_duration": [238],
                        "20kmh_flooded_bus_duration": [238]
                    }
                ]
            }
        ]
    }
}


bus_route_example = {
    "service": "10",
    "directions": [
        {
            "direction": 0,
            "coordinates": [[1.2968, 103.8525], [1.3554, 103.8873]]
        },
        {
            "direction": 1,
            "coordinates": [[1.3554, 103.8873], [1.2968, 103.8525]]
        }
    ]
}