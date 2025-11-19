top_critical_segment_example= {
  "type": "FeatureCollection",
  "properties": {
    "count": 1,
    "metric": "betweenness"
  },
  "features": [
    {
      "type": "Feature",
      "properties": {
        "u": 4726909201,
        "v": 139642645,
        "key": 0,
        "road_name": "Pan-Island Expressway",
        "road_type": "motorway",
        "length": 574.6739475884235,
        "betweenness": 0.12339134451803783,
        "norm_betweenness": 1.0,
        "rank": 1,
        "is_critical": True
      },
      "geometry": {
        "type": "LineString",
        "coordinates": [
          [103.8731976, 1.3228709],
          [103.8731271, 1.3229474],
          [103.8718905, 1.3245788],
          [103.8713716, 1.3252961],
          [103.8711791, 1.3255622],
          [103.8707583, 1.3260784],
          [103.8705419, 1.3263043],
          [103.8704383, 1.3264083],
          [103.8702489, 1.3265981],
          [103.8701297, 1.3267101],
          [103.8699451, 1.3268735]
        ]
      }
    }
  ]
}


road_criticality_example = {
    "type": "FeatureCollection",
    "properties": {
        "count": 3,
        "match": "contains",
        "metric": "betweenness",
        "road_query": "simei"
    },
    "features": [
        {
            "type": "Feature",
            "properties": {
                "betweenness": 0.013764875069258779,
                "is_critical": True,
                "key": 0,
                "length": 448.0652452205202,
                "norm_betweenness": 1.0,
                "rank": 1,
                "road_name": "Simei Avenue",
                "road_type": "primary",
                "u": 242933217,
                "v": 2619397803
            },
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [103.9465521, 1.3420968],
                    [103.9474058, 1.3410743],
                    [103.9475603, 1.3408933],
                    [103.9482501, 1.340085],
                    [103.94867, 1.3395915],
                    [103.9488555, 1.3393317],
                    [103.9489447, 1.3392216],
                    [103.9491283, 1.3389991]
                ]
            }
        },
        {
            "type": "Feature",
            "properties": {
                "betweenness": 0.013413178796520838,
                "is_critical": True,
                "key": 0,
                "length": 15.213610349231,
                "norm_betweenness": 0.9744497301306143,
                "rank": 2,
                "road_name": "Simei Avenue",
                "road_type": "primary",
                "u": 878256176,
                "v": 878256169
            },
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [103.9492633, 1.338615],
                    [103.9491752, 1.3387197]
                ]
            }
        },
        {
            "type": "Feature",
            "properties": {
                "betweenness": 0.013226084534729819,
                "is_critical": True,
                "key": 0,
                "length": 30.253636557333003,
                "norm_betweenness": 0.960857579032283,
                "rank": 3,
                "road_name": "Simei Avenue",
                "road_type": "primary",
                "u": 878256169,
                "v": 395220081
            },
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [103.9491752, 1.3387197],
                    [103.9491533, 1.338745],
                    [103.9489973, 1.3389256]
                ]
            }
        }
    ]
}