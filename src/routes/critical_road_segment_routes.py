from flask import Blueprint
from flasgger import swag_from
from ..examples_for_doc.critical_road_examples import *
from ..examples_for_doc.critical_road_schemas import *
from src.controllers.critical_road_controller import (
    top_critical_segments, road_criticality)


critical_roads_route = Blueprint("critical_road_segments", __name__)

@critical_roads_route.route("/top_critical_segments", methods=["GET"])
@swag_from({
    
    "tags": ["Critical Road Segments"],
    "parameters": [
  {
    "name": "limit",
    "in": "query",
    "type": "integer",
    "required": False,
    "default": 50,
     "description": (
      "Maximum number of segments to return. \n"
      "Example: `/top_critical_segments?limit=3`"
  )
  }
    ],
    "responses": {
        200: {
            "description": "A list of top critical road segments",
            "schema": top_critical_segments_schema
        }
    }
})
def get_top_critical_segments():
    
    
    return top_critical_segments()

@critical_roads_route.route("/road_criticality", methods=["GET"])

@swag_from({
    "tags": ["Critical Road Segments"],
    "parameters": [
    {
        "name": "road_name",
        "in": "query",
        "type": "string",
        "required": True,
        "description": (
            "Name of the road to retrieve segments for.\n\n"
            "This parameter is required.\n"
            "Example usage:\n"
            "`/road_criticality?road_name=simei`"
        ),
        "example": "simei"
    }
                ],
    "responses": {
        200: {
            "description": "Road segments along the queried road with betweenness criticality.",
            "schema": road_criticality_schema,
            "examples": {"application/json": road_criticality_example}
        },
        400: {
            "description": "Missing or invalid parameters.",
            "schema": {
                "type": "object",
                "properties": {
                    "error": {"type": "string", "example": "road_name is required"}
                }
            }
        }
    }
})

def get_road_criticality():
    
    
    return road_criticality()
