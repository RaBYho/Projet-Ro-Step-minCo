<template>
  <div class="flex flex-col items-center gap-8 py-12">
    <!-- Spinner -->
    <div class="relative w-20 h-20">
      <svg class="w-20 h-20 animate-spin" viewBox="0 0 80 80">
        <circle cx="40" cy="40" r="34" fill="none" stroke="currentColor"
          class="text-stone-200 dark:text-gray-800" stroke-width="6"/>
        <circle cx="40" cy="40" r="34" fill="none"
          stroke="url(#grad)" stroke-width="6"
          stroke-linecap="round" stroke-dasharray="60 154"/>
        <defs>
          <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#6366f1"/>
            <stop offset="100%" stop-color="#8b5cf6"/>
          </linearGradient>
        </defs>
      </svg>
      <div class="absolute inset-0 flex items-center justify-center">
        <div class="w-8 h-8 rounded-xl bg-indigo-600 flex items-center justify-center">
          <svg class="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7"/>
          </svg>
        </div>
      </div>
    </div>

    <!-- Barres de progression -->
    <div class="w-72 flex flex-col gap-4">
      <div v-for="(b, i) in barres" :key="i">
        <div class="flex justify-between text-xs mb-1.5">
          <span :class="b.actif ? 'text-indigo-600 dark:text-indigo-400 font-medium'
            : b.done ? 'text-gray-400 dark:text-gray-500' : 'text-gray-300 dark:text-gray-600'">
            {{ b.label }}
          </span>
          <span :class="b.done ? 'text-emerald-500' : b.actif ? 'text-indigo-500' : 'text-gray-300 dark:text-gray-700'"
            class="font-mono">
            {{ b.done ? '✓' : b.actif ? b.progress + '%' : '—' }}
          </span>
        </div>
        <div class="h-1.5 rounded-full bg-stone-100 dark:bg-gray-800 overflow-hidden">
          <div class="h-full rounded-full transition-all duration-300"
            :class="b.done ? 'bg-emerald-400' : 'bg-indigo-500'"
            :style="{ width: b.done ? '100%' : b.actif ? b.progress + '%' : '0%' }">
          </div>
        </div>
      </div>
    </div>

    <p class="text-sm text-gray-400 dark:text-gray-500 animate-pulse">{{ message }}</p>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
defineProps({ message: String })

const barres = ref([
  { label: 'Connexion serveur', progress: 0, actif: false, done: false },
  { label: 'Solution initiale (Coût Min.)', progress: 0, actif: false, done: false },
  { label: 'Optimisation Stepping Stone', progress: 0, actif: false, done: false },
])
let etape = 0, iv = null

function avancer() {
  if (etape >= barres.value.length) return
  const b = barres.value[etape]
  b.actif = true
  iv = setInterval(() => {
    b.progress = Math.min(100, b.progress + Math.floor(Math.random() * 18) + 5)
    if (b.progress >= 100) {
      b.done = true; b.actif = false
      clearInterval(iv); etape++
      setTimeout(avancer, 250)
    }
  }, 180)
}
onMounted(() => setTimeout(avancer, 200))
onUnmounted(() => clearInterval(iv))
</script>
