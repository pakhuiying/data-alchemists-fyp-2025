top_critical_segments_schema = {
    "type": "object",
    "properties": {
        "type": {
            "type": "string",
            "description": "GeoJSON type of the collection",
            "example": "FeatureCollection"
        },
        "properties": {
            "type": "object",
            "description": "Metadata for this collection",
            "properties": {
                "count": {
                    "type": "integer",
                    "description": "Number of features returned",
                    "example": 3
                },
                "metric": {
                    "type": "string",
                    "description": "Centrality metric used to rank segments",
                    "example": "betweenness"
                }
            }
        },
        "features": {
            "type": "array",
            "description": "List of road segments as GeoJSON Features",
            "items": {
                "type": "object",
                "properties": {
                    "type": {
                        "type": "string",
                        "description": "GeoJSON type of the feature",
                        "example": "Feature"
                    },
                    "geometry": {
                        "type": "object",
                        "description": "GeoJSON geometry of the road segment",
                        "properties": {
                            "type": {
                                "type": "string",
                                "description": "Geometry type",
                                "example": "LineString"
                            },
                            "coordinates": {
                                "type": "array",
                                "description": "Array of [longitude, latitude] coordinate pairs",
                                "items": {
                                    "type": "array",
                                    "items": {"type": "number"},
                                    "example": [103.8731976, 1.3228709]
                                }
                            }
                        }
                    },
                    "properties": {
                        "type": "object",
                        "description": "Centrality metrics and road attributes",
                        "properties": {
                            "u": {
                                "type": "integer",
                                "description": "Source node ID",
                                "example": 4726909201
                            },
                            "v": {
                                "type": "integer",
                                "description": "Target node ID",
                                "example": 139642645
                            },
                            "key": {
                                "type": "integer",
                                "description": "Edge key for multi-edges in the graph",
                                "example": 0
                            },
                            "road_name": {
                                "type": "string",
                                "description": "Name of the road segment",
                                "example": "Pan-Island Expressway"
                            },
                            "road_type": {
                                "type": "string",
                                "description": "Type of road / OSM highway classification",
                                "example": "motorway"
                            },
                            "length": {
                                "type": "number",
                                "format": "float",
                                "description": "Length of the road segment in meters",
                                "example": 574.6739
                            },
                            "betweenness": {
                                "type": "number",
                                "format": "float",
                                "description": "Edge betweenness centrality score",
                                "example": 0.1233913445
                            },
                            "norm_betweenness": {
                                "type": "number",
                                "format": "float",
                                "description": "Betweenness centrality normalized by max in result set",
                                "example": 1.0
                            },
                            "rank": {
                                "type": "integer",
                                "description": "Rank of this segment by centrality",
                                "example": 1
                            },
                            "is_critical": {
                                "type": "boolean",
                                "description": "Whether this segment is considered critical",
                                "example": True
                            }
                        },
                        "required": [
                            "u",
                            "v",
                            "key",
                            "road_name",
                            "road_type",
                            "length",
                            "betweenness",
                            "norm_betweenness",
                            "rank",
                            "is_critical"
                        ]
                    }
                },
                "required": ["type", "geometry", "properties"]
            }
        }
    },
    "required": ["type", "features"]
}


road_criticality_schema = {
    "type": "object",
    "description": "GeoJSON FeatureCollection of road segments with betweenness criticality.",
    "properties": {
        "type": {
            "type": "string",
            "description": "GeoJSON type of the collection",
            "example": "FeatureCollection"
        },
        "properties": {
            "type": "object",
            "description": "Metadata about this query and result set.",
            "properties": {
                "count": {
                    "type": "integer",
                    "description": "Number of segments returned in this result.",
                    "example": 82
                },
                "match": {
                    "type": "string",
                    "description": "Matching mode used for road_name (exact or contains).",
                    "example": "contains"
                },
                "metric": {
                    "type": "string",
                    "description": "Centrality metric used to score segments.",
                    "example": "betweenness"
                },
                "road_query": {
                    "type": "string",
                    "description": "The road_name query string used in the request.",
                    "example": "simei"
                }
            },
            "required": ["count", "match", "metric", "road_query"]
        },
        "features": {
            "type": "array",
            "description": "List of road segments as GeoJSON Features.",
            "items": {
                "type": "object",
                "properties": {
                    "type": {
                        "type": "string",
                        "description": "GeoJSON type of the feature",
                        "example": "Feature"
                    },
                    "geometry": {
                        "type": "object",
                        "description": "GeoJSON geometry of the road segment.",
                        "properties": {
                            "type": {
                                "type": "string",
                                "description": "Geometry type.",
                                "example": "LineString"
                            },
                            "coordinates": {
                                "type": "array",
                                "description": "Array of [longitude, latitude] coordinate pairs.",
                                "items": {
                                    "type": "array",
                                    "items": {"type": "number"},
                                    "example": [103.9465521, 1.3420968]
                                }
                            }
                        },
                        "required": ["type", "coordinates"]
                    },
                    "properties": {
                        "type": "object",
                        "description": "Centrality metrics and road attributes for this segment.",
                        "properties": {
                            "u": {
                                "type": "integer",
                                "description": "Source node ID in the graph.",
                                "example": 242933217
                            },
                            "v": {
                                "type": "integer",
                                "description": "Target node ID in the graph.",
                                "example": 2619397803
                            },
                            "key": {
                                "type": "integer",
                                "description": "Edge key for multi-edges.",
                                "example": 0
                            },
                            "road_name": {
                                "type": "string",
                                "description": "Name of the road (or main road) for this segment.",
                                "example": "Simei Avenue"
                            },
                            "road_type": {
                                "type": "string",
                                "description": "OSM road classification.",
                                "example": "primary"
                            },
                            "length": {
                                "type": "number",
                                "format": "float",
                                "description": "Length of the road segment in meters.",
                                "example": 448.0652452205202
                            },
                            "betweenness": {
                                "type": "number",
                                "format": "float",
                                "description": (
                                    "Betweenness centrality score for this edge "
                                    "(higher means more important for network connectivity)."
                                ),
                                "example": 0.013764875069258779
                            },
                            "norm_betweenness": {
                                "type": "number",
                                "format": "float",
                                "description": (
                                    "Betweenness centrality normalized by the maximum value "
                                    "in this result set (0–1)."
                                ),
                                "example": 1.0
                            },
                            "rank": {
                                "type": "integer",
                                "description": "Rank of this segment in the sorted list (1 = most critical).",
                                "example": 1
                            },
                            "is_critical": {
                                "type": "boolean",
                                "description": "Whether this segment is marked as critical.",
                                "example": True
                            }
                        },
                        "required": [
                            "u", "v", "key",
                            "road_name", "road_type",
                            "length", "betweenness",
                            "norm_betweenness", "rank",
                            "is_critical"
                        ]
                    }
                },
                "required": ["type", "geometry", "properties"]
            }
        }
    },
    "required": ["type", "properties", "features"]
}