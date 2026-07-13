<template>
  <div>
    <div class="overflow-x-auto">
      <table class="border-collapse w-full text-sm">
        <thead>
          <tr>
            <th class="p-2 w-16 py-3"></th>
            <th
              v-for="(dest, j) in metadata.destinations"
              :key="j"
              class="p-2 py-3 text-center"
            >
              <div
                class="text-xs font-semibold"
                :class="isDark ? 'text-indigo-400' : 'text-indigo-600'"
              >
                {{ dest }}
              </div>
              <div
                v-if="potentiels"
                class="text-[10px] font-mono mt-0.5"
                :class="isDark ? 'text-stone-500' : 'text-stone-400'"
              >
                v={{ formatPotentiel(potentiels.v?.[j]) }}
              </div>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(source, i) in metadata.sources" :key="i">
            <td class="p-2 pr-3 whitespace-nowrap">
              <div
                class="text-xs font-semibold"
                :class="isDark ? 'text-indigo-400' : 'text-indigo-600'"
              >
                {{ source }}
              </div>
              <div
                v-if="potentiels"
                class="text-[10px] font-mono mt-0.5"
                :class="isDark ? 'text-stone-500' : 'text-stone-400'"
              >
                u={{ formatPotentiel(potentiels.u?.[i]) }}
              </div>
            </td>
            <td v-for="(dest, j) in metadata.destinations" :key="j" class="p-2">
              <div
                :class="getCellClass(i, j)"
                class="group relative min-w-[6rem] py-4 rounded-xl flex items-center justify-center transition-all duration-200 ease-out cursor-default"
              >
                <!-- Coût unitaire, coin haut-gauche -->
                <span
                  class="absolute top-1.5 left-2.5 text-[11px] font-mono opacity-50 leading-none"
                >
                  {{ config.couts[i][j] }}
                </span>

                <!-- Valeur du flux -->
                <span
                  class="text-base font-bold font-mono leading-none transition-transform duration-200"
                  :class="
                    estActive(i, j) || estEpsilon(i, j) ? 'scale-110' : ''
                  "
                >
                  {{ formatFlux(flux[i][j], i, j) }}
                </span>

                <!-- Badge position cycle (+ / -) -->
                <span
                  v-if="estDansCycle(i, j)"
                  :class="
                    positionCycle(i, j) % 2 === 0
                      ? 'bg-violet-500 text-white'
                      : 'bg-rose-500 text-white'
                  "
                  class="absolute -top-2 -right-2 w-5 h-5 rounded-full flex items-center justify-center text-[10px] font-bold leading-none shadow"
                >
                  {{ positionCycle(i, j) % 2 === 0 ? "+" : "−" }}
                </span>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Légende -->
    <div
      class="flex flex-wrap gap-x-6 gap-y-3 mt-6 pt-4 text-xs border-t"
      :class="
        isDark
          ? 'text-gray-500 border-gray-800'
          : 'text-gray-400 border-stone-200'
      "
    >
      <span class="flex items-center gap-1.5">
        <span
          class="w-3.5 h-3.5 rounded-md inline-block ring-2"
          :class="
            isDark
              ? 'bg-indigo-900/50 ring-indigo-500'
              : 'bg-indigo-100 ring-indigo-400'
          "
        ></span>
        Case active
      </span>
      <span class="flex items-center gap-1.5">
        <span
          class="w-3.5 h-3.5 rounded-md inline-block ring-2"
          :class="
            isDark
              ? 'bg-amber-900/40 ring-amber-500'
              : 'bg-amber-100 ring-amber-400'
          "
        ></span>
        Epsilon (ε)
      </span>
      <span class="flex items-center gap-1.5">
        <span
          class="w-3.5 h-3.5 rounded-full inline-flex items-center justify-center text-[8px] font-bold text-white bg-violet-500"
          >+</span
        >
        Cycle (entrée)
      </span>
      <span class="flex items-center gap-1.5">
        <span
          class="w-3.5 h-3.5 rounded-full inline-flex items-center justify-center text-[8px] font-bold text-white bg-rose-500"
          >−</span
        >
        Cycle (sortie)
      </span>
      <span class="flex items-center gap-1.5">
        <span
          class="w-3.5 h-3.5 rounded-md inline-block"
          :class="isDark ? 'bg-emerald-900/20' : 'bg-emerald-50'"
        ></span>
        Flux positif
      </span>
      <span class="flex items-center gap-1.5">
        <span
          class="w-3.5 h-3.5 rounded-md inline-block"
          :class="isDark ? 'bg-gray-800/60' : 'bg-stone-50'"
        ></span>
        Flux nul
      </span>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  flux: Array,
  config: Object,
  metadata: Object,
  caseActive: Array,
  cycle: Array,
  potentiels: Object,
  casesEpsilon: Array,
  isDark: Boolean,
});

function formatFlux(v, i, j) {
  if (estEpsilon(i, j)) return "ε";
  if (!v || v < 1e-6) return "—";
  return Number.isInteger(v) ? String(v) : v.toFixed(1);
}

function formatPotentiel(v) {
  if (v === undefined || v === null) return "·";
  return Number.isInteger(v) ? String(v) : v.toFixed(1);
}

function estActive(i, j) {
  return (
    props.caseActive && props.caseActive[0] === i && props.caseActive[1] === j
  );
}
function estEpsilon(i, j) {
  return props.casesEpsilon?.some(([r, c]) => r === i && c === j) ?? false;
}
function estDansCycle(i, j) {
  return props.cycle?.some(([r, c]) => r === i && c === j) ?? false;
}
function positionCycle(i, j) {
  return props.cycle?.findIndex(([r, c]) => r === i && c === j) ?? -1;
}

function getCellClass(i, j) {
  const active = estActive(i, j);
  const cycle = estDansCycle(i, j);
  const epsilon = estEpsilon(i, j);
  const v = props.flux?.[i]?.[j] ?? 0;

  if (active) {
    return props.isDark
      ? "bg-indigo-900/40 ring-2 ring-indigo-500 shadow-sm scale-105 text-indigo-200"
      : "bg-indigo-100 ring-2 ring-indigo-400 shadow-sm scale-105 text-indigo-700";
  }
  if (cycle) {
    return positionCycle(i, j) % 2 === 0
      ? props.isDark
        ? "bg-violet-900/30 ring-1 ring-violet-600 text-violet-200"
        : "bg-violet-100 ring-1 ring-violet-400 text-violet-700"
      : props.isDark
        ? "bg-rose-900/30 ring-1 ring-rose-600 text-rose-200"
        : "bg-rose-100 ring-1 ring-rose-400 text-rose-700";
  }
  if (epsilon) {
    return props.isDark
      ? "bg-amber-900/40 ring-2 ring-amber-500 scale-105 text-amber-300"
      : "bg-amber-100 ring-2 ring-amber-400 scale-105 text-amber-700";
  }
  if (v > 1e-6) {
    return props.isDark
      ? "bg-emerald-900/20 text-emerald-300"
      : "bg-emerald-50 text-emerald-700";
  }
  return props.isDark
    ? "bg-gray-800/60 text-gray-500"
    : "bg-stone-50 text-gray-300";
}
</script>
