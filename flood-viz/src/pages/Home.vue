<script setup lang="ts">
import { ref } from 'vue'

/* ─────────────────────────────
   VIDEO CAROUSEL STATE
   ───────────────────────────── */
const currentSlide = ref(0)
const totalSlides = 2

function nextSlide() {
  currentSlide.value = (currentSlide.value + 1) % totalSlides
}

function prevSlide() {
  currentSlide.value = (currentSlide.value - 1 + totalSlides) % totalSlides
}

function goToSlide(n: number) {
  currentSlide.value = n
}
</script>

<template>
  <!-- FULL BLEED WRAPPER -->
  <div
    class="full-bleed w-screen min-h-screen text-slate-800 relative overflow-hidden bg-gradient-to-b from-sky-100 via-sky-50 to-slate-100"
  >
    <!-- ===== BACKGROUND LAYERS ===== -->
    <div aria-hidden="true" class="absolute inset-0 w-full overflow-hidden">
      <!-- Soft color blobs -->
      <div class="absolute -top-40 -left-40 size-[520px] rounded-full bg-sky-300/30 blur-3xl"></div>
      <div class="absolute -bottom-20 left-1/2 -translate-x-1/2 size-[640px] rounded-full bg-indigo-300/20 blur-3xl"></div>
      <div class="absolute -right-40 top-1/4 size-[480px] rounded-full bg-cyan-300/25 blur-3xl"></div>

      <!-- Animated raindrop pattern -->
      <svg
        aria-hidden="true"
        class="absolute inset-0 opacity-[0.18] animate-rain"
        width="100%"
        height="100%"
        preserveAspectRatio="none"
      >
        <defs>
          <pattern id="drops" x="0" y="0" width="40" height="40" patternUnits="userSpaceOnUse">
            <path d="M8 10c0-3 4-3 4 0 0 2-2 4-2 4s-2-2-2-4z" fill="#38bdf8" />
            <path d="M28 30c0-3 4-3 4 0 0 2-2 4-2 4s-2-2-2-4z" fill="#38bdf8" />
            <circle cx="24" cy="12" r="1.2" fill="#38bdf8" />
            <circle cx="14" cy="28" r="1.2" fill="#38bdf8" />
          </pattern>
        </defs>
        <rect x="0" y="0" width="100%" height="100%" fill="url(#drops)" />
      </svg>

      <!-- Mist / Vignette -->
      <div class="absolute inset-x-0 top-0 h-32 sm:h-48 bg-gradient-to-b from-white/80 to-transparent"></div>

      <!-- Waves at bottom -->
      <div class="absolute inset-x-0 bottom-0">
        <svg class="w-full h-20 sm:h-28 block opacity-70" viewBox="0 0 1440 160" preserveAspectRatio="none">
          <path
            d="M0,64 C160,128 320,0 480,48 C640,96 800,176 960,144 C1120,112 1280,48 1440,96 L1440,160 L0,160 Z"
            fill="url(#waveFill)"
          />
          <defs>
            <linearGradient id="waveFill" x1="0" x2="0" y1="0" y2="1">
              <stop offset="0%" stop-color="#60a5fa" stop-opacity="0.45" />
              <stop offset="100%" stop-color="#0ea5e9" stop-opacity="0.35" />
            </linearGradient>
          </defs>
        </svg>
      </div>
    </div>

    <!-- ===== PAGE CONTENT ===== -->
    <main class="relative z-10">
      <!-- HERO -->
      <section class="py-16 sm:py-24 px-4 sm:px-6 lg:px-8">
        <div class="max-w-5xl mx-auto text-center">
          <h1 class="text-3xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight drop-shadow-sm">
            Smarter Routes, Safer Commutes
          </h1>
          <p class="mt-4 text-slate-700/90 text-base sm:text-lg leading-relaxed max-w-2xl mx-auto">
            Discover how flooding impacts Singapore’s transport network — visualize affected roads and bus routes
            in real time with our interactive platform.
          </p>

          <div
            class="mt-6 sm:mt-8 mx-auto w-full sm:w-fit rounded-2xl border border-slate-300 bg-white/70 backdrop-blur-md shadow-md"
          >
            <div
              class="p-3 flex flex-col sm:flex-row items-center justify-center gap-1 sm:gap-2 text-xs sm:text-sm text-slate-600"
            >
              💡 Flood-aware routing • Live overlays • Delay analytics
            </div>
          </div>

          <div
            class="mt-6 sm:mt-7 flex flex-col sm:flex-row justify-center gap-3 sm:gap-4 w-full sm:w-auto max-w-md mx-auto"
          >
            <a
              href="#video"
              class="w-full sm:w-auto px-6 py-3 rounded-xl font-semibold bg-blue-600 text-white shadow-md hover:bg-blue-700 transition text-sm sm:text-base"
            >
              Watch Demo
            </a>
            <a
              href="#features"
              class="w-full sm:w-auto px-6 py-3 rounded-xl font-semibold border border-slate-300 bg-white/70 backdrop-blur hover:bg-slate-100 transition text-sm sm:text-base"
            >
              Learn More
            </a>
          </div>
        </div>
      </section>

      <!-- FEATURES -->
      <section id="features" class="py-12 sm:py-16 bg-white/70 backdrop-blur">
        <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 class="text-2xl sm:text-3xl font-extrabold text-center">Key Features</h2>
          <p class="mt-3 text-center text-slate-600 text-sm sm:text-base max-w-2xl mx-auto">
            Understand where floods occur, which roads and services are most affected, and how delays propagate
            through the network.
          </p>

          <div class="mt-8 sm:mt-10 grid gap-5 sm:gap-6 sm:grid-cols-2 lg:grid-cols-3">
            <div class="card">
              <div class="text-2xl sm:text-3xl mb-2">🚌</div>
              <h3 class="font-semibold text-base sm:text-lg mb-1">Bus Services Visualization</h3>
              <p class="muted">
                See affected bus services on an interactive Leaflet map with hover details and clickable routes.
              </p>
            </div>
            <div class="card">
              <div class="text-2xl sm:text-3xl mb-2">🌧️</div>
              <h3 class="font-semibold text-base sm:text-lg mb-1">Flood Event Layers</h3>
              <p class="muted">
                Overlay flood polygons and points dynamically. Tooltip caching ensures instant details.
              </p>
            </div>
            <div class="card">
              <div class="text-2xl sm:text-3xl mb-2">🗺️</div>
              <h3 class="font-semibold text-base sm:text-lg mb-1">Route & Travel Delay Analysis</h3>
              <p class="muted">
                Compare baseline vs flooded travel times across different road segments with custom styling.
              </p>
            </div>
          </div>
        </div>
      </section>

      <!-- VIDEO SECTION (CAROUSEL) -->
      <section id="video" class="py-12 sm:py-16">
        <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 class="text-2xl sm:text-3xl font-extrabold mb-4 sm:mb-6">Demo Videos</h2>
          <p class="text-slate-600 text-sm sm:text-base max-w-2xl mx-auto mb-6">
            Explore our walkthroughs showing how Flood-Viz helps planners and commuters understand flood impacts on the go.
          </p>

          <!-- CAROUSEL WRAPPER -->
          <div class="relative w-full max-w-4xl mx-auto">
            <!-- Slides -->
            <div class="overflow-hidden rounded-xl shadow-lg bg-slate-200/40 backdrop-blur">
              <div
                class="whitespace-nowrap transition-transform duration-500"
                :style="{ transform: `translateX(-${currentSlide * 100}%)` }"
              >
                <!-- Slide 1 -->
                <div class="inline-block w-full">
                  <div class="video-frame">
                    <iframe
                      class="w-full h-full"
                      src="https://www.youtube.com/embed/25zSy3B9G0M?si=LeQiPKZs5gIMt-p3"
                      title="Flood-Viz Demo Video 1"
                      frameborder="0"
                      allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                      allowfullscreen
                    ></iframe>
                  </div>
                </div>

                <!-- Slide 2 -->
                <div class="inline-block w-full">
                  <div class="video-frame">
                    <iframe
                      class="w-full h-full"
                      src="https://www.youtube.com/embed/uT3dUmaStpk?si=18cRmpAIZvqXRN-o"
                      title="Flood-Viz Demo Video 2"
                      frameborder="0"
                      allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                      allowfullscreen
                    ></iframe>
                  </div>
                </div>
              </div>
            </div>

            <!-- Prev Button -->
            <button
              @click="prevSlide"
              class="absolute top-1/2 left-2 -translate-y-1/2 bg-white/80 backdrop-blur rounded-full p-2.5 shadow-md hover:bg-white hover:shadow-lg transition flex items-center justify-center"
              aria-label="Previous video"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 24 24"
                class="w-5 h-5 text-slate-700"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
              >
                <path d="M15 19l-7-7 7-7" />
              </svg>
            </button>

            <!-- Next Button -->
            <button
              @click="nextSlide"
              class="absolute top-1/2 right-2 -translate-y-1/2 bg-white/80 backdrop-blur rounded-full p-2.5 shadow-md hover:bg-white hover:shadow-lg transition flex items-center justify-center"
              aria-label="Next video"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 24 24"
                class="w-5 h-5 text-slate-700"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
              >
                <path d="M9 5l7 7-7 7" />
              </svg>
            </button>

            <!-- Dots -->
            <div class="mt-4 flex justify-center gap-2">
              <span
                v-for="n in totalSlides"
                :key="n"
                @click="goToSlide(n - 1)"
                class="cursor-pointer w-3 h-3 rounded-full transition"
                :class="currentSlide === (n - 1) ? 'bg-blue-600' : 'bg-slate-300'"
              ></span>
            </div>
          </div>
        </div>
      </section>
    </main>

    <!-- FOOTER -->
    <footer
      class="relative z-10 py-6 sm:py-10 border-t border-slate-200 text-center text-xs sm:text-sm text-slate-600 bg-white/70 backdrop-blur px-4"
    >
      © {{ new Date().getFullYear() }} Flood-Viz. All rights reserved.
    </footer>
  </div>
</template>

<style scoped lang="postcss">
/* Force full-bleed even inside centered layouts */
.full-bleed {
  position: relative;
  left: 50%;
  right: 50%;
  margin-left: -50vw;
  margin-right: -50vw;
  width: 100vw;
}

.muted {
  @apply text-slate-600 text-sm sm:text-[0.95rem] leading-relaxed;
}

.card {
  @apply h-full p-5 sm:p-6 rounded-xl border border-slate-200 bg-white/80 backdrop-blur shadow-sm hover:shadow-md transition flex flex-col;
}

.video-frame {
  @apply relative aspect-[16/9] w-full max-w-4xl mx-auto rounded-xl overflow-hidden shadow-lg;
}

/* Rain animation */
@keyframes rainShift {
  0% {
    transform: translate3d(0, 0, 0);
  }
  100% {
    transform: translate3d(-80px, 120px, 0);
  }
}

.animate-rain {
  animation: rainShift 18s linear infinite;
}

@media (prefers-reduced-motion: reduce) {
  .animate-rain {
    animation: none !important;
  }
}

/* Light headline glow */
:where(h1, h2, h3) {
  text-shadow: 0 1px 0 rgba(255, 255, 255, 0.15);
}
</style>

<style>
html,
body {
  overflow-x: hidden;
  background: #f8fafc; /* Tailwind slate-50 */
}
</style>
