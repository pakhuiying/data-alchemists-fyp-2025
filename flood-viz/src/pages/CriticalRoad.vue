<script setup lang="ts">
import { ref, computed, onMounted, watch, nextTick } from 'vue'
import * as L from 'leaflet'
import proj4 from 'proj4'
import {
  getAllFloodEvents,
  getFloodEventById,
  getCriticalSegmentsNearFlood,
  type CriticalSegmentsNearFloodResponse,
  // make sure these exist in your api.ts (see notes at bottom)
  getTopCriticalSegments,
  getRoadCriticality,
} from '@/api/api'

/* ────────── Projections (SVY21 → WGS84) for flood critical segments ────────── */
proj4.defs(
  'EPSG:3414',
  '+proj=tmerc +lat_0=1.36666666666667 +lon_0=103.833333333333 +k=1 +x_0=28001.642 +y_0=38744.572 +ellps=WGS84 +units=m +no_defs'
)
const toWGS84 = (x: number, y: number): [number, number] => {
  const [lon, lat] = proj4('EPSG:3414', 'WGS84', [x, y]) as [number, number]
  return [lat, lon]
}

/* ────────── Tabs & UI state ────────── */
type Tab = 'flood' | 'road'
const activeTab = ref<Tab>('flood')

const layersOpen = ref(true) // collapsible
const showFloodMarkers = ref(true)
const showFloodCritical = ref(true)
const showRoadCritical  = ref(true)
const showHighlight     = ref(true)

const loading = ref(true)
const errorMsg = ref<string | null>(null)
const infoMsg  = ref<string | null>(null)

/* ────────── Flood mode state ────────── */
const bufferM  = ref<number>(50)
const eventsAll = ref<any[]>([])
const q = ref('')
const topN = ref(500)

const filteredEvents = computed(() => {
  const query = q.value.trim().toLowerCase()
  const rows = Array.isArray(eventsAll.value) ? eventsAll.value : []
  const filtered = query
    ? rows.filter(e => (e.flooded_location || e.name || '').toLowerCase().includes(query))
    : rows
  return filtered.slice(0, Math.max(1, Number(topN.value) || 0))
})

const selectedFloodId = ref<number | null>(null)
const lastPayload = ref<CriticalSegmentsNearFloodResponse | null>(null)

/* Flood detail cache (tooltip) */
const detailCache = new Map<number, any>()
const detailPromise = new Map<number, Promise<any>>()
async function getDetailCached(id: number) {
  if (detailCache.has(id)) return detailCache.get(id)
  if (detailPromise.has(id)) return detailPromise.get(id)!
  const p = (async () => {
    const raw = await getFloodEventById(id)
    const detail = Array.isArray(raw) ? raw[0] ?? raw : raw
    detailCache.set(id, detail)
    detailPromise.delete(id)
    return detail
  })().catch(e => { detailPromise.delete(id); throw e })
  detailPromise.set(id, p)
  return p
}

/* Formatters & flood tooltip */
const fmt = {
  min: (n: any) => Number.isFinite(+n) ? `${(+n).toFixed(2)} min` : '—',
  km:  (m: any) => Number.isFinite(+m) ? `${(+m/1000).toFixed(3)} km` : '—',
  date: (s: any) => { try { return s ? new Date(s).toLocaleString() : '—' } catch { return String(s) } }
}
function buildFloodTooltip(detail: any, fallback: { id?: any, name?: string } = {}) {
  const id        = detail?.id ?? detail?.flood_id ?? fallback?.id ?? '—'
  const loc       = detail?.flooded_location ?? detail?.name ?? fallback?.name ?? 'Flood event'
  const startedAt = detail?.started_at ?? detail?.start_time ?? detail?.timestamp
  const roadName  = (typeof detail?.road_name === 'string' && detail.road_name.trim()) ? detail.road_name : 'Unnamed Road'
  const roadType  = detail?.road_type ?? '—'
  const lenM      = Number(detail?.length_m)
  const t20       = Number(detail?.time_20kmh_min)
  const t50       = Number(detail?.time_50kmh_min)
  const delay     = Number(detail?.time_travel_delay_min ?? detail?.delay_min ?? detail?.delay)

  return `
    <div class="flood-tt">
      <div class="tt-title">Flood details</div>
      <div class="tt-subtle">ID: ${id}</div>
      <div class="tt-section">Location</div>
      <table class="tt-table">
        <tr><th>Name</th><td>${loc}</td></tr>
        <tr><th>Start</th><td>${fmt.date(startedAt)}</td></tr>
      </table>
      <div class="tt-section">Road segment</div>
      <table class="tt-table">
        <tr><th>Road name</th><td>${roadName}</td></tr>
        <tr><th>Type</th><td>${roadType}</td></tr>
        <tr><th>Length</th><td>${fmt.km(lenM)}</td></tr>
      </table>
      <div class="tt-section">Traffic impact</div>
      <table class="tt-table">
        <tr><th>Time @ 20 km/h</th><td>${fmt.min(t20)}</td></tr>
        <tr><th>Time @ 50 km/h</th><td>${fmt.min(t50)}</td></tr>
        <tr><th>Travel delay</th><td>${fmt.min(delay)}</td></tr>
      </table>
    </div>`
}

/* ────────── Road criticality mode state ────────── */
type GeoFeature = {
  type: 'Feature',
  geometry: { type: 'LineString', coordinates: [number, number][] },
  properties: Record<string, any>
}
const roadQuery = ref('') // e.g., "Pan-Island Expressway"
const roadFeatures = ref<GeoFeature[]>([])  // search result
const topFeatures  = ref<GeoFeature[]>([])  // top 50 default
const roadLoading  = ref(false)
const roadError    = ref<string | null>(null)

/* ────────── Map + layers ────────── */
const mapEl = ref<HTMLDivElement | null>(null)
let map: L.Map
let floodMarkersLayer: L.LayerGroup | null = null
let floodCriticalLayer: L.LayerGroup | null = null
let roadCriticalLayer: L.LayerGroup | null = null
let highlighted: L.Polyline | null = null

function ensureMap() {
  if (map) return
  const token = import.meta.env.VITE_MAPBOX_TOKEN
  const styleId = 'mapbox/streets-v12'
  map = L.map(mapEl.value as HTMLDivElement, {
    center: [1.3521, 103.8198],
    zoom: 12,
    zoomControl: true,
  })
  const url = `https://api.mapbox.com/styles/v1/${styleId}/tiles/512/{z}/{x}/{y}@2x?access_token=${token}`
  L.tileLayer(url, {
    tileSize: 512,
    zoomOffset: -1,
    maxZoom: 19,
    attribution:
      '&copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors ' +
      '&copy; <a href="https://www.mapbox.com/">Mapbox</a>',
  }).addTo(map)
}

function makeFloodIcon(selected: boolean) {
  const fill = selected ? '#dc2626' : '#2563eb'
  const stroke = selected ? '#991b1b' : '#1e3a8a'
  const svg = `
  <svg viewBox="0 0 32 40" width="32" height="40" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
    <path d="M16 0C8.28 0 2 6.28 2 14c0 8.28 9.1 18.22 13.08 22.07a1.5 1.5 0 0 0 2.06 0C20.1 32.22 30 22.28 30 14 30 6.28 23.72 0 16 0z"
          fill="${fill}" stroke="${stroke}" stroke-width="2" />
    <circle cx="16" cy="14" r="5.2" fill="white"/>
  </svg>`
  return L.divIcon({ className: 'flood-pin', html: svg, iconSize: [32, 40], iconAnchor: [16, 40], popupAnchor: [0, -36], tooltipAnchor: [0, -36] })
}

/* Layer utils */
function setLayerVisibility(layer: L.Layer | null, visible: boolean) {
  if (!map || !layer) return
  const onMap = (map as any)._layers && Object.values((map as any)._layers).includes(layer)
  if (visible && !onMap) (layer as any).addTo(map)
  if (!visible && onMap) map.removeLayer(layer)
}
function clearHighlight() { if (highlighted) { map.removeLayer(highlighted); highlighted = null } }
function clearFloodCritical() { if (floodCriticalLayer) { map.removeLayer(floodCriticalLayer); floodCriticalLayer = null } clearHighlight() }
function clearRoadCritical() { if (roadCriticalLayer) { map.removeLayer(roadCriticalLayer); roadCriticalLayer = null } clearHighlight() }

/* ────────── Flood drawing ────────── */
function renderFloodMarkers() {
  if (!map) return
  if (floodMarkersLayer) { map.removeLayer(floodMarkersLayer); floodMarkersLayer = null }
  floodMarkersLayer = L.layerGroup()
  const bounds = L.latLngBounds([])

  for (const e of filteredEvents.value) {
    const name: string = e.flooded_location || e.name || ''
    const lat = e.latitude ?? e.lat ?? e.center_lat
    const lon = e.longitude ?? e.lon ?? e.center_lon ?? e.lng
    if (!Number.isFinite(+lat) || !Number.isFinite(+lon)) continue

    const isSelected = selectedFloodId.value === Number(e.flood_id ?? e.id)
    const marker = L.marker([+lat, +lon], { icon: makeFloodIcon(isSelected) })
      .bindTooltip(
        `<div class="flood-tt"><div class="tt-title">${name || 'Flood event'}</div><div class="tt-subtle">ID: ${e.flood_id ?? e.id ?? '—'}</div></div>`,
        { sticky: true, direction: 'top', opacity: 0.95, className: 'flood-tooltip' }
      )
      .on('mouseover', async (ev: L.LeafletMouseEvent) => {
        try {
          const id = Number(e.flood_id ?? e.id)
          if (!Number.isFinite(id)) return
          const tt = (marker as any).getTooltip?.()
          tt?.setContent(`<div class="flood-tt">Loading…</div>`)
          ;(marker as any).openTooltip?.(ev.latlng)
          const detail = await getDetailCached(id)
          tt?.setContent(buildFloodTooltip(detail, { id, name }))
          ;(marker as any).openTooltip?.(ev.latlng)
        } catch {
          (marker as any).getTooltip?.()?.setContent(`<div class="flood-tt">Failed to load details</div>`)
        }
      })
      .on('click', () => onSelectFloodRow(e))

    floodMarkersLayer.addLayer(marker)
    bounds.extend([+lat, +lon])
  }

  setLayerVisibility(floodMarkersLayer, showFloodMarkers.value)
  if (bounds.isValid()) map.fitBounds(bounds.pad(0.12))
}

function onSelectFloodRow(e: any) {
  const id = Number(e?.flood_id ?? e?.id)
  if (!Number.isFinite(id) || id <= 0) { errorMsg.value = 'Invalid flood id.'; return }
  selectedFloodId.value = id
  renderFloodMarkers()
  fetchAndDrawCriticalNearFlood(id)
}

async function fetchAndDrawCriticalNearFlood(fid: number) {
  errorMsg.value = null; infoMsg.value = null; clearFloodCritical()
  if (!Number.isFinite(fid) || fid <= 0) { errorMsg.value = 'Select a valid flood event (flood_id > 0).'; return }
  const buf = Math.max(1, Number(bufferM.value || 50))
  try {
    const payload = await getCriticalSegmentsNearFlood({ flood_id: fid, buffer_m: buf }) as any
    if (payload && typeof payload.message === 'string') {
      lastPayload.value = null
      infoMsg.value = payload.message || 'No critical roads near this flood.'
      drawOnlyFloodPoint(fid)
      return
    }
    lastPayload.value = payload
    drawFloodCritical(payload)
  } catch (e: any) {
    console.error(e); errorMsg.value = e?.message || 'Failed to fetch critical segments.'
  }
}

function drawOnlyFloodPoint(fid: number) {
  clearFloodCritical()
  floodCriticalLayer = L.layerGroup()
  setLayerVisibility(floodCriticalLayer, showFloodCritical.value)

  const evt = eventsAll.value.find(e => Number(e.flood_id ?? e.id) === Number(fid))
  const lat = evt?.latitude ?? evt?.lat ?? evt?.center_lat
  const lon = evt?.longitude ?? evt?.lon ?? evt?.center_lon ?? evt?.lng
  if (!Number.isFinite(+lat) || !Number.isFinite(+lon)) return

  const m = L.circleMarker([+lat, +lon], {
    radius: 5, color: '#991b1b', weight: 2, fillColor: '#ef4444', fillOpacity: 0.9, interactive: false,
  })
  floodCriticalLayer.addLayer(m)
  setLayerVisibility(floodCriticalLayer, showFloodCritical.value)
  map.fitBounds(L.latLngBounds([[+lat, +lon]]).pad(0.25))
}

function drawFloodCritical(p: CriticalSegmentsNearFloodResponse) {
  clearFloodCritical()
  floodCriticalLayer = L.layerGroup()
  const bounds = L.latLngBounds([])

  const fp = (p as any).flood_point
  if (fp?.type === 'Point' && Array.isArray(fp.coordinates) && fp.coordinates.length === 2) {
    const [lon, lat] = fp.coordinates
    const m = L.circleMarker([lat, lon], {
      radius: 5, color: '#991b1b', weight: 2, fillColor: '#ef4444', fillOpacity: 0.9, interactive: false,
    })
    floodCriticalLayer.addLayer(m)
    bounds.extend([lat, lon])
  }

  for (const seg of (p as any).critical_segments || []) {
    const coords: [number, number][] = seg?.geometry?.coordinates || []
    const latlngs: [number, number][] = []
    for (const [x, y] of coords) {
      const [lat, lon] = toWGS84(x, y)
      latlngs.push([lat, lon])
      bounds.extend([lat, lon])
    }
    if (!latlngs.length) continue

    const safeName = (typeof seg.road_name === 'string' && seg.road_name.trim()) ? seg.road_name : 'Unnamed Road'
    const poly = L.polyline(latlngs, {
      color: '#dc2626', weight: 6, opacity: 0.95, dashArray: '4,6',
    }).bindTooltip(`
      <div class="flood-tt">
        <div class="tt-title">${safeName}</div>
        <div class="tt-subtle">${seg.road_type || '—'}</div>
        <table class="tt-table" style="margin-top:6px;">
          <tr><th>Length</th><td>${Number(seg.length_m).toFixed(2)} m</td></tr>
          <tr><th>Centrality</th><td>${Number(seg.centrality_score).toFixed(6)}</td></tr>
          <tr><th>Buffer</th><td>${(p as any).buffer_m} m</td></tr>
        </table>
      </div>
    `, { sticky: true, direction: 'top', opacity: 0.95, className: 'flood-tooltip' })

    ;(poly as any).__meta = { seg }
    floodCriticalLayer.addLayer(poly)
  }

  setLayerVisibility(floodCriticalLayer, showFloodCritical.value)
  if (bounds.isValid()) map.fitBounds(bounds.pad(0.12))
}

function highlightPolylineFromLayer(layer: L.LayerGroup | null, idx: number) {
  if (!layer) return
  if (highlighted) { map.removeLayer(highlighted); highlighted = null }

  let i = 0; let target: L.Polyline | null = null
  layer.eachLayer((l: any) => {
    if (l instanceof L.Polyline) { if (i === idx) target = l; i++ }
  })
  if (target) {
    const latlngs = (target as any).getLatLngs?.() as L.LatLng[] | L.LatLng[][]
    const flat = Array.isArray(latlngs?.[0]) ? (latlngs as L.LatLng[][]).flat() : (latlngs as L.LatLng[])
    if (flat?.length) {
      highlighted = L.polyline(flat, { color: '#7c3aed', weight: 7, opacity: 0.95 })
      if (showHighlight.value) highlighted.addTo(map)
      map.fitBounds(L.latLngBounds(flat as any).pad(0.2))
    }
  }
}

/* ────────── Betweenness color scale + legend (ROAD MODE) ────────── */
let roadLegend: L.Control | null = null

function getBetweennessRange(features: any[]) {
  let min = +Infinity, max = -Infinity
  for (const f of features || []) {
    const b = Number(f?.properties?.betweenness)
    if (Number.isFinite(b)) { if (b < min) min = b; if (b > max) max = b }
  }
  if (!Number.isFinite(min) || !Number.isFinite(max)) { min = 0; max = 1 }
  if (min === max) max = min + 1e-9
  return { min, max }
}
function hueForT(t: number, hStart = 220, hEnd = 0) {
  const h = hStart + (hEnd - hStart) * t
  return `hsl(${h}, 85%, 50%)`
}
function colorByBetweenness(b: number, min: number, max: number) {
  if (!Number.isFinite(b)) return '#999'
  const t = (b - min) / (max - min)
  return hueForT(Math.min(1, Math.max(0, t)))
}

function removeRoadLegend() {
  if (roadLegend) {
    // Either: (roadLegend as any).remove();  // works too
    if (map) map.removeControl(roadLegend)
    roadLegend = null
  }
}

function addOrUpdateRoadLegend(min: number, max: number) {
  if (!map) return
  removeRoadLegend()

  const legend = new L.Control({ position: 'bottomright' })

  // TS-safe: attach onAdd before assigning to roadLegend
  ;(legend as any).onAdd = () => {
    const div = L.DomUtil.create('div', 'legend-box')
    div.innerHTML = `
      <div class="legend-title">Betweenness</div>
      <div class="legend-gradient"></div>
      <div class="legend-scale">
        <span>${min.toExponential(2)}</span>
        <span>${max.toExponential(2)}</span>
      </div>`
    return div
  }

  legend.addTo(map)
  roadLegend = legend
}

/* ────────── Road drawing (WGS84) with hue scale ────────── */
function drawRoadCritical(features: GeoFeature[]) {
  clearRoadCritical()
  roadCriticalLayer = L.layerGroup()
  const bounds = L.latLngBounds([])

  const { min, max } = getBetweennessRange(features as any[])
  if (showRoadCritical.value) addOrUpdateRoadLegend(min, max)

  for (const f of features) {
    const coords = f?.geometry?.coordinates || []
    if (!Array.isArray(coords) || !coords.length) continue

    const latlngs: [number, number][] = []
    for (const [lon, lat] of coords) { latlngs.push([lat, lon]); bounds.extend([lat, lon]) }

    const name = (f.properties?.road_name && String(f.properties.road_name).trim())
      ? String(f.properties.road_name) : 'Unnamed Road'
    const rank = f.properties?.rank
    const braw = Number(f.properties?.betweenness)
    const nb   = Number(f.properties?.norm_betweenness)
    const color = colorByBetweenness(braw, min, max)

    const poly = L.polyline(latlngs, {
      color, weight: 5, opacity: 0.95,
    }).bindTooltip(`
      <div class="flood-tt">
        <div class="tt-title">${name}</div>
        <div class="tt-subtle">Rank: ${rank ?? '—'}</div>
        <table class="tt-table" style="margin-top:6px;">
          <tr><th>Betweenness</th><td>${Number(braw).toExponential(6)}</td></tr>
          <tr><th>Norm. Betweenness</th><td>${Number(nb).toFixed(6)}</td></tr>
        </table>
      </div>
    `, { sticky: true, direction: 'top', opacity: 0.95, className: 'flood-tooltip' })

    ;(poly as any).__meta = { feature: f }
    roadCriticalLayer.addLayer(poly)
  }

  setLayerVisibility(roadCriticalLayer, showRoadCritical.value)
  if (bounds.isValid()) map.fitBounds(bounds.pad(0.12))
}

/* Public row click handlers */
function highlightFloodSegment(idx: number) { highlightPolylineFromLayer(floodCriticalLayer, idx) }
function highlightRoadSegment(idx: number) { highlightPolylineFromLayer(roadCriticalLayer, idx) }

/* ────────── Watches ────────── */
watch([filteredEvents, selectedFloodId], () => { renderFloodMarkers() })

let bufTimer: number | undefined
watch(bufferM, () => {
  if (!selectedFloodId.value) return
  window.clearTimeout(bufTimer)
  bufTimer = window.setTimeout(() => fetchAndDrawCriticalNearFlood(selectedFloodId.value!), 400)
})

watch(showFloodMarkers, v => setLayerVisibility(floodMarkersLayer, v))
watch(showFloodCritical, v => setLayerVisibility(floodCriticalLayer, v))
watch(showRoadCritical,  v => {
  setLayerVisibility(roadCriticalLayer, v)
  // Update/remove legend with toggle
  if (v) {
    const list = (roadQuery.value ? roadFeatures.value : topFeatures.value) as any[]
    const { min, max } = getBetweennessRange(list)
    addOrUpdateRoadLegend(min, max)
  } else {
    removeRoadLegend()
  }
})
watch(showHighlight, v => {
  if (!highlighted) return
  if (v) highlighted.addTo(map)
  else map.removeLayer(highlighted)
})

/* Refresh legend when datasets change */
watch([roadFeatures, topFeatures], () => {
  if (!showRoadCritical.value) return
  const list = (roadQuery.value ? roadFeatures.value : topFeatures.value) as any[]
  const { min, max } = getBetweennessRange(list)
  addOrUpdateRoadLegend(min, max)
})

/* ────────── Road fetchers ────────── */
async function loadTopRoadCritical() {
  roadLoading.value = true; roadError.value = null
  try {
    const fc = await getTopCriticalSegments(50) as any // GeoJSON FeatureCollection
    topFeatures.value = Array.isArray(fc?.features) ? fc.features : []
    drawRoadCritical(topFeatures.value)
  } catch (e: any) {
    roadError.value = e?.message || 'Failed to load top critical segments.'
  } finally { roadLoading.value = false }
}

async function searchRoadCritical() {
  const name = roadQuery.value.trim()
  if (!name) {
    drawRoadCritical(topFeatures.value)
    roadFeatures.value = []
    return
  }
  roadLoading.value = true; roadError.value = null
  try {
    const fc = await getRoadCriticality(name) as any // GeoJSON FeatureCollection
    roadFeatures.value = Array.isArray(fc?.features) ? fc.features : []
    drawRoadCritical(roadFeatures.value)
  } catch (e: any) {
    roadError.value = e?.message || 'Failed to search road criticality.'
  } finally { roadLoading.value = false }
}

/* ────────── Lifecycle ────────── */
onMounted(async () => {
  ensureMap()
  try {
    const events = await getAllFloodEvents()
    eventsAll.value = Array.isArray(events) ? events : []
  } catch (e: any) {
    console.error(e); errorMsg.value = e?.message || 'Failed to load flood events.'
  } finally {
    loading.value = false
    await nextTick()
    renderFloodMarkers()
  }

  // Load top-50 road criticality
  loadTopRoadCritical()

  // Deep links (?flood_id=&buffer_m=)
  const qs = new URLSearchParams(window.location.search)
  const fid = Number(qs.get('flood_id'))
  const buf = Number(qs.get('buffer_m'))
  if (Number.isFinite(buf) && buf >= 1) bufferM.value = buf
  if (Number.isFinite(fid) && fid > 0) {
    selectedFloodId.value = fid
    renderFloodMarkers()
    fetchAndDrawCriticalNearFlood(fid)
  }
})
</script>

<template>
  <div class="h-full grid grid-cols-12 gap-4 p-4">
    <!-- LEFT: tabs + panels -->
    <aside class="col-span-4 space-y-4">
      <!-- Layers (collapsible) -->
      <div class="bg-white rounded shadow">
        <div
          class="px-3 py-2 flex items-center justify-between cursor-pointer select-none border-b"
          @click="layersOpen = !layersOpen"
        >
          <div class="text-sm font-semibold">Layers</div>
          <div class="text-xs text-gray-500">{{ layersOpen ? 'Hide' : 'Show' }}</div>
        </div>
        <div v-show="layersOpen" class="p-3 space-y-2 text-sm">
          <label class="flex items-center gap-2">
            <input type="checkbox" v-model="showFloodMarkers" />
            Flood markers
          </label>
          <label class="flex items-center gap-2">
            <input type="checkbox" v-model="showFloodCritical" />
            Flood critical segments
          </label>
          <label class="flex items-center gap-2">
            <input type="checkbox" v-model="showRoadCritical" />
            Road critical segments (colored by betweenness)
          </label>
          <label class="flex items-center gap-2">
            <input type="checkbox" v-model="showHighlight" />
            Highlight selected segment
          </label>
        </div>
      </div>

      <!-- Tabs -->
      <div class="bg-white rounded shadow">
        <div class="flex border-b">
          <button
            class="flex-1 px-3 py-2 text-sm font-medium"
            :class="activeTab === 'flood' ? 'bg-gray-100' : ''"
            @click="activeTab = 'flood'"
          >
            Flood Mode
          </button>
          <button
            class="flex-1 px-3 py-2 text-sm font-medium"
            :class="activeTab === 'road' ? 'bg-gray-100' : ''"
            @click="activeTab = 'road'"
          >
            Road Criticality Mode
          </button>
        </div>

        <!-- Flood Mode -->
        <div v-if="activeTab === 'flood' " class="p-3 space-y-3">
          <div class="text-sm font-semibold">Critical Roads Near Flood</div>

          <div class="grid grid-cols-2 gap-2">
            <label class="text-xs text-gray-600 self-center">Buffer (m)</label>
            <input v-model.number="bufferM" type="number" min="1" step="1" class="px-2 py-1 border rounded text-sm" />
            <label class="text-xs text-gray-600 self-center">Filter by location</label>
            <input v-model="q" type="text" placeholder="e.g. Yishun Ave 2" class="px-2 py-1 border rounded text-sm" />
          </div>

          <div v-if="errorMsg" class="text-xs text-red-600">{{ errorMsg }}</div>
          <div v-if="infoMsg" class="text-xs text-amber-700">{{ infoMsg }}</div>

          <div class="text-xs text-gray-600">
            <div>Events loaded: <span class="font-medium">{{ eventsAll.length }}</span></div>
            <div>Showing: <span class="font-medium">{{ filteredEvents.length }}</span></div>
            <div v-if="lastPayload">Selected Flood: <span class="font-medium">{{ lastPayload.flood_id }}</span> • Segments: <span class="font-medium">{{ lastPayload.count_critical_segments }}</span></div>
          </div>

          <!-- Flood events table -->
          <div class="border rounded">
            <div class="flex items-center justify-between px-2 py-1 text-xs text-gray-500 border-b">
              <div class="font-medium">Flood Events</div>
              <div>Click a row to draw</div>
            </div>

            <div v-if="loading" class="p-2 text-gray-500 text-sm">Loading…</div>
            <div v-else-if="!eventsAll.length" class="p-2 text-gray-500 text-sm">No flood events.</div>

            <div v-else class="max-h-[40vh] overflow-auto">
              <table class="min-w-full text-sm">
                <thead class="bg-gray-100 text-gray-700 sticky top-0">
                  <tr>
                    <th class="px-2 py-1 border text-left">Location</th>
                    <th class="px-2 py-1 border text-right">ID</th>
                  </tr>
                </thead>
                <tbody>
                  <tr
                    v-for="e in filteredEvents"
                    :key="e.flood_id ?? e.id"
                    class="hover:bg-gray-50 cursor-pointer"
                    @click="onSelectFloodRow(e)"
                    :title="`Zoom & draw critical segments for Flood ${e.flood_id ?? e.id}`"
                  >
                    <td class="px-2 py-1 border">{{ e.flooded_location || e.name || 'Flood event' }}</td>
                    <td class="px-2 py-1 border text-right">{{ e.flood_id ?? e.id }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Flood critical table -->
          <div v-if="lastPayload && lastPayload.critical_segments?.length" class="border rounded mt-3">
            <div class="flex items-center justify-between px-2 py-1 text-xs text-gray-500 border-b">
              <div class="font-medium">Critical Segments</div>
              <div>Click a row to zoom</div>
            </div>
            <div class="max-h-[32vh] overflow-auto">
              <table class="min-w-full text-sm">
                <thead class="bg-gray-100 text-gray-700 sticky top-0">
                  <tr>
                    <th class="px-2 py-1 border text-left">Road</th>
                    <th class="px-2 py-1 border text-left">Type</th>
                    <th class="px-2 py-1 border text-right">Len (m)</th>
                    <th class="px-2 py-1 border text-right">Centrality</th>
                  </tr>
                </thead>
                <tbody>
                  <tr
                    v-for="(seg, idx) in lastPayload.critical_segments"
                    :key="idx"
                    class="hover:bg-gray-50 cursor-pointer"
                    @click="highlightFloodSegment(idx)"
                  >
                    <td class="px-2 py-1 border">{{ (typeof seg.road_name === 'string' && seg.road_name.trim()) ? seg.road_name : 'Unnamed Road' }}</td>
                    <td class="px-2 py-1 border">{{ seg.road_type || '—' }}</td>
                    <td class="px-2 py-1 border text-right">{{ Number(seg.length_m).toFixed(2) }}</td>
                    <td class="px-2 py-1 border text-right">{{ Number(seg.centrality_score).toFixed(6) }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- Road Criticality -->
        <div v-else class="p-3 space-y-3">
          <div class="text-sm font-semibold">Road Criticality</div>

          <div class="grid grid-cols-3 gap-2">
            <div class="col-span-2">
              <input
                v-model="roadQuery"
                type="text"
                placeholder="Search road name e.g. Pan-Island Expressway"
                class="px-2 py-1 border rounded text-sm w-full"
                @keydown.enter="searchRoadCritical"
              />
            </div>
            <button class="px-2 py-1 border rounded text-sm bg-gray-50 hover:bg-gray-100" @click="searchRoadCritical">
              Search
            </button>
          </div>

          <div class="text-xs text-gray-600">
            Shows Top 50 by default. Enter a road name to filter by name.
          </div>

          <div v-if="roadError" class="text-xs text-red-600">{{ roadError }}</div>
          <div v-if="roadLoading" class="text-sm text-gray-500">Loading…</div>

          <div class="border rounded">
            <div class="flex items-center justify-between px-2 py-1 text-xs text-gray-500 border-b">
              <div class="font-medium">{{ roadQuery ? 'Search Results' : 'Top 50 Critical Segments' }}</div>
              <div>Click a row to zoom</div>
            </div>
            <div class="max-h-[60vh] overflow-auto">
              <table class="min-w-full text-sm">
                <thead class="bg-gray-100 text-gray-700 sticky top-0">
                  <tr>
                    <th class="px-2 py-1 border text-right">Rank</th>
                    <th class="px-2 py-1 border text-left">Road</th>
                    <th class="px-2 py-1 border text-left">Type</th>
                    <th class="px-2 py-1 border text-right">Betw.</th>
                    <th class="px-2 py-1 border text-right">Norm</th>
                  </tr>
                </thead>
                <tbody>
                  <tr
                    v-for="(f, idx) in (roadQuery ? roadFeatures : topFeatures)"
                    :key="idx"
                    class="hover:bg-gray-50 cursor-pointer"
                    @click="highlightRoadSegment(idx)"
                  >
                    <td class="px-2 py-1 border text-right">{{ f?.properties?.rank ?? '—' }}</td>
                    <td class="px-2 py-1 border">
                      {{ (f?.properties?.road_name && String(f.properties.road_name).trim()) ? f.properties.road_name : 'Unnamed Road' }}
                    </td>
                    <td class="px-2 py-1 border">{{ f?.properties?.road_type ?? '—' }}</td>
                    <td class="px-2 py-1 border text-right">{{ Number(f?.properties?.betweenness).toExponential(2) }}</td>
                    <td class="px-2 py-1 border text-right">{{ Number(f?.properties?.norm_betweenness).toFixed(6) }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

        </div>
      </div>
    </aside>

    <!-- RIGHT: shared map -->
    <main class="col-span-8">
      <div class="bg-white rounded shadow h-[calc(100vh-2.5rem)] p-2">
        <div ref="mapEl" class="w-full h-full"></div>
      </div>
    </main>
  </div>
</template>

<style>
/* Tooltips */
.flood-tooltip { padding: 0 !important; border: 0; background: transparent; box-shadow: none; }
.flood-tt {
  background:#fff; border:1px solid #e5e7eb; border-radius:8px;
  box-shadow:0 8px 24px rgba(0,0,0,.12); padding:10px 12px;
  font:12px/1.35 system-ui,-apple-system,Segoe UI,Roboto,Inter,Arial,sans-serif;
  color:#111827; max-width:260px;
}
.flood-tt .tt-title { font-weight:600; margin-bottom:2px; }
.flood-tt .tt-subtle { color:#6b7280; font-size:11px; margin-bottom:8px; }
.flood-tt .tt-section { margin-top:8px; font-weight:600; color:#374151; }
.flood-tt .tt-table { width:100%; border-collapse:collapse; margin-top:4px; }
.flood-tt .tt-table th, .flood-tt .tt-table td { border:1px solid #e5e7eb; padding:4px 6px; vertical-align:top; font-size:12px; }
.flood-tt .tt-table th { width:48%; background:#f9fafb; color:#374151; font-weight:600; }
.leaflet-marker-icon.flood-pin { filter: drop-shadow(0 2px 6px rgba(0,0,0,.25)); }

/* Legend for betweenness */
.legend-box {
  background:#fff; border:1px solid #e5e7eb; border-radius:8px;
  box-shadow:0 8px 24px rgba(0,0,0,.12); padding:8px 10px; width: 200px;
  font:12px/1.35 system-ui,-apple-system,Segoe UI,Roboto,Inter,Arial,sans-serif;
  color:#111827;
}
.legend-title { font-weight:600; margin-bottom:6px; }
.legend-gradient {
  height: 10px; border-radius: 4px; margin: 6px 0;
  background: linear-gradient(to right,
    hsl(220,85%,50%), hsl(180,85%,50%), hsl(140,85%,50%),
    hsl(100,85%,50%), hsl(60,85%,50%), hsl(20,85%,50%), hsl(0,85%,50%)
  );
}
.legend-scale { display:flex; justify-content:space-between; color:#374151; }
</style>
