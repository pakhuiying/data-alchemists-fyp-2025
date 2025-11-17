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


# ============================================================================
# INITIALIZATION - Load the unsimplified graph
# ============================================================================
# Option 1: If you need to recreate the graph (do this once)
def create_unsimplified_graph():
    """
    Run this once to create a new graph file with proper geometry
    """
    print("Creating unsimplified graph for Singapore...")
    G = ox.graph_from_place(
        "Singapore",
        network_type='drive',
        simplify=False  # Keep all nodes for accurate geometry
    )
    
    # Add speed and travel time data
    G = ox.add_edge_speeds(G)
    G = ox.add_edge_travel_times(G)
    
    # Save it
    ox.save_graphml(G, "singapore_drive_unsimplified.graphml")
    print("Graph saved to singapore_drive_unsimplified.graphml")
    return G

# Option 2: Load existing graph (use this in your Flask app)
# If the unsimplified graph doesn't exist yet, create it first
try:
    G = ox.load_graphml("singapore_drive_unsimplified.graphml")
    print("Loaded unsimplified graph")
except FileNotFoundError:
    print("Unsimplified graph not found, creating it now...")
    G = create_unsimplified_graph()

# Assuming you have flood_buffers defined elsewhere
# flood_buffers = [...]  # Your flood polygons

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def compute_detour_route(G, node_route, flooded_segments):
    """
    Compute alternative route avoiding flooded segments
    """
    if not flooded_segments:
        return None  

    flooded_geoms = {seg["geometry"] for seg in flooded_segments}
    PENALTY_FACTOR = 1000
    
    def weight_function(u, v, data):
        geom = data.get("geometry")
        if geom:
            # Convert geometry to WKT for comparison
            geom_wkt = geom.wkt if hasattr(geom, 'wkt') else str(geom)
            if geom_wkt in flooded_geoms:
                return data.get("length", 1) * PENALTY_FACTOR
        return data.get("length", 1)
    
    try:
        orig_node = node_route[0]
        dest_node = node_route[-1]
        new_node_route = nx.shortest_path(G, orig_node, dest_node, weight=weight_function)
        return new_node_route
    except:
        return None

def get_route_geometry(G, node_route):
    """
    Extract route geometry that properly follows roads.
    Handles both edges with detailed geometry and simple node-to-node edges.
    """
    route_coords = []
    
    for u, v in zip(node_route[:-1], node_route[1:]):
        edge = G.get_edge_data(u, v, 0)
        
        # Get geometry if it exists
        geom = edge.get("geometry")
        
        if geom and hasattr(geom, 'coords'):
            # Has detailed geometry - use it
            # Convert to (lat, lon) format
            coords = [(pt[1], pt[0]) for pt in geom.coords]
            # Add all points except the last one to avoid duplicates
            route_coords.extend(coords[:-1])
        else:
            # No detailed geometry - use node positions
            u_coord = (G.nodes[u]['y'], G.nodes[u]['x'])
            if not route_coords or route_coords[-1] != u_coord:
                route_coords.append(u_coord)
    
    # Add final node
    final_node = node_route[-1]
    route_coords.append((G.nodes[final_node]['y'], G.nodes[final_node]['x']))
    
    return route_coords

def get_edge_geometry(G, u, v):
    """
    Get the geometry of a specific edge as a LineString
    """
    edge = G.get_edge_data(u, v, 0)
    geom = edge.get("geometry")
    
    if geom:
        # Already a LineString
        if hasattr(geom, 'coords'):
            return LineString([(pt[0], pt[1]) for pt in geom.coords])
    
    # Create LineString from node positions
    return LineString([
        (G.nodes[u]['x'], G.nodes[u]['y']),
        (G.nodes[v]['x'], G.nodes[v]['y'])
    ])

# ============================================================================
# MAIN ENDPOINT
# ============================================================================

def get_car_route():
    """
    Main endpoint for route calculation with flood detection
    """
    start_address = request.args.get('start_address')
    end_address = request.args.get('end_address')

    if not start_address or not end_address:
        return jsonify({"error": "start_address and end_address are required"}), 400

    # Geocoding function
    def geocode_address(address):
        result = gmaps.geocode(address)
        if not result:
            return None
        return {
            'lat': result[0]['geometry']['location']['lat'],
            'lon': result[0]['geometry']['location']['lng']
        }

    # Geocode addresses
    start = geocode_address(start_address)
    end = geocode_address(end_address)
    
    if not start or not end:
        return jsonify({"error": "Could not geocode one or both addresses"}), 404

    # Find nearest nodes in the graph
    try:
        orig_node = ox.distance.nearest_nodes(G, start['lon'], start['lat'])
        dest_node = ox.distance.nearest_nodes(G, end['lon'], end['lat'])
        node_route = nx.shortest_path(G, orig_node, dest_node, weight="length")
    except Exception as e:
        return jsonify({"error": f"Could not compute route: {str(e)}"}), 500

    # Get proper route geometry
    route_coords = get_route_geometry(G, node_route)

    # Speed definitions
    speeds = {
        "5kph": 5, "10kph": 10, "20kph": 20,
        "45kph": 45, "72kph": 72, "81kph": 81,
        "90kph": 90  # baseline
    }
    
    # Precompute speed in m/s
    speeds_mps = {label: speed * 1000 / 3600 for label, speed in speeds.items()}

    # Analyze route for flooded segments
    flooded_segments = []
    total_delay = {k: 0.0 for k in speeds.keys()}
    route_total_length_m = 0

    for u, v in zip(node_route[:-1], node_route[1:]):
        edge = G.get_edge_data(u, v, 0)
        if not edge or "length" not in edge:
            continue

        length_m = edge["length"]
        route_total_length_m += length_m

        # Get edge geometry
        geom = get_edge_geometry(G, u, v)

        # Check if flooded
        flooded = any(geom.intersects(b) for b in flood_buffers)
        
        if flooded:
            # Calculate delays for each speed
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

    # Calculate normal travel times
    normal_time_sec = {
        label: route_total_length_m / speed_mps
        for label, speed_mps in speeds_mps.items()
    }

    # Compute detour route if there are flooded segments
    detour_node_route = compute_detour_route(G, node_route, flooded_segments)

    if detour_node_route:
        detour_coords = get_route_geometry(G, detour_node_route)
        
        # Calculate detour length
        detour_length_m = sum(
            G.get_edge_data(u, v, 0).get("length", 0)
            for u, v in zip(detour_node_route[:-1], detour_node_route[1:])
        )
        
        # Calculate detour travel times
        detour_total_travel_time_seconds = {
            label: detour_length_m / speed_mps
            for label, speed_mps in speeds_mps.items()
        }
        has_detour = True
    else:
        detour_coords = None
        detour_total_travel_time_seconds = None
        has_detour = False

    # Compare flooded route vs detour
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


# ============================================================================
# OPTIONAL: Diagnostic function to check route quality
# ============================================================================

def diagnose_route_geometry(G, node_route):
    """
    Check which edges might have geometry issues
    Returns list of problematic edges
    """
    problems = []
    
    for i, (u, v) in enumerate(zip(node_route[:-1], node_route[1:])):
        edge = G.get_edge_data(u, v, 0)
        
        has_geometry = edge.get("geometry") is not None
        highway_type = edge.get("highway", "unknown")
        length = edge.get("length", 0)
        
        # Check if edge geometry is just a straight line
        if has_geometry:
            geom = edge["geometry"]
            num_points = len(list(geom.coords)) if hasattr(geom, 'coords') else 2
        else:
            num_points = 2  # Just start and end
        
        # Suspicious: long edge with no intermediate points
        if num_points == 2 and length > 100:
            problems.append({
                "segment": i,
                "nodes": (u, v),
                "highway": highway_type,
                "length": length,
                "has_geometry": has_geometry,
                "num_points": num_points
            })
    
    return problems