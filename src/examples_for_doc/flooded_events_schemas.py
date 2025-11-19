flood_events_schema = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "flood_id": {
                "type": "integer",
                "description": "Unique identifier of the flood event"
            },
            "flooded_location": {
                "type": "string",
                "description": "Location name where the flood occurred"
            },
            "date": {
                "type": "string",
                "format": "date",
                "description": "Date of the flood event"
            },
            "daily rainfall total (mm)": {
                "type": "number",
                "description": "Total daily rainfall (in mm)"
            },
            "highest 30 min rainfall (mm)": {
                "type": "number",
                "description": "Maximum rainfall within 30 minutes (in mm)"
            },
            "highest 60 min rainfall (mm)": {
                "type": "number",
                "description": "Maximum rainfall within 60 minutes (in mm)"
            },
            "highest 120 min rainfall (mm)": {
                "type": "number",
                "description": "Maximum rainfall within 120 minutes (in mm)"
            },
            "mean_pr": {
                "type": "number",
                "description": "Mean precipitation rate"
            },
            "latitude": {
                "type": "number",
                "format": "float",
                "description": "Latitude of the flood location"
            },
            "longitude": {
                "type": "number",
                "format": "float",
                "description": "Longitude of the flood location"
            },
            "geom": {
                "type": "object",
                "description": "GeoJSON geometry of the flood event",
                "properties": {
                    "type": {"type": "string", "example": "Point"},
                    "coordinates": {
                        "type": "array",
                        "items": {"type": "number"},
                        "example": [103.8349951, 1.429525229]
                    },
                    "crs": {
                        "type": "object",
                        "properties": {
                            "type": {"type": "string", "example": "name"},
                            "properties": {
                                "type": "object",
                                "properties": {
                                    "name": {"type": "string", "example": "EPSG:4326"}
                                }
                            }
                        }
                    }
                }
            }
        },
        "required": ["flood_id", "flooded_location", "date", "latitude", "longitude"]
    }
}



flood_event_by_id_schema = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "flood_id": {
                "type": "integer",
                "description": "Unique identifier of the flood event"
            },
            "road_name": {
                "type": "string",
                "description": "Name of the nearest road affected by the flood"
            },
            "road_type": {
                "type": "string",
                "description": "Type of road (e.g., primary, residential)"
            },
            "length_m": {
                "type": "number",
                "format": "float",
                "description": "Length of affected road segment in meters"
            },
            "geometry": {
                "type": "string",
                "description": "WKT LINESTRING representing the road geometry"
            }
        }
    }
}


flood_event_location_schema= {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "count": {
                "type": "integer",
                "description": "Number of events or road segments aggregated at this location.",
                "example": 13
            },
            "location": {
                "type": "string",
                "description": "Human-readable location name or code.",
                "example": "21229"
            },
            "latitude": {
                "type": "number",
                "format": "float",
                "description": "Latitude of the location in WGS84.",
                "example": 1.342064137
            },
            "longitude": {
                "type": "number",
                "format": "float",
                "description": "Longitude of the location in WGS84.",
                "example": 103.7160202
            },
            "road_length": {
                "type": "number",
                "format": "float",
                "description": "Total length of affected road near this location (in meters).",
                "example": 429.73680893532423
            },
            "time_20kmh_min": {
                "type": "number",
                "format": "float",
                "description": "Estimated travel time at 20 km/h (in minutes).",
                "example": 1.29
            },
            "time_50kmh_min": {
                "type": "number",
                "format": "float",
                "description": "Estimated travel time at 50 km/h (in minutes).",
                "example": 0.52
            },
            "time_travel_delay_min": {
                "type": "number",
                "format": "float",
                "description": "Additional travel time (in minutes), e.g. delay between 50 km/h and 20 km/h.",
                "example": 0.77
            }
        },
        "required": [
            "count",
            "location",
            "latitude",
            "longitude",
            "road_length",
            "time_20kmh_min",
            "time_50kmh_min",
            "time_travel_delay_min"
        ]
    }
}


get_buses_affected_by_floods_schema = {
    "type": "object",
    "properties": {
        "results": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "affected_bus_services": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of bus service numbers affected by the flood event"
                    },
                    "candidate_stops": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "distance_m": {"type": "number", "format": "float", "description": "Distance from flood point to stop in meters"},
                                "stop_code": {"type": "string", "description": "Transit stop code"},
                                "stop_lat": {"type": "number", "format": "float", "description": "Stop latitude"},
                                "stop_lon": {"type": "number", "format": "float", "description": "Stop longitude"},
                                "stop_name": {"type": "string", "description": "Stop name"}
                            },
                            "required": ["distance_m", "stop_code", "stop_lat", "stop_lon", "stop_name"]
                        },
                        "description": "Candidate bus stops near the flooded road segments"
                    },
                    "flood_id": {"type": "integer", "description": "ID of the flood event"}
                },
                "required": ["affected_bus_services", "candidate_stops", "flood_id"]
            }
        }
    },
    "required": ["results"]
}


get_flood_events_by_date_range_schema = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "daily rainfall total (mm)": {"type": "number", "description": "Total daily rainfall in mm"},
            "date": {"type": "string", "description": "Date/time of the flood event"},
            "flood_id": {"type": "integer", "description": "Flood event ID"},
            "flooded_location": {"type": "string", "description": "Flood location name"},
            "geom": {"type": "string", "description": "Point geometry (WKB)"},
            "geometry": {"type": "string", "description": "Road geometry (WKT LINESTRING)"},
            "highest 120 min rainfall (mm)": {"type": "number", "description": "Max rainfall in 120 minutes (mm)"},
            "highest 30 min rainfall (mm)": {"type": "number", "description": "Max rainfall in 30 minutes (mm)"},
            "highest 60 min rainfall (mm)": {"type": "number", "description": "Max rainfall in 60 minutes (mm)"},
            "latitude": {"type": "number", "format": "float", "description": "Latitude"},
            "longitude": {"type": "number", "format": "float", "description": "Longitude"},
            "length_m": {"type": "number", "format": "float", "description": "Length of affected road in meters"},
            "mean_pr": {"type": "number", "description": "Mean precipitation rate"},
            "road_name": {"type": "string", "description": "Name of the affected road"},
            "road_type": {"type": "string", "description": "Type of road"},
            "time_20kmh_min": {"type": "number", "format": "float", "description": "Estimated travel time at 20 km/h in minutes"},
            "time_50kmh_min": {"type": "number", "format": "float", "description": "Estimated travel time at 50 km/h in minutes"},
            "time_travel_delay_min": {"type": "number", "format": "float", "description": "Additional travel time (minutes)"}
        },
        "required": ["flood_id", "date", "flooded_location"]
    }
}


critical_segments_schema = {
    "type": "object",
    "properties": {
        "buffer_m": {"type": "number", "description": "Buffer radius in meters used to select segments"},
        "count_critical_segments": {"type": "integer", "description": "Number of critical segments returned"},
        "critical_segments": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "centrality_score": {"type": "number", "description": "Betweenness centrality score"},
                    "geometry": {
                        "type": "object",
                        "properties": {
                            "coordinates": {"type": "array", "description": "List of coordinate pairs (projected units)", "items": {"type": "array", "items": {"type": "number"}}},
                            "type": {"type": "string", "example": "LineString"}
                        }
                    },
                    "length_m": {"type": "number", "description": "Segment length in meters"},
                    "road_name": {"oneOf": [{"type": "string"}, {"type": "array", "items": {"type": "string"}}], "description": "Name(s) of the road(s)"},
                    "road_type": {"type": "string", "description": "Road type (e.g., residential, primary)"}
                }
            }
        },
        "flood_id": {"type": "integer", "description": "ID of the flood event"},
        "flood_point": {"type": "object", "properties": {"coordinates": {"type": "array", "items": {"type": "number"}}, "type": {"type": "string"}}, "description": "GeoJSON point of flood location"}
    },
    "required": ["flood_id"]
}


get_unique_flood_events_by_location_schema = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "flood_id": {"type": "integer", "description": "Unique flood event identifier"},
            "flooded_location": {"type": "string", "description": "Human readable flooded location"},
            "latitude": {"type": "number", "format": "float", "description": "Latitude of the event"},
            "longitude": {"type": "number", "format": "float", "description": "Longitude of the event"},
            "time_travel_delay_min": {"type": "number", "format": "float", "description": "Estimated travel delay in minutes at typical speeds"}
        },
        "required": ["flood_id", "flooded_location", "latitude", "longitude"]
    }
}