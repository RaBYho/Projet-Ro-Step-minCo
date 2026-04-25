<template>
  <div class="space-y-4">

    <!-- ── En-tête statut ───────────────────────────────────────────────── -->
    <div :class="etape.optimal
        ? 'bg-emerald-50 dark:bg-emerald-900/20 border-emerald-200 dark:border-emerald-800'
        : 'bg-white dark:bg-gray-900 border-stone-200 dark:border-gray-800'"
      class="rounded-2xl border p-5 shadow-sm">

      <div class="flex items-center gap-3 mb-1">
        <span class="text-xs font-bold uppercase tracking-widest px-3 py-1 rounded-full"
          :class="etape.optimal
            ? 'bg-emerald-100 dark:bg-emerald-800/60 text-emerald-700 dark:text-emerald-300'
            : 'bg-violet-100 dark:bg-violet-900/50 text-violet-700 dark:text-violet-300'">
          Itération {{ etape.iteration }}
        </span>
        <span v-if="etape.optimal"
          class="text-xs font-semibold text-emerald-600 dark:text-emerald-400 flex items-center gap-1">
          ✓ Solution optimale atteinte
        </span>
      </div>

      <!-- Coût avant → après -->
      <div v-if="!etape.optimal" class="flex items-center gap-3 mt-3 flex-wrap">
        <div class="text-center">
          <p class="text-xs text-gray-400 mb-0.5">Coût avant</p>
          <p class="text-xl font-bold font-mono text-gray-700 dark:text-gray-200">
            {{ etape.cout_avant?.toFixed(2) }}
          </p>
        </div>
        <div class="flex flex-col items-center">
          <svg class="w-6 h-5 text-gray-300 dark:text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
          </svg>
        </div>
        <div class="text-center">
          <p class="text-xs text-gray-400 mb-0.5">Coût après</p>
          <p class="text-xl font-bold font-mono text-indigo-600 dark:text-indigo-400">
            {{ etape.cout_apres?.toFixed(2) }}
          </p>
        </div>
        <div class="ml-auto text-right">
          <p class="text-xs text-gray-400 mb-0.5">Réduction</p>
          <p class="text-xl font-bold font-mono text-emerald-600 dark:text-emerald-400">
            −{{ etape.reduction_cout?.toFixed(2) }}
          </p>
        </div>
      </div>

      <!-- Cas optimal : coût final -->
      <div v-else class="mt-3">
        <p class="text-xs text-gray-400 mb-1">Coût total final</p>
        <p class="text-3xl font-bold font-mono text-emerald-600 dark:text-emerald-300">
          {{ etape.cout_apres?.toFixed(2) }}
        </p>
      </div>
    </div>

    <!-- ── Potentiels u, v ───────────────────────────────────────────────── -->
    <div class="bg-white dark:bg-gray-900 rounded-2xl border border-stone-200 dark:border-gray-800 p-5 shadow-sm">
      <button @click="showPotentiels = !showPotentiels"
        class="w-full flex items-center justify-between text-left">
        <h4 class="text-xs font-semibold tracking-widest uppercase text-gray-400 dark:text-gray-500">
          Potentiels u, v
        </h4>
        <svg class="w-4 h-4 text-gray-400 transition-transform" :class="showPotentiels ? 'rotate-180' : ''" fill="none" viewBox="0 0 24 24" stroke="currentColor">
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
          <p class="text-xs text-gray-400 italic mt-1">
            Calculés via : u<sub>i</sub> + v<sub>j</sub> = c<sub>ij</sub> pour chaque case de base (flux &gt; 0)
          </p>
        </div>
      </Transition>
    </div>

    <!-- ── Tableau des indices marginaux ────────────────────────────────── -->
    <div class="bg-white dark:bg-gray-900 rounded-2xl border border-stone-200 dark:border-gray-800 p-5 shadow-sm">
      <button @click="showIndices = !showIndices"
        class="w-full flex items-center justify-between text-left mb-1">
        <h4 class="text-xs font-semibold tracking-widest uppercase text-gray-400 dark:text-gray-500">
          Indices marginaux — cases vides
        </h4>
        <svg class="w-4 h-4 text-gray-400 transition-transform" :class="showIndices ? 'rotate-180' : ''" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
        </svg>
      </button>
      <p class="text-xs text-gray-400 mb-3">
        Formule : Δ<sub>ij</sub> = c<sub>ij</sub> − (u<sub>i</sub> + v<sub>j</sub>)
      </p>

      <Transition name="collapse">
        <div v-if="showIndices" class="space-y-2">
          <div v-for="d in etape.details_indices" :key="`${d.i}-${d.j}`"
            :class="[
              d.est_meilleur
                ? 'border-violet-400 dark:border-violet-500 bg-violet-50 dark:bg-violet-900/30 shadow-md'
                : d.indice < 0
                  ? 'border-amber-200 dark:border-amber-800 bg-amber-50 dark:bg-amber-900/20'
                  : 'border-stone-100 dark:border-gray-800 bg-stone-50 dark:bg-gray-800/40'
            ]"
            class="rounded-xl border px-4 py-2.5 flex items-center justify-between gap-3 transition-all">

            <!-- Label case -->
            <div class="flex items-center gap-2 min-w-0">
              <span v-if="d.est_meilleur"
                class="text-[10px] font-bold bg-violet-500 text-white px-1.5 py-0.5 rounded-md shrink-0">
                PIVOT
              </span>
              <span class="text-xs font-semibold text-gray-600 dark:text-gray-300 shrink-0">
                Δ(U{{ d.i+1 }}, C{{ d.j+1 }})
              </span>
            </div>

            <!-- Formule de calcul -->
            <span class="text-xs font-mono text-gray-400 dark:text-gray-500 hidden sm:block">
              = {{ d.formule }}
            </span>

            <!-- Valeur finale -->
            <span class="text-sm font-bold font-mono shrink-0"
              :class="d.est_meilleur
                ? 'text-violet-600 dark:text-violet-300'
                : d.indice < 0
                  ? 'text-amber-600 dark:text-amber-300'
                  : 'text-emerald-600 dark:text-emerald-400'">
              {{ d.indice >= 0 ? '+' : '' }}{{ d.indice.toFixed(2) }}
            </span>
          </div>

          <!-- Légende -->
          <div class="flex flex-wrap gap-3 pt-2 text-xs text-gray-400">
            <span class="flex items-center gap-1.5">
              <span class="w-3 h-3 rounded bg-violet-200 dark:bg-violet-700 inline-block"></span>Pivot (plus négatif)
            </span>
            <span class="flex items-center gap-1.5">
              <span class="w-3 h-3 rounded bg-amber-100 dark:bg-amber-900/40 border border-amber-300 inline-block"></span>Négatif (amélioration possible)
            </span>
            <span class="flex items-center gap-1.5">
              <span class="w-3 h-3 rounded bg-stone-100 dark:bg-gray-800 border border-stone-200 inline-block"></span>Positif (optimal pour cette case)
            </span>
          </div>
        </div>
      </Transition>
    </div>

    <!-- ── Cycle & Theta ─────────────────────────────────────────────────── -->
    <div v-if="!etape.optimal"
      class="bg-white dark:bg-gray-900 rounded-2xl border border-stone-200 dark:border-gray-800 p-5 shadow-sm">
      <h4 class="text-xs font-semibold tracking-widest uppercase text-gray-400 dark:text-gray-500 mb-3">
        Cycle Stepping Stone &amp; Theta
      </h4>

      <!-- Cycle lisible -->
      <div class="bg-stone-50 dark:bg-gray-800/60 rounded-xl p-3 mb-3 overflow-x-auto">
        <p class="text-xs text-gray-400 mb-2">Chemin du pivot :</p>
        <div class="flex items-center gap-1 flex-wrap">
          <span v-for="(node, idx) in etape.cycle" :key="idx"
            class="flex items-center gap-1">
            <span :class="idx % 2 === 0
                ? 'bg-violet-100 dark:bg-violet-900/50 border-violet-300 dark:border-violet-600 text-violet-700 dark:text-violet-300'
                : 'bg-rose-100 dark:bg-rose-900/50 border-rose-300 dark:border-rose-600 text-rose-700 dark:text-rose-300'"
              class="border rounded-lg px-2.5 py-1 text-xs font-mono font-bold inline-flex items-center gap-1">
              <span class="text-[10px]">{{ idx % 2 === 0 ? '+' : '-' }}</span>
              [{{ node[0]+1 }},{{ node[1]+1 }}]
            </span>
            <svg v-if="idx < etape.cycle.length - 1"
              class="w-3 h-3 text-gray-300 dark:text-gray-600 shrink-0"
              fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
            </svg>
          </span>
          <!-- Flèche retour -->
          <span class="text-xs text-gray-400 ml-1">↩ retour [{{ etape.cycle[0][0]+1 }},{{ etape.cycle[0][1]+1 }}]</span>
        </div>
      </div>

      <!-- Theta -->
      <div class="grid grid-cols-2 gap-3">
        <div class="bg-stone-50 dark:bg-gray-800/60 rounded-xl p-3">
          <p class="text-xs text-gray-400 mb-1">θ (quantité déplacée)</p>
          <p class="text-xl font-bold font-mono text-violet-600 dark:text-violet-300">
            {{ etape.theta?.toFixed(4) }}
          </p>
          <p class="text-xs text-gray-400 mt-1">
            = min des cases moins du cycle
          </p>
        </div>
        <div class="bg-stone-50 dark:bg-gray-800/60 rounded-xl p-3">
          <p class="text-xs text-gray-400 mb-1">Case sortante</p>
          <p class="text-xl font-bold font-mono text-rose-500 dark:text-rose-400" v-if="etape.case_sortante">
            [{{ etape.case_sortante[0]+1 }}, {{ etape.case_sortante[1]+1 }}]
          </p>
          <p class="text-xs text-gray-400 mt-1">quitte la base (flux → 0)</p>
        </div>
      </div>

      <!-- Meilleur indice sélectionné -->
      <div v-if="etape.meilleur_indice"
        class="mt-3 border border-violet-200 dark:border-violet-700 bg-violet-50 dark:bg-violet-900/20 rounded-xl p-3">
        <p class="text-xs text-gray-400 mb-1">Case entrante (meilleur indice)</p>
        <p class="text-sm font-mono">
          <span class="text-gray-600 dark:text-gray-300">Δ(U{{ etape.meilleur_indice.i+1 }}, C{{ etape.meilleur_indice.j+1 }})</span>
          <span class="text-gray-400 mx-2">=</span>
          <span class="text-gray-500 dark:text-gray-400">{{ etape.meilleur_indice.formule }}</span>
          <span class="text-gray-400 mx-2">=</span>
          <span class="font-bold text-violet-600 dark:text-violet-300">{{ etape.meilleur_indice.valeur?.toFixed(2) }}</span>
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
  transition: all 0.25s ease;
  overflow: hidden;
}
.collapse-enter-from, .collapse-leave-to {
  opacity: 0;
  max-height: 0;
}
.collapse-enter-to, .collapse-leave-from {
  opacity: 1;
  max-height: 600px;
}
</style>