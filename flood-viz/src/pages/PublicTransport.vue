<script setup lang="ts">
import { computed, ref, watch, onMounted, onActivated, onUnmounted } from 'vue'
import { onBeforeRouteLeave } from 'vue-router'
import { useAppStore } from '@/store/app'
import StopDetailsPanel from '@/components/StopDetailsPanel.vue'
import ControlsPanel from '@/components/ControlsPanel.vue'
import MapCanvas from '@/components/MapCanvas.vue'
import TravelTimeBarChart from '@/components/TravelTimeBarChart.vue'
import { useUrlStateSync } from '@/components/useUrlStateSync'
import { getBusesAffectedByFloods, getBusRouteByService } from '@/api/api'  /* ← added */

useUrlStateSync()
const store = useAppStore()

/* ─────────────────────────────
   ACTIVE TAB: 'itinerary' | 'flood'
   ───────────────────────────── */
const activeTab = ref<'itinerary' | 'flood'>('itinerary')

function setTab(tab: 'itinerary' | 'flood') {
  activeTab.value = tab

  // map-layer visibility rules
  if (tab === 'flood') {
    store.setLayerVisible('stops', false)
    store.setLayerVisible('floodEvents', true)
  } else {
    // itinerary tab
    store.setLayerVisible('stops', true)
    store.setLayerVisible('floodEvents', false)
    clearFloodUI()
  }
}

/* ─────────────────────────────
   RESET CHART ON (RE)ENTER PAGE
   ───────────────────────────── */
function resetChart() {
  ;(store as any).serviceRouteOverlay = null
}
onMounted(resetChart)
onActivated(resetChart)
onBeforeRouteLeave(resetChart)
onUnmounted(resetChart)

/* ================= Chart ================= */
const chartEntry = computed(() => {
  const o: any = (store as any).serviceRouteOverlay
  const d = o?.directions?.[0]
  if (!d || !Number.isFinite(d.duration_s) || !d.floodSummary) return null
  return { duration_s: Number(d.duration_s), floodSummary: d.floodSummary }
})

/* ================= Flood / affected bus services ================= */
const selectedFloodId = ref<number | null>(null)
const affectedServices = ref<string[]>([])
const loadingAffected = ref(false)
const affectedError = ref<string | null>(null)

function clearFloodUI() {
  selectedFloodId.value = null
  affectedServices.value = []
  affectedError.value = null
  loadingAffected.value = false
}

async function onFloodClick(payload: { floodId: number }) {
  // Only respond if we're actually looking at flood tab
  if (activeTab.value !== 'flood') return

  selectedFloodId.value = payload.floodId
  loadingAffected.value = true
  affectedError.value = null
  affectedServices.value = []

  try {
    const res: any = await getBusesAffectedByFloods(payload.floodId)

    if (!res || typeof res !== 'object' || !Array.isArray(res.results)) {
      throw new Error('Unexpected response shape (missing results).')
    }

    const first: any = res.results[0]
    if (!first || typeof first !== 'object') {
      affectedServices.value = []
      return
    }

    if (first.flood_id != null && !Number.isNaN(Number(first.flood_id))) {
      selectedFloodId.value = Number(first.flood_id)
    }

    const raw: unknown[] = Array.isArray(first.affected_bus_services)
      ? first.affected_bus_services
      : []

    const names: string[] = raw
      .map(s => String(s ?? '').trim())
      .filter((s): s is string => s.length > 0)

    affectedServices.value = Array.from(new Set(names)).sort((a, b) =>
      a.localeCompare(b, undefined, { numeric: true })
    )
  } catch (e: any) {
    const msg =
      e?.message ||
      e?.error ||
      (typeof e?.toString === 'function' ? e.toString() : '') ||
      'Failed to load affected services.'
    affectedError.value = msg
  } finally {
    loadingAffected.value = false
  }
}

/* If something else flips layers externally, keep things sane */
watch(
  () => activeTab.value,
  (tab) => {
    if (tab !== 'flood') clearFloodUI()
  }
)

/* ========= NEW: helpers to draw a service route when a list item is clicked ========= */
const BASE_COLOR = '#2563eb'
const FLOODED_COLOR = '#dc2626'

// Remove consecutive duplicate points
function dedupeConsecutive(points: [number, number][]) {
  const out: [number, number][] = []
  let prev: string | null = null
  for (const p of points) {
    const key = `${p[0].toFixed(7)},${p[1].toFixed(7)}`
    if (key !== prev) out.push(p)
    prev = key
  }
  return out
}

// Build polylines from backend geometry (supports flooded_spans)
function buildColoredPolylinesFromDirection(d: {
  coordinates: [number, number][],
  flooded_spans?: Array<[number, number]>
}) {
  const coords = dedupeConsecutive(d.coordinates || [])
  if (!coords.length) return []
  if (Array.isArray(d.flooded_spans) && d.flooded_spans.length) {
    const mask = new Array(coords.length).fill(false)
    for (const [a, b] of d.flooded_spans) {
      const lo = Math.max(0, Math.min(a, b))
      const hi = Math.min(coords.length - 1, Math.max(a, b))
      for (let i = lo; i <= hi; i++) mask[i] = true
    }
    const out: Array<{ path:[number,number][], color:string, flooded:boolean }> = []
    let runStart = 0
    for (let i = 1; i <= coords.length; i++) {
      if (i === coords.length || mask[i] !== mask[i-1]) {
        const seg = coords.slice(runStart, i)
        if (seg.length >= 2) {
          out.push({ path: seg, color: mask[i-1] ? FLOODED_COLOR : BASE_COLOR, flooded: !!mask[i-1] })
        }
        runStart = i
      }
    }
    return out
  }
  return [{ path: coords, color: BASE_COLOR, flooded: false }]
}

async function drawServiceRouteFromBackend(serviceNo: string | number) {
  if (!serviceNo) return
  try {
    const resp = await getBusRouteByService(serviceNo)
    const directions = (resp?.directions || []).map((d: any) => {
      const polylines = buildColoredPolylinesFromDirection(d)
      const points = dedupeConsecutive(d.coordinates || [])
      return {
        dir: Number(d.direction ?? 1),
        points,
        stopCodes: [],
        roadPath: points,
        polylines,
      }
    })

    if (!directions.length) {
      alert(`No geometry for service ${serviceNo}`)
      return
    }

    store.setServiceRouteOverlay?.({
      serviceNo: String(resp?.service ?? serviceNo),
      directions
    })

    ;(store as any).setColoredPolylines?.(
      directions.flatMap((d: any) => d.polylines || [])
      )
    ;(store as any).fitToOverlayBounds?.()
  } catch (e: any) {
    console.error(e)
    alert(`Failed to load route for ${serviceNo}: ${e?.message || e}`)
  }
}
</script>

<template>
  <!-- PAGE WRAPPER -->
  <div
    class="min-h-screen w-full bg-gradient-to-br from-[#eaf4ef] via-[#f8fafc] to-[#f4f9f6] text-gray-800 p-4"
  >
    <!-- Main grid -->
    <div class="h-[calc(100vh-2rem)] grid grid-cols-12 gap-5">

      <!-- LEFT SIDEBAR -->
      <aside class="col-span-3 flex flex-col gap-5 min-h-0">

        <!-- Header / Branding Card -->
        <div
          class="rounded-2xl border border-[#007b3a]/20 bg-white/80 shadow-sm backdrop-blur-sm px-4 py-3 flex items-start gap-3"
        >
          <div
            class="h-10 w-10 flex items-center justify-center rounded-xl bg-[#007b3a] text-white font-bold text-sm shadow-md"
            title="Public Transport Flood Impact Dashboard"
          >
            🚍
          </div>

          <div class="flex-1 min-w-0">
            <div class="text-sm font-semibold text-gray-900 leading-tight">
              Flood-Viz Transit
            </div>
            <div class="text-[11px] text-gray-500 leading-snug">
              Bus availability & flood impact around Singapore
            </div>
          </div>
        </div>

        <!-- TAB SWITCHER (Itinerary / Flood only) -->
        <div
          class="rounded-2xl shadow-inner bg-gradient-to-r from-[#007b3a]/10 to-[#00b36b]/10 border border-[#007b3a]/20 p-3"
        >
          <div class="grid grid-cols-2 gap-2 text-[13px] font-semibold">

            <!-- Itinerary -->
            <button
              class="py-2 rounded-lg transition-all duration-200 leading-snug text-center"
              :class="activeTab === 'itinerary'
                ? 'bg-[#6a1b9a] text-white shadow-md shadow-[#6a1b9a]/30'
                : 'bg-white text-[#6a1b9a] border border-[#6a1b9a]/30 hover:bg-[#faf5ff]'"
              @click="setTab('itinerary')"
            >
              <div class="flex flex-col">
                <span class="flex items-center justify-center gap-1">
                  <span class="text-[14px]">🧭</span>
                  <span>Itinerary</span>
                </span>
              </div>
            </button>

            <!-- Flood Impact -->
            <button
              class="py-2 rounded-lg transition-all duration-200 leading-snug text-center"
              :class="activeTab === 'flood'
                ? 'bg-[#c62828] text-white shadow-md shadow-[#c62828]/30'
                : 'bg-white text-[#c62828] border border-[#c62828]/30 hover:bg-[#fff5f5]'"
              @click="setTab('flood')"
            >
              <div class="flex flex-col">
                <span class="flex items-center justify-center gap-1">
                  <span class="text-[14px]">🌧️</span>
                  <span>Affected</span>
                </span>
                <span class="-mt-0.5">Buses</span>
              </div>
            </button>
          </div>
        </div>

        <!-- PANEL UNDER TABS -->
        <div
          class="rounded-2xl border border-gray-200/70 bg-white/90 shadow-sm backdrop-blur-sm px-4 py-4 min-h-[240px] flex flex-col"
        >
          <!-- ITINERARY TAB -->
          <template v-if="activeTab === 'itinerary'">
            <div class="flex items-center gap-2 text-sm font-semibold text-gray-800 mb-3">
              <span class="inline-flex h-7 w-7 items-center justify-center rounded-md bg-[#6a1b9a] text-white text-xs font-bold shadow">
                1
              </span>
              <span>Compare itineraries</span>
            </div>

            <StopDetailsPanel mode="itinerary" />

            <p class="text-[11px] text-gray-500 mt-4 leading-snug">
              We’ll consider transfers, wait time and walking to suggest the smoothest journey.
            </p>
          </template>

          <!-- FLOOD TAB -->
          <template v-else>
            <div class="flex items-center gap-2 text-sm font-semibold text-gray-800 mb-3">
              <span class="inline-flex h-7 w-7 items-center justify-center rounded-md bg-[#c62828] text-white text-xs font-bold shadow">
                !
              </span>
              <span>Flood impact near bus stops</span>
            </div>

            <!-- instructions -->
            <div v-if="!selectedFloodId" class="text-[12px] text-gray-600 leading-snug mb-3">
              Click a <span class="font-medium text-[#c62828]">flood marker</span> on the map
              to list bus services affected.
            </div>

            <!-- details -->
            <div v-else class="space-y-2">
              <div class="text-[12px] text-gray-500 leading-snug">
                Flood ID:
                <span class="font-medium text-gray-800">{{ selectedFloodId }}</span>
              </div>

              <div v-if="loadingAffected" class="text-[12px] text-gray-700 animate-pulse">
                Checking nearby routes…
              </div>

              <div v-else-if="affectedError" class="text-[12px] text-red-600">
                {{ affectedError }}
              </div>

              <div
                v-else-if="!affectedServices.length"
                class="text-[12px] text-gray-600 leading-snug"
              >
                No affected bus services reported for this location.
              </div>

              <ul
                v-else
                class="space-y-1 max-h-40 overflow-y-auto pr-1"
              >
                <li
                  v-for="svc in affectedServices"
                  :key="svc"
                  class="px-3 py-2 border border-[#007b3a]/20 rounded-lg text-[13px] bg-[#f9fff9] flex items-center justify-between
                         hover:bg-[#eefcf2] cursor-pointer transition-colors"
                  @click="drawServiceRouteFromBackend(svc)"   
                  title="Show this service route on the map"
                >
                  <div class="font-semibold text-[#007b3a] flex items-center gap-2">
                    <span
                      class="inline-flex items-center justify-center text-[11px] font-bold leading-none text-white bg-[#007b3a] rounded px-2 py-1 shadow-sm"
                    >
                      BUS
                    </span>
                    <span>Service {{ svc }}</span>
                  </div>

                  <svg
                    class="h-4 w-4 text-gray-400"
                    viewBox="0 0 20 20"
                    fill="currentColor"
                    aria-hidden="true"
                  >
                    <path
                      fill-rule="evenodd"
                      d="M7.21 14.77a.75.75 0 0 1-.02-1.06L10.17 10 7.2 6.29a.75.75 0 1 1 1.1-1.02l3.5 3.75a.75.75 0 0 1 0 1.02l-3.5 3.75a.75.75 0 0 1-1.08-.02z"
                      clip-rule="evenodd"
                    />
                  </svg>
                </li>
              </ul>
            </div>

          </template>
        </div>

      </aside>

      <!-- RIGHT: CHART + MAP -->
      <section class="col-span-9 min-h-0 flex flex-col">
        <div
          class="flex-1 rounded-2xl border border-gray-200/70 bg-white/80 shadow-sm backdrop-blur-sm p-4 flex flex-col min-h-0"
        >
          <!-- CHART CARD -->
          <div v-if="chartEntry" class="mb-4 rounded-xl border border-gray-200 bg-white shadow-sm p-4">
            <div class="flex items-start justify-between flex-wrap gap-2 mb-3">
              <div>
                <div class="text-sm font-semibold text-gray-800 flex items-center gap-2">
                  <span
                    class="inline-flex items-center justify-center rounded bg-[#004b87] text-white text-[10px] font-bold leading-none h-5 px-2 shadow"
                  >
                    ETA
                  </span>
                  <span>Travel Time Scenarios</span>
                </div>
                <div class="text-[11px] text-gray-500 leading-snug mt-1">
                  Baseline vs flood slowdown along suggested route
                </div>
              </div>

              <div class="text-[10px] text-gray-400 leading-tight max-w-[180px]">
                Values are modelled. Actual road closure / bus diversion may differ.
              </div>
            </div>

            <TravelTimeBarChart
              :entry="chartEntry"
              title="Travel Time Scenarios"
            />
          </div>

          <!-- MAP CARD -->
          <div
            class="flex-1 min-h-0 overflow-hidden rounded-xl border-2 border-[#007b3a]/20 shadow-inner bg-white relative"
          >
            <!-- subtle top label bar -->
            <div
              class="absolute left-0 right-0 top-0 z-[5] flex items-center justify-between text-[11px] text-gray-700 bg-gradient-to-r from-white/80 via-[#f0fff5]/80 to-white/80 px-3 py-2 border-b border-[#007b3a]/20"
            >
              <span class="flex items-center gap-2 font-medium text-[#007b3a]">
                <span
                  class="inline-flex items-center justify-center rounded bg-[#007b3a] text-white text-[10px] font-bold leading-none h-5 px-2 shadow-sm"
                >
                  MAP
                </span>
                <span>Singapore Bus & Flood View</span>
              </span>
              <span class="text-gray-400">
                Click a stop or flood marker for details
              </span>
            </div>

            <!-- actual map -->
            <div class="absolute inset-0 pt-[34px]">
              <MapCanvas @flood-click="onFloodClick" />
            </div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>
