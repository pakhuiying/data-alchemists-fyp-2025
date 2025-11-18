<script setup lang="ts">
import { ref, computed, nextTick } from 'vue'
import MapCanvasCar from '@/components/MapCanvasCar.vue'
import TravelTimeBarChart from '@/components/TravelTimeBarChart.vue'
import AddressDetailsPanel from '@/components/AddressDetailsPanel.vue'
import TransportModeToggle from '@/components/TransportModeToggle.vue'
import { getOnemapCarRoute } from '@/api/api'

const USE_MOCK = false
const MOCK_ROUTE_RESPONSE: any = {}

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

/* ───────────────────── Helpers: geometry & distance ───────────────────── */

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
    // WKT is lon lat → convert to [lat, lon]
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

/* Distance helpers (lat/lon in degrees) */

function haversineMeters(lat1: number, lon1: number, lat2: number, lon2: number): number {
  const R = 6371000 // metres
  const toRad = (deg: number) => (deg * Math.PI) / 180
  const dLat = toRad(lat2 - lat1)
  const dLon = toRad(lon2 - lon1)
  const a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(toRad(lat1)) *
      Math.cos(toRad(lat2)) *
      Math.sin(dLon / 2) *
      Math.sin(dLon / 2)
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a))
  return R * c
}

function polylineLengthMetersLatLon(path: [number, number][]): number {
  if (!Array.isArray(path) || path.length < 2) return 0
  let total = 0
  for (let i = 1; i < path.length; i++) {
    const [lat1, lon1] = path[i - 1]
    const [lat2, lon2] = path[i]
    total += haversineMeters(lat1, lon1, lat2, lon2)
  }
  return total
}

/* ───────────────────── Route list from API response ───────────────────── */

const allRoutesRaw = computed<any[]>(() => {
  const resp = routeResp.value
  if (!resp) return []

  const list: any[] = []

  // 45 km/h baseline from normal (non-flooded) travel time
  let baseline45: number | undefined
  const normal = resp.normal_travel_time_seconds
  if (normal && typeof normal === 'object' && normal['45kph'] != null) {
    const v = Number(normal['45kph'])
    if (Number.isFinite(v)) baseline45 = v
  }

  // 1) Flooded shortest path – Route 1
  if (Array.isArray(resp.route_geometry) && resp.route_geometry.length) {
    const distMeters = polylineLengthMetersLatLon(resp.route_geometry as [number, number][])

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
          resp.estimated_total_travel_time_seconds?.['45kph'] ??
          baseline45 ??
          0,
        total_distance: distMeters,
      },
    })
  }

  // 2) Detour route – Route 2
  if (resp.has_detour && Array.isArray(resp.detour_route_geometry) && resp.detour_route_geometry.length) {
    const distMeters = polylineLengthMetersLatLon(resp.detour_route_geometry as [number, number][])

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
          resp.detour_total_travel_time_seconds?.['45kph'] ??
          baseline45 ??
          0,
        total_distance: distMeters,
      },
    })
  }

  // 3) Fallback for “normal” Onemap-style responses
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

/* ───────────────────── Simplified routes for MapCanvasCar ───────────────────── */

const routes = computed(() => {
  const list = allRoutesRaw.value
  if (!list.length) return []

  const items = list.map((r: any, i: number) => {
    const lines = normalizeToPolylineList(r)

    // ── duration (seconds) ─────────────────────────────
    const rawDuration = Number(
      r?.summary?.duration_s ??
        r?.route_summary?.total_time ??
        r?.duration_s ??
        r?.duration ??
        r?.time_s ??
        r?.time
    )

    const duration_s: number | undefined =
      Number.isFinite(rawDuration) && rawDuration > 0 ? rawDuration : undefined

    // ── distance (meters) ─────────────────────────────
    let distance_m: number | undefined

    const rawDistance = Number(
      r?.summary?.distance_m ??
        r?.route_summary?.total_distance ??
        r?.distance_m ??
        r?.distance ??
        r?.length_m
    )

    if (Number.isFinite(rawDistance) && rawDistance > 0) {
      distance_m = rawDistance
    } else if (lines.length && lines[0].length > 1) {
      // fallback: compute from first polyline
      distance_m = polylineLengthMetersLatLon(lines[0])
    }
    // else leave distance_m as undefined

    return {
      idx: i,
      label: r?.summary?.label || r?.__label || (i === 0 ? 'Primary' : `Alternative ${i}`),
      duration_s,
      distance_m,
      polylines: lines,
      flooded_segments: normalizeFloodedSegments(r),
    }
  })

  const sel = Math.min(Math.max(selectedIdx.value ?? 0, 0), items.length - 1)
  const [picked] = items.splice(sel, 1)
  return [picked, ...items]
})

const selectedRouteRaw = computed(() => {
  const list = allRoutesRaw.value
  if (!list.length) return null
  const idx = Math.min(Math.max(selectedIdx.value ?? 0, 0), list.length - 1)
  return list[idx]
})


/* ───────────────────── Endpoints for A/B markers ───────────────────── */

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

/* ───────────────────── Travel time chart ───────────────────── */

const chartEntry = computed(() => {
  const r = routeResp.value as any
  if (!r) return null

  const selected = selectedRouteRaw.value as any | null
  const isDetour = selected?.__kind === 'detour'

  const scenariosList: { scenario: string; duration_s: number }[] = []
  let baseline45: number | undefined
  let showDelayBars = true

  if (isDetour) {
    // ───────── DETOUR: absolute times, no pink bars ─────────
    const detourTotals = r.detour_total_travel_time_seconds
    if (!detourTotals || typeof detourTotals !== 'object') return null

    baseline45 = sec(detourTotals['45kph'])
    if (baseline45 == null) return null

    const labelMap: Record<string, string> = {
      '5kph': '5 km/h (detour)',
      '10kph': '10 km/h (detour)',
      '20kph': '20 km/h (detour)',
    }
    const speeds: Array<'5kph' | '10kph' | '20kph'> = ['5kph', '10kph', '20kph']

    for (const key of speeds) {
      const t = sec(detourTotals[key])
      if (t == null) continue
      scenariosList.push({
        scenario: labelMap[key],
        duration_s: t,          // absolute detour travel time (seconds)
      })
    }

    showDelayBars = false
  } else {
    // ───────── FLOODED SHORTEST PATH: baseline + delay (pink) ─────────
    const normal = r.normal_travel_time_seconds
    if (!normal || typeof normal !== 'object') return null

    baseline45 = sec(normal['45kph'])
    if (baseline45 == null) return null

    const totalDelay = r.total_delay_seconds || {}
    const labelMap: Record<string, string> = {
      '5kph': '5 km/h (delay)',
      '10kph': '10 km/h (delay)',
      '20kph': '20 km/h (delay)',
    }
    const speeds: Array<'5kph' | '10kph' | '20kph'> = ['5kph', '10kph', '20kph']

    for (const key of speeds) {
      const delaySec = sec(totalDelay[key])
      if (delaySec == null) continue
      const totalTravelSec = baseline45 + delaySec
      scenariosList.push({
        scenario: labelMap[key],
        duration_s: totalTravelSec,   // baseline + extra delay
      })
    }

    showDelayBars = true
  }

  if (!scenariosList.length || baseline45 == null) return null

  return {
    duration_s: baseline45,
    floodSummary: {
      baseline_s: baseline45,
      scenarios: scenariosList,
    },
    showDelayBars,
  }
})

/* ───────────────────── Fetch route from backend ───────────────────── */

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
    <!-- Main grid -->
    <div class="h-[calc(100vh-2rem)] grid grid-cols-1 lg:grid-cols-12 gap-5">
      <!-- LEFT: controls + routes -->
      <aside class="col-span-12 lg:col-span-3 flex flex-col gap-4 min-h-0">
        <!-- Header / address panel -->
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

        <!-- Routes list -->
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
      </aside>

      <!-- RIGHT: chart + map (like Transit page) -->
      <section class="col-span-12 lg:col-span-9 min-h-0 flex flex-col">
        <div
          class="flex-1 rounded-2xl border border-gray-200 bg-white/80 shadow-sm backdrop-blur-sm p-4 flex flex-col min-h-0"
        >
          <!-- CHART CARD on top -->
          <div
            v-if="chartEntry"
            class="mb-4 rounded-xl border border-gray-200 bg-white shadow-sm p-4"
          >
            <div class="flex items-start justify-between flex-wrap gap-2 mb-3">
              <div>
                <div class="text-sm font-semibold text-gray-800 flex items-center gap-2">
                  <span
                    class="inline-flex items-center justify-center rounded bg-[#1e3a8a] text-white text-[10px] font-bold leading-none h-5 px-2 shadow"
                  >
                    ETA
                  </span>
                  <span>Travel Time Simulation</span>
                </div>
                <div class="text-[11px] text-gray-500 leading-snug mt-1">
                  Baseline vs additional delay under different flood speeds
                </div>
              </div>

              <div class="text-[10px] text-gray-400 leading-tight max-w-[180px]">
                Values are modelled. Actual driving time may vary with traffic and diversions.
              </div>
            </div>

            <div class="mt-2 h-72 overflow-y-auto">
              <TravelTimeBarChart :entry="chartEntry" title="Time Travel Simulation" />
            </div>
          </div>

          <!-- MAP CARD -->
          <div
            class="flex-1 min-h-0 overflow-hidden rounded-xl border-2 border-blue-200 shadow-inner bg-white relative"
          >
            <!-- top label bar -->
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

            <!-- actual map -->
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
      </section>
    </div>

    <!-- Transport mode switch at bottom (like Transit page) -->
    <TransportModeToggle />
  </div>
</template>
