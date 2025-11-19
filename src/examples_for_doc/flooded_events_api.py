get_all_flood_events_example = [
    {
        "flood_id": 1,
        "flooded_location": "Yishun MRT",
        "date": "2014-03-20",
        "daily rainfall total (mm)": 45,
        "highest 30 min rainfall (mm)": 40.8,
        "highest 60 min rainfall (mm)": 44,
        "highest 120 min rainfall (mm)": 44.2,
        "mean_pr": 17.3950819672131,
        "latitude": 1.429525229,
        "longitude": 103.8349951,
        "geom": {
            "type": "Point",
            "coordinates": [103.8349951, 1.429525229],
            "crs": {
                "type": "name",
                "properties": {"name": "EPSG:4326"}
            }
        }
    },
    {
        "flood_id": 2,
        "flooded_location": "2 KAKI BUKIT ROAD 3",
        "date": "2014-04-04",
        "daily rainfall total (mm)": 25,
        "highest 30 min rainfall (mm)": 21,
        "highest 60 min rainfall (mm)": 25,
        "highest 120 min rainfall (mm)": 25,
        "mean_pr": 7.99354838709677,
        "latitude": 1.337333619,
        "longitude": 103.9019432,
        "geom": {
            "type": "Point",
            "coordinates": [103.9019432, 1.337333619],
            "crs": {
                "type": "name",
                "properties": {"name": "EPSG:4326"}
            }
        }
    }
]


flood_event_by_id_example = [
    {
        "flood_id": 1,
        "road_name": "Yishun Avenue 2",
        "road_type": "primary",
        "length_m": 616.4873388504224,
        "geometry": "LINESTRING (103.8350704 1.4248212, 103.8350717 1.4248739, 103.8351006 1.4260113, ...)"
    },
    {
        "flood_id": 12,
        "road_name": "MacKenzie Road",
        "road_type": "residential",
        "length_m": 257.5635671396551,
        "geometry": "LINESTRING (103.8484492 1.3055518, 103.8483005 1.3056599, 103.8481111 1.3057976, ...)"
    }
]

flood_event_locations_example = [
    {
        "count": 13,
        "location": "21229",
        "latitude": 1.342064137,
        "longitude": 103.7160202,
        "road_length": 429.73680893532423,
        "time_20kmh_min": 1.29,
        "time_50kmh_min": 0.52,
        "time_travel_delay_min": 0.77
    },
    {
        "count": 6,
        "location": "PSC Building",
        "latitude": 1.328862581,
        "longitude": 103.7061887,
        "road_length": 226.04681299510216,
        "time_20kmh_min": 0.68,
        "time_50kmh_min": 0.27,
        "time_travel_delay_min": 0.41
    }
]
 

get_buses_affected_by_floods_example = {
    "results": [
        {
            "affected_bus_services": ["151", "154", "165", "52", "74"],
            "candidate_stops": [
                {
                    "distance_m": 7.49,
                    "stop_code": "17109",
                    "stop_lat": 1.31552714122807,
                    "stop_lon": 103.77218311911328,
                    "stop_name": "Opp Blk 352"
                },
                {
                    "distance_m": 14.62,
                    "stop_code": "17119",
                    "stop_lat": 1.31728446989719,
                    "stop_lon": 103.77193266319904,
                    "stop_name": "Opp Blk 343"
                }
            ],
            "flood_id": 188
        }
    ]
}


get_flood_events_by_date_range_example = [
    {
        "daily rainfall total (mm)": 116.2,
        "date": "Thu, 30 Apr 2020 00:00:00 GMT",
        "flood_id": 163,
        "flooded_location": "Upper Paya Lebar Road",
        "geom": "0101000020E61000007F6374E5D8F859409A4ECC29EA5CF53F",
        "geometry": "LINESTRING (103.8876971 1.3324664, 103.8883351 1.3329487, 103.8885668 1.3331203, 103.888676 1.3332495, 103.8887393 1.3334761, 103.888734 1.333705, 103.8886906 1.3339114, 103.8886155 1.3341665, 103.8882449 1.3351452, 103.8882144 1.335221, 103.8878412 1.3360758, 103.8877121 1.3365183)",
        "highest 120 min rainfall (mm)": 100.2,
        "highest 30 min rainfall (mm)": 55.0,
        "highest 60 min rainfall (mm)": 82.4,
        "latitude": 1.335184253,
        "length_m": 524.83,
        "longitude": 103.8882383,
        "mean_pr": 42.8,
        "road_name": "Upper Paya Lebar Road",
        "road_type": "motorway_link",
        "time_20kmh_min": 1.57,
        "time_50kmh_min": 0.63,
        "time_travel_delay_min": 0.94
    },
    {
        "daily rainfall total (mm)": 116.2,
        "date": "Thu, 30 Apr 2020 00:00:00 GMT",
        "flood_id": 164,
        "flooded_location": "Lorong Gambir",
        "geom": "0101000020E6100000661CD94B09F8594086BAFE131287F53F",
        "geometry": "LINESTRING (103.8753266 1.3459374, 103.8753439 1.3459026, 103.8754434 1.3457127, 103.8757305 1.3452728, 103.875769 1.3452186)",
        "highest 120 min rainfall (mm)": 100.2,
        "highest 30 min rainfall (mm)": 55.0,
        "highest 60 min rainfall (mm)": 82.4,
        "latitude": 1.345476225,
        "length_m": 93.96,
        "longitude": 103.8755674,
        "mean_pr": 42.8,
        "road_name": "Lorong Gambir",
        "road_type": "residential",
        "time_20kmh_min": 0.28,
        "time_50kmh_min": 0.11,
        "time_travel_delay_min": 0.17
    },
    {
        "daily rainfall total (mm)": 123.9,
        "date": "Thu, 30 Apr 2020 00:00:00 GMT",
        "flood_id": 165,
        "flooded_location": "50 Hougang Avenue 1",
        "geom": "0101000020E6100000C2E8A859D6F859402BFF8A97CFC3F53F",
        "geometry": "LINESTRING (103.8884286 1.3601609, 103.8884072 1.3603979, 103.8883903 1.3605313, 103.8883796 1.3606533)",
        "highest 120 min rainfall (mm)": 0.0,
        "highest 30 min rainfall (mm)": 0.0,
        "highest 60 min rainfall (mm)": 0.0,
        "latitude": 1.360305397,
        "length_m": 55.03,
        "longitude": 103.8880829,
        "mean_pr": 42.8,
        "road_name": "Hougang Avenue 1",
        "road_type": "secondary",
        "time_20kmh_min": 0.17,
        "time_50kmh_min": 0.07,
        "time_travel_delay_min": 0.1
    },
    {
        "daily rainfall total (mm)": 62.8,
        "date": "Thu, 30 Apr 2020 00:00:00 GMT",
        "flood_id": 166,
        "flooded_location": "Serangoon Avenue 2",
        "geom": "0101000020E6100000CC43A67C88F75940E3C0DED673A8F53F",
        "geometry": "LINESTRING (103.8697879 1.3514979, 103.8697247 1.3515293, 103.8694516 1.3516657, 103.8689974 1.3518902, 103.8688415 1.3519779, 103.86869 1.3521009, 103.8686046 1.3521846, 103.8684578 1.3523609, 103.8683299 1.3525627, 103.868283 1.3526673, 103.86825 1.3527698, 103.8681916 1.3530087, 103.86816 1.353136, 103.8681396 1.3532183, 103.8681185 1.3533032, 103.868051 1.3535757, 103.8679839 1.3538219, 103.867941 1.3540224, 103.867929 1.3540838, 103.8678896 1.3543036, 103.8678646 1.3544785, 103.8678505 1.3546055, 103.8678165 1.3549197)",
        "highest 120 min rainfall (mm)": 61.8,
        "highest 30 min rainfall (mm)": 40.2,
        "highest 60 min rainfall (mm)": 57.6,
        "latitude": 1.353626098,
        "length_m": 474.03,
        "longitude": 103.8677055,
        "mean_pr": 42.8,
        "road_name": "Serangoon Avenue 2",
        "road_type": "secondary",
        "time_20kmh_min": 1.42,
        "time_50kmh_min": 0.57,
        "time_travel_delay_min": 0.85
    },
    {
        "daily rainfall total (mm)": 116.2,
        "date": "Thu, 30 Apr 2020 00:00:00 GMT",
        "flood_id": 167,
        "flooded_location": "Lichi Avenue",
        "geom": "0101000020E610000029CDE67118F8594025ACD4869F54F53F",
        "geometry": "LINESTRING (103.8766146 1.3331791, 103.8763816 1.333105, 103.8759694 1.3329673)",
        "highest 120 min rainfall (mm)": 100.2,
        "highest 30 min rainfall (mm)": 55.0,
        "highest 60 min rainfall (mm)": 82.4,
        "latitude": 1.333159949,
        "length_m": 75.49,
        "longitude": 103.876492,
        "mean_pr": 42.8,
        "road_name": "Lichi Avenue",
        "road_type": "residential",
        "time_20kmh_min": 0.23,
        "time_50kmh_min": 0.09,
        "time_travel_delay_min": 0.14
    },
    {
        "daily rainfall total (mm)": 123.9,
        "date": "Thu, 30 Apr 2020 00:00:00 GMT",
        "flood_id": 168,
        "flooded_location": "Jalan Teliti",
        "geom": "0101000020E6100000519E1E80F9F85940F611748B2BC4F53F",
        "geometry": "LINESTRING (103.8910788 1.3604831, 103.88878 1.3602068, 103.8886099 1.3601871, 103.8885356 1.3601774)",
        "highest 120 min rainfall (mm)": 0.0,
        "highest 30 min rainfall (mm)": 0.0,
        "highest 60 min rainfall (mm)": 0.0,
        "latitude": 1.36039309,
        "length_m": 284.75,
        "longitude": 103.8902283,
        "mean_pr": 42.8,
        "road_name": "Jalan Teliti",
        "road_type": "residential",
        "time_20kmh_min": 0.85,
        "time_50kmh_min": 0.34,
        "time_travel_delay_min": 0.51
    },
    {
        "daily rainfall total (mm)": 41.0,
        "date": "Fri, 22 May 2020 00:00:00 GMT",
        "flood_id": 169,
        "flooded_location": "Craig Road",
        "geom": "0101000020E610000030A990E1E7F559400CE0F3E41672F43F",
        "geometry": "LINESTRING (103.8424956 1.2776434, 103.8424772 1.2776421, 103.8424719 1.2776433, 103.8424677 1.2776457, 103.8424328 1.2776683, 103.842406 1.2776938, 103.842351 1.2777595, 103.8422508 1.2779398, 103.8421679 1.2780559, 103.8420984 1.2781618)",
        "highest 120 min rainfall (mm)": 39.8,
        "highest 30 min rainfall (mm)": 19.0,
        "highest 60 min rainfall (mm)": 24.4,
        "latitude": 1.277853865,
        "length_m": 74.34,
        "longitude": 103.8422779,
        "mean_pr": 38.3291666666667,
        "road_name": "Craig Road",
        "road_type": "residential",
        "time_20kmh_min": 0.22,
        "time_50kmh_min": 0.09,
        "time_travel_delay_min": 0.13
    },
    {
        "daily rainfall total (mm)": 91.6,
        "date": "Tue, 23 Jun 2020 00:00:00 GMT",
        "flood_id": 170,
        "flooded_location": "Jurong Town Hall Road",
        "geom": "0101000020E61000009E40D82956EF594029CA081CC74FF53F",
        "geometry": "LINESTRING (103.7401917 1.3315065, 103.7401098 1.3315615, 103.7392151 1.3321625, 103.7391456 1.3322075, 103.7390889 1.3322452, 103.7386421 1.3325487, 103.7381322 1.3329222, 103.7380265 1.3330014)",
        "highest 120 min rainfall (mm)": 57.0,
        "highest 30 min rainfall (mm)": 23.8,
        "highest 60 min rainfall (mm)": 40.8,
        "latitude": 1.331976995,
        "length_m": 292.57,
        "longitude": 103.739634,
        "mean_pr": 68.5571428571429,
        "road_name": "Jurong Town Hall Road",
        "road_type": "primary",
        "time_20kmh_min": 0.88,
        "time_50kmh_min": 0.35,
        "time_travel_delay_min": 0.53
    },
    {
        "daily rainfall total (mm)": 34.4,
        "date": "Tue, 23 Jun 2020 00:00:00 GMT",
        "flood_id": 171,
        "flooded_location": "Changi Fire Station",
        "geom": "0101000020E6100000449CF3F8E2FC5940DEBE83A9AA5BF53F",
        "geometry": "LINESTRING (103.9509211 1.3344645, 103.9512066 1.3346059, 103.9513927 1.3347016, 103.9517942 1.3348698)",
        "highest 120 min rainfall (mm)": 23.4,
        "highest 30 min rainfall (mm)": 14.0,
        "highest 60 min rainfall (mm)": 20.4,
        "latitude": 1.334879553,
        "length_m": 107.08,
        "longitude": 103.9513533,
        "mean_pr": 68.5571428571429,
        "road_name": "Upper Changi Road",
        "road_type": "tertiary",
        "time_20kmh_min": 0.32,
        "time_50kmh_min": 0.13,
        "time_travel_delay_min": 0.19
    },
    {
        "daily rainfall total (mm)": 113.4,
        "date": "Tue, 23 Jun 2020 00:00:00 GMT",
        "flood_id": 172,
        "flooded_location": "New Upper Changi Road",
        "geom": "0101000020E6100000748FB63B35FC5940E228FFAE5D2FF53F",
        "geometry": "LINESTRING (103.9407022 1.3252465, 103.9405735 1.3252205, 103.9405245 1.3252106, 103.9401652 1.325153, 103.9400397 1.3251358, 103.9398587 1.325109, 103.9391291 1.3250099, 103.9385832 1.3249464, 103.9379529 1.324869, 103.9372404 1.3247658)",
        "highest 120 min rainfall (mm)": 98.2,
        "highest 30 min rainfall (mm)": 47.2,
        "highest 60 min rainfall (mm)": 85.8,
        "latitude": 1.324063953,
        "length_m": 388.6,
        "longitude": 103.9407491,
        "mean_pr": 68.5571428571429,
        "road_name": "New Upper Changi Road",
        "road_type": "primary",
        "time_20kmh_min": 1.17,
        "time_50kmh_min": 0.47,
        "time_travel_delay_min": 0.7
    }
]


get_unique_flood_events_by_location_example = [
    {
        "flood_id": 1,
        "flooded_location": "Yishun MRT",
        "latitude": 1.429525229,
        "longitude": 103.8349951,
        "time_travel_delay_min": 1.11
    },
    {
        "flood_id": 2,
        "flooded_location": "2 KAKI BUKIT ROAD 3",
        "latitude": 1.337333619,
        "longitude": 103.9019432,
        "time_travel_delay_min": 0.52
    }
]


critical_segments_example = {
    "buffer_m": 50.0,
    "count_critical_segments": 6,
    "critical_segments": [
        {
            "centrality_score": 0.0216,
            "geometry": {"coordinates": [[29526.93464188134,33930.41467469784],[29539.922059690733,33953.126825279185],[29556.76007124428,33982.56195038662],[29560.210028111607,33988.37820809062],[29563.771297096668,33990.25800103967],[29568.523374289533,33991.186856895954],[29625.35933402046,33963.432892544704],[29635.698207414734,33957.937382418124],[29665.457248868952,33942.1364109711],[29669.88660538995,33939.78119292817]],"type":"LineString"},
            "length_m": 189.67,
            "road_name": ["Jalan Tan Tock Seng","Bassein Road"],
            "road_type": "residential"
        },
        {
            "centrality_score": 0.021144,
            "geometry": {"coordinates": [[29669.88660538995,33939.78119292817],[29674.182413239283,33937.54760650581],[29691.399032275473,33928.62431917182],[29729.237759258696,33909.030686010046],[29736.12665294469,33902.440466830194]],"type":"LineString"},
            "length_m": 76.42,
            "road_name": "Bassein Road",
            "road_type": "residential"
        },
        {
            "centrality_score": 0.021144,
            "geometry": {"coordinates": [[29669.88660538995,33939.78119292817],[29672.090122000176,33944.005166350864],[29684.910577060604,33969.216315010286],[29697.096691779047,33991.99481325103],[29705.49898022953,34009.10079774674]],"type":"LineString"},
            "length_m": 78.27,
            "road_name": "Akyab Road",
            "road_type": "residential"
        },
        {
            "centrality_score": 0.021144,
            "geometry": {"coordinates": [[29669.88660538995,33939.78119292817],[29665.457248868952,33942.1364109711],[29635.698207414734,33957.937382418124],[29625.35933402046,33963.432892544704],[29568.523374289533,33991.186856895954],[29563.771297096668,33990.25800103967],[29560.210028111607,33988.37820809062],[29556.76007124428,33982.56195038662],[29539.922059690733,33953.126825279185],[29526.93464188134,33930.41467469784]],"type":"LineString"},
            "length_m": 189.67,
            "road_name": ["Jalan Tan Tock Seng","Bassein Road"],
            "road_type": "residential"
        },
        {
            "centrality_score": 0.020712,
            "geometry": {"coordinates": [[29736.12665294469,33902.440466830194],[29729.237759258696,33909.030686010046],[29691.399032275473,33928.62431917182],[29674.182413239283,33937.54760650581],[29669.88660538995,33939.78119292817]],"type":"LineString"},
            "length_m": 76.42,
            "road_name": "Bassein Road",
            "road_type": "residential"
        },
        {
            "centrality_score": 0.020712,
            "geometry": {"coordinates": [[29705.49898022953,34009.10079774674],[29697.096691779047,33991.99481325103],[29684.910577060604,33969.216315010286],[29672.090122000176,33944.005166350864],[29669.88660538995,33939.78119292817]],"type":"LineString"},
            "length_m": 78.27,
            "road_name": "Akyab Road",
            "road_type": "residential"
        }
    ],
    "flood_id": 14,
    "flood_point": {"coordinates": [103.8480877,1.323315904], "type": "Point"}
}
    
