from pathlib import Path
from src.database import supabase
from flask import jsonify, request, Blueprint
import osmnx as ox
import os
from collections import Counter
import pandas as pd
import json
from datetime import datetime
import requests
import math
from shapely import wkb
from dotenv import load_dotenv
from src.utils.onemap_auth import get_valid_token
import geopandas as gpd
from shapely import wkb
from shapely.geometry import LineString, Point, mapping
import pickle

# PROJECT_ROOT = Path(__file__).resolve().parents[2]

BETWEENNESS_PKL = "Gcar_edge_betweenness_centrality.pkl"
CLOSENESS_PKL = "Gcar_edge_closeness_centrality.pkl"
# BETWEENNESS_PKL = "../../Gcar_edge_betweenness_centrality.pkl"
# CLOSENESS_PKL   = "../../Gcar_edge_closeness_centrality.pkl"

# Lazy, in-process caches
_EDGES_WGS84 = None
_METRICS = {}

def _ensure_edges_loaded():
    global _EDGES_WGS84
    if _EDGES_WGS84 is not None:
        return
    # Use your global G (import from wherever you keep it)
    # e.g., from app_state import G
    from app import G  # <-- change to your actual module if needed
    edges = ox.graph_to_gdfs(G, nodes=False).reset_index()  # typically EPSG:4326 already
    # Normalize columns used in properties
    if "road_name" not in edges.columns:
        edges["road_name"] = edges.get("name").fillna("(unnamed)")
    if "road_type" not in edges.columns:
        edges["road_type"] = edges.get("highway")
    _EDGES_WGS84 = edges

def _load_metric(metric: str):
    """Load a centrality dict keyed by (u,v,key). Cached."""
    if metric in _METRICS:
        return _METRICS[metric]
    if metric == "betweenness":
        pkl_path = BETWEENNESS_PKL
    elif metric == "closeness":
        pkl_path = CLOSENESS_PKL
    else:
        raise ValueError("metric must be 'betweenness' or 'closeness'")
    with open(pkl_path, "rb") as f:
        data = pickle.load(f)
    _METRICS[metric] = data
    return data



def _ensure_edges_loaded():
    global _EDGES_WGS84
    if _EDGES_WGS84 is not None:
        return
    # Use your global G (import from wherever you keep it)
    # e.g., from app_state import G
    from app import G  # <-- change to your actual module if needed
    edges = ox.graph_to_gdfs(G, nodes=False).reset_index()  # typically EPSG:4326 already
    # Normalize columns used in properties
    if "road_name" not in edges.columns:
        edges["road_name"] = edges.get("name").fillna("(unnamed)")
    if "road_type" not in edges.columns:
        edges["road_type"] = edges.get("highway")
    _EDGES_WGS84 = edges

def _load_metric(metric: str):
    """Load a centrality dict keyed by (u,v,key). Cached."""
    if metric in _METRICS:
        return _METRICS[metric]
    if metric == "betweenness":
        pkl_path = BETWEENNESS_PKL
    elif metric == "closeness":
        pkl_path = CLOSENESS_PKL
    else:
        raise ValueError("metric must be 'betweenness' or 'closeness'")
    with open(pkl_path, "rb") as f:
        data = pickle.load(f)
    _METRICS[metric] = data
    return data

# @bp_critical.route("/top_critical_segments", methods=["GET"])
def top_critical_segments():
    """
    Returns a GeoJSON FeatureCollection of the top N (default 50) edges by centrality.
    Query params:
      - metric=betweenness|closeness (default: betweenness)
      - limit=int (default: 50, max: 1000)
      - bbox=minx,miny,maxx,maxy (optional, WGS84)
    """
    try:
        _ensure_edges_loaded()
        metric = request.args.get("metric", "betweenness").lower()
        limit = min(max(int(request.args.get("limit", 50)), 1), 1000)
        bbox = request.args.get("bbox", "").strip()
        
        metric_map = _load_metric(metric)
        gdf = _EDGES_WGS84.copy()

        # Optional bbox filter
        if bbox:
            try:
                minx, miny, maxx, maxy = map(float, bbox.split(","))
                gdf = gdf.clip_by_rect(minx, miny, maxx, maxy)
            except Exception:
                return jsonify({"error": "Invalid bbox. Use minx,miny,maxx,maxy"}), 400

        # Attach centrality
        gdf[metric] = gdf.apply(lambda r: float(metric_map.get((r["u"], r["v"], r["key"]), 0.0)), axis=1)

        if gdf.empty:
            return jsonify({
                "type": "FeatureCollection", "properties": {"metric": metric, "count": 0}, "features": []
            }), 200

        top = gdf.sort_values(metric, ascending=False).head(limit).copy()
        max_c = float(top[metric].max())
        top["norm_"+metric] = top[metric] / max_c if max_c > 0 else 0.0

        features = []
        for rank, (_, row) in enumerate(top.iterrows(), start=1):
            props = {
                "u": int(row["u"]), "v": int(row["v"]), "key": int(row["key"]),
                "road_name": row.get("road_name", "(unnamed)"),
                "road_type": row.get("road_type", "Unknown"),
                "length": float(row.get("length") or 0.0),
                metric: float(row[metric]),
                "norm_"+metric: float(row["norm_"+metric]),
                "rank": rank,
                "is_critical": True
            }
            features.append({
                "type": "Feature",
                "properties": props,
                "geometry": mapping(row["geometry"])
            })

        return jsonify({
            "type": "FeatureCollection",
            "properties": {"metric": metric, "count": len(features)},
            "features": features
        }), 200

    except FileNotFoundError:
        return jsonify({"error": f"Centrality file not found for '{metric}'"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ============================================================
# Endpoint 2: Road-specific Criticality by Betweenness
# ============================================================
# @bp_critical.route("/road_criticality", methods=["GET"])
def road_criticality():
    """
    Returns all segments of a given road with betweenness criticality.
    Query params:
      - road_name (required)
      - match=exact|contains (default: contains)
      - limit=int (default: 100, max: 2000)
      - bbox=minx,miny,maxx,maxy (optional, WGS84)
      - format=geojson|json (default: geojson)
    """
    try:
        _ensure_edges_loaded()
        bet_map = _load_metric("betweenness")

        road_name = (request.args.get("road_name") or "").strip()
        if not road_name:
            return jsonify({"error": "road_name is required"}), 400

        match_mode = (request.args.get("match") or "contains").lower()
        limit = min(max(int(request.args.get("limit", 100)), 1), 2000)
        out_fmt = (request.args.get("format") or "geojson").lower()

        gdf = _EDGES_WGS84.copy()

        # Optional bbox filter
        bbox = request.args.get("bbox", "").strip()
        if bbox:
            try:
                minx, miny, maxx, maxy = map(float, bbox.split(","))
                gdf = gdf.clip_by_rect(minx, miny, maxx, maxy)
            except Exception:
                return jsonify({"error": "Invalid bbox. Use minx,miny,maxx,maxy"}), 400

       # make sure everything is a string and no NAs survive
        rn = gdf["road_name"].astype("string").fillna("")

        if match_mode == "exact":
            # case-insensitive exact match
            mask = rn.str.casefold() == road_name.casefold()
        else:
            # substring match; ensure no NA in result
            mask = rn.str.contains(road_name, case=False, regex=False, na=False)

        # extra safety: if anything weird slipped through
        # mask = mask.fillna(False)

        sel = gdf.loc[mask].copy()

        # Attach betweenness
        sel["betweenness"] = sel.apply(lambda r: float(bet_map.get((r["u"], r["v"], r["key"]), 0.0)), axis=1)
        sel = sel.sort_values("betweenness", ascending=False).head(limit)
        max_b = float(sel["betweenness"].max())
        sel["norm_betweenness"] = sel["betweenness"] / max_b if max_b > 0 else 0.0

        if out_fmt == "json":
            data = []
            for rank, (_, row) in enumerate(sel.iterrows(), start=1):
                data.append({
                    "u": int(row.u), "v": int(row.v), "key": int(row.key),
                    "road_name": row.road_name, "road_type": row.road_type,
                    "length_m": float(row.get("length") or 0.0),
                    "betweenness": float(row.betweenness),
                    "norm_betweenness": float(row.norm_betweenness),
                    "rank": rank,
                    "geometry": mapping(row.geometry)
                })
            return jsonify({
                "road_query": road_name, "match": match_mode,
                "metric": "betweenness", "count": len(data),
                "segments": data
            }), 200

        # GeoJSON for Mapbox
        features = []
        for rank, (_, row) in enumerate(sel.iterrows(), start=1):
            features.append({
                "type": "Feature",
                "properties": {
                    "u": int(row["u"]), "v": int(row["v"]), "key": int(row["key"]),
                    "road_name": row.road_name, "road_type": row.road_type,
                    "length": float(row.get("length") or 0.0),
                    "betweenness": float(row.betweenness),
                    "norm_betweenness": float(row.norm_betweenness),
                    "rank": rank,
                    "is_critical": True
                },
                "geometry": mapping(row.geometry)
            })

        return jsonify({
            "type": "FeatureCollection",
            "properties": {
                "road_query": road_name,
                "match": match_mode,
                "metric": "betweenness",
                "count": len(features)
            },
            "features": features
        }), 200

    except FileNotFoundError:
        return jsonify({"error": "Betweenness pickle not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500