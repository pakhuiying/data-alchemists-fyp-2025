<script setup lang="ts">
import { RouterLink, RouterView, useRoute } from 'vue-router'
import { computed, ref, watch } from 'vue'

const route = useRoute()

const navItems = [
  { name: 'Home', path: '/' },
  { name: 'About', path: '/about' },
  { name: 'Public Transport', path: '/PublicTransport' },
  { name: 'Private Transport', path: '/PrivateTransport' },
  { name: 'Flood Vulnerabilities', path: '/Flood' },
  // { name: 'Critical Roads', path: '/CriticalRoad' },
]

const isActive = (path: string) =>
  computed(() => route.path === path)

const isNavOpen = ref(false)

// Close mobile menu whenever route changes
watch(
  () => route.path,
  () => {
    isNavOpen.value = false
  }
)
</script>

<template>
  <div class="min-h-screen w-screen bg-gray-50 flex flex-col">
    <!-- HEADER -->
    <header class="bg-white shadow-sm border-b">
      <div
        class="max-w-7xl mx-auto h-16 px-4 sm:px-6 lg:px-10 flex items-center justify-between gap-4"
      >
        <!-- Logo -->
        <h1 class="font-bold text-xl sm:text-2xl text-blue-600 tracking-wide whitespace-nowrap">
          Flood-Viz
        </h1>

        <!-- Desktop nav (≥ md) -->
        <nav class="hidden md:flex text-sm sm:text-base items-center gap-6 lg:gap-8">
          <RouterLink
            v-for="item in navItems"
            :key="item.path"
            :to="item.path"
            :class="[
              'transition-colors duration-200 hover:text-blue-600',
              isActive(item.path).value
                ? 'text-blue-600 font-semibold'
                : 'text-gray-700'
            ]"
          >
            {{ item.name }}
          </RouterLink>
        </nav>

        <!-- Mobile hamburger (< md) -->
        <button
          type="button"
          class="md:hidden inline-flex items-center justify-center p-2 rounded-md border border-gray-200 text-gray-700 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
          @click="isNavOpen = !isNavOpen"
          aria-label="Toggle navigation"
        >
          <span v-if="!isNavOpen">
            <!-- hamburger icon -->
            <svg class="h-5 w-5" viewBox="0 0 24 24" fill="none">
              <path
                d="M4 7h16M4 12h16M4 17h16"
                stroke="currentColor"
                stroke-width="1.8"
                stroke-linecap="round"
              />
            </svg>
          </span>
          <span v-else>
            <!-- X icon -->
            <svg class="h-5 w-5" viewBox="0 0 24 24" fill="none">
              <path
                d="M6 6l12 12M18 6l-12 12"
                stroke="currentColor"
                stroke-width="1.8"
                stroke-linecap="round"
              />
            </svg>
          </span>
        </button>
      </div>

      <!-- Mobile nav panel -->
      <nav v-if="isNavOpen" class="md:hidden border-t border-gray-100 bg-white">
        <div class="px-4 py-2 flex flex-col space-y-1">
          <RouterLink
            v-for="item in navItems"
            :key="item.path"
            :to="item.path"
            class="block px-2 py-2 rounded-md text-sm font-medium transition-colors"
            :class="[
              isActive(item.path).value
                ? 'text-blue-600 bg-blue-50'
                : 'text-gray-700 hover:bg-gray-100'
            ]"
          >
            {{ item.name }}
          </RouterLink>
        </div>
      </nav>
    </header>

    <!-- MAIN CONTENT -->
    <main class="flex-1 overflow-y-auto p-4 sm:p-6 lg:p-8">
      <RouterView />
    </main>
  </div>
</template>
