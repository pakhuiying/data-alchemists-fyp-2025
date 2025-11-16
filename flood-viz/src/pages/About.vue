<script setup lang="ts">
</script>

<template>
  <div
    class="min-h-screen w-full bg-gradient-to-br from-[#eef2ff] via-[#f8fafc] to-[#ecfeff] text-gray-800 p-6"
  >
    <div class="max-w-4xl mx-auto space-y-6">
      <!-- Header -->
      <div class="flex items-start gap-3">
        <div
          class="h-11 w-11 flex items-center justify-center rounded-xl bg-indigo-600 text-white font-bold shadow"
        >
          ℹ️
        </div>
        <div>
          <h1 class="text-2xl font-semibold text-gray-900">
            About Flood-Viz
          </h1>
          <p class="text-sm text-gray-600 mt-1">
            A research dashboard exploring flood impact on Singapore’s transport network.
          </p>
        </div>
      </div>

      <!-- What this project is -->
      <div class="rounded-2xl p-5 bg-white/90 shadow-sm border border-gray-200 space-y-3">
        <h2 class="text-lg font-semibold text-gray-900">What this project does</h2>
        <p class="text-sm text-gray-700 leading-relaxed">
          Flood-Viz is an interactive geospatial dashboard designed to help users understand
          how flood events affect mobility across Singapore. By combining historical flood
          locations, road-network centrality, and transport routing, the system allows
          students, planners, and researchers to explore travel vulnerabilities in a
          data-driven way.
        </p>
      </div>

      <!-- Key features -->
      <div class="rounded-2xl p-5 bg-white/90 shadow-sm border border-gray-200 space-y-3">
        <h2 class="text-lg font-semibold text-gray-900">Key features</h2>

        <ul class="text-sm text-gray-700 space-y-2 leading-relaxed">
          <li>
            <span class="font-semibold text-indigo-700">• Flood Operations View</span> —
            Explore historical flood hotspots, inspect event details, and examine nearby
            critical road segments using network centrality.
          </li>

          <li>
            <span class="font-semibold text-emerald-700">• Public Transport View</span> —
            Visualise bus stops, bus routes, and check which services may be affected when a
            flood occurs near a transport corridor.
          </li>

          <li>
            <span class="font-semibold text-sky-700">• Private Transport View</span> —
            Simulate car travel time under different flood-slowdown scenarios to understand
            how travel speeds and routing are impacted.
          </li>
        </ul>
      </div>

      <!-- Why this matters -->
      <div class="rounded-2xl p-5 bg-white/90 shadow-sm border border-gray-200 space-y-3">
        <h2 class="text-lg font-semibold text-gray-900">Why this research matters</h2>
        <p class="text-sm text-gray-700 leading-relaxed">
          With Singapore’s increasing rainfall intensity and rising urban density, even
          localised flooding can disrupt road traffic and public transport. Flood-Viz enables
          transparent exploration of these interactions — helping improve resilience planning,
          inform policy discussions, and support academic analysis.
        </p>
      </div>

      <!-- Footer text -->
      <p class="text-xs text-gray-500 text-center mt-8">
        Built as a student research project — Data Alchemists FYP 2025.
      </p>
    </div>
  </div>
</template>

<style scoped>
/* subtle page fade-in */
:root {
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(6px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
