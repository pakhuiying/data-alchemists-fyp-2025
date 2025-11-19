from flask import Blueprint
from src.controllers.flood_events_controller import get_all_flood_events, get_critical_road_segments_near_flood, get_flood_event_by_id, get_flood_events_by_location, get_buses_affected_by_floods, get_flood_events_by_date_range, get_unique_flood_events_by_location
from flasgger import swag_from
from ..examples_for_doc.flooded_events_api import *
from ..examples_for_doc.flooded_events_schemas import *
flood_events_route = Blueprint('flood_events_route', __name__)

@flood_events_route.route('/flood_events', methods=['GET'])

@swag_from({
    "tags": ["Flood Events"],
    "responses": {
        200: {
            "description": "List of flood event records",
            "schema": flood_events_schema,
            "examples": {"application/json": get_all_flood_events_example}
        },
        404: {
            "description": "No flood events found",
            "schema": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "example": "No records found"
                    }
                }
            }
        }
    }
})
def all_flood_events():
   
    return get_all_flood_events()

@flood_events_route.route('/flood_events/id/', methods=['GET'])
@swag_from({
    "tags": ["Flood Events"],
    "parameters": [
        {
            "name": "flood_event_ids",
            "in": "query",
            "required": True,
            "type": "string",
            "description": "Comma-separated list of flood event IDs"
        }
    ],
    "responses": {
        200: {
            "description": "Flood event road info for each flood_event_id",
            "schema": flood_event_by_id_schema,
            "examples": {"application/json": flood_event_by_id_example}
        },
        400: {
            "description": "Missing or invalid flood_event_ids query parameter",
            "schema": {
                "type": "object",
                "properties": {
                    "error": {"type": "string", "example": "flood_event_ids parameter is required"}
                }
            }
        },
        404: {
            "description": "No flood events found for given IDs",
            "schema": {
                "type": "object",
                "properties": {
                    "error": {"type": "string", "example": "Flood event(s) not found"}
                }
            }
        },
        500: {
            "description": "Internal server error",
            "schema": {
                "type": "object",
                "properties": {
                    "error": {"type": "string", "example": "Server error occurred"}
                }
            }
        }
    }
})

def flood_event_by_id():

    return get_flood_event_by_id()

@flood_events_route.route('/flood_events/location', methods=['GET'])
@swag_from({
    "tags": ["Flood Events"],   
    "responses": {
        200: {
            "description": "List of flood event locations with aggregated data",
            "schema": flood_event_location_schema,
            "examples": {"application/json": flood_event_locations_example }
        },
        404: {
            "description": "No flood event locations found",
            "schema": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "example": "No records found"
                    }
                }
            }
        }
    }})
def flood_event_by_location():
    return get_flood_events_by_location()

@flood_events_route.route('/get_buses_affected_by_floods', methods=['GET'])

@swag_from({
    "tags": ["Flood Events"],
    "parameters": [
        {
            "name": "flood_id",
            "in": "query",
            "required": True,
            "type": "string",
            "description": (
                "ID of the flood event to query affected buses for. \n"
                "Accepts a single ID or comma-separated list. Example: `/get_buses_affected_by_floods?flood_id=188`"
            )
        }
    ],
    "responses": {
        200: {
            "description": "Buses and candidate stops affected by the flood event",
            "schema": get_buses_affected_by_floods_schema,
            "examples": {"application/json": get_buses_affected_by_floods_example}
        },
        400: {
            "description": "Missing or invalid flood_id",
            "schema": {
                "type": "object",
                "properties": {
                    "error": {"type": "string", "example": "flood_id parameter is required"}
                }
            }
        }
    }
})
def get_buses_affected_by_floods_route():
    return get_buses_affected_by_floods()

@flood_events_route.route("/get_flood_events_by_date_range", methods=['GET'])
@swag_from({
    "tags": ["Flood Events"],
    "parameters": [
        {
            "name": "start_date",
            "in": "query",
            "required": True,
            "type": "string",
            "description": (
                "Start date (YYYY-MM-DD) for the range. \n"
                "Example: `/get_flood_events_by_date_range?start_date=2020-01-01&end_date=2020-07-07`"
            )
        },
        {
            "name": "end_date",
            "in": "query",
            "required": True,
            "type": "string",
            "description": "End date (YYYY-MM-DD) for the range"
        }
    ],
    "responses": {
        200: {
            "description": "List of flood events within the requested date range. If no events are found the endpoint returns a 200 with a message object.",
            "schema": get_flood_events_by_date_range_schema,
            "examples": {"application/json": get_flood_events_by_date_range_example}
        },
        400: {
            "description": "Missing or invalid date parameters",
            "schema": {"type": "object", "properties": {"error": {"type": "string", "example": "start_date and end_date parameters are required"}}}
        }
    }
})
def get_flood_events_by_date():
    return get_flood_events_by_date_range()

@flood_events_route.route("/critical-segments", methods=["GET"])
@swag_from({
    "tags": ["Flood Events"],
    "parameters": [
        {
            "name": "flood_id",
            "in": "query",
            "required": True,
            "type": "integer",
            "description": (
                "Flood event ID to find nearby critical segments. \n"
                "Example: `/critical-segments?flood_id=14`"
            )
        },
        {
            "name": "buffer_m",
            "in": "query",
            "required": False,
            "type": "number",
            "description": "Optional buffer in meters to search for critical segments (default provided by API)"
        }
    ],
    "responses": {
        200: {
            "description": "Critical road segments near the specified flood point",
            "schema": critical_segments_schema,
            "examples": {"application/json": critical_segments_example}
        },
        400: {
            "description": "Missing or invalid flood_id",
            "schema": {"type": "object", "properties": {"error": {"type": "string", "example": "flood_id parameter is required"}}}
        },
        404: {
            "description": "Flood not found",
            "schema": {"type": "object", "properties": {"error": {"type": "string", "example": "Flood 14 not found"}}}
        }
    }
})
def get_critical_segments_endpoint():
    return get_critical_road_segments_near_flood()

@flood_events_route.route("/unique-flood-events/location", methods=["GET"])
@swag_from({
    "tags": ["Flood Events"],
    "responses": {
        200: {
            "description": "List of unique flood event locations",
            "schema": get_unique_flood_events_by_location_schema,
            "examples": {"application/json": get_unique_flood_events_by_location_example}
        },
        404: {
            "description": "No flood events found or missing data",
            "schema": {"type": "object", "properties": {"error": {"type": "string", "example": "No flood events found or missing 'flooded_location' column"}}}
        }
    }
})
def unique_flood_events_by_location():
    return get_unique_flood_events_by_location()