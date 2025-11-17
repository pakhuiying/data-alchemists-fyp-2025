<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useAppStore } from '@/store/app'
import { getAllBusStops, getOneMapPtRoute } from '@/api/api'

const { mode = 'route' } = defineProps<{
  mode?: 'route' | 'itinerary'
}>()

const store = useAppStore()
const isItinerary = computed(() => mode === 'itinerary')

let currentRouteAbort: AbortController | null = null

function toLonLat(p: [number, number]) {
  const [lat, lon] = p
  return `${lon},${lat}`
}

/** Zoom the map to this direction’s geometry (roadPath preferred) */
function viewDirectionOnMap(d: {
  roadPath?: [number, number][],
  points?: [number, number][],
}) {
  const coords = (Array.isArray(d?.roadPath) && d.roadPath.length >= 2)
    ? d.roadPath
    : (Array.isArray(d?.points) && d.points.length >= 2)
      ? d.points
      : []

  if (!coords.length) return

  ;(store as any)._fitBoundsCoords = coords
  ;(store as any).setActiveTab?.('stops')
}

function clearMapRoutes() {
  try { currentRouteAbort?.abort() } catch {}
  currentRouteAbort = null

  ;(store as any).setServiceRouteOverlay?.(null)
  ;(store as any).clearColoredPolylines?.()
  ;(store as any).busTripOverlay = null
  ;(store as any)._fitBoundsCoords = null

  ;(store as any).setHighlightOrigin?.(null)
  ;(store as any).setHighlightDest?.(null)
  ;(store as any).highlightOrigin = null
  ;(store as any).highlightDest = null
  ;(store as any).highlightStop?.(null)

  ;(store as any).setOrigin?.(null)
  ;(store as any).setDestination?.(null)
  ;(store as any).setOriginStopCode?.(null)
  ;(store as any).setDestStopCode?.(null)

  originText.value = ''
  destText.value = ''

  store.clearSelection?.()
}

/* ───────────── OSRM helpers ───────────── */

type OsrmRoute = { path: [number, number][], distance_m: number, duration_s: number }

async function osrmRouteVia(pointsLatLon: [number, number][], signal?: AbortSignal): Promise<OsrmRoute | null> {
  if (!pointsLatLon || pointsLatLon.length < 2) return null
  const coords = pointsLatLon.map(([lat, lon]) => `${lon},${lat}`).join(';')
  const url = `https://router.project-osrm.org/route/v1/driving/${coords}?overview=full&geometries=geojson&steps=false`
  const r = await fetch(url, { signal })
  if (!r.ok) throw new Error(`OSRM ${r.status}`)
  const j = await r.json()
  const route = j?.routes?.[0]
  const line = route?.geometry?.coordinates
  if (!Array.isArray(line)) return null
  return {
    path: line.map(([lon, lat]: [number, number]) => [lat, lon]) as [number, number][],
    distance_m: Number(route?.distance ?? 0),
    duration_s: Number(route?.duration ?? 0),
  }
}

async function osrmRouteViaChunked(points: [number,number][], chunkSize = 90, signal?: AbortSignal): Promise<OsrmRoute | null> {
  if (points.length <= chunkSize) return await osrmRouteVia(points, signal)
  const pieces: OsrmRoute[] = []
  for (let i = 0; i < points.length - 1; i += (chunkSize - 1)) {
    const slice = points.slice(i, Math.min(points.length, i + chunkSize))
    if (slice.length >= 2) {
      const seg = await osrmRouteVia(slice, signal)
      if (seg && seg.path.length) pieces.push(seg)
    }
    await new Promise(r => setTimeout(r, 50))
  }
  if (!pieces.length) return null
  const joined: [number,number][] = []
  let dist = 0, dura = 0
  for (let i = 0; i < pieces.length; i++) {
    const seg = pieces[i]
    if (!seg?.path?.length) continue
    if (i === 0) joined.push(...seg.path)
    else joined.push(...seg.path.slice(1))
    dist += seg.distance_m
    dura += seg.duration_s
  }
  return { path: joined, distance_m: dist, duration_s: dura }
}

/* ───────────── Bus stops index (for drawing legs) ───────────── */

type StopIdx = { id: string; code: string; name: string; lat: number; lon: number; q: string }
const allStops = ref<StopIdx[]>([])
const loaded = ref(false)

const stopIndexByCode = computed<Record<string, { lat:number; lon:number; name:string }>>(() => {
  const m: Record<string, any> = {}
  for (const s of allStops.value) {
    if (s.code && Number.isFinite(s.lat) && Number.isFinite(s.lon)) {
      m[s.code] = { lat: s.lat, lon: s.lon, name: s.name }
    }
  }
  return m
})

function pickStopFields(s: any) {
  const lat = s.lat ?? s.latitude ?? s.stop_lat
  const lon = s.lon ?? s.lng ?? s.longitude ?? s.stop_lon
  const name = s.name ?? s.stop_name ?? s.description ?? s.stop_desc ?? ''
  const code = s.stop_code ?? s.code ?? s.id ?? s.stop_id ?? ''
  const id = s.stop_id ?? s.id
  return { lat: Number(lat), lon: Number(lon), name: String(name), code: String(code), id }
}

function norm(s: any) {
  return String(s ?? '')
    .toLowerCase()
    .normalize('NFKD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/\s+/g, ' ')
    .trim()
}

function latLonFromCode(code: string): [number, number] | null {
  const p = stopIndexByCode.value[code]
  if (!p) return null
  return [p.lat, p.lon]
}

/* ───────────── Itinerary + flood helpers ───────────── */

function toNumOrUndefined(val: unknown): number | undefined {
  if (typeof val === 'number' && Number.isFinite(val)) return val
  if (Array.isArray(val) && val.length && Number.isFinite(val[0] as any)) return Number(val[0])
  return undefined
}

function legIsFlooded(leg: any): boolean {
  if (!leg || leg.mode !== 'BUS') return false
  const flag = String(leg?.overall_bus_route_status || '').toLowerCase()
  if (flag === 'flooded') return true
  if (flag === 'clear') return false

  const base = toNumOrUndefined(leg.non_flooded_bus_duration)
  if (!Number.isFinite(base)) return false
  const candidates = [
    toNumOrUndefined(leg['5kmh_flooded_bus_duration']),
    toNumOrUndefined(leg['10kmh_flooded_bus_duration']),
    toNumOrUndefined(leg['20kmh_flooded_bus_duration']),
  ].filter((x): x is number => Number.isFinite(x as any))
  return candidates.some(v => v! > (base as number))
}

function summarizeFloodDurations(legs: any[]) {
  let baseline_s = 0
  let anyBaseline = false
  const map = new Map<string, number>()

  for (const leg of legs ?? []) {
    if (leg?.mode !== 'BUS') continue

    const base = toNumOrUndefined((leg as any).non_flooded_bus_duration)
    if (Number.isFinite(base)) {
      baseline_s += base!
      anyBaseline = true
    }

    const pairs: Array<[label: string, key: string]> = [
      ['5 km/h flooded',  '5kmh_flooded_bus_duration'],
      ['10 km/h flooded', '10kmh_flooded_bus_duration'],
      ['20 km/h flooded', '20kmh_flooded_bus_duration'],
    ]
    for (const [label, key] of pairs) {
      const v = toNumOrUndefined((leg as any)[key])
      if (Number.isFinite(v)) {
        map.set(label, (map.get(label) ?? 0) + (v as number))
      }
    }
  }

  return {
    baseline_s: anyBaseline ? baseline_s : undefined,
    scenarios: Array.from(map.entries()).map(([scenario, duration_s]) => ({ scenario, duration_s }))
      .sort((a,b) => a.duration_s - b.duration_s),
  }
}

function legStops(leg: any): string[] {
  if (!leg?.transitLeg || leg?.mode !== 'BUS') return []
  const arr: string[] = []
  const a = leg?.from?.stopCode && String(leg.from.stopCode)
  const b = leg?.to?.stopCode && String(leg.to.stopCode)
  if (a) arr.push(a)
  if (Array.isArray(leg?.intermediateStops)) {
    for (const st of leg.intermediateStops) {
      if (st?.stopCode) arr.push(String(st.stopCode))
    }
  }
  if (b) arr.push(b)
  return arr.filter((c, i) => i === 0 || c !== arr[i - 1])
}

function legStatus(leg: any): 'flooded' | 'clear' {
  const flag = String(leg?.overall_bus_route_status || '').toLowerCase()
  if (flag === 'flooded') return 'flooded'
  if (flag === 'clear') return 'clear'
  return legIsFlooded(leg) ? 'flooded' : 'clear'
}

function legChipStyle(leg: any) {
  const s = legStatus(leg)
  return s === 'flooded'
    ? { bg: '#fee2e2', text: '#b91c1c', ring: 'rgba(239,68,68,.25)' }
    : { bg: '#dbeafe', text: '#1d4ed8', ring: 'rgba(59,130,246,.25)' }
}

function routeLabel(leg: any) {
  return leg?.routeShortName || leg?.route || 'BUS'
}

/* colors for flooded vs clear polylines */
const BASE_COLOR = '#2563eb'
const FLOODED_COLOR = '#dc2626'

async function computeRoadPathForSegment(codes: string[]): Promise<OsrmRoute | null> {
  const points: [number,number][] = []
  for (const c of codes) {
    const p = stopIndexByCode.value[c]
    if (p) points.push([p.lat, p.lon])
  }
  if (points.length < 2) return null

  const estimatedLen = points.length * 24
  const useChunked = estimatedLen > 7000
  const res = useChunked
    ? await osrmRouteViaChunked(points, 90)
    : await osrmRouteVia(points).catch(() => osrmRouteViaChunked(points, 90))
  return res && res.path.length >= 2 ? res : null
}

async function buildColoredPolylinesFromItinerary(it: any) {
  const legs: any[] = Array.isArray(it?.legs) ? it.legs : []
  const busLegs = legs.filter(l => l?.mode === 'BUS')

  const polylines: Array<{ path: [number,number][], color: string, flooded: boolean }> = []
  const segments: Array<{ points: [number,number][], flooded: boolean }> = []

  for (const leg of busLegs) {
    const codes: string[] = []
    const a = leg?.from?.stopCode
    const b = leg?.to?.stopCode
    if (a) codes.push(String(a))
    const interm = Array.isArray(leg?.intermediateStops) ? leg.intermediateStops : []
    for (const st of interm) if (st?.stopCode) codes.push(String(st.stopCode))
    if (b && (!codes.length || codes[codes.length - 1] !== String(b))) codes.push(String(b))

    let path: [number,number][] | undefined
    if (codes.length >= 2) {
      const osrm = await computeRoadPathForSegment(codes)
      path = osrm?.path
    }
    if (!path || path.length < 2) {
      const pts = [a, b].map((c:string)=>latLonFromCode(String(c))).filter(Boolean) as [number,number][]
      if (pts.length >= 2) path = pts
    }
    if (!path || path.length < 2) continue

    const flooded = legIsFlooded(leg)
    const color = flooded ? FLOODED_COLOR : BASE_COLOR

    polylines.push({ path, color, flooded })
    segments.push({ points: path, flooded })
  }

  const stopCodes: string[] = []
  for (const leg of busLegs) {
    const a = leg?.from?.stopCode
    const b = leg?.to?.stopCode
    if (a) stopCodes.push(String(a))
    if (Array.isArray(leg?.intermediateStops)) {
      for (const st of leg.intermediateStops) if (st?.stopCode) stopCodes.push(String(st.stopCode))
    }
    if (b) stopCodes.push(String(b))
  }
  const seen = new Set<string>()
  const segmentCodes = stopCodes.filter(c => !seen.has(c) && seen.add(c))
  const points: [number, number][] = segmentCodes
    .map(c => latLonFromCode(c))
    .filter(Boolean) as [number, number][]

  const roadPath: [number, number][] =
    polylines.length
      ? polylines.flatMap((pl, i) => (i === 0 ? pl.path : pl.path.slice(1)))
      : []

  return { polylines, segments, stopCodes: segmentCodes, points, roadPath }
}

/* ───────────── Itinerary state ───────────── */

type BuiltItinerary = {
  duration_s: number
  transfers: number
  floodSummary: { baseline_s?: number, scenarios: {scenario:string; duration_s:number}[] }
  polylines: Array<{ path:[number,number][], color:string, flooded:boolean }>
  segments: Array<{ points:[number,number][], flooded:boolean }>
  stopCodes: string[]
  points: [number,number][]
  legs: any[]
  roadPath?: [number, number][]
}
const ptItins = ref<BuiltItinerary[]>([])
const selectedItinIdx = ref<number>(0)

/** OneMap PT (address) state */
const ptLoading = ref(false)
const ptError = ref<string | null>(null)

/** UI state: plain address text fields */
const originText = ref<string>('') // address only
const destText   = ref<string>('') // address only

function mins(n?: number) {
  if (!Number.isFinite(n)) return '-'
  return `${Math.round(Number(n) / 60)} min`
}

function applyItineraryToMap(i: number) {
  const it = ptItins.value[i]
  if (!it) return
  ;(store as any).setServiceRouteOverlay?.({
    serviceNo: `OneMap PT • Option ${i+1}`,
    directions: [{
      dir: 1,
      points: it.points,
      stopCodes: it.stopCodes,
      duration_s: it.duration_s,
      floodSummary: it.floodSummary,
      segments: it.segments,
      roadPath: (it.roadPath && it.roadPath.length >= 2) ? it.roadPath : undefined,
    }],
    polylines: it.polylines,
    baseColor: BASE_COLOR,
    floodedColor: FLOODED_COLOR,
  })
  ;(store as any).setColoredPolylines?.(it.polylines)
  ;(store as any).setActiveTab?.('stops')
  ;(store as any).fitToOverlayBounds?.()
}

/** ---------- OneMap PT: address-to-address ---------- */
async function queryPtRouteViaOneMap() {
  if (!originText.value || !destText.value) {
    alert('Enter a start and end address to use OneMap PT routing.')
    return
  }

  if (currentRouteAbort) currentRouteAbort.abort()
  currentRouteAbort = new AbortController()

  ptLoading.value = true
  ptError.value = null

  try {
    const res: any = await getOneMapPtRoute({
      start_address: originText.value,
      end_address: destText.value,
      time: '07:00:00',
    })

    const itins: any[] = Array.isArray(res?.plan?.itineraries) ? res.plan.itineraries : []
    if (!itins.length) {
      alert('No PT itinerary found.')
      return
    }

    const built: BuiltItinerary[] = []
    for (const it of itins) {
      const duration_s = Number(it?.duration ?? 0)
      const transfers = Number(it?.transfers ?? 0)
      const floodSummary = summarizeFloodDurations(it?.legs || [])
      const { polylines, segments, stopCodes, points, roadPath } = await buildColoredPolylinesFromItinerary(it)
      built.push({ duration_s, transfers, floodSummary, polylines, segments, stopCodes, points, legs: it?.legs || [], roadPath })
    }
    ptItins.value = built
    selectedItinIdx.value = 0
    applyItineraryToMap(0)
    ;(store as any).oneMapLegs = built[0]?.legs
  } catch (e: any) {
    ptError.value = e?.message || 'PT route failed'
    console.error(e)
  } finally {
    ptLoading.value = false
  }
}

/** ---------- lifecycle ---------- */
onMounted(async () => {
  const rows = await getAllBusStops()
  allStops.value = rows
    .map(pickStopFields)
    .filter(s => Number.isFinite(s.lat) && Number.isFinite(s.lon) && s.code)
    .map(s => ({ ...s, q: norm(`${s.name} ${s.code}`) }))
  loaded.value = true
})
</script>

<template>
  <div class="bg-white rounded shadow p-3 relative z-[12000]">
    <div class="text-base font-semibold mb-2">
      {{ isItinerary ? 'Addresses' : 'Stops' }}
    </div>

    <div class="space-y-2 mb-3">
      <!-- Starts At -->
      <label class="block">
        <div class="text-xs text-gray-600 mb-1">
          {{ isItinerary ? 'Start address' : 'Starts At' }}
        </div>
        <input
          v-model="originText"
          type="text"
          :placeholder="isItinerary ? 'Type a start address' : 'Type stop name/code or an address'"
          class="w-full rounded border border-gray-300 px-2 py-1 text-sm focus:outline-none focus:ring focus:ring-blue-200"
          autocomplete="off"
        />
      </label>

      <!-- Ends At -->
      <label class="block mt-2">
        <div class="text-xs text-gray-600 mb-1">
          {{ isItinerary ? 'End address' : 'Ends At' }}
        </div>
        <input
          v-model="destText"
          type="text"
          :placeholder="isItinerary ? 'Type a destination address' : 'Type stop name/code or an address'"
          class="w-full rounded border border-gray-300 px-2 py-1 text-sm focus:outline-none focus:ring focus:ring-blue-200"
          autocomplete="off"
        />
      </label>

      <!-- Action buttons row -->
      <div class="flex items-center gap-2 flex-wrap mt-3">
        <!-- PURPLE: only in 'itinerary' mode (address-to-address) -->
        <button
          v-if="mode === 'itinerary'"
          class="inline-flex items-center gap-2 rounded bg-violet-600 text-white px-3 py-1.5 text-sm hover:bg-violet-700 disabled:opacity-60"
          @click="queryPtRouteViaOneMap"
          :disabled="ptLoading"
          title="Public transport via OneMap (type addresses above)"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 24 24" fill="currentColor">
            <path
              d="M6 3a3 3 0 0 0-3 3v8a3 3 0 0 0 3 3v2a1 1 0 1 0 2 0v-2h8v2a1 1 0 1 0 2 0v-2a3 3 0 0 0 3-3V6a3 3 0 0 0-3-3H6zm0 2h12a1 1 0 0 1 1 1v6H5V6a1 1 0 0 1 1-1zm1.5 12a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3zm9 0a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3z"
            />
          </svg>
          {{ ptLoading ? 'Routing…' : 'Find best bus itinerary' }}
        </button>

        <!-- Clear all (always visible) -->
        <button
          class="inline-flex items-center gap-2 rounded border border-gray-300 px-3 py-1.5 text-sm text-gray-700 hover:bg-gray-50"
          @click="clearMapRoutes"
          title="Clear all drawn routes and map markers"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M6 18L18 6M6 6l12 12"/>
          </svg>
          Clear Map & Routes
        </button>

        <span v-if="ptError" class="text-xs text-rose-600">{{ ptError }}</span>
      </div>
    </div>

    <!-- ====== Itinerary list (address-based) ====== -->
    <div
      v-if="mode === 'itinerary' && ptItins.length"
      class="mb-4"
    >
      <div class="text-sm font-semibold mb-2">
        Itineraries ({{ ptItins.length }})
      </div>

      <div class="space-y-3">
        <div
          v-for="(it, idx) in ptItins"
          :key="'it-' + idx"
          :class="[
            'rounded-xl border p-3 shadow-sm',
            selectedItinIdx === idx
              ? 'border-blue-400 ring-2 ring-blue-200'
              : 'border-gray-200'
          ]"
        >
          <div class="flex items-center gap-3">
            <div class="text-base font-semibold">Option {{ idx + 1 }}</div>
            <div class="text-sm text-gray-700">
              ~ {{ Math.round(it.duration_s / 60) }} min
              <span class="text-gray-400">•</span>
              {{ it.transfers }} transfer{{ it.transfers === 1 ? '' : 's' }}
            </div>
            <div class="ml-auto">
              <button
                class="rounded-md border px-2 py-1 text-xs"
                :class="selectedItinIdx === idx
                  ? 'bg-blue-600 text-white border-blue-600'
                  : 'text-gray-700 hover:bg-gray-50'"
                @click="selectedItinIdx = idx; applyItineraryToMap(idx)"
                title="Show this itinerary on the map"
              >
                {{ selectedItinIdx === idx ? 'Shown on map' : 'Show on map' }}
              </button>
            </div>
          </div>

          <!-- Stops & segments -->
          <details class="mt-2 rounded-md bg-gray-50 p-3 open:bg-gray-100">
            <summary class="cursor-pointer select-none text-sm text-gray-700">
              Stops & segments
            </summary>

            <div class="space-y-4 mt-2">
              <div
                v-for="(L, li) in it.legs.filter(x => x.mode==='BUS')"
                :key="'legstops-'+li"
                class="rounded-md border p-2"
                :style="{
                  borderColor: legStatus(L)==='flooded'
                    ? '#fecaca'
                    : '#bfdbfe'
                }"
              >
                <div class="flex items-center gap-2 text-sm mb-2">
                  <span
                    class="inline-flex items-center gap-1 rounded-full px-2 py-0.5 text-xs font-medium ring-1"
                    :style="{
                      backgroundColor: legChipStyle(L).bg,
                      color: legChipStyle(L).text,
                      boxShadow: `0 0 0 1px ${legChipStyle(L).ring} inset`
                    }"
                  >
                    Bus {{ routeLabel(L) }}
                  </span>
                  <span
                    class="text-xs"
                    :class="legStatus(L)==='flooded'
                      ? 'text-rose-600'
                      : 'text-blue-600'"
                  >
                    {{ legStatus(L)==='flooded' ? 'Flooded' : 'Clear' }}
                  </span>
                </div>

                <ol class="space-y-1">
                  <li
                    v-for="(code, si) in legStops(L)"
                    :key="code + '-' + si"
                    class="flex items-center gap-2 text-sm"
                  >
                    <span
                      class="inline-flex h-5 w-5 items-center justify-center rounded-full text-white text-[11px]"
                      :style="{
                        backgroundColor: legStatus(L)==='flooded'
                          ? '#dc2626'
                          : '#2563eb'
                      }"
                    >
                      {{ si + 1 }}
                    </span>
                    <span class="truncate">
                      {{ stopIndexByCode[code]?.name || 'Stop' }}
                    </span>
                    <span class="text-xs text-gray-500">
                      ({{ code }})
                    </span>
                  </li>
                </ol>
              </div>
            </div>
          </details>
        </div>
      </div>
    </div>

    <!-- ====== Selected stop detail (no live arrivals anymore) ====== -->
    <div
      v-if="store.selectedStopLoading"
      class="text-sm text-gray-500"
    >
      Loading stop details...
    </div>

    <div
      v-else-if="!store.selectedStop"
    >
      <div class="text-sm text-gray-500">
        Click a stop on the map to see details here.
      </div>
    </div>

    <div v-else>
      <div class="flex items-center justify-between mb-2">
        <div>
          <div class="font-semibold">
            {{
              (store.selectedStop as any)?.name ||
              (store.selectedStop as any)?.stop_name ||
              'Stop details'
            }}
          </div>
        </div>
        <button
          class="text-xs text-gray-500 hover:text-gray-700"
          @click="store.clearSelection()"
        >
          clear
        </button>
      </div>

      <div
        v-if="Array.isArray((store.selectedStop as any)?.service_routes)"
        class="mt-2"
      >
        <div class="text-sm font-medium mb-1">Service routes</div>
        <ul class="space-y-1">
          <li
            v-for="(r, i) in (store.selectedStop as any).service_routes"
            :key="i"
            class="text-sm"
          >
            {{
              r?.name ||
              r?.route_short_name ||
              r?.route_long_name ||
              r?.id ||
              'route'
            }}
          </li>
        </ul>
      </div>

      <!-- Raw JSON (optional debug) -->
      <details class="mt-3">
        <summary class="cursor-pointer text-xs text-gray-500">
          Raw
        </summary>
        <pre class="text-[11px] bg-gray-50 p-2 rounded overflow-auto">
{{ JSON.stringify(store.selectedStop, null, 2) }}
        </pre>
      </details>
    </div>
  </div>
</template>
