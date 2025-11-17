from src.database import supabase
from flask import jsonify, request, Blueprint
import googlemaps
import requests
from datetime import datetime
import os
from dotenv import load_dotenv
from src.utils.onemap_auth import get_valid_token
import osmnx as ox
from shapely import wkb
import geopandas as gpd
import pandas as pd
from pathlib import Path
from shapely.geometry import LineString
import networkx as nx
import copy

load_dotenv()
ROOT_DIR = Path(__file__).resolve().parents[2]
one_map_route = Blueprint('one_map_route', __name__)
ONEMAP_BASE_URL = "https://www.onemap.gov.sg/api/public/routingsvc/route"
gmaps = googlemaps.Client(os.getenv("GOOGLE_MAPS_API_KEY"))
G = ox.load_graphml(ROOT_DIR/"SG_car_network.graphml")
flood_events_df = pd.read_csv(ROOT_DIR/"flood_events_rows.csv")

flood_events_df['geom_parsed'] = flood_events_df['geom'].apply(
    lambda g: wkb.loads(bytes.fromhex(g))
)


flood_buffers = gpd.GeoSeries(flood_events_df['geom_parsed']).buffer(0.00090)

# def get_all_car_trips_flooded():
#     response = supabase.table('car_trips_flooded').select('*').execute()
#     if not response.data:  
#         return jsonify({"message": "No records found"}), 404

#     return jsonify(response.data), 200

# def get_car_trip_flooded_by_id():
#     car_trip_ids_param = request.args.get('car_trip_ids')  
#     if not car_trip_ids_param:
#         return jsonify({'error': 'car_trip_ids parameter is required'}), 400

#     try:
#         car_trip_ids = [int(id.strip()) for id in car_trip_ids_param.split(',')]
#     except ValueError:
#         return jsonify({'error': 'car_trip_ids must be a comma-separated list of integers'}), 400
    
#     try:
#         response = supabase.table('car_trips_flooded').select('*').in_('car_trip_id', car_trip_ids).execute()
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

#     if not response.data or len(response.data) == 0:
#         return jsonify({'error': 'Trips not found'}), 404

#     return jsonify(response.data), 200

# def get_all_car_trips_dry():
#     response = supabase.table("car_trips_dry").select("*").execute()
#     if not response.data:  
#         return jsonify({"message": "No records found"}), 404

#     return jsonify(response.data), 200
    
# def get_all_car_trips_dry_by_id():
#     car_trip_ids_param = request.args.get('car_trip_ids')  
#     if not car_trip_ids_param:
#         return jsonify({'error': 'car_trip_ids parameter is required'}), 400

#     try:
#         car_trip_ids = [int(id.strip()) for id in car_trip_ids_param.split(',')]
#     except ValueError:
#         return jsonify({'error': 'car_trip_ids must be a comma-separated list of integers'}), 400
    
#     try:
#         response = supabase.table('car_trips_dry').select('*').in_('car_trip_id', car_trip_ids).execute()
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

#     if not response.data or len(response.data) == 0:
#         return jsonify({'error': 'Trips not found'}), 404

#     return jsonify(response.data), 200

def get_all_car_trips_by_id():
    car_trip_ids_param = request.args.get('car_trip_ids')  
    if not car_trip_ids_param:
        return jsonify({'error': 'car_trip_ids parameter is required'}), 400

    try:
        car_trip_ids = [int(id.strip()) for id in car_trip_ids_param.split(',')]
    except ValueError:
        return jsonify({'error': 'car_trip_ids must be a comma-separated list of integers'}), 400
    
    try:
        response = supabase.table('car_trips').select('*').in_('car_trip_id', car_trip_ids).execute()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    if not response.data or len(response.data) == 0:
        return jsonify({'error': 'Trips not found'}), 404

    return jsonify(response.data), 200

def compute_detour_route(G, node_route, flooded_segments):
    if not flooded_segments:
        return None  

    flooded_geoms = {seg["geometry"] for seg in flooded_segments}
    PENALTY_FACTOR = 1000
    
    def weight_function(u, v, data):
        geom = data.get("geometry")
        if geom and geom.wkt in flooded_geoms:
            return data.get("length", 1) * PENALTY_FACTOR
        return data.get("length", 1)
    
    try:
        orig_node = node_route[0]
        dest_node = node_route[-1]
        new_node_route = nx.shortest_path(G, orig_node, dest_node, weight=weight_function)
        return new_node_route
    except:
        return None

def extract_route_geometry(G, node_route):
    """Extract detailed route geometry from node route"""
    route_coords = []
    
    for u, v in zip(node_route[:-1], node_route[1:]):
        edge = G.get_edge_data(u, v, 0)
        if edge and 'geometry' in edge:
        
            geom = edge['geometry']
           
            route_coords.extend([(pt[1], pt[0]) for pt in geom.coords[:-1]])
        else:
            route_coords.append((G.nodes[u]['y'], G.nodes[u]['x']))
    
    route_coords.append((G.nodes[node_route[-1]]['y'], G.nodes[node_route[-1]]['x']))
    
    return route_coords

def get_car_route():
    start_address = request.args.get('start_address')
    end_address = request.args.get('end_address')

    if not start_address or not end_address:
        return jsonify({"error": "start_address and end_address are required"}), 400

    def geocode_address(address):
        result = gmaps.geocode(address)
        if not result:
            return None
        return {
            'lat': result[0]['geometry']['location']['lat'],
            'lon': result[0]['geometry']['location']['lng']
        }

    start = geocode_address(start_address)
    end = geocode_address(end_address)
    if not start or not end:
        return jsonify({"error": "Could not geocode one or both addresses"}), 404

    try:
        orig_node = ox.distance.nearest_nodes(G, start['lon'], start['lat'])
        dest_node = ox.distance.nearest_nodes(G, end['lon'], end['lat'])
        node_route = nx.shortest_path(G, orig_node, dest_node, weight="length")
    except:
        return jsonify({"error": "Could not compute route using GraphML"}), 500

    
    route_coords = extract_route_geometry(G, node_route)

    speeds = {
        "5kph": 5, "10kph": 10, "20kph": 20,
        "45kph": 45, "72kph": 72, "81kph": 81,
        "90kph": 90  # baseline
    }
    
    # Precompute speed in m/s
    speeds_mps = {label: speed * 1000 / 3600 for label, speed in speeds.items()}

    flooded_segments = []
    total_delay = {k: 0.0 for k in speeds.keys()}
    route_total_length_m = 0

    for u, v in zip(node_route[:-1], node_route[1:]):
        edge = G.get_edge_data(u, v, 0)
        if not edge or "length" not in edge:
            continue

        length_m = edge["length"]
        route_total_length_m += length_m

        geom = edge.get("geometry")
        if geom:
            geom = LineString([(pt[0], pt[1]) for pt in geom.coords])
        else:
            geom = LineString([(G.nodes[u]['x'], G.nodes[u]['y']),
                               (G.nodes[v]['x'], G.nodes[v]['y'])])

        flooded = any(geom.intersects(b) for b in flood_buffers)
        if flooded:
            delays = {label: length_m / speed_mps for label, speed_mps in speeds_mps.items()}
            normal = delays["90kph"]
            
            delays_with_suffix = {}
            for label in speeds.keys():
                delay = delays[label] - normal
                delays_with_suffix[label] = delays[label]
                delays_with_suffix[label + "_delay"] = delay
                total_delay[label] += delay

            flooded_segments.append({
                "road_name": edge.get("name", "Unnamed Road"),
                "geometry": geom.wkt,
                "length_m": length_m,
                "travel_time_seconds": delays_with_suffix
            })

    normal_time_sec = {
        "5kph":   route_total_length_m / speeds_mps["5kph"],
        "10kph":  route_total_length_m / speeds_mps["10kph"],
        "20kph":  route_total_length_m / speeds_mps["20kph"],
        "45kph":  route_total_length_m / speeds_mps["45kph"],
        "72kph":  route_total_length_m / speeds_mps["72kph"],
        "81kph":  route_total_length_m / speeds_mps["81kph"],
        "90kph":  route_total_length_m / speeds_mps["90kph"]
    }

    detour_node_route = compute_detour_route(G, node_route, flooded_segments)

    if detour_node_route:
        detour_coords = extract_route_geometry(G, detour_node_route)
        detour_length_m = sum(
            G.get_edge_data(u, v, 0).get("length", 0)
            for u, v in zip(detour_node_route[:-1], detour_node_route[1:])
        )
        detour_total_travel_time_seconds = {
            label: detour_length_m / speed_mps
            for label, speed_mps in speeds_mps.items()
        }
        has_detour = True
    else:
        detour_coords = None
        detour_total_travel_time_seconds = None
        has_detour = False

    detour_comparison = {}
    if has_detour:
        for label in speeds.keys():
            flooded_time = normal_time_sec[label] + total_delay[label]
            detour_time = detour_total_travel_time_seconds[label]
            detour_comparison[label] = {
                "flooded_route_time_sec": flooded_time,
                "detour_route_time_sec": detour_time,
                "difference_sec": detour_time - flooded_time
            }

    return jsonify({
        "route_geometry": route_coords,
        "overall_route_status": "flooded" if flooded_segments else "clear",
        "flooded_segments": flooded_segments,
        "total_delay_seconds": total_delay,
        "normal_travel_time_seconds": normal_time_sec,
        "has_detour": has_detour,
        "detour_route_geometry": detour_coords,
        "detour_total_travel_time_seconds": detour_total_travel_time_seconds,
        "detour_comparison": detour_comparison
    }), 200