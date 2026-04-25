<template>
  <div class="w-full">

    <!-- Toggle potentiels / offre-demande -->
    <div class="flex items-center gap-2 mb-3 flex-wrap">
      <span class="text-xs text-gray-400 dark:text-gray-500">Nœuds :</span>
      <div class="flex gap-1 bg-stone-100 dark:bg-gray-800 p-0.5 rounded-lg">
        <button @click="mode = 'potentiels'"
          :disabled="!aPotentiels"
          :class="mode === 'potentiels'
            ? 'bg-white dark:bg-gray-900 shadow text-gray-800 dark:text-white'
            : 'text-gray-400 dark:text-gray-500 disabled:opacity-40 disabled:cursor-not-allowed'"
          class="px-3 py-1 rounded-md text-xs font-semibold transition-all">
          Potentiels u, v
        </button>
        <button @click="mode = 'offre'"
          :class="mode === 'offre'
            ? 'bg-white dark:bg-gray-900 shadow text-gray-800 dark:text-white'
            : 'text-gray-400 dark:text-gray-500'"
          class="px-3 py-1 rounded-md text-xs font-semibold transition-all">
          Offre / Demande
        </button>
      </div>
      <!-- Petit badge quand potentiels dispo -->
      <span v-if="aPotentiels && mode === 'potentiels'"
        class="text-xs text-indigo-500 dark:text-indigo-400 font-mono">
        u<sub>i</sub> + v<sub>j</sub> = c<sub>ij</sub>
      </span>
    </div>

    <!-- SVG principal -->
    <svg :viewBox="`0 0 ${W} ${H}`" class="w-full h-auto" style="min-height:200px" overflow="visible">

      <!-- Titres colonnes -->
      <!-- <text :x="SX" y="16" text-anchor="middle"
        fill="#818cf8" font-size="8" font-weight="700" letter-spacing="1" class="select-none">
        SOURCES
      </text>
      <text :x="DX" y="16" text-anchor="middle"
        fill="#2dd4bf" font-size="8" font-weight="700" letter-spacing="1" class="select-none">
        DESTINATIONS
      </text> -->

      <!-- ── Arêtes ──────────────────────────────────────────────────────── -->
      <line
        v-for="lien in liens" :key="`l-${lien.i}-${lien.j}`"
        :x1="SX" :y1="ySrc(lien.i)"
        :x2="DX" :y2="yDst(lien.j)"
        :stroke="strokeLien(lien)"
        :stroke-width="epaisLien(lien)"
        :stroke-dasharray="lien.flux <= 1e-6 ? '3 3' : 'none'"
        stroke-linecap="round"
        class="transition-all duration-500"
      />

      <!-- Label flux au milieu de l'arête (si flux > 0) -->
      <text
        v-for="lien in liensActifs" :key="`lf-${lien.i}-${lien.j}`"
        :x="(SX + DX) / 2"
        :y="(ySrc(lien.i) + yDst(lien.j)) / 2 - 7"
        text-anchor="middle" dominant-baseline="middle"
        :fill="estDansCycle(lien.i, lien.j) ? '#a78bfa' : '#9ca3af'"
        font-size="9" class="select-none">
        {{ lien.flux.toFixed(0) }}
      </text>

      <!-- Flèches sur arêtes actives -->
      <polygon
        v-for="lien in liensActifs" :key="`a-${lien.i}-${lien.j}`"
        :points="arrowPoints(ySrc(lien.i), yDst(lien.j))"
        :fill="strokeLien(lien)"
        class="transition-all duration-500"
      />

      <!-- ── Nœuds sources (gauche) ──────────────────────────────────────── -->
      <g v-for="(src, i) in metadata.sources" :key="`s-${i}`">
        <circle
          :cx="SX" :cy="ySrc(i)" r="26"
          :fill="srcActif(i) ? '#6366f1' : (isDark ? '#1f2937' : '#eef2ff')"
          :stroke="srcActif(i) ? '#4f46e5' : '#a5b4fc'"
          stroke-width="1.5"
          class="transition-all duration-300"
        />
        <!-- Nom Ui -->
        <text :x="SX" :y="ySrc(i) - 8"
          text-anchor="middle" dominant-baseline="middle"
          :fill="srcActif(i) ? '#ffffff' : '#6366f1'"
          font-size="9" font-weight="700" class="select-none">
          U{{ i + 1 }}
        </text>
        <!-- Valeur : potentiel ui ou offre -->
        <text :x="SX" :y="ySrc(i) + 9"
          text-anchor="middle" dominant-baseline="middle"
          :fill="srcActif(i) ? '#e0e7ff' : (mode === 'potentiels' ? '#4f46e5' : '#6b7280')"
          font-size="11" font-weight="700" class="select-none">
          {{ valSrc(i) }}
        </text>
        <!-- Badge u= à gauche du cercle -->
        <!-- <text v-if="mode === 'potentiels' && aPotentiels"
          :x="SX - 36" :y="ySrc(i)"
          text-anchor="middle" dominant-baseline="middle"
          fill="#a5b4fc" font-size="8" class="select-none">
          u={{ valSrc(i) }}
        </text> -->
      </g>

      <!-- ── Nœuds destinations (droite) ────────────────────────────────── -->
      <g v-for="(dst, j) in metadata.destinations" :key="`d-${j}`">
        <circle
          :cx="DX" :cy="yDst(j)" r="26"
          :fill="dstActif(j) ? '#14b8a6' : (isDark ? '#1f2937' : '#f0fdfa')"
          :stroke="dstActif(j) ? '#0d9488' : '#5eead4'"
          stroke-width="1.5"
          class="transition-all duration-300"
        />
        <!-- Nom Cj -->
        <text :x="DX" :y="yDst(j) - 8"
          text-anchor="middle" dominant-baseline="middle"
          :fill="dstActif(j) ? '#ffffff' : '#0d9488'"
          font-size="9" font-weight="700" class="select-none">
          C{{ j + 1 }}
        </text>
        <!-- Valeur : potentiel vj ou demande -->
        <text :x="DX" :y="yDst(j) + 9"
          text-anchor="middle" dominant-baseline="middle"
          :fill="dstActif(j) ? '#ccfbf1' : (mode === 'potentiels' ? '#0d9488' : '#6b7280')"
          font-size="11" font-weight="700" class="select-none">
          {{ valDst(j) }}
        </text>
        <!-- Badge v= à droite du cercle -->
        <!-- <text v-if="mode === 'potentiels' && aPotentiels"
          :x="DX + 36" :y="yDst(j)"
          text-anchor="middle" dominant-baseline="middle"
          fill="#5eead4" font-size="8" class="select-none">
          v={{ valDst(j) }}
        </text> -->
      </g>

    </svg>

    <!-- Bandeau info : potentiels pas encore dispo (étapes init) -->
    <div v-if="mode === 'potentiels' && !aPotentiels"
      class="mt-2 flex items-center gap-2 bg-amber-50 dark:bg-amber-900/20 border border-amber-200
        dark:border-amber-800 rounded-xl px-3 py-2 text-xs text-amber-600 dark:text-amber-400">
      <svg class="w-3.5 h-3.5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
          d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
      </svg>
      Potentiels u, v disponibles uniquement pendant les étapes d'optimisation.
    </div>

    <!-- Légende -->
    <div class="flex flex-wrap gap-3 mt-3 text-xs text-gray-400 dark:text-gray-500">
      <span class="flex items-center gap-1.5">
        <span class="inline-block w-5 h-0.5 bg-indigo-300 rounded"></span>Flux actif
      </span>
      <span class="flex items-center gap-1.5">
        <span class="inline-block w-5 h-0.5 bg-stone-300 dark:bg-gray-700 rounded" style="border-top: 1px dashed"></span>Flux nul
      </span>
      <span v-if="hasCycle" class="flex items-center gap-1.5">
        <span class="inline-block w-5 h-0.5 bg-violet-400 rounded"></span>Cycle +
      </span>
      <span v-if="hasCycle" class="flex items-center gap-1.5">
        <span class="inline-block w-5 h-0.5 bg-rose-400 rounded"></span>Cycle -
      </span>
    </div>

  </div>
</template>

<script setup>
import { computed, ref, watch } from 'vue'

const props = defineProps({
  flux:       Array,
  metadata:   Object,
  config:     Object,
  caseActive: Array,
  cycle:      Array,
  potentiels: Object,   // { u: [number|null, ...], v: [number|null, ...] }
  isDark:     Boolean
})

// ── Mode d'affichage ─────────────────────────────────────────────────────────
const mode = ref('potentiels')

// ── Dimensions SVG ───────────────────────────────────────────────────────────
const W   = 340
const PAD_TOP = 28
const PAD_BOT = 16
const SX  = 80           // x des sources
const DX  = computed(() => W - 80)   // x des destinations

const nbS = computed(() => props.metadata?.sources?.length      ?? 0)
const nbD = computed(() => props.metadata?.destinations?.length ?? 0)

const H = computed(() => {
  const maxN = Math.max(nbS.value, nbD.value, 1)
  return PAD_TOP + PAD_BOT + maxN * 68
})

// Positions y des nœuds
function yPositions(n) {
  const total = H.value - PAD_TOP - PAD_BOT
  const step  = n > 1 ? total / (n - 1) : 0
  return (i) => n === 1 ? H.value / 2 : PAD_TOP + i * step
}

const ySrc = computed(() => yPositions(nbS.value))
const yDst = computed(() => yPositions(nbD.value))

// ── Potentiels ───────────────────────────────────────────────────────────────
const arrU = computed(() => props.potentiels?.u ?? [])
const arrV = computed(() => props.potentiels?.v ?? [])

// aPotentiels = true si au moins un u_i est un nombre (pas null)
const aPotentiels = computed(() => {
  const arr = arrU.value
  if (!Array.isArray(arr) || arr.length === 0) return false
  return arr.some(x => x !== null && x !== undefined)
})

// Basculer automatiquement selon la disponibilité
watch(aPotentiels, (ok) => {
  mode.value = ok ? 'potentiels' : 'offre'
}, { immediate: true })

function fmt(val) {
  if (val === null || val === undefined) return '—'
  const n = Number(val)
  if (isNaN(n)) return '—'
  return Number.isInteger(n) ? String(n) : n.toFixed(1)
}

// Valeur affichée sur les nœuds
function valSrc(i) {
  if (mode.value === 'potentiels' && aPotentiels.value) return fmt(arrU.value[i])
  return String(props.config?.offres?.[i] ?? '')
}
function valDst(j) {
  if (mode.value === 'potentiels' && aPotentiels.value) return fmt(arrV.value[j])
  return String(props.config?.demandes?.[j] ?? '')
}

// ── Liens ────────────────────────────────────────────────────────────────────
const liens = computed(() => {
  const res = []
  for (let i = 0; i < nbS.value; i++)
    for (let j = 0; j < nbD.value; j++)
      res.push({ i, j, flux: props.flux?.[i]?.[j] ?? 0 })
  return res
})

const liensActifs = computed(() => liens.value.filter(l => l.flux > 1e-6))
const hasCycle    = computed(() => Array.isArray(props.cycle) && props.cycle.length > 0)

// ── Helpers cycle / active ───────────────────────────────────────────────────
function estDansCycle(i, j) {
  return props.cycle?.some(([r, c]) => r === i && c === j) ?? false
}
function posCycle(i, j) {
  return props.cycle?.findIndex(([r, c]) => r === i && c === j) ?? -1
}
function estActive(i, j) {
  return props.caseActive?.[0] === i && props.caseActive?.[1] === j
}
function srcActif(i) {
  if (props.caseActive?.[0] === i) return true
  return props.cycle?.some(([r]) => r === i) ?? false
}
function dstActif(j) {
  if (props.caseActive?.[1] === j) return true
  return props.cycle?.some(([, c]) => c === j) ?? false
}

// ── Style des arêtes ─────────────────────────────────────────────────────────
function strokeLien({ i, j, flux }) {
  if (estDansCycle(i, j)) return posCycle(i, j) % 2 === 0 ? '#a78bfa' : '#f87171'
  if (estActive(i, j))    return '#6366f1'
  if (flux > 1e-6)        return '#a5b4fc'
  return '#e2e8f0'
}
function epaisLien({ i, j, flux }) {
  if (estDansCycle(i, j) || estActive(i, j)) return 2.5
  if (flux > 1e-6) return Math.max(1, Math.min(3.5, flux / 35))
  return 0.7
}

// ── Flèches ──────────────────────────────────────────────────────────────────
function arrowPoints(y1, y2) {
  const dx  = DX.value - SX
  const dy  = y2 - y1
  const len = Math.sqrt(dx * dx + dy * dy)
  const ux  = dx / len, uy = dy / len
  const mx  = (SX + DX.value) / 2
  const my  = (y1 + y2) / 2
  const s   = 5
  return [
    `${mx + ux*s},${my + uy*s}`,
    `${mx - ux*s + uy*s*0.5},${my - uy*s - ux*s*0.5}`,
    `${mx - ux*s - uy*s*0.5},${my - uy*s + ux*s*0.5}`
  ].join(' ')
}
</script>