<template>
  <div class="space-y-4">

    <!-- ── En-tête : coût avant / après / réduction ─────────────────────── -->
    <div :class="etape.optimal
        ? 'bg-emerald-50 dark:bg-emerald-900/20 border-emerald-200 dark:border-emerald-800'
        : 'bg-white dark:bg-gray-900 border-stone-200 dark:border-gray-800'"
      class="rounded-2xl border p-5 shadow-sm">

      <div class="flex items-center gap-3 mb-3">
        <span class="text-xs font-bold uppercase tracking-widest px-3 py-1 rounded-full"
          :class="etape.optimal
            ? 'bg-emerald-100 dark:bg-emerald-800/60 text-emerald-700 dark:text-emerald-300'
            : 'bg-violet-100 dark:bg-violet-900/50 text-violet-700 dark:text-violet-300'">
          Itération {{ etape.iteration }}
        </span>
        <span v-if="etape.optimal" class="text-xs font-semibold text-emerald-600 dark:text-emerald-400">
          ✓ Solution optimale — tous les gains ≤ 0
        </span>
      </div>

      <!-- Coût avant → après avec réduction -->
      <div v-if="!etape.optimal" class="flex items-center gap-4 flex-wrap">
        <div>
          <p class="text-[10px] text-gray-400 uppercase tracking-wider mb-0.5">Coût avant</p>
          <p class="text-2xl font-bold font-mono text-gray-700 dark:text-gray-200">
            {{ etape.cout_avant?.toFixed(2) }}
          </p>
        </div>
        <svg class="w-5 h-5 text-gray-300 dark:text-gray-600 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
        </svg>
        <div>
          <p class="text-[10px] text-gray-400 uppercase tracking-wider mb-0.5">Coût après</p>
          <p class="text-2xl font-bold font-mono text-indigo-600 dark:text-indigo-400">
            {{ etape.cout_apres?.toFixed(2) }}
          </p>
        </div>
        <div class="ml-auto text-right bg-emerald-50 dark:bg-emerald-900/30 border border-emerald-200
          dark:border-emerald-700 rounded-xl px-4 py-2">
          <p class="text-[10px] text-emerald-500 uppercase tracking-wider mb-0.5">Réduction</p>
          <p class="text-xl font-bold font-mono text-emerald-600 dark:text-emerald-300">
            −{{ etape.reduction_cout?.toFixed(2) }}
          </p>
        </div>
      </div>

      <!-- Cas optimal -->
      <div v-else>
        <p class="text-[10px] text-gray-400 uppercase tracking-wider mb-1">Coût total minimal</p>
        <p class="text-3xl font-bold font-mono text-emerald-600 dark:text-emerald-300">
          {{ etape.cout_apres?.toFixed(2) }}
        </p>
      </div>
    </div>

    <!-- ── Potentiels u, v ────────────────────────────────────────────────── -->
    <div class="bg-white dark:bg-gray-900 rounded-2xl border border-stone-200 dark:border-gray-800 p-5 shadow-sm">
      <button @click="showPotentiels = !showPotentiels"
        class="w-full flex items-center justify-between text-left">
        <h4 class="text-xs font-semibold tracking-widest uppercase text-gray-400 dark:text-gray-500">
          Potentiels u, v
        </h4>
        <svg class="w-4 h-4 text-gray-400 transition-transform" :class="showPotentiels ? 'rotate-180':''"
          fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
        </svg>
      </button>
      <Transition name="collapse">
        <div v-if="showPotentiels" class="mt-3 space-y-2">
          <div class="flex flex-wrap gap-2">
            <span v-for="(val, i) in etape.potentiels?.u" :key="`u${i}`"
              class="bg-indigo-50 dark:bg-indigo-900/30 border border-indigo-200 dark:border-indigo-700
                rounded-lg px-3 py-1.5 text-xs font-mono">
              <span class="text-gray-400">u<sub>{{ i+1 }}</sub> =</span>
              <span class="text-indigo-600 dark:text-indigo-300 ml-1 font-bold">{{ val?.toFixed(0) ?? '—' }}</span>
            </span>
          </div>
          <div class="flex flex-wrap gap-2">
            <span v-for="(val, j) in etape.potentiels?.v" :key="`v${j}`"
              class="bg-teal-50 dark:bg-teal-900/30 border border-teal-200 dark:border-teal-700
                rounded-lg px-3 py-1.5 text-xs font-mono">
              <span class="text-gray-400">v<sub>{{ j+1 }}</sub> =</span>
              <span class="text-teal-600 dark:text-teal-300 ml-1 font-bold">{{ val?.toFixed(0) ?? '—' }}</span>
            </span>
          </div>
          <p class="text-xs text-gray-400 italic">
            u<sub>i</sub> + v<sub>j</sub> = c<sub>ij</sub> pour chaque case de base
          </p>
        </div>
      </Transition>
    </div>

    <!-- ── Tableau des indices + gains ───────────────────────────────────── -->
    <div class="bg-white dark:bg-gray-900 rounded-2xl border border-stone-200 dark:border-gray-800 p-5 shadow-sm">
      <button @click="showIndices = !showIndices"
        class="w-full flex items-center justify-between text-left mb-1">
        <h4 class="text-xs font-semibold tracking-widest uppercase text-gray-400 dark:text-gray-500">
          Indices marginaux &amp; Gains
        </h4>
        <svg class="w-4 h-4 text-gray-400 transition-transform" :class="showIndices ? 'rotate-180':''"
          fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
        </svg>
      </button>
      <!-- Formules rappel -->
      <div class="flex flex-wrap gap-3 text-xs text-gray-400 mb-3">
        <span>ρ<sub>ij</sub> = c<sub>ij</sub> − (u<sub>i</sub> + v<sub>j</sub>)</span>
        <span class="text-gray-300 dark:text-gray-600">·</span>
        <span class="text-violet-500 dark:text-violet-400 font-semibold">
          Gain = ρ<sub>ij</sub> × θ → pivot sur le gain maximal
        </span>
      </div>

      <Transition name="collapse">
        <div v-if="showIndices" class="space-y-2">

          <!-- En-têtes colonnes -->
          <div class="grid grid-cols-12 gap-1 px-2 mb-1">
            <span class="col-span-3 text-[10px] text-gray-400 uppercase tracking-wider">Case</span>
            <span class="col-span-3 text-[10px] text-gray-400 uppercase tracking-wider hidden sm:block">Formule ρ</span>
            <span class="col-span-2 text-[10px] text-gray-400 uppercase tracking-wider text-right">ρ</span>
            <span class="col-span-2 text-[10px] text-gray-400 uppercase tracking-wider text-right">θ</span>
            <span class="col-span-2 text-[10px] text-gray-400 uppercase tracking-wider text-right">Gain</span>
          </div>

          <div v-for="d in etape.details_indices" :key="`${d.i}-${d.j}`"
            :class="d.est_meilleur
              ? 'border-violet-400 dark:border-violet-500 bg-violet-50 dark:bg-violet-900/30 shadow-md ring-1 ring-violet-300 dark:ring-violet-700'
              : d.gain > 0
                ? 'border-amber-200 dark:border-amber-800 bg-amber-50 dark:bg-amber-900/20'
                : 'border-stone-100 dark:border-gray-800 bg-stone-50 dark:bg-gray-800/40'"
            class="rounded-xl border px-3 py-2 grid grid-cols-12 gap-1 items-center transition-all">

            <!-- Case + badge PIVOT -->
            <div class="col-span-3 flex items-center gap-1.5 min-w-0">
              <span v-if="d.est_meilleur"
                class="text-[9px] font-bold bg-violet-500 text-white px-1.5 py-0.5 rounded shrink-0">
                PIVOT
              </span>
              <span class="text-xs font-semibold text-gray-700 dark:text-gray-200 truncate">
                ρ(U{{ d.i+1 }},C{{ d.j+1 }})
              </span>
            </div>

            <!-- Formule -->
            <span class="col-span-3 text-xs font-mono text-gray-400 dark:text-gray-500 hidden sm:block truncate">
              {{ d.formule }}
            </span>

            <!-- Valeur ρ -->
            <span class="col-span-2 text-sm font-bold font-mono text-right"
              :class="d.est_meilleur
                ? 'text-violet-600 dark:text-violet-300'
                : d.indice < 0 ? 'text-amber-600 dark:text-amber-300'
                : 'text-emerald-600 dark:text-emerald-400'">
              {{ d.indice >= 0 ? '+' : '' }}{{ d.indice.toFixed(2) }}
            </span>

            <!-- Theta -->
            <span class="col-span-2 text-xs font-mono text-right"
              :class="d.gain > 0 ? 'text-gray-600 dark:text-gray-300' : 'text-gray-300 dark:text-gray-600'">
              {{ d.theta > 0 ? d.theta.toFixed(1) : '—' }}
            </span>

            <!-- Gain = |ρ| × θ -->
            <span class="col-span-2 text-sm font-bold font-mono text-right"
              :class="d.est_meilleur
                ? 'text-violet-600 dark:text-violet-300'
                : d.gain > 0 ? 'text-amber-600 dark:text-amber-400'
                : 'text-gray-300 dark:text-gray-600'">
              {{ d.gain > 0 ? d.gain.toFixed(2) : '—' }}
            </span>
          </div>

          <!-- Légende -->
          <div class="flex flex-wrap gap-3 pt-2 text-xs text-gray-400">
            <span class="flex items-center gap-1.5">
              <span class="w-3 h-3 rounded bg-violet-200 dark:bg-violet-800 inline-block"></span>
              Pivot (gain max)
            </span>
            <span class="flex items-center gap-1.5">
              <span class="w-3 h-3 rounded bg-amber-100 dark:bg-amber-900/40 border border-amber-200 inline-block"></span>
              Gain positif
            </span>
            <span class="flex items-center gap-1.5">
              <span class="w-3 h-3 rounded bg-stone-100 dark:bg-gray-800 border border-stone-200 inline-block"></span>
              ρ ≥ 0 (pas de gain)
            </span>
          </div>
        </div>
      </Transition>
    </div>

    <!-- ── Cycle & Theta & Gain du pivot ─────────────────────────────────── -->
    <div v-if="!etape.optimal"
      class="bg-white dark:bg-gray-900 rounded-2xl border border-stone-200 dark:border-gray-800 p-5 shadow-sm">
      <h4 class="text-xs font-semibold tracking-widest uppercase text-gray-400 dark:text-gray-500 mb-4">
        Cycle Stepping Stone
      </h4>

      <!-- Cycle visuel -->
      <div class="bg-stone-50 dark:bg-gray-800/60 rounded-xl p-3 mb-4 overflow-x-auto">
        <p class="text-[10px] text-gray-400 uppercase tracking-wider mb-2">Chemin du pivot :</p>
        <div class="flex items-center gap-1 flex-wrap">
          <span v-for="(node, idx) in etape.cycle" :key="idx" class="flex items-center gap-1">
            <span :class="idx % 2 === 0
                ? 'bg-violet-100 dark:bg-violet-900/50 border-violet-300 dark:border-violet-600 text-violet-700 dark:text-violet-200'
                : 'bg-rose-100 dark:bg-rose-900/50 border-rose-300 dark:border-rose-600 text-rose-700 dark:text-rose-200'"
              class="border rounded-lg px-2.5 py-1 text-xs font-mono font-bold inline-flex items-center gap-1 shrink-0">
              {{ idx % 2 === 0 ? '+' : '-' }} [{{ node[0]+1 }},{{ node[1]+1 }}]
            </span>
            <svg v-if="idx < etape.cycle.length - 1"
              class="w-3 h-3 text-gray-300 dark:text-gray-600 shrink-0"
              fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
            </svg>
          </span>
        </div>
      </div>

      <!-- Grille θ / case sortante / gain pivot -->
      <div class="grid grid-cols-3 gap-3 mb-4">
        <div class="bg-stone-50 dark:bg-gray-800/60 rounded-xl p-3">
          <p class="text-[10px] text-gray-400 uppercase tracking-wider mb-1">θ</p>
          <p class="text-xl font-bold font-mono text-violet-600 dark:text-violet-300">
            {{ etape.theta?.toFixed(2) }}
          </p>
          <p class="text-[10px] text-gray-400 mt-1">min des cases -</p>
        </div>
        <div class="bg-stone-50 dark:bg-gray-800/60 rounded-xl p-3">
          <p class="text-[10px] text-gray-400 uppercase tracking-wider mb-1">Case sortante</p>
          <p class="text-xl font-bold font-mono text-rose-500 dark:text-rose-400" v-if="etape.case_sortante">
            [{{ etape.case_sortante[0]+1 }},{{ etape.case_sortante[1]+1 }}]
          </p>
          <p class="text-[10px] text-gray-400 mt-1">flux → 0</p>
        </div>
        <div class="bg-violet-50 dark:bg-violet-900/30 border border-violet-200 dark:border-violet-700 rounded-xl p-3">
          <p class="text-[10px] text-violet-500 uppercase tracking-wider mb-1">Gain réel</p>
          <p class="text-xl font-bold font-mono text-violet-600 dark:text-violet-300">
            {{ etape.meilleur_indice?.gain?.toFixed(2) ?? '—' }}
          </p>
          <p class="text-[10px] text-violet-400 mt-1">
            {{ etape.meilleur_indice?.formule_gain ?? '' }}
          </p>
        </div>
      </div>

      <!-- Récap case entrante -->
      <div v-if="etape.meilleur_indice"
        class="bg-violet-50 dark:bg-violet-900/20 border border-violet-200 dark:border-violet-700 rounded-xl p-3">
        <p class="text-[10px] text-gray-400 uppercase tracking-wider mb-1">Case entrante (pivot)</p>
        <p class="text-sm font-mono flex flex-wrap gap-1 items-center">
          <span class="text-gray-700 dark:text-gray-200 font-semibold">
            ρ(U{{ etape.meilleur_indice.i+1 }},C{{ etape.meilleur_indice.j+1 }})
          </span>
          <span class="text-gray-400">=</span>
          <span class="text-gray-500 dark:text-gray-400">{{ etape.meilleur_indice.formule }}</span>
          <span class="text-gray-400">=</span>
          <span class="font-bold text-violet-600 dark:text-violet-300">
            {{ etape.meilleur_indice.valeur?.toFixed(2) }}
          </span>
          <span class="text-gray-400 mx-1">→</span>
          <span class="text-gray-500 dark:text-gray-400">
            Gain = |{{ etape.meilleur_indice.valeur?.toFixed(2) }}| × {{ etape.theta?.toFixed(2) }}
          </span>
          <span class="text-gray-400">=</span>
          <span class="font-bold text-emerald-600 dark:text-emerald-300">
            {{ etape.meilleur_indice.gain?.toFixed(2) }}
          </span>
        </p>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref } from 'vue'
defineProps({ etape: Object })
const showPotentiels = ref(true)
const showIndices    = ref(true)
</script>

<style scoped>
.collapse-enter-active, .collapse-leave-active {
  transition: all 0.3s ease;
  overflow: hidden;
}
.collapse-enter-from, .collapse-leave-to { opacity: 0; max-height: 0; }
.collapse-enter-to, .collapse-leave-from { opacity: 1; max-height: 800px; }
</style>