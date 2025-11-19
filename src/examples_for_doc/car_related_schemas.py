car_trips_schema = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "car_trip_id": {
                "type": "integer",
                "description": "Unique identifier of the car trip"
            },
            "start_area_code": {
                "type": "string",
                "description": "Area code for trip origin"


            },
            "start_lat": {
                "type": "number",
                "format": "float",
                "description": "Latitude of trip origin"
            },
            "start_lon": {
                "type": "number",
                "format": "float",
                "description": "Longitude of trip origin"
            },
            "start_node_id": {
                "type": "integer",
                "description": "Node ID of the starting location"
            },
            "start_region_code": {
                "type": "string",
                "description": "Region code of the starting location"
            },
            "end_area_code": {
                "type": "string",
                "description": "Area code for trip destination"
            },
            "end_lat": {
                "type": "number",
                "format": "float",
                "description": "Latitude of trip destination"
            },
            "end_lon": {
                "type": "number",
                "format": "float",
                "description": "Longitude of trip destination"
            },
            "end_node_id": {
                "type": "integer",
                "description": "Node ID of the destination location"
            },
            "end_region_code": {
                "type": "string",
                "description": "Region code of the destination location"
            },
            "5kph_total_duration": {
                "type": "number",
                "description": "Total trip duration (seconds) assuming 5 km/h speed due to flooding"
            },
            "10kph_total_duration": {
                "type": "number",
                "description": "Total trip duration (seconds) assuming 10 km/h speed due to flooding"
            },
            "20kph_total_duration": {
                "type": "number",
                "description": "Total trip duration (seconds) assuming 20 km/h speed due to flooding"
            },
            "45kph_total_duration": {
                "type": "number",
                "description": "Total trip duration (seconds) assuming 45 km/h speed due to flooding"
            },
            "72kph_total_duration": {
                "type": "number",
                "description": "Total trip duration (seconds) assuming 72 km/h speed due to flooding"
            },
            "81kph_total_duration": {
                "type": "number",
                "description": "Total trip duration (seconds) assuming 81 km/h speed due to flooding"
            },
            "90kph_total_duration": {
                "type": "number",
                "description": "Total trip duration (seconds) assuming 90 km/h speed when not flooded"
            }
        }
        
    }
}


car_trips_detailed_schema = {
"type": "array",
"items": {
    "type": "object",
    "properties": {
        "detour_comparison": {"type": "object", "description": "Map of speed profiles to detour/flooded times"},
        "detour_route_geometry": {"type": "array", "items": {"type": "array", "items": {"type": "number"}}},
        "detour_total_travel_time_seconds": {"type": "object"},
        "flooded_segments": {"type": "array", "items": {"type": "object", "properties": {
            "geometry": {"type": "string"},
            "length_m": {"type": "number"},
            "road_name": {"type": "string"},
            "travel_time_seconds": {"type": "object"}
        }}},
        "has_detour": {"type": "boolean"},
        "normal_travel_time_seconds": {"type": "object"},
        "overall_route_status": {"type": "string"},
        "route_geometry": {"type": "array", "items": {"type": "array", "items": {"type": "number"}}}
    }
}
}