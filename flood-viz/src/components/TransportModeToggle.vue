<script setup lang="ts">
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

const currentMode = computed<'public' | 'private'>(() =>
  route.path === '/PrivateTransport' ? 'private' : 'public'
)

function switchMode(mode: 'public' | 'private') {
  if (mode === currentMode.value) return
  router.push(mode === 'public' ? '/PublicTransport' : '/PrivateTransport')
}
</script>

<template>
  <!-- Fixed bottom-centre pill -->
  <div class="fixed bottom-4 left-1/2 -translate-x-1/2 z-30 fade-in">
    <div
      class="inline-flex items-center gap-1 rounded-full bg-white/90 border border-gray-200 shadow-lg
             px-2 py-1 text-[12px] sm:text-[13px] backdrop-blur"
    >
      <!-- Public -->
      <button
        class="px-3 py-1 rounded-full font-medium transition-all"
        :class="currentMode === 'public'
          ? 'bg-emerald-600 text-white shadow'
          : 'text-emerald-700 hover:bg-emerald-50'"
        @click="switchMode('public')"
      >
        🚍 Public
      </button>

      <span class="w-px h-4 bg-gray-200" />

      <!-- Private -->
      <button
        class="px-3 py-1 rounded-full font-medium transition-all"
        :class="currentMode === 'private'
          ? 'bg-indigo-600 text-white shadow'
          : 'text-indigo-700 hover:bg-indigo-50'"
        @click="switchMode('private')"
      >
        🚗 Private
      </button>
    </div>
  </div>
</template>

<style scoped>
.fade-in {
  animation: fadeIn 0.28s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translate(-50%, 10px);
  }
  to {
    opacity: 1;
    transform: translate(-50%, 0);
  }
}
</style>
