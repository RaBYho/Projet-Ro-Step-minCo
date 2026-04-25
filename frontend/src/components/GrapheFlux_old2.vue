<template>
  <div class="w-full">

    <!-- Toggle potentiels / flux -->
    <div class="flex items-center gap-2 mb-3">
      <span class="text-xs text-gray-400 dark:text-gray-500">Afficher sur les nœuds :</span>
      <div class="flex gap-1 bg-stone-100 dark:bg-gray-800 p-0.5 rounded-lg">
        <button @click="mode = 'potentiels'"
          :class="mode === 'potentiels'
            ? 'bg-white dark:bg-gray-900 shadow text-gray-800 dark:text-white'
            : 'text-gray-400 dark:text-gray-500'"
          class="px-3 py-1 rounded-md text-xs font-semibold transition-all">
          Potentiels u, v
        </button>
        <button @click="mode = 'flux'"
          :class="mode === 'flux'
            ? 'bg-white dark:bg-gray-900 shadow text-gray-800 dark:text-white'
            : 'text-gray-400 dark:text-gray-500'"
          class="px-3 py-1 rounded-md text-xs font-semibold transition-all">
          Offre / Demande
        </button>
      </div>
    </div>

    <svg :viewBox="`0 0 ${W} ${H}`" class="w-full h-auto" style="min-height:220px">

      <!-- Arêtes -->
      <g v-for="lien in liens" :key="`${lien.i}-${lien.j}`">
        <line
          :x1="sourceX" :y1="positionsSource[lien.i]"
          :x2="destX"   :y2="positionsDest[lien.j]"
          :class="getLienClass(lien)"
          :stroke-width="getLienEpaisseur(lien)"
          class="transition-all duration-500"
          stroke-linecap="round"
        />
        <!-- Valeur de flux sur l'arête (si flux actif) -->
        <text v-if="lien.flux > 1e-6"
          :x="(sourceX + destX) / 2"
          :y="(positionsSource[lien.i] + positionsDest[lien.j]) / 2 - 6"
          text-anchor="middle" dominant-baseline="middle"
          class="select-none"
          :fill="estDansCycle(lien.i, lien.j) ? '#a78bfa' : '#9ca3af'"
          font-size="9" font-weight="500">
          {{ lien.flux.toFixed(0) }}
        </text>
      </g>

      <!-- Flèches directionnelles sur les arêtes actives -->
      <g v-for="lien in liensActifs" :key="`arrow-${lien.i}-${lien.j}`">
        <polygon
          :points="getArrowPoints(positionsSource[lien.i], positionsDest[lien.j])"
          :class="getArrowClass(lien)"
          class="transition-all duration-500"
        />
      </g>

      <!-- Nœuds sources (gauche) -->
      <g v-for="(source, i) in metadata.sources" :key="`s${i}`">
        <!-- Cercle principal -->
        <circle
          :cx="sourceX" :cy="positionsSource[i]" r="24"
          :class="isSourceActive(i)
            ? 'fill-indigo-500'
            : 'fill-indigo-50 dark:fill-gray-800'"
          class="transition-all duration-400"
          :stroke="isSourceActive(i) ? '#6366f1' : '#a5b4fc'"
          stroke-width="1.5"
        />
        <!-- Label U_i -->
        <text :x="sourceX" :y="positionsSource[i] - 7"
          text-anchor="middle" dominant-baseline="middle"
          :fill="isSourceActive(i) ? '#ffffff' : '#6366f1'"
          font-size="9" font-weight="700" class="select-none">
          U{{ i+1 }}
        </text>
        <!-- Valeur potentiel u_i ou offre -->
        <text :x="sourceX" :y="positionsSource[i] + 7"
          text-anchor="middle" dominant-baseline="middle"
          :fill="isSourceActive(i) ? '#e0e7ff' : (mode === 'potentiels' ? '#4f46e5' : '#6b7280')"
          font-size="10" font-weight="600" class="select-none font-mono">
          {{ mode === 'potentiels' ? formatPotentiel(potentielsU[i]) : (config?.offres?.[i] ?? '') }}
        </text>
        <!-- Badge "u=" à gauche -->
        <text v-if="mode === 'potentiels'"
          :x="sourceX - 34" :y="positionsSource[i]"
          text-anchor="middle" dominant-baseline="middle"
          fill="#a5b4fc" font-size="8" class="select-none">
          u={{ formatPotentiel(potentielsU[i]) }}
        </text>
      </g>

      <!-- Nœuds destinations (droite) -->
      <g v-for="(dest, j) in metadata.destinations" :key="`d${j}`">
        <!-- Cercle principal -->
        <circle
          :cx="destX" :cy="positionsDest[j]" r="24"
          :class="isDestActive(j)
            ? 'fill-teal-500'
            : 'fill-teal-50 dark:fill-gray-800'"
          class="transition-all duration-400"
          :stroke="isDestActive(j) ? '#14b8a6' : '#5eead4'"
          stroke-width="1.5"
        />
        <!-- Label C_j -->
        <text :x="destX" :y="positionsDest[j] - 7"
          text-anchor="middle" dominant-baseline="middle"
          :fill="isDestActive(j) ? '#ffffff' : '#0d9488'"
          font-size="9" font-weight="700" class="select-none">
          C{{ j+1 }}
        </text>
        <!-- Valeur potentiel v_j ou demande -->
        <text :x="destX" :y="positionsDest[j] + 7"
          text-anchor="middle" dominant-baseline="middle"
          :fill="isDestActive(j) ? '#ccfbf1' : (mode === 'potentiels' ? '#0f766e' : '#6b7280')"
          font-size="10" font-weight="600" class="select-none font-mono">
          {{ mode === 'potentiels' ? formatPotentiel(potentielsV[j]) : (config?.demandes?.[j] ?? '') }}
        </text>
        <!-- Badge "v=" à droite -->
        <text v-if="mode === 'potentiels'"
          :x="destX + 36" :y="positionsDest[j]"
          text-anchor="middle" dominant-baseline="middle"
          fill="#5eead4" font-size="8" class="select-none">
          v={{ formatPotentiel(potentielsV[j]) }}
        </text>
      </g>

      <!-- Labels colonnes -->
      <text :x="sourceX" y="16" text-anchor="middle"
        fill="#818cf8" font-size="8" font-weight="700" letter-spacing="1" class="select-none">
        SOURCES
      </text>
      <text :x="destX" y="16" text-anchor="middle"
        fill="#2dd4bf" font-size="8" font-weight="700" letter-spacing="1" class="select-none">
        DESTINATIONS
      </text>

    </svg>

    <!-- Bandeau info potentiels non disponibles -->
    <div v-if="mode === 'potentiels' && !aPotentiels"
      class="mt-2 flex items-center gap-2 bg-amber-50 dark:bg-amber-900/20 border border-amber-200
        dark:border-amber-800 rounded-xl px-3 py-2 text-xs text-amber-600 dark:text-amber-400">
      <svg class="w-3.5 h-3.5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
          d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
      </svg>
      Potentiels u, v disponibles uniquement lors des étapes d'optimisation.
      Les nœuds affichent l'offre / demande pour l'instant.
    </div>

    <!-- Légende -->
    <div class="flex flex-wrap gap-3 mt-2 text-xs text-gray-400 dark:text-gray-500">
      <span class="flex items-center gap-1.5">
        <span class="w-5 h-0.5 bg-indigo-300 inline-block rounded"></span>Flux actif
      </span>
      <span class="flex items-center gap-1.5">
        <span class="w-5 h-0.5 bg-stone-200 dark:bg-gray-700 inline-block rounded"></span>Flux nul
      </span>
      <span v-if="cyclePresent" class="flex items-center gap-1.5">
        <span class="w-5 h-0.5 bg-violet-400 inline-block rounded"></span>Cycle ➕
      </span>
      <span v-if="cyclePresent" class="flex items-center gap-1.5">
        <span class="w-5 h-0.5 bg-rose-400 inline-block rounded"></span>Cycle ➖
      </span>
      <span v-if="mode === 'potentiels' && aPotentiels" class="flex items-center gap-1.5 ml-auto text-xs">
        <span class="text-indigo-400 font-mono">u<sub>i</sub></span>
        <span class="text-gray-300 mx-0.5">+</span>
        <span class="text-teal-400 font-mono">v<sub>j</sub></span>
        <span class="text-gray-400 ml-1">= c<sub>ij</sub> (cases de base)</span>
      </span>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'

const props = defineProps({
  flux:        Array,
  metadata:    Object,
  config:      Object,
  caseActive:  Array,
  cycle:       Array,
  potentiels:  Object   // { u: [...], v: [...] } — passé depuis AffichageEtapes
})

const mode = ref('potentiels')  // 'potentiels' | 'flux'

// ── Dimensions SVG ──────────────────────────────────────────────────────────
const W           = 360
const PADDING_TOP = 28
const PADDING_BOT = 16

const nbSources = computed(() => props.metadata.sources.length)
const nbDests   = computed(() => props.metadata.destinations.length)

const H = computed(() => {
  const maxN = Math.max(nbSources.value, nbDests.value)
  return PADDING_TOP + PADDING_BOT + maxN * 64
})

const sourceX = 85
const destX   = computed(() => W - 85)

function positions(n) {
  const total = H.value - PADDING_TOP - PADDING_BOT
  const step  = n > 1 ? total / (n - 1) : 0
  return Array.from({ length: n }, (_, i) =>
    n === 1 ? H.value / 2 : PADDING_TOP + i * step
  )
}

const positionsSource = computed(() => positions(nbSources.value))
const positionsDest   = computed(() => positions(nbDests.value))

// ── Potentiels ───────────────────────────────────────────────────────────────
const potentielsU = computed(() => props.potentiels?.u ?? [])
const potentielsV = computed(() => props.potentiels?.v ?? [])
const aPotentiels = computed(() =>
  potentielsU.value.length > 0 && potentielsU.value.some(v => v !== null)
)

function formatPotentiel(val) {
  if (val === null || val === undefined) return '—'
  return Number.isInteger(val) ? String(val) : val.toFixed(1)
}

// ── Liens ────────────────────────────────────────────────────────────────────
const liens = computed(() => {
  const res = []
  for (let i = 0; i < nbSources.value; i++)
    for (let j = 0; j < nbDests.value; j++)
      res.push({ i, j, flux: props.flux?.[i]?.[j] ?? 0 })
  return res
})

const liensActifs  = computed(() => liens.value.filter(l => l.flux > 1e-6))
const cyclePresent = computed(() => props.cycle && props.cycle.length > 0)

// ── Helpers ──────────────────────────────────────────────────────────────────
function estDansCycle(i, j) {
  return props.cycle?.some(([r, c]) => r === i && c === j) ?? false
}
function positionCycle(i, j) {
  return props.cycle?.findIndex(([r, c]) => r === i && c === j) ?? -1
}
function estActive(i, j) {
  return props.caseActive && props.caseActive[0] === i && props.caseActive[1] === j
}
function isSourceActive(i) {
  if (props.caseActive?.[0] === i) return true
  if (props.cycle?.some(([r]) => r === i)) return true
  return false
}
function isDestActive(j) {
  if (props.caseActive?.[1] === j) return true
  if (props.cycle?.some(([, c]) => c === j)) return true
  return false
}

function getLienClass(lien) {
  const { i, j, flux } = lien
  if (estDansCycle(i, j)) {
    return positionCycle(i, j) % 2 === 0
      ? 'stroke-violet-400' : 'stroke-rose-400'
  }
  if (estActive(i, j)) return 'stroke-indigo-500'
  if (flux > 1e-6) return 'stroke-indigo-300 dark:stroke-indigo-700'
  return 'stroke-stone-200 dark:stroke-gray-800'
}

function getArrowClass(lien) {
  const { i, j } = lien
  if (estDansCycle(i, j))
    return positionCycle(i, j) % 2 === 0 ? 'fill-violet-400' : 'fill-rose-400'
  return 'fill-indigo-300 dark:fill-indigo-700'
}

function getLienEpaisseur(lien) {
  const { i, j, flux } = lien
  if (estDansCycle(i, j) || estActive(i, j)) return 2.5
  if (flux > 1e-6) return Math.max(1, Math.min(3.5, flux / 35))
  return 0.7
}

function getArrowPoints(y1, y2) {
  const mx = (sourceX + destX.value) / 2
  const my = (y1 + y2) / 2
  const dx = destX.value - sourceX
  const dy = y2 - y1
  const len = Math.sqrt(dx * dx + dy * dy)
  const ux = dx / len, uy = dy / len
  const s = 5
  return [
    `${mx + ux * s},${my + uy * s}`,
    `${mx - ux * s + uy * s * 0.5},${my - uy * s - ux * s * 0.5}`,
    `${mx - ux * s - uy * s * 0.5},${my - uy * s + ux * s * 0.5}`
  ].join(' ')
}
</script>