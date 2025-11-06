from flask import Blueprint
from flasgger import swag_from
from src.controllers.critical_road_controller import (
    top_critical_segments, road_criticality)


critical_roads_route = Blueprint("critical_road_segments", __name__)

@critical_roads_route.route("/top_critical_segments", methods=["GET"])
def get_top_critical_segments():
    return top_critical_segments()

@critical_roads_route.route("/road_criticality", methods=["GET"])
def get_road_criticality():
    return road_criticality()
