<template>
  <div
    class="flex flex-col items-center justify-center gap-10 py-16 min-h-[50vh]"
  >
    <!-- Spinner -->
    <div class="relative w-16 h-16">
      <svg class="w-16 h-16 animate-spin" viewBox="0 0 80 80">
        <circle
          cx="40"
          cy="40"
          r="34"
          fill="none"
          stroke="currentColor"
          class="text-stone-200 dark:text-gray-800"
          stroke-width="5"
        />
        <circle
          cx="40"
          cy="40"
          r="34"
          fill="none"
          :stroke="`url(#grad-${uid})`"
          stroke-width="5"
          stroke-linecap="round"
          stroke-dasharray="60 154"
        />
        <defs>
          <linearGradient :id="`grad-${uid}`" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#6366f1" />
            <stop offset="100%" stop-color="#8b5cf6" />
          </linearGradient>
        </defs>
      </svg>
      <div class="absolute inset-0 flex items-center justify-center">
        <div
          class="w-7 h-7 rounded-lg bg-indigo-600 flex items-center justify-center shadow-lg shadow-indigo-500/30"
        >
          <svg
            class="w-3.5 h-3.5 text-white"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7"
            />
          </svg>
        </div>
      </div>
    </div>

    <!-- Barres de progression -->
    <div class="w-72 flex flex-col gap-5">
      <div v-for="(b, i) in barres" :key="i">
        <div class="flex justify-between text-xs mb-1.5">
          <span
            :class="
              b.actif
                ? 'text-indigo-600 dark:text-indigo-400 font-medium'
                : b.done
                  ? 'text-stone-400 dark:text-stone-500'
                  : 'text-stone-300 dark:text-stone-600'
            "
          >
            {{ b.label }}
          </span>
          <span
            :class="
              b.done
                ? 'text-emerald-500'
                : b.actif
                  ? 'text-indigo-500'
                  : 'text-stone-300 dark:text-stone-700'
            "
            class="font-mono tabular-nums"
          >
            {{ b.done ? "✓" : b.actif ? b.progress + "%" : "—" }}
          </span>
        </div>
        <div
          class="h-2 rounded-full bg-stone-100 dark:bg-gray-800 overflow-hidden"
        >
          <div
            class="h-full rounded-full transition-all duration-500 ease-out"
            :class="b.done ? 'bg-emerald-500' : 'bg-indigo-500'"
            :style="{
              width: b.done ? '100%' : b.actif ? b.progress + '%' : '0%',
            }"
          ></div>
        </div>
      </div>
    </div>

    <!-- Message -->
    <p class="text-sm text-stone-500 dark:text-stone-400 animate-pulse">
      {{ message }}
    </p>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from "vue";

const props = defineProps({ message: String, isDark: Boolean });

// Identifiant unique pour le gradient SVG
const uid = Math.random().toString(36).slice(2, 9);

const barres = ref([
  { label: "Connexion serveur", progress: 0, actif: false, done: false },
  {
    label: "Solution initiale (Coût Min.)",
    progress: 0,
    actif: false,
    done: false,
  },
  {
    label: "Optimisation Stepping Stone",
    progress: 0,
    actif: false,
    done: false,
  },
]);

let etape = 0,
  iv = null;

function avancer() {
  if (etape >= barres.value.length) return;
  const b = barres.value[etape];
  b.actif = true;
  iv = setInterval(() => {
    b.progress = Math.min(100, b.progress + Math.floor(Math.random() * 18) + 5);
    if (b.progress >= 100) {
      b.done = true;
      b.actif = false;
      clearInterval(iv);
      etape++;
      setTimeout(avancer, 250);
    }
  }, 180);
}

onMounted(() => setTimeout(avancer, 200));
onUnmounted(() => clearInterval(iv));
</script>
