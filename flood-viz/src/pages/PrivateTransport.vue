<!-- File: src/pages/PrivateTransport.vue -->
<script setup lang="ts">
import { ref, computed, nextTick } from 'vue'
import MapCanvasCar from '@/components/MapCanvasCar.vue'
import TravelTimeBarChart from '@/components/TravelTimeBarChart.vue'
import AddressDetailsPanel from '@/components/AddressDetailsPanel.vue'
import TransportModeToggle from '@/components/TransportModeToggle.vue'  
import { getOnemapCarRoute } from '@/api/api'


const USE_MOCK = false

const MOCK_ROUTE_RESPONSE: any = {
  "detour_comparison": {
    "10kph": {
      "detour_route_time_sec": 99993316.56507452,
      "difference_sec": 99892889.40243399,
      "flooded_route_time_sec": 100427.16264052676
    },
    "20kph": {
      "detour_route_time_sec": 49996658.28253726,
      "difference_sec": 49946261.0867822,
      "flooded_route_time_sec": 50397.19575506016
    },
    "45kph": {
      "detour_route_time_sec": 22220737.014461003,
      "difference_sec": 22198134.244753424,
      "flooded_route_time_sec": 22602.769707578722
    },
    "5kph": {
      "detour_route_time_sec": 199986633.13014904,
      "difference_sec": 199786146.03373757,
      "flooded_route_time_sec": 200487.09641145996
    },
    "72kph": {
      "detour_route_time_sec": 13887960.634038126,
      "difference_sec": 13873696.192144793,
      "flooded_route_time_sec": 14264.441893334288
    },
    "81kph": {
      "detour_route_time_sec": 12344853.896922778,
      "difference_sec": 12332133.58980986,
      "flooded_route_time_sec": 12720.307112918652
    },
    "90kph": {
      "detour_route_time_sec": 11110368.507230502,
      "difference_sec": 11098883.507941915,
      "flooded_route_time_sec": 11484.999288586143
    }
  },
  "detour_route_geometry": [
    [
      1.2976481,
      103.8532709
    ],
    [
      1.2984936,
      103.8539445
    ],
    [
      1.2991413,
      103.8531659
    ],
    [
      1.2997589,
      103.8523901
    ],
    [
      1.2998005,
      103.85234
    ],
    [
      1.3003614,
      103.8516212
    ],
    [
      1.3009856,
      103.8507754
    ],
    [
      1.3015323,
      103.8500249
    ],
    [
      1.3016585,
      103.8500298
    ],
    [
      1.3017664,
      103.8500362
    ],
    [
      1.3042268,
      103.8503359
    ],
    [
      1.3047524,
      103.8506967
    ],
    [
      1.3062304,
      103.8491727
    ],
    [
      1.3081271,
      103.8471998
    ],
    [
      1.3083079,
      103.8470452
    ],
    [
      1.308532,
      103.8468388
    ],
    [
      1.3087089,
      103.8466995
    ],
    [
      1.3103388,
      103.8447303
    ],
    [
      1.3104347,
      103.8444226
    ],
    [
      1.3105068,
      103.8441993
    ],
    [
      1.310591,
      103.8439104
    ],
    [
      1.3107801,
      103.8434921
    ],
    [
      1.3111973,
      103.8425774
    ],
    [
      1.3114021,
      103.8421704
    ],
    [
      1.3114891,
      103.8419805
    ],
    [
      1.3119099,
      103.8408111
    ],
    [
      1.3125343,
      103.8394482
    ],
    [
      1.3126126,
      103.839239
    ],
    [
      1.3125787,
      103.8391022
    ],
    [
      1.3125737,
      103.8390029
    ],
    [
      1.31266,
      103.8388059
    ],
    [
      1.3128436,
      103.8386853
    ],
    [
      1.3130024,
      103.8387115
    ],
    [
      1.3133062,
      103.8385896
    ],
    [
      1.3142712,
      103.8377573
    ],
    [
      1.3147575,
      103.8373462
    ],
    [
      1.3153092,
      103.8369445
    ],
    [
      1.3154506,
      103.8368282
    ],
    [
      1.3168789,
      103.8355342
    ],
    [
      1.3170779,
      103.8353593
    ],
    [
      1.3172182,
      103.8352303
    ],
    [
      1.3172916,
      103.8351582
    ],
    [
      1.3173568,
      103.8350218
    ],
    [
      1.3174118,
      103.8348536
    ],
    [
      1.3178129,
      103.833633
    ],
    [
      1.3179191,
      103.8333117
    ],
    [
      1.318722,
      103.8308655
    ],
    [
      1.3189078,
      103.830218
    ],
    [
      1.3190386,
      103.8298449
    ],
    [
      1.3194497,
      103.828619
    ],
    [
      1.3196353,
      103.8280883
    ],
    [
      1.319682,
      103.8277037
    ],
    [
      1.3198461,
      103.8271003
    ],
    [
      1.3200472,
      103.826486
    ],
    [
      1.3202816,
      103.8257777
    ],
    [
      1.3203696,
      103.8255401
    ],
    [
      1.3204387,
      103.8253398
    ],
    [
      1.3205427,
      103.8250411
    ],
    [
      1.3209416,
      103.8238065
    ],
    [
      1.3211769,
      103.8231027
    ],
    [
      1.3214032,
      103.822749
    ],
    [
      1.3216033,
      103.8220829
    ],
    [
      1.3217894,
      103.821429
    ],
    [
      1.3218918,
      103.8210326
    ],
    [
      1.3222083,
      103.8198195
    ],
    [
      1.3222251,
      103.8197532
    ],
    [
      1.3222575,
      103.8195999
    ],
    [
      1.3227025,
      103.8168248
    ],
    [
      1.3227924,
      103.8146926
    ],
    [
      1.3228082,
      103.8145973
    ],
    [
      1.3229372,
      103.8137018
    ],
    [
      1.3230207,
      103.8134366
    ],
    [
      1.3230618,
      103.8131374
    ],
    [
      1.3231047,
      103.8127553
    ],
    [
      1.3231327,
      103.8124243
    ],
    [
      1.3232055,
      103.8116553
    ],
    [
      1.3234072,
      103.8111458
    ],
    [
      1.3237818,
      103.8106199
    ],
    [
      1.3224245,
      103.8094355
    ],
    [
      1.3217657,
      103.8087097
    ],
    [
      1.3217747,
      103.8080924
    ],
    [
      1.3218003,
      103.8071339
    ],
    [
      1.3216137,
      103.8060768
    ],
    [
      1.3216505,
      103.8055628
    ],
    [
      1.3218817,
      103.8053453
    ],
    [
      1.3222498,
      103.8050144
    ],
    [
      1.322819,
      103.8039978
    ],
    [
      1.3224967,
      103.8021381
    ],
    [
      1.3226244,
      103.8009247
    ],
    [
      1.3226811,
      103.8005138
    ],
    [
      1.322733,
      103.8001375
    ],
    [
      1.3216975,
      103.796735
    ],
    [
      1.3216452,
      103.7965264
    ],
    [
      1.3221413,
      103.7959727
    ],
    [
      1.3233052,
      103.7945655
    ],
    [
      1.3242962,
      103.7933834
    ],
    [
      1.3249444,
      103.7926153
    ],
    [
      1.3254071,
      103.7928852
    ],
    [
      1.3259262,
      103.7931035
    ],
    [
      1.3261315,
      103.7931739
    ],
    [
      1.3271597,
      103.793525
    ],
    [
      1.3277143,
      103.7937896
    ],
    [
      1.3280435,
      103.7939667
    ],
    [
      1.3282494,
      103.7940881
    ],
    [
      1.3287022,
      103.7943631
    ],
    [
      1.3289944,
      103.7945177
    ],
    [
      1.3295829,
      103.7948201
    ],
    [
      1.3296488,
      103.7948055
    ],
    [
      1.3302956,
      103.795081
    ],
    [
      1.3311493,
      103.7945283
    ],
    [
      1.3318798,
      103.7945977
    ],
    [
      1.3319497,
      103.7943964
    ],
    [
      1.3320445,
      103.7941434
    ],
    [
      1.3325072,
      103.7928615
    ],
    [
      1.3327049,
      103.7922632
    ],
    [
      1.3330925,
      103.7909537
    ],
    [
      1.3336248,
      103.7893926
    ],
    [
      1.3338413,
      103.7887779
    ],
    [
      1.3346765,
      103.7864303
    ]
  ],
  "detour_total_travel_time_seconds": {
    "10kph": 99993316.56507452,
    "20kph": 49996658.28253726,
    "45kph": 22220737.014461003,
    "5kph": 199986633.13014904,
    "72kph": 13887960.634038126,
    "81kph": 12344853.896922778,
    "90kph": 11110368.507230502
  },
  "estimated_total_travel_time_seconds": {
    "10kph": 100427.16264052676,
    "20kph": 50397.19575506016,
    "45kph": 22602.769707578722,
    "5kph": 200487.09641145996,
    "72kph": 14264.441893334288,
    "81kph": 12720.307112918652,
    "90kph": 11484.999288586143
  },
  "flooded_segments": [
    {
      "geometry": "LINESTRING (103.8408111 1.3119099, 103.8407372 1.3119407, 103.8405714 1.312015, 103.840361 1.3121107, 103.8401165 1.3122227, 103.839945 1.3123022, 103.8398053 1.3123681, 103.8396338 1.3124479, 103.8394482 1.3125343)",
      "length_m": 166.66727647304762,
      "road_name": [
        "Monk's Hill Terrace",
        "Bukit Timah Road"
      ],
      "travel_time_seconds": {
        "10kph": 60.000219530297144,
        "10kph_delay": 53.33352847137524,
        "20kph": 30.000109765148572,
        "20kph_delay": 23.333418706226666,
        "45kph": 13.33338211784381,
        "45kph_delay": 6.666691058921905,
        "5kph": 120.00043906059429,
        "5kph_delay": 113.33374800167239,
        "72kph": 8.33336382365238,
        "72kph_delay": 1.6666727647304755,
        "81kph": 7.4074345099132275,
        "81kph_delay": 0.7407434509913227,
        "90kph": 6.666691058921905,
        "90kph_delay": 0.0
      }
    },
    {
      "geometry": "LINESTRING (103.8394482 1.3125343, 103.8394133 1.3125496, 103.839239 1.3126126)",
      "length_m": 24.84000162019868,
      "road_name": "Bukit Timah Road",
      "travel_time_seconds": {
        "10kph": 8.942400583271525,
        "10kph_delay": 7.948800518463577,
        "20kph": 4.471200291635762,
        "20kph_delay": 3.477600226827815,
        "45kph": 1.9872001296158945,
        "45kph_delay": 0.9936000648079473,
        "5kph": 17.88480116654305,
        "5kph_delay": 16.891201101735103,
        "72kph": 1.242000081009934,
        "72kph_delay": 0.24840001620198682,
        "81kph": 1.1040000720088303,
        "81kph_delay": 0.11040000720088305,
        "90kph": 0.9936000648079473,
        "90kph_delay": 0.0
      }
    },
    {
      "geometry": "LINESTRING (103.839239 1.3126126, 103.8391799 1.3125898, 103.8391022 1.3125787)",
      "length_m": 15.767427532265742,
      "road_name": "Newton Circus",
      "travel_time_seconds": {
        "10kph": 5.6762739116156675,
        "10kph_delay": 5.045576810325038,
        "20kph": 2.8381369558078338,
        "20kph_delay": 2.207439854517204,
        "45kph": 1.2613942025812594,
        "45kph_delay": 0.6306971012906297,
        "5kph": 11.352547823231335,
        "5kph_delay": 10.721850721940704,
        "72kph": 0.7883713766132872,
        "72kph_delay": 0.15767427532265743,
        "81kph": 0.7007745569895886,
        "81kph_delay": 0.07007745569895885,
        "90kph": 0.6306971012906297,
        "90kph_delay": 0.0
      }
    },
    {
      "geometry": "LINESTRING (103.8391022 1.3125787, 103.8390029 1.3125737)",
      "length_m": 11.052766712727971,
      "road_name": "Newton Circus",
      "travel_time_seconds": {
        "10kph": 3.9789960165820695,
        "10kph_delay": 3.5368853480729507,
        "20kph": 1.9894980082910347,
        "20kph_delay": 1.547387339781916,
        "45kph": 0.8842213370182377,
        "45kph_delay": 0.44211066850911884,
        "5kph": 7.957992033164139,
        "5kph_delay": 7.51588136465502,
        "72kph": 0.5526383356363985,
        "72kph_delay": 0.11052766712727968,
        "81kph": 0.49123407612124315,
        "81kph_delay": 0.049123407612124304,
        "90kph": 0.44211066850911884,
        "90kph_delay": 0.0
      }
    },
    {
      "geometry": "LINESTRING (103.8390029 1.3125737, 103.8389211 1.3125965, 103.8388551 1.3126266, 103.8388059 1.31266)",
      "length_m": 24.115615388859418,
      "road_name": "Newton Circus",
      "travel_time_seconds": {
        "10kph": 8.68162153998939,
        "10kph_delay": 7.716996924435013,
        "20kph": 4.340810769994695,
        "20kph_delay": 3.376186154440318,
        "45kph": 1.9292492311087535,
        "45kph_delay": 0.9646246155543767,
        "5kph": 17.36324307997878,
        "5kph_delay": 16.398618464424402,
        "72kph": 1.205780769442971,
        "72kph_delay": 0.24115615388859424,
        "81kph": 1.071805128393752,
        "81kph_delay": 0.10718051283937524,
        "90kph": 0.9646246155543767,
        "90kph_delay": 0.0
      }
    },
    {
      "geometry": "LINESTRING (103.8388059 1.31266, 103.8387334 1.3127389, 103.8386853 1.3128436)",
      "length_m": 24.724633362290994,
      "road_name": "Newton Circus",
      "travel_time_seconds": {
        "10kph": 8.900868010424759,
        "10kph_delay": 7.91188267593312,
        "20kph": 4.450434005212379,
        "20kph_delay": 3.4614486707207397,
        "45kph": 1.9779706689832794,
        "45kph_delay": 0.9889853344916397,
        "5kph": 17.801736020849518,
        "5kph_delay": 16.812750686357877,
        "72kph": 1.2362316681145498,
        "72kph_delay": 0.24724633362291004,
        "81kph": 1.0988725938795998,
        "81kph_delay": 0.10988725938796007,
        "90kph": 0.9889853344916397,
        "90kph_delay": 0.0
      }
    },
    {
      "geometry": "LINESTRING (103.8386853 1.3128436, 103.8386836 1.3129264, 103.8387115 1.3130024)",
      "length_m": 18.21088892541529,
      "road_name": "Newton Circus",
      "travel_time_seconds": {
        "10kph": 6.555920013149505,
        "10kph_delay": 5.827484456132893,
        "20kph": 3.2779600065747525,
        "20kph_delay": 2.549524449558141,
        "45kph": 1.4568711140332231,
        "45kph_delay": 0.7284355570166116,
        "5kph": 13.11184002629901,
        "5kph_delay": 12.383404469282398,
        "72kph": 0.9105444462707645,
        "72kph_delay": 0.18210888925415292,
        "81kph": 0.8093728411295684,
        "81kph_delay": 0.08093728411295686,
        "90kph": 0.7284355570166116,
        "90kph_delay": 0.0
      }
    },
    {
      "geometry": "LINESTRING (103.8387115 1.3130024, 103.8387131 1.3131105, 103.8386751 1.3131941, 103.8385896 1.3133062)",
      "length_m": 37.90749875092105,
      "road_name": "Unnamed Road",
      "travel_time_seconds": {
        "10kph": 13.64669955033158,
        "10kph_delay": 12.130399600294737,
        "20kph": 6.82334977516579,
        "20kph_delay": 5.3070498251289475,
        "45kph": 3.032599900073684,
        "45kph_delay": 1.516299950036842,
        "5kph": 27.29339910066316,
        "5kph_delay": 25.777099150626317,
        "72kph": 1.8953749375460525,
        "72kph_delay": 0.37907498750921054,
        "81kph": 1.6847777222631577,
        "81kph_delay": 0.16847777222631577,
        "90kph": 1.516299950036842,
        "90kph_delay": 0.0
      }
    },
    {
      "geometry": "LINESTRING (103.8385896 1.3133062, 103.8384967 1.3134143, 103.8384341 1.313484, 103.8379979 1.3139864, 103.8377573 1.3142712)",
      "length_m": 141.68940358514905,
      "road_name": "Bukit Timah Road",
      "travel_time_seconds": {
        "10kph": 51.00818529065366,
        "10kph_delay": 45.3406091472477,
        "20kph": 25.50409264532683,
        "20kph_delay": 19.836516501920865,
        "45kph": 11.335152286811924,
        "45kph_delay": 5.667576143405962,
        "5kph": 102.01637058130731,
        "5kph_delay": 96.34879443790135,
        "72kph": 7.084470179257453,
        "72kph_delay": 1.4168940358514908,
        "81kph": 6.297306826006625,
        "81kph_delay": 0.6297306826006626,
        "90kph": 5.667576143405962,
        "90kph_delay": 0.0
      }
    },
    {
      "geometry": "LINESTRING (103.8255401 1.3203696, 103.8253398 1.3204387)",
      "length_m": 23.554886983439566,
      "road_name": "Bukit Timah Road",
      "travel_time_seconds": {
        "10kph": 8.479759314038244,
        "10kph_delay": 7.537563834700661,
        "20kph": 4.239879657019122,
        "20kph_delay": 3.297684177681539,
        "45kph": 1.8843909586751653,
        "45kph_delay": 0.9421954793375826,
        "5kph": 16.959518628076488,
        "5kph_delay": 16.017323148738907,
        "72kph": 1.1777443491719783,
        "72kph_delay": 0.2355488698343957,
        "81kph": 1.0468838659306474,
        "81kph_delay": 0.10468838659306479,
        "90kph": 0.9421954793375826,
        "90kph_delay": 0.0
      }
    },
    {
      "geometry": "LINESTRING (103.8253398 1.3204387, 103.8252577 1.3204638, 103.8250411 1.3205427)",
      "length_m": 35.17090178359952,
      "road_name": "Bukit Timah Road",
      "travel_time_seconds": {
        "10kph": 12.661524642095827,
        "10kph_delay": 11.254688570751846,
        "20kph": 6.330762321047914,
        "20kph_delay": 4.923926249703933,
        "45kph": 2.8136721426879614,
        "45kph_delay": 1.4068360713439807,
        "5kph": 25.323049284191654,
        "5kph_delay": 23.916213212847673,
        "72kph": 1.7585450891799759,
        "72kph_delay": 0.3517090178359952,
        "81kph": 1.5631511903822009,
        "81kph_delay": 0.15631511903822015,
        "90kph": 1.4068360713439807,
        "90kph_delay": 0.0
      }
    },
    {
      "geometry": "LINESTRING (103.8250411 1.3205427, 103.8240549 1.3208586, 103.8238065 1.3209416)",
      "length_m": 144.23639078144222,
      "road_name": "Bukit Timah Road",
      "travel_time_seconds": {
        "10kph": 51.9251006813192,
        "10kph_delay": 46.15564505006151,
        "20kph": 25.9625503406596,
        "20kph_delay": 20.19309470940191,
        "45kph": 11.538911262515377,
        "45kph_delay": 5.769455631257689,
        "5kph": 103.8502013626384,
        "5kph_delay": 98.08074573138072,
        "72kph": 7.211819539072112,
        "72kph_delay": 1.442363907814423,
        "81kph": 6.410506256952988,
        "81kph_delay": 0.641050625695299,
        "90kph": 5.769455631257689,
        "90kph_delay": 0.0
      }
    },
    {
      "geometry": "LINESTRING (103.8238065 1.3209416, 103.8231027 1.3211769)",
      "length_m": 82.49725415049834,
      "road_name": "Bukit Timah Road",
      "travel_time_seconds": {
        "10kph": 29.699011494179402,
        "10kph_delay": 26.399121328159467,
        "20kph": 14.849505747089701,
        "20kph_delay": 11.549615581069768,
        "45kph": 6.599780332039867,
        "45kph_delay": 3.2998901660199333,
        "5kph": 59.398022988358804,
        "5kph_delay": 56.09813282233887,
        "72kph": 4.124862707524917,
        "72kph_delay": 0.8249725415049838,
        "81kph": 3.666544628911037,
        "81kph_delay": 0.3666544628911037,
        "90kph": 3.2998901660199333,
        "90kph_delay": 0.0
      }
    },
    {
      "geometry": "LINESTRING (103.8231027 1.3211769, 103.8228298 1.3213515, 103.822749 1.3214032)",
      "length_m": 46.68192387348684,
      "road_name": "Bukit Timah Road",
      "travel_time_seconds": {
        "10kph": 16.805492594455263,
        "10kph_delay": 14.93821563951579,
        "20kph": 8.402746297227631,
        "20kph_delay": 6.535469342288158,
        "45kph": 3.734553909878947,
        "45kph_delay": 1.8672769549394734,
        "5kph": 33.610985188910526,
        "5kph_delay": 31.743708233971052,
        "72kph": 2.334096193674342,
        "72kph_delay": 0.46681923873486864,
        "81kph": 2.0747521721549704,
        "81kph_delay": 0.207475217215497,
        "90kph": 1.8672769549394734,
        "90kph_delay": 0.0
      }
    },
    {
      "geometry": "LINESTRING (103.822749 1.3214032, 103.8220829 1.3216033)",
      "length_m": 77.31803088378078,
      "road_name": "Bukit Timah Road",
      "travel_time_seconds": {
        "10kph": 27.834491118161083,
        "10kph_delay": 24.74176988280985,
        "20kph": 13.917245559080541,
        "20kph_delay": 10.82452432372931,
        "45kph": 6.185442470702462,
        "45kph_delay": 3.092721235351231,
        "5kph": 55.668982236322165,
        "5kph_delay": 52.57626100097093,
        "72kph": 3.8659015441890388,
        "72kph_delay": 0.7731803088378078,
        "81kph": 3.4363569281680344,
        "81kph_delay": 0.3436356928168034,
        "90kph": 3.092721235351231,
        "90kph_delay": 0.0
      }
    },
    {
      "geometry": "LINESTRING (103.7887779 1.3338413, 103.7886844 1.3338644, 103.7882419 1.3340162, 103.7878789 1.334146, 103.7877266 1.3342013, 103.7873876 1.3343242, 103.7873435 1.3343402, 103.7867409 1.3345587, 103.7864303 1.3346765)",
      "length_m": 277069.8255740073,
      "road_name": "Bukit Timah Road",
      "travel_time_seconds": {
        "10kph": 99745.13720664263,
        "10kph_delay": 88662.34418368233,
        "20kph": 49872.56860332131,
        "20kph_delay": 38789.77558036102,
        "45kph": 22165.586045920583,
        "45kph_delay": 11082.793022960292,
        "5kph": 199490.27441328525,
        "5kph_delay": 188407.48139032497,
        "72kph": 13853.491278700365,
        "72kph_delay": 2770.6982557400734,
        "81kph": 12314.21446995588,
        "81kph_delay": 1231.4214469955878,
        "90kph": 11082.793022960292,
        "90kph_delay": 0.0
      }
    }
  ],
  "has_detour": true,
  "normal_travel_time_seconds": 11484.999288586143,
  "overall_route_status": "flooded",
  "route_geometry": [
    [
      1.2976481,
      103.8532709
    ],
    [
      1.2984936,
      103.8539445
    ],
    [
      1.2991413,
      103.8531659
    ],
    [
      1.2997589,
      103.8523901
    ],
    [
      1.2998005,
      103.85234
    ],
    [
      1.3003614,
      103.8516212
    ],
    [
      1.3009856,
      103.8507754
    ],
    [
      1.3015323,
      103.8500249
    ],
    [
      1.3016585,
      103.8500298
    ],
    [
      1.3017664,
      103.8500362
    ],
    [
      1.3042268,
      103.8503359
    ],
    [
      1.3047524,
      103.8506967
    ],
    [
      1.3062304,
      103.8491727
    ],
    [
      1.3081271,
      103.8471998
    ],
    [
      1.3083079,
      103.8470452
    ],
    [
      1.308532,
      103.8468388
    ],
    [
      1.3087089,
      103.8466995
    ],
    [
      1.3103388,
      103.8447303
    ],
    [
      1.3104347,
      103.8444226
    ],
    [
      1.3105068,
      103.8441993
    ],
    [
      1.310591,
      103.8439104
    ],
    [
      1.3107801,
      103.8434921
    ],
    [
      1.3111973,
      103.8425774
    ],
    [
      1.3114021,
      103.8421704
    ],
    [
      1.3114891,
      103.8419805
    ],
    [
      1.3119099,
      103.8408111
    ],
    [
      1.3125343,
      103.8394482
    ],
    [
      1.3126126,
      103.839239
    ],
    [
      1.3125787,
      103.8391022
    ],
    [
      1.3125737,
      103.8390029
    ],
    [
      1.31266,
      103.8388059
    ],
    [
      1.3128436,
      103.8386853
    ],
    [
      1.3130024,
      103.8387115
    ],
    [
      1.3133062,
      103.8385896
    ],
    [
      1.3142712,
      103.8377573
    ],
    [
      1.3147575,
      103.8373462
    ],
    [
      1.3153092,
      103.8369445
    ],
    [
      1.3154506,
      103.8368282
    ],
    [
      1.3168789,
      103.8355342
    ],
    [
      1.3170779,
      103.8353593
    ],
    [
      1.3172182,
      103.8352303
    ],
    [
      1.3172916,
      103.8351582
    ],
    [
      1.3173568,
      103.8350218
    ],
    [
      1.3174118,
      103.8348536
    ],
    [
      1.3178129,
      103.833633
    ],
    [
      1.3179191,
      103.8333117
    ],
    [
      1.318722,
      103.8308655
    ],
    [
      1.3189078,
      103.830218
    ],
    [
      1.3190386,
      103.8298449
    ],
    [
      1.3194497,
      103.828619
    ],
    [
      1.3196353,
      103.8280883
    ],
    [
      1.319682,
      103.8277037
    ],
    [
      1.3198461,
      103.8271003
    ],
    [
      1.3200472,
      103.826486
    ],
    [
      1.3202816,
      103.8257777
    ],
    [
      1.3203696,
      103.8255401
    ],
    [
      1.3204387,
      103.8253398
    ],
    [
      1.3205427,
      103.8250411
    ],
    [
      1.3209416,
      103.8238065
    ],
    [
      1.3211769,
      103.8231027
    ],
    [
      1.3214032,
      103.822749
    ],
    [
      1.3216033,
      103.8220829
    ],
    [
      1.3217894,
      103.821429
    ],
    [
      1.3218918,
      103.8210326
    ],
    [
      1.3222083,
      103.8198195
    ],
    [
      1.3222251,
      103.8197532
    ],
    [
      1.3222575,
      103.8195999
    ],
    [
      1.3227025,
      103.8168248
    ],
    [
      1.3227924,
      103.8146926
    ],
    [
      1.3228082,
      103.8145973
    ],
    [
      1.3229372,
      103.8137018
    ],
    [
      1.3230207,
      103.8134366
    ],
    [
      1.3230618,
      103.8131374
    ],
    [
      1.3231047,
      103.8127553
    ],
    [
      1.3231327,
      103.8124243
    ],
    [
      1.3232055,
      103.8116553
    ],
    [
      1.3234072,
      103.8111458
    ],
    [
      1.3237818,
      103.8106199
    ],
    [
      1.3224245,
      103.8094355
    ],
    [
      1.3217657,
      103.8087097
    ],
    [
      1.3217747,
      103.8080924
    ],
    [
      1.3218003,
      103.8071339
    ],
    [
      1.3216137,
      103.8060768
    ],
    [
      1.3216505,
      103.8055628
    ],
    [
      1.3218817,
      103.8053453
    ],
    [
      1.3222498,
      103.8050144
    ],
    [
      1.322819,
      103.8039978
    ],
    [
      1.3224967,
      103.8021381
    ],
    [
      1.3226244,
      103.8009247
    ],
    [
      1.3226811,
      103.8005138
    ],
    [
      1.322733,
      103.8001375
    ],
    [
      1.3216975,
      103.796735
    ],
    [
      1.3216452,
      103.7965264
    ],
    [
      1.3221413,
      103.7959727
    ],
    [
      1.3233052,
      103.7945655
    ],
    [
      1.3242962,
      103.7933834
    ],
    [
      1.3249444,
      103.7926153
    ],
    [
      1.3254071,
      103.7928852
    ],
    [
      1.3259262,
      103.7931035
    ],
    [
      1.3261315,
      103.7931739
    ],
    [
      1.3271597,
      103.793525
    ],
    [
      1.3277143,
      103.7937896
    ],
    [
      1.3280435,
      103.7939667
    ],
    [
      1.3282494,
      103.7940881
    ],
    [
      1.3287022,
      103.7943631
    ],
    [
      1.3289944,
      103.7945177
    ],
    [
      1.3295829,
      103.7948201
    ],
    [
      1.3296488,
      103.7948055
    ],
    [
      1.3302956,
      103.795081
    ],
    [
      1.3311493,
      103.7945283
    ],
    [
      1.3318798,
      103.7945977
    ],
    [
      1.3319497,
      103.7943964
    ],
    [
      1.3320445,
      103.7941434
    ],
    [
      1.3325072,
      103.7928615
    ],
    [
      1.3327049,
      103.7922632
    ],
    [
      1.3330925,
      103.7909537
    ],
    [
      1.3336248,
      103.7893926
    ],
    [
      1.3338413,
      103.7887779
    ],
    [
      1.3346765,
      103.7864303
    ]
  ],
  "total_delay_seconds": {
    "10kph": 88942.16335194062,
    "20kph": 38912.196466474015,
    "45kph": 11117.770418992577,
    "5kph": 189002.09712287382,
    "72kph": 2779.4426047481447,
    "81kph": 1235.3078243325083,
    "90kph": 0.0
  }
}


const startAddress = ref('143 Victoria St, Singapore 188019')
const endAddress = ref('961 Bukit Timah Rd, Singapore 588179')
const date = ref<string>('')  
const time = ref<string>('')  

const loading = ref(false)
const errorMsg = ref<string | null>(null)
const routeResp = ref<any | null>(null)
const selectedIdx = ref<number>(0)

const overallStatus = computed<'clear' | 'flooded' | undefined>(
  () => routeResp.value?.overall_route_status
)

function sec(n: any): number | undefined {
  const v = Number(n)
  return Number.isFinite(v) ? Math.round(v) : undefined
}


function decodePolyline(str: string): [number, number][] {
  let index = 0,
    lat = 0,
    lon = 0
  const out: [number, number][] = []
  while (index < str.length) {
    let b = 0,
      shift = 0,
      result = 0
    do {
      b = str.charCodeAt(index++) - 63
      result |= (b & 0x1f) << shift
      shift += 5
    } while (b >= 0x20)
    const dlat = (result & 1) ? ~(result >> 1) : (result >> 1)
    lat += dlat
    shift = 0
    result = 0
    do {
      b = str.charCodeAt(index++) - 63
      result |= (b & 0x1f) << shift
      shift += 5
    } while (b >= 0x20)
    const dlon = (result & 1) ? ~(result >> 1) : (result >> 1)
    lon += dlon
    out.push([lat / 1e5, lon / 1e5])
  }
  return out
}

function parseWktLineString(wkt: string): [number, number][] | null {
  const m = wkt.match(/LINESTRING\s*\((.+)\)/i)
  if (!m) return null
  const body = m[1].trim()
  const pairs = body.split(',').map((s) => s.trim())
  const coords: [number, number][] = []
  for (const p of pairs) {
    const [xStr, yStr] = p.split(/\s+/)
    const x = Number(xStr)
    const y = Number(yStr)
    if (!Number.isFinite(x) || !Number.isFinite(y)) continue
    coords.push([y, x])
  }
  return coords.length ? coords : null
}


function normalizeToPolylineList(route: any): [number, number][][] {
  if (!route) return []

  // 1) encoded polyline in `route_geometry` / `encoded`
  if (typeof route?.route_geometry === 'string') {
    return [decodePolyline(route.route_geometry)]
  }
  if (typeof route?.encoded === 'string') {
    return [decodePolyline(route.encoded)]
  }

  // 2) direct list: polyline / path / points / route_geometry
  const direct = route.polyline || route.path || route.points || route.route_geometry
  if (Array.isArray(direct) && direct.length && Array.isArray(direct[0])) {
    const guess = direct[0] as any
    const looksLonLat = Math.abs(guess[0]) > Math.abs(guess[1]) 

    const mapped: [number, number][] = direct.map((p: any): [number, number] => {
      const a = Number(p[0])
      const b = Number(p[1])
      return looksLonLat ? [b, a] : [a, b] 
    })
    return [mapped]
  }

  // 3) GeoJSON-like geometry
  const gj = route.geometry || route.geojson || route.shape
  if (gj && gj.type && Array.isArray(gj.coordinates)) {
    if (gj.type === 'LineString') {
      const arr: [number, number][] = gj.coordinates.map(
        ([lon, lat]: any): [number, number] => [Number(lat), Number(lon)]
      )
      return [arr]
    }

    if (gj.type === 'MultiLineString') {
      const multi: [number, number][][] = gj.coordinates.map((seg: any[]): [number, number][] =>
        seg.map(([lon, lat]: any): [number, number] => [Number(lat), Number(lon)])
      )
      return multi
    }
  }

  return []
}

function normalizeFloodedSegments(r: any): [number, number][][] | null {
  if (Array.isArray(r?.flooded_segments) && r.flooded_segments.length) {
    const segs: [number, number][][] = []

    for (const seg of r.flooded_segments) {
      if (Array.isArray(seg) && seg.length) {
        const first = seg[0]
        const looksLonLat = Array.isArray(first) && Math.abs(first[0]) > Math.abs(first[1])
        const mapped = seg.map(([a, b]: any) => (looksLonLat ? [b, a] : [a, b]))
        segs.push(mapped as [number, number][])
      }
    }

    if (!segs.length) {
      for (const seg of r.flooded_segments) {
        if (typeof seg?.geometry === 'string') {
          const coords = parseWktLineString(seg.geometry)
          if (coords && coords.length) {
            segs.push(coords)
          }
        }
      }
    }

    if (segs.length) return segs
  }

  if (typeof r?.flooded_geometry === 'string') return [decodePolyline(r.flooded_geometry)]
  return null
}

const allRoutesRaw = computed<any[]>(() => {
  const resp = routeResp.value
  if (!resp) return []

  const list: any[] = []

  // 1) flooded shortest path
  if (Array.isArray(resp.route_geometry)) {
    list.push({
      ...resp,
      __kind: 'flooded',
      __label: 'Flooded shortest path',
      
      route_geometry: resp.route_geometry,
      geometry: {
        type: 'LineString',
        coordinates: resp.route_geometry.map(
          ([lat, lon]: [number, number]) => [lon, lat]
        ),
      },
      route_summary: {
        total_time:
          resp.estimated_total_travel_time_seconds?.['90kph'] ??
          resp.normal_travel_time_seconds ??
          0,
        total_distance: 0,
      },
    })
  }

  // 2) detour route
  if (resp.has_detour && Array.isArray(resp.detour_route_geometry)) {
    list.push({
      ...resp,
      __kind: 'detour',
      __label: 'Detour (avoid flooded segments)',
      
      route_geometry: resp.detour_route_geometry,
      geometry: {
        type: 'LineString',
        coordinates: resp.detour_route_geometry.map(
          ([lat, lon]: [number, number]) => [lon, lat]
        ),
      },
      route_summary: {
        total_time:
          resp.detour_total_travel_time_seconds?.['90kph'] ??
          resp.normal_travel_time_seconds ??
          0,
        total_distance: 0,
      },
    })
  }

  if (!list.length) {
    const main = resp
    const phy = resp?.phyroute
    const alts = Array.isArray(resp?.alternativeroute) ? resp.alternativeroute : []

    if (main && (main.route_geometry || main.geometry || main.encoded)) {
      list.push({ ...main, __label: main?.subtitle || 'Fastest route' })
    }
    if (phy && (phy.route_geometry || phy.geometry || phy.encoded)) {
      list.push({ ...phy, __label: phy?.subtitle || 'Shortest distance' })
    }
    for (const a of alts) {
      if (a && (a.route_geometry || a.geometry || a.encoded)) {
        list.push({ ...a, __label: a?.subtitle || 'Alternative' })
      }
    }
  }

  return list
})

const routes = computed(() => {
  const list = allRoutesRaw.value
  if (!list.length) return []
  const items = list.map((r: any, i: number) => {
    const lines = normalizeToPolylineList(r)
    const duration_s = Number(
      r?.summary?.duration_s ??
        r?.route_summary?.total_time ??
        r?.duration_s ??
        r?.duration ??
        r?.time_s ??
        r?.time
    )
    const distance_m = Number(
      r?.summary?.distance_m ??
        r?.route_summary?.total_distance ??
        r?.distance_m ??
        r?.distance ??
        r?.length_m
    )
    return {
      idx: i,
      label: r?.summary?.label || r?.__label || (i === 0 ? 'Primary' : `Alternative ${i}`),
      duration_s: Number.isFinite(duration_s) ? duration_s : undefined,
      distance_m: Number.isFinite(distance_m) ? distance_m : undefined,
      polylines: lines,
      flooded_segments: normalizeFloodedSegments(r),
    }
  })
  const sel = Math.min(Math.max(selectedIdx.value ?? 0, 0), items.length - 1)
  const [picked] = items.splice(sel, 1)
  return [picked, ...items]
})

const selectedRouteRaw = computed<any | null>(() => {
  const list = allRoutesRaw.value
  if (!list.length) return null
  const idx = Math.min(Math.max(selectedIdx.value ?? 0, 0), list.length - 1)
  return list[idx]
})

const endpoints = computed(() => {
  const r0 = routes.value?.[0]
  if (!r0 || !r0.polylines?.length || !r0.polylines[0]?.length) {
    return { start: null, end: null }
  }
  const first = r0.polylines[0][0]
  const lastSeg = [...r0.polylines].reverse().find((seg) => seg && seg.length)
  const last = lastSeg ? lastSeg[lastSeg.length - 1] : null
  return {
    start: first ? { lat: first[0], lon: first[1] } : null,
    end: last ? { lat: last[0], lon: last[1] } : null,
  }
})


const chartEntry = computed(() => {
  const r = routeResp.value
  if (!r) return null

  const baselineTravelSeconds = sec(
    r.estimated_total_travel_time_seconds?.['90kph'] ??
      r.normal_travel_time_seconds
  )

  const totalDelay = r.total_delay_seconds || {}

  const scenariosList: { scenario: string; duration_s: number }[] = []

  // non-flooded baseline: delay = 0
  // scenariosList.push({
  //   scenario: 'No flood (baseline)',
  //   duration_s: 0,
  // })

  const speeds: Array<'5kph' | '10kph' | '20kph'> = ['5kph', '10kph', '20kph']
  const labelMap: Record<string, string> = {
    '5kph': '5 km/h',
    '10kph': '10 km/h',
    '20kph': '20 km/h',
  }

  for (const key of speeds) {
    const delaySec = sec(totalDelay[key])
    if (delaySec !== undefined && delaySec !== null) {
      scenariosList.push({
        scenario: `${labelMap[key]} (delay)`,
        duration_s: delaySec,
      })
    }
  }

  if (!scenariosList.length) return null

  return {
    duration_s: baselineTravelSeconds ?? 0,
    floodSummary: {
      baseline_s: baselineTravelSeconds ?? 0,
      scenarios: scenariosList,
    },
  }
})



async function fetchRoute() {
  errorMsg.value = null
  routeResp.value = null
  selectedIdx.value = 0

  if (!startAddress.value.trim() || !endAddress.value.trim()) {
    errorMsg.value = 'Please input start and end address.'
    return
  }

  loading.value = true
  try {
    const res: any = await getOnemapCarRoute({
      start_address: startAddress.value.trim(),
      end_address: endAddress.value.trim(),
      date: date.value || undefined,
      time: time.value || undefined,
    })
    if (USE_MOCK) {
      routeResp.value = MOCK_ROUTE_RESPONSE
    } else {
      if (!res || (!res.route_geometry && !res.detour_route_geometry)) {
        errorMsg.value = 'No route returned from server.'
      } else {
        routeResp.value = res
      }
    }


    await nextTick()
  } catch (e: any) {
    if (USE_MOCK) {
      routeResp.value = MOCK_ROUTE_RESPONSE
    } else {
      errorMsg.value = e?.message || 'Failed to fetch route.'
    }
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div
    class="min-h-screen bg-gradient-to-br from-[#f1f5f9] via-[#f8fafc] to-[#e2e8f0] text-gray-800 p-5"
  >
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-5 h-[calc(100vh-2rem)]">
      <!-- LEFT -->
      <div class="col-span-12 lg:col-span-3 flex flex-col gap-4">
        <div
          class="rounded-2xl border border-blue-200 bg-white/90 shadow-sm backdrop-blur-sm p-4"
        >
          <div class="flex items-start gap-3 mb-3">
            <div
              class="h-10 w-10 flex items-center justify-center rounded-xl bg-[#1e3a8a] text-white font-bold text-sm shadow"
            >
              🚗
            </div>
            <div>
              <div class="text-sm font-semibold text-gray-900">Flood-Viz Drive</div>
              <div class="text-[11px] text-gray-500 leading-snug">
                Simulate flood-affected travel times for private cars
              </div>
            </div>
          </div>

          <AddressDetailsPanel
            v-model:startAddress="startAddress"
            v-model:endAddress="endAddress"
            v-model:date="date"
            v-model:time="time"
            :loading="loading"
            :errorMsg="errorMsg"
            :overallStatus="overallStatus"
            @search="fetchRoute"
          />
        </div>

        <div
          v-if="allRoutesRaw.length"
          class="rounded-2xl border border-gray-200 bg-white/90 shadow-sm backdrop-blur-sm p-4"
        >
          <div class="flex items-center justify-between mb-2">
            <div class="text-sm font-semibold text-gray-800">
              Available Routes ({{ allRoutesRaw.length }})
            </div>
            <span
              v-if="overallStatus"
              class="text-xs px-2 py-0.5 rounded-full font-medium"
              :class="
                overallStatus === 'flooded'
                  ? 'bg-rose-100 text-rose-700'
                  : 'bg-emerald-100 text-emerald-700'
              "
            >
              {{ overallStatus }}
            </span>
          </div>

          <div class="space-y-3">
            <div
              v-for="(r, i) in allRoutesRaw"
              :key="i"
              class="border rounded-xl p-3 hover:border-blue-300 transition-all duration-200"
              :class="i === selectedIdx ? 'ring-2 ring-blue-200 bg-blue-50/40' : 'bg-white'"
            >
              <div class="flex items-center gap-2 text-sm text-gray-700">
                <span class="font-medium">
                  Route {{ i + 1 }}
                  <span v-if="r.__kind === 'detour'">· Detour</span>
                </span>
                <span class="text-gray-400">•</span>
                <span>
                  ~
                  {{
                    Math.round(
                      (r?.route_summary?.total_time ?? r?.summary?.duration_s ?? 0) / 60
                    )
                  }}
                  min
                </span>
                <span class="text-gray-400">•</span>
                <span>
                  {{
                    ((r?.route_summary?.total_distance ?? r?.summary?.distance_m ?? 0) /
                      1000)
                      .toFixed(2)
                  }}
                  km
                </span>
              </div>
              <div class="text-[11px] text-gray-500 mt-1">
                via
                {{
                  r?.viaRoute ||
                  (Array.isArray(r?.route_name) ? r.route_name.join(' → ') : '-')
                }}
              </div>

              <div class="mt-2 flex items-center gap-2">
                <button
                  class="inline-flex items-center gap-1 bg-[#0ea5e9] hover:bg-[#0284c7] text-white text-sm font-medium rounded-md px-3 py-1.5 transition"
                  @click="selectedIdx = i"
                  :disabled="selectedIdx === i"
                >
                  Show on Map
                </button>
              </div>
            </div>
          </div>
        </div>

         <!-- Travel time chart -->
          <div v-if="chartEntry" class="mb-4 border border-gray-200 bg-gray-50 rounded-xl p-4">
            <div class="flex items-center gap-2 mb-2 text-sm font-semibold text-gray-800">
              <span
                class="inline-flex items-center justify-center rounded bg-[#1e3a8a] text-white text-[10px] font-bold leading-none h-5 px-2 shadow"
              >
                ETA
              </span>
              <span>Travel Time Simulation</span>
            </div>

            <!-- scroll container -->
            <div class="mt-2 h-72 overflow-y-scroll">
              <TravelTimeBarChart :entry="chartEntry" title="Time Travel Simulation" />
            </div>

          </div>

      </div>

      <!-- RIGHT -->
      <div class="col-span-12 lg:col-span-9 flex flex-col gap-4">
        <div
          class="flex-1 rounded-2xl border border-gray-200 bg-white/80 shadow-sm backdrop-blur-sm p-4 flex flex-col"
        >
         

          <!-- Map -->
          <div class="flex-1 relative rounded-xl border-2 border-blue-200 overflow-hidden">
            <div
              class="absolute left-0 right-0 top-0 z-[5] flex items-center justify-between bg-gradient-to-r from-white/80 via-blue-50/60 to-white/80 text-[11px] text-gray-700 px-3 py-2 border-b border-blue-100"
            >
              <span class="font-medium text-[#1e3a8a] flex items-center gap-1">
                <span
                  class="inline-flex items-center justify-center rounded bg-[#1e3a8a] text-white text-[10px] font-bold leading-none h-5 px-2 shadow-sm"
                >
                  MAP
                </span>
                Car Route Simulation
              </span>
              <span class="text-gray-400">Zoom or click to inspect flooded segments</span>
            </div>

            <div class="absolute inset-0 pt-[34px]">
              <MapCanvasCar
                :routes="routes"
                :overall-status="overallStatus"
                :simulation="null"
                :endpoints="endpoints"
              />
            </div>
          </div>
        </div>
      </div>
	  <TransportModeToggle />
    </div>
  </div>
</template>
