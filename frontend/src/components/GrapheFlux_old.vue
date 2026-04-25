<template>
  <div class="w-full">
    <svg :viewBox="`0 0 ${W} ${H}`" class="w-full h-auto" style="min-height:220px">

      <!-- Arêtes (flux) -->
      <g v-for="lien in liens" :key="`${lien.i}-${lien.j}`">
        <line
          :x1="sourceX" :y1="positionsSource[lien.i]"
          :x2="destX"   :y2="positionsDest[lien.j]"
          :class="getLienClass(lien)"
          :stroke-width="getLienEpaisseur(lien)"
          class="transition-all duration-500"
          stroke-linecap="round"
        />
        <!-- Label flux au milieu -->
        <text v-if="lien.flux > 1e-6"
          :x="(sourceX + destX) / 2"
          :y="(positionsSource[lien.i] + positionsDest[lien.j]) / 2 - 5"
          text-anchor="middle" dominant-baseline="middle"
          class="text-[10px] font-mono fill-gray-500 dark:fill-gray-400 select-none"
          font-size="10">
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
        <circle
          :cx="sourceX" :cy="positionsSource[i]" r="22"
          :class="isSourceActive(i)
            ? 'fill-indigo-500 dark:fill-indigo-500'
            : 'fill-indigo-100 dark:fill-gray-800'"
          class="transition-all duration-400 stroke-indigo-300 dark:stroke-indigo-700"
          stroke-width="1.5"
        />
        <text :x="sourceX" :y="positionsSource[i]"
          text-anchor="middle" dominant-baseline="middle"
          :class="isSourceActive(i) ? 'fill-white' : 'fill-indigo-600 dark:fill-indigo-400'"
          font-size="10" font-weight="600" class="select-none font-mono">
          U{{ i+1 }}
        </text>
        <!-- Offre -->
        <text :x="sourceX - 32" :y="positionsSource[i]"
          text-anchor="middle" dominant-baseline="middle"
          class="fill-gray-400 dark:fill-gray-500 select-none"
          font-size="9">
          {{ offreSource(i) }}
        </text>
      </g>

      <!-- Nœuds destinations (droite) -->
      <g v-for="(dest, j) in metadata.destinations" :key="`d${j}`">
        <circle
          :cx="destX" :cy="positionsDest[j]" r="22"
          :class="isDestActive(j)
            ? 'fill-teal-500 dark:fill-teal-500'
            : 'fill-teal-100 dark:fill-gray-800'"
          class="transition-all duration-400 stroke-teal-300 dark:stroke-teal-700"
          stroke-width="1.5"
        />
        <text :x="destX" :y="positionsDest[j]"
          text-anchor="middle" dominant-baseline="middle"
          :class="isDestActive(j) ? 'fill-white' : 'fill-teal-600 dark:fill-teal-400'"
          font-size="10" font-weight="600" class="select-none font-mono">
          C{{ j+1 }}
        </text>
        <!-- Demande -->
        <text :x="destX + 32" :y="positionsDest[j]"
          text-anchor="middle" dominant-baseline="middle"
          class="fill-gray-400 dark:fill-gray-500 select-none"
          font-size="9">
          {{ demandeDest(j) }}
        </text>
      </g>

      <!-- Labels colonnes -->
      <text :x="sourceX" y="18" text-anchor="middle"
        class="fill-indigo-400 dark:fill-indigo-500 select-none"
        font-size="9" font-weight="700" letter-spacing="1">SOURCES</text>
      <text :x="destX" y="18" text-anchor="middle"
        class="fill-teal-400 dark:fill-teal-500 select-none"
        font-size="9" font-weight="700" letter-spacing="1">DESTINATIONS</text>
    </svg>

    <!-- Légende graphe -->
    <div class="flex flex-wrap gap-3 mt-2 text-xs text-gray-400 dark:text-gray-500">
      <span class="flex items-center gap-1.5">
        <span class="w-6 h-0.5 bg-indigo-400 inline-block rounded"></span>Flux actif
      </span>
      <span class="flex items-center gap-1.5">
        <span class="w-6 h-0.5 bg-stone-200 dark:bg-gray-700 inline-block rounded border-dashed border"></span>Flux nul
      </span>
      <span class="flex items-center gap-1.5">
        <span class="w-6 h-0.5 bg-violet-400 inline-block rounded"></span>Cycle +
      </span>
      <span class="flex items-center gap-1.5">
        <span class="w-6 h-0.5 bg-rose-400 inline-block rounded"></span>Cycle −
      </span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  flux: Array,
  metadata: Object,
  config: Object,
  caseActive: Array,
  cycle: Array
})

const W = 340
const PADDING_TOP = 30
const PADDING_BOT = 20
const NODE_R = 22

const nbSources = computed(() => props.metadata.sources.length)
const nbDests   = computed(() => props.metadata.destinations.length)

const H = computed(() => {
  const maxN = Math.max(nbSources.value, nbDests.value)
  return PADDING_TOP + PADDING_BOT + maxN * 60
})

const sourceX = 80
const destX   = computed(() => W - 80)

function positions(n) {
  const total = H.value - PADDING_TOP - PADDING_BOT
  const step  = n > 1 ? total / (n - 1) : 0
  return Array.from({ length: n }, (_, i) =>
    n === 1 ? H.value / 2 : PADDING_TOP + i * step
  )
}

const positionsSource = computed(() => positions(nbSources.value))
const positionsDest   = computed(() => positions(nbDests.value))

// Tous les liens possibles
const liens = computed(() => {
  const res = []
  for (let i = 0; i < nbSources.value; i++) {
    for (let j = 0; j < nbDests.value; j++) {
      res.push({ i, j, flux: props.flux?.[i]?.[j] ?? 0 })
    }
  }
  return res
})

const liensActifs = computed(() => liens.value.filter(l => l.flux > 1e-6))

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
  if (props.caseActive && props.caseActive[0] === i) return true
  if (props.cycle?.some(([r]) => r === i)) return true
  return false
}
function isDestActive(j) {
  if (props.caseActive && props.caseActive[1] === j) return true
  if (props.cycle?.some(([, c]) => c === j)) return true
  return false
}

function offreSource(i) { return props.config?.offres?.[i] ?? '' }
function demandeDest(j) { return props.config?.demandes?.[j] ?? '' }

function getLienClass(lien) {
  const { i, j, flux } = lien
  if (estDansCycle(i, j)) {
    const pos = positionCycle(i, j)
    return pos % 2 === 0 ? 'stroke-violet-400 dark:stroke-violet-400' : 'stroke-rose-400 dark:stroke-rose-400'
  }
  if (estActive(i, j)) return 'stroke-indigo-500 dark:stroke-indigo-400'
  if (flux > 1e-6) return 'stroke-indigo-300 dark:stroke-indigo-600'
  return 'stroke-stone-200 dark:stroke-gray-800'
}

function getArrowClass(lien) {
  const { i, j } = lien
  if (estDansCycle(i, j)) {
    return positionCycle(i, j) % 2 === 0
      ? 'fill-violet-400 dark:fill-violet-400'
      : 'fill-rose-400 dark:fill-rose-400'
  }
  return 'fill-indigo-400 dark:fill-indigo-500'
}

function getLienEpaisseur(lien) {
  const { i, j, flux } = lien
  if (estDansCycle(i, j) || estActive(i, j)) return 2.5
  if (flux > 1e-6) return Math.max(1, Math.min(4, flux / 30))
  return 0.8
}

function getArrowPoints(y1, y2) {
  const mx = (sourceX + destX.value) / 2
  const my = (y1 + y2) / 2
  const dx = destX.value - sourceX
  const dy = y2 - y1
  const len = Math.sqrt(dx * dx + dy * dy)
  const ux = dx / len, uy = dy / len
  const s = 6
  return [
    `${mx + ux * s},${my + uy * s}`,
    `${mx - ux * s + uy * s * 0.5},${my - uy * s - ux * s * 0.5}`,
    `${mx - ux * s - uy * s * 0.5},${my - uy * s + ux * s * 0.5}`
  ].join(' ')
}
</script>
