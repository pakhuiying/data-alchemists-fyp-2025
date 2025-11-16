<!-- File: src/pages/PrivateTransport.vue -->
<script setup lang="ts">
import { ref, computed, nextTick } from 'vue'
import MapCanvasCar from '@/components/MapCanvasCar.vue'
import TravelTimeBarChart from '@/components/TravelTimeBarChart.vue'
import AddressDetailsPanel from '@/components/AddressDetailsPanel.vue'
import { getOnemapCarRoute } from '@/api/api'


const USE_MOCK = false

const MOCK_ROUTE_RESPONSE: any = {
  detour_comparison: {
    '10kph': {
      detour_route_time_sec: 430.0013991235393,
      difference_sec: 373.1853161106778,
      flooded_route_time_sec: 56.81608301286149,
    },
    '20kph': {
      detour_route_time_sec: 215.00069956176964,
      difference_sec: 163.26857579842152,
      flooded_route_time_sec: 51.7321237633481,
    },
    '45kph': {
      detour_route_time_sec: 95.5558664718976,
      difference_sec: 46.648164513834715,
      flooded_route_time_sec: 48.90770195806289,
    },
    '5kph': {
      detour_route_time_sec: 860.0027982470785,
      difference_sec: 793.0187967351903,
      flooded_route_time_sec: 66.98400151188827,
    },
    '72kph': {
      detour_route_time_sec: 59.722416544936,
      difference_sec: 11.662041128458682,
      flooded_route_time_sec: 48.06037541647732,
    },
    '81kph': {
      detour_route_time_sec: 53.08659248438756,
      difference_sec: 5.183129390426082,
      flooded_route_time_sec: 47.90346309396148,
    },
    '90kph': {
      detour_route_time_sec: 47.7779332359488,
      difference_sec: 0.0,
      flooded_route_time_sec: 47.7779332359488,
    },
  },
  detour_route_geometry: [
    [1.430354, 103.8354347],
    [1.4303601, 103.8352969],
    [1.4304762, 103.8352987],
    [1.4304695, 103.8354352],

    // slightly shifted north (lat + 0.003)
    [1.4334034, 103.8369211],
    [1.4333981, 103.8370463],
    [1.4331963, 103.8386916],
    [1.4331534, 103.8387956],

    [1.4271206, 103.8408406],
    [1.4270443, 103.8408288],
    [1.4260129, 103.8405884],
    [1.424475, 103.8399701],
    [1.4243985, 103.8398904],
    [1.4244727, 103.8398256],
  ],

  detour_total_travel_time_seconds: {
    '10kph': 430.0013991235393,
    '20kph': 215.00069956176964,
    '45kph': 95.5558664718976,
    '5kph': 860.0027982470785,
    '72kph': 59.722416544936,
    '81kph': 53.08659248438756,
    '90kph': 47.7779332359488,
  },
  estimated_total_travel_time_seconds: {
    '10kph': 56.81608301286149,
    '20kph': 51.7321237633481,
    '45kph': 48.90770195806289,
    '5kph': 66.98400151188827,
    '72kph': 48.06037541647732,
    '81kph': 47.90346309396148,
    '90kph': 47.7779332359488,
  },
  flooded_segments: [
    {
      geometry: 'LINESTRING (103.8354347 1.430354, 103.8352969 1.4303601)',
      length_m: 15.332918333136167,
      road_name: 'Yishun Avenue 5',
      travel_time_seconds: {
        '10kph': 5.51985059992902,
        '10kph_delay': 4.906533866603573,
        '20kph': 2.75992529996451,
        '20kph_delay': 2.1466085666390633,
        '45kph': 1.2266334666508933,
        '45kph_delay': 0.6133167333254467,
        '5kph': 11.03970119985804,
        '5kph_delay': 10.426384466532594,
        '72kph': 0.7666459166568084,
        '72kph_delay': 0.1533291833313617,
        '81kph': 0.681463037028274,
        '81kph_delay': 0.06814630370282737,
        '90kph': 0.6133167333254467,
        '90kph_delay': 0.0,
      },
    },
    {
      geometry: 'LINESTRING (103.8352969 1.4303601, 103.8352987 1.4304762)',
      length_m: 12.911299719715984,
      road_name: 'Yishun Avenue 2',
      travel_time_seconds: {
        '10kph': 4.648067899097755,
        '10kph_delay': 4.131615910309115,
        '20kph': 2.3240339495488773,
        '20kph_delay': 1.807581960760238,
        '45kph': 1.0329039775772788,
        '45kph_delay': 0.5164519887886394,
        '5kph': 9.29613579819551,
        '5kph_delay': 8.779683809406869,
        '72kph': 0.6455649859857993,
        '72kph_delay': 0.12911299719715985,
        '81kph': 0.5738355430984882,
        '81kph_delay': 0.05738355430984876,
        '90kph': 0.5164519887886394,
        '90kph_delay': 0.0,
      },
    },
  ],
  has_detour: true,
  normal_travel_time_seconds: 47.7779332359488,
  overall_route_status: 'flooded',
  route_geometry: [
    [
      1.430354, 
      103.8354347
    ],
    [
      1.4303601,
      103.8352969
    ],
    [
      1.4304762,
      103.8352987
    ],
    [
      1.4304695,
      103.8354352
    ],
    [
      1.4304034,
      103.8369211
    ],
    [
      1.4303981,
      103.8370463
    ],
    [
      1.4301963,
      103.8386916
    ],
    [
      1.4301534,
      103.8387956
    ],
    [
      1.4271206,
      103.8408406
    ],
    [
      1.4270443,
      103.8408288
    ],
    [
      1.4260129,
      103.8405884
    ],
    [
      1.424475,
      103.8399701
    ],
    [
      1.4243985,
      103.8398904
    ],
    [
      1.4244727,
      103.8398256
    ]
  ],
  total_delay_seconds: {
    '10kph': 9.03814977691269,
    '20kph': 3.954190527399301,
    '45kph': 1.1297687221140862,
    '5kph': 19.206068275939465,
    '72kph': 0.28244218052852155,
    '81kph': 0.12552985801267613,
    '90kph': 0.0,
  },
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

  const baselineSeconds = sec(
    r.normal_travel_time_seconds ?? r.estimated_total_travel_time_seconds?.['90kph']
  )
  if (baselineSeconds === undefined || baselineSeconds === null) {
    return null
  }

  const est = r.estimated_total_travel_time_seconds || {}
  const det = r.detour_total_travel_time_seconds || {}
  const hasDetour = !!r.has_detour

  const scenariosList: { scenario: string; duration_s: number }[] = []

  // baseline 行
  scenariosList.push({
    scenario: 'Baseline (90 km/h, no flood)',
    duration_s: baselineSeconds,
  })

  const labelMap: Record<string, string> = {
    '5kph': '5 km/h flooded',
    '10kph': '10 km/h flooded',
    '20kph': '20 km/h flooded',
    '45kph': '45 km/h flooded',
    '72kph': '72 km/h flooded',
    '81kph': '81 km/h flooded',
    '90kph': '90 km/h flooded',
  }

  for (const key of Object.keys(labelMap)) {
    const floodedT = sec(est[key])
    if (floodedT !== undefined && floodedT !== null) {
      scenariosList.push({
        scenario: labelMap[key],
        duration_s: floodedT,
      })
    }

    if (hasDetour) {
      const detourT = sec(det[key])
      if (detourT !== undefined && detourT !== null) {
        scenariosList.push({
          scenario: labelMap[key] + ' (detour)',
          duration_s: detourT,
        })
      }
    }
  }

  if (!scenariosList.length) return null

  return {
    duration_s: baselineSeconds,
    floodSummary: {
      baseline_s: baselineSeconds,
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
              <div class="text-[12px] text-gray-500 mt-1">
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
            <div class="mt-2 max-h-72 overflow-y-auto">
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
    </div>
  </div>
</template>