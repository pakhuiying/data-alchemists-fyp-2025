from flask import Blueprint
from src.controllers.bus_controller import (get_all_bus_stops, get_bus_stop_by_stop_code, get_all_bus_trip, get_bus_trip_by_id,get_all_bus_trip_segment, get_bus_trip_segment_by_id, get_unique_end_area_codes, get_bus_trip_segment_delay, get_onemap_route, get_bus_route)
from flasgger import swag_from
from ..examples_for_doc.bus_api_examples import *
from ..examples_for_doc.bus_related_schemas import *
bus_route = Blueprint('bus_route', __name__)



@bus_route.route('/bus_stops', methods=['GET'])
@swag_from({
    "tags": ["Bus"],
    "responses": {
        200: {
            "description": "Bus stop details",
            "schema": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "stop_id": {"type": "string", "description": "Unique identifier of the bus stop"},
                        "stop_code": {"type": "string", "description": "Official bus stop code"},
                        "stop_name": {"type": "string", "description": "Name of the bus stop"},
                        "stop_lat": {"type": "number", "format": "float", "description": "Latitude"},
                        "stop_lon": {"type": "number", "format": "float", "description": "Longitude"},
                        "wheelchair_boarding": {"type": "string", "description": "1 if wheelchair accessible, 0 if not"},
                        "geom": {"type": "string", "nullable": True, "description": "Geometry data for mapping"},
                        "stop_desc": {"type": "string", "nullable": True, "description": "Optional description"},
                        "stop_url": {"type": "string", "nullable": True, "description": "Optional URL for more info"}
                    }
                }
            },
            "examples": {"application/json": bus_stops_example}
        },
        404: {"description": "Bus stop not found"}
    }
})
def all_bus_stops():
 
    return get_all_bus_stops()

@bus_route.route('/bus_stops/<string:stop_code>', methods=['GET'])
@swag_from({
    "tags": ["Bus"],
    "parameters": [
        {
            "name": "stop_code",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "Bus stop code"
        }
    ],
    "responses": {
        200: {
            "description": "Bus stop details",
            "schema":  bus_stops_schema,
            "examples": {"application/json": bus_stops_example}
        },
        404: {"description": "Bus stop not found"}
    }
})
def bus_stop_by_stop_code(stop_code):
  
    return get_bus_stop_by_stop_code(stop_code)

# @bus_route.route('/bus_trip', methods=['GET'])
# def all_bus_trips():
#     return get_all_bus_trip()

@bus_route.route('/bus_trip/<int:bus_trip_id>', methods=['GET'])
@swag_from({
    "tags": ["Bus"],
    "parameters": [
        {
            "name": "bus_trip_id",
            "in": "path",
            "type": "integer",
            "required": True,
            "description": "Bus trip ID"
        }
    ],
    "responses": {
        200: {
            "description": "Bus trip details",
            "schema": bus_trip_schema,
            "examples": {"application/json": bus_trips_get_example}
        },
        404: {"description": "Bus trip not found"}
    }
})
def bus_trip_by_id(bus_trip_id):
    return get_bus_trip_by_id(bus_trip_id)

# @bus_route.route('/bus_trip_segment', methods=['GET'])
# def all_bus_trip_segments():
#     return get_all_bus_trip_segment()

@bus_route.route('/bus_trip_segment/<int:bus_trip_id>', methods=['GET'])
@swag_from({
    "tags": ["Bus"],
    "parameters": [
        {
            "name": "bus_trip_id",
            "in": "path",
            "type": "integer",
            "required": True,
            "description": "Bus trip ID"
        }
    ],
    "responses": {
        200: {
            "description": "Bus trip segment details",
            "schema": bus_trip_segment_schema,
            "examples": {"application/json": bus_trip_segment_example}
        },
        404: {"description": "Bus trip segment not found"}
    }
})
def bus_trip_segment_by_id(bus_trip_id):

    return get_bus_trip_segment_by_id(bus_trip_id)


@bus_route.route('/bus_trips/end_area_codes', methods=['GET'])
@swag_from({
    "tags": ["Bus"],
    "responses": {
        200: {
            "description": "Mapping of end area names to codes",
            "schema": end_area_codes_schema,
            "examples": {"application/json": end_area_codes_example}
        }
    }
})
def bus_trips_end_area_codes():
    return get_unique_end_area_codes()

@bus_route.route('/bus_trip_segments/delay', methods=['GET'])
@swag_from({
    "tags": ["Bus"],
    "description": "Example: GET /bus_trip_segments/delay?start_stop=01013&end_stop=60121",
    "parameters": [
        {"name": "start_stop", "in": "query", "type": "string", "required": True, "description": "Origin stop code"},
        {"name": "end_stop", "in": "query", "type": "string", "required": True, "description": "Destination stop code"}
    ],
    "responses": {
        200: {
            "description": "Delay information for a bus trip segment",
            "schema": bus_delayed_schema,
            "examples": {"application/json": bus_trips_delayed_example}
        },
        400: {"description": "Missing required parameters"},
        404: {"description": "No matching bus trip segment found"}
    }
})
def bus_trip_segments_with_delay():
    return get_bus_trip_segment_delay()

@bus_route.route('/get_route', methods=['GET'])
@swag_from({
    "tags": ["Bus"],
    "description": "Example: GET start_address=pasir+ris+mall end_address=dunman+secondary+school time=07%3A00%3A00",
    "parameters": [
        {"name": "start_address", "in": "query", "type": "string", "required": True, "description": "Start address string"},
        {"name": "end_address", "in": "query", "type": "string", "required": True, "description": "End address string"},
        {"name": "date", "in": "query", "type": "string", "required": False, "description": "Date (optional)"},
        {"name": "time", "in": "query", "type": "string", "required": False, "description": "Time (optional)"}
    ],
    "responses": {
        200: {
            "description": "OneMap route plan (may include augmented bus leg durations)",
            "schema": get_route_schema,
            "examples": {"application/json": get_route_example}
        },
        400: {"description": "Missing start/end address"},
        504: {"description": "OneMap API timeout"}
    }
})
def onemap_route():
    return get_onemap_route()

@bus_route.route("/bus/route", methods=["GET"])
@swag_from({
    "tags": ["Bus"],
    "description": "Example: GET /bus/route?service=10",
    "parameters": [
        {"name": "service", "in": "query", "type": "string", "required": True, "description": "Bus service number"}
    ],
    "responses": {
        200: {
            "description": "Bus route geometry by service",
            "schema": bus_route_schema,
            "examples": {"application/json": bus_route_example}
        },
        400: {"description": "Missing service parameter"},
        404: {"description": "No route found for service"}
    }
})
def bus_routes():
    return get_bus_route()