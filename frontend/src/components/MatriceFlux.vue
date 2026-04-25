<template>
  <div>
    <div class="overflow-x-auto">
      <table class="border-collapse w-full text-sm">
        <thead>
          <tr>
            <th class="p-2 w-16"></th>
            <th v-for="(dest, j) in metadata.destinations" :key="j"
              class="p-2 text-xs font-semibold text-indigo-500 dark:text-indigo-400 text-center">
              {{ dest }}
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(source, i) in metadata.sources" :key="i">
            <td class="p-2 text-xs font-semibold text-indigo-500 dark:text-indigo-400 whitespace-nowrap pr-3">
              {{ source }}
            </td>
            <td v-for="(dest, j) in metadata.destinations" :key="j" class="p-1">
              <div :class="getCellClass(i, j)"
                class="relative min-w-15 h-14 rounded-xl flex flex-col items-center justify-center
                  transition-all duration-400 border cursor-default">
                <span class="text-sm font-bold font-mono leading-none">
                  {{ formatFlux(flux[i][j], i, j) }}
                </span>
                <span class="text-[10px] opacity-40 mt-0.5">c={{ config.couts[i][j] }}</span>
                <!-- Badge position cycle -->
                <span v-if="estDansCycle(i, j)"
                  :class="positionCycle(i, j) % 2 === 0
                    ? 'bg-violet-500 text-white' : 'bg-rose-500 text-white'"
                  class="absolute -top-1.5 -right-1.5 w-5 h-5 rounded-full flex items-center justify-center text-[10px] font-bold shadow">
                  {{ positionCycle(i, j) + 1 }}
                </span>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Légende -->
    <div class="flex flex-wrap gap-3 mt-4 text-xs text-gray-400 dark:text-gray-500">
      <span class="flex items-center gap-1.5">
        <span class="w-4 h-4 rounded-md bg-indigo-100 dark:bg-indigo-900/50 border border-indigo-300 dark:border-indigo-700 inline-block"></span>
        Case active
      </span>
      <span class="flex items-center gap-1.5">
        <span class="w-4 h-4 rounded-md bg-emerald-50 dark:bg-emerald-900/30 border border-emerald-200 dark:border-emerald-800 inline-block"></span>
        Flux positif
      </span>
      <span class="flex items-center gap-1.5">
        <span class="w-4 h-4 rounded-md bg-stone-50 dark:bg-gray-800/60 border border-stone-200 dark:border-gray-700 inline-block"></span>
        Flux nul
      </span>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({ flux: Array, config: Object, metadata: Object, caseActive: Array, cycle: Array, casesEpsilon: Array })

function formatFlux(v, i, j) {
  if (estEpsilon(i, j)) return 'ε'
  if (!v || v < 1e-6) return '—'
  return Number.isInteger(v) ? String(v) : v.toFixed(1)
}
function estActive(i, j) { return props.caseActive && props.caseActive[0] === i && props.caseActive[1] === j }
function estEpsilon(i, j) { return props.casesEpsilon?.some(([r, c]) => r === i && c === j) ?? false }
function estDansCycle(i, j) { return props.cycle?.some(([r, c]) => r === i && c === j) ?? false }
function positionCycle(i, j) { return props.cycle?.findIndex(([r, c]) => r === i && c === j) ?? -1 }

function getCellClass(i, j) {
  if (estActive(i, j))
    return 'bg-indigo-100 dark:bg-indigo-900/50 border-indigo-400 dark:border-indigo-500 text-indigo-700 dark:text-indigo-200 shadow-md scale-105'
  if (estDansCycle(i, j)) {
    return positionCycle(i, j) % 2 === 0
      ? 'bg-violet-100 dark:bg-violet-900/40 border-violet-400 dark:border-violet-600 text-violet-700 dark:text-violet-200 scale-105'
      : 'bg-rose-100 dark:bg-rose-900/40 border-rose-400 dark:border-rose-600 text-rose-700 dark:text-rose-200 scale-105'
  }
  if (estEpsilon(i, j))
    return 'bg-amber-100 dark:bg-amber-900/40 border-2 border-amber-400 dark:border-amber-500 text-amber-700 dark:text-amber-300 scale-105'
  const v = props.flux?.[i]?.[j] ?? 0
  if (v > 1e-6) return 'bg-emerald-50 dark:bg-emerald-900/20 border-emerald-200 dark:border-emerald-800 text-emerald-700 dark:text-emerald-300'
  return 'bg-stone-50 dark:bg-gray-800/60 border-stone-200 dark:border-gray-700 text-gray-300 dark:text-gray-600'
}
</script>