<template>
  <div class="space-y-4">

    <!-- Alerte principale -->
    <div class="bg-amber-50 dark:bg-amber-900/20 border-2 border-amber-400 dark:border-amber-600 rounded-2xl p-5 shadow-md">
      <div class="flex items-start gap-3">
        <div class="w-10 h-10 rounded-xl bg-amber-100 dark:bg-amber-900/60 border border-amber-300
          dark:border-amber-700 flex items-center justify-center shrink-0 mt-0.5">
          <svg class="w-5 h-5 text-amber-600 dark:text-amber-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
          </svg>
        </div>
        <div class="flex-1">
          <h3 class="text-base font-bold text-amber-800 dark:text-amber-200 mb-1">Cas dégénéré détecté</h3>
          <p class="text-sm text-amber-700 dark:text-amber-300">{{ etape.message }}</p>
        </div>
      </div>
    </div>

    <!-- Explication théorique + comptage -->
    <div class="bg-white dark:bg-gray-900 rounded-2xl border border-stone-200 dark:border-gray-800 p-5 shadow-sm">
      <h4 class="text-xs font-semibold tracking-widest uppercase text-gray-400 dark:text-gray-500 mb-3">
        Pourquoi ce cas se produit-il ?
      </h4>
      <div class="space-y-2 text-sm text-gray-600 dark:text-gray-300 mb-4">
        <p>
          Un problème <strong>m × n</strong> requiert exactement <strong>m + n − 1</strong> cases de base
          pour que les potentiels u<sub>i</sub>, v<sub>j</sub> soient calculables.
          La dégénérescence survient quand une ligne et une colonne s'épuisent
          <em>simultanément</em>, réduisant le nombre de cases actives en dessous du seuil.
        </p>
      </div>
      <div class="grid grid-cols-3 gap-3">
        <div class="bg-stone-50 dark:bg-gray-800 rounded-xl p-3 text-center border border-stone-200 dark:border-gray-700">
          <p class="text-[10px] text-gray-400 uppercase tracking-wider mb-1">Cases remplies</p>
          <p class="text-2xl font-bold font-mono text-red-500 dark:text-red-400">{{ casesRemplies }}</p>
        </div>
        <div class="bg-stone-50 dark:bg-gray-800 rounded-xl p-3 text-center border border-stone-200 dark:border-gray-700">
          <p class="text-[10px] text-gray-400 uppercase tracking-wider mb-1">Requises (m+n−1)</p>
          <p class="text-2xl font-bold font-mono text-gray-700 dark:text-gray-200">{{ casesRequises }}</p>
        </div>
        <div class="bg-amber-50 dark:bg-amber-900/30 rounded-xl p-3 text-center border border-amber-200 dark:border-amber-700">
          <p class="text-[10px] text-amber-600 uppercase tracking-wider mb-1">ε ajoutés</p>
          <p class="text-2xl font-bold font-mono text-amber-600 dark:text-amber-300">
            {{ etape.cases_epsilon?.length ?? 0 }}
          </p>
        </div>
      </div>
    </div>

    <!-- Nœuds epsilon avec indication "visibles dans la matrice et le graphe" -->
    <!-- <div class="bg-white dark:bg-gray-900 rounded-2xl border-2 border-dashed border-amber-300 dark:border-amber-700 p-5 shadow-sm">
      <h4 class="text-xs font-semibold tracking-widest uppercase text-amber-600 dark:text-amber-400 mb-3 flex items-center gap-2">
        <span class="w-2.5 h-2.5 rounded-sm bg-amber-400 animate-pulse inline-block"></span>
        Nœuds epsilon ε insérés dans la base
      </h4>

      <div class="flex flex-wrap gap-3 mb-4">
        <div v-for="([i, j]) in etape.cases_epsilon" :key="`eps-${i}-${j}`"
          class="flex items-center gap-2 bg-amber-50 dark:bg-amber-900/30 border-2 border-amber-400
            dark:border-amber-500 rounded-xl px-4 py-2.5 shadow-sm">
          <span class="text-xl font-bold text-amber-500 dark:text-amber-300 leading-none font-mono">ε</span>
          <div>
            <p class="text-sm font-bold font-mono text-amber-700 dark:text-amber-200">[U{{ i+1 }}, C{{ j+1 }}]</p>
            <p class="text-[10px] text-amber-500 dark:text-amber-400">flux ≈ 0 (fictif)</p>
          </div>
        </div>
      </div>

      <div class="bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800 rounded-xl p-3 space-y-1.5">
        <p class="text-xs text-amber-700 dark:text-amber-300">
          <strong>Dans la matrice →</strong> ces cases sont surlignées en jaune avec le badge <strong>ε</strong>.
        </p>
        <p class="text-xs text-amber-700 dark:text-amber-300">
          <strong>Dans le graphe →</strong> les nœuds sources et destinations concernés apparaissent en <strong>jaune</strong>.
        </p>
        <p class="text-xs text-amber-700 dark:text-amber-300">
          <strong>Élimination →</strong> au fur des itérations, les ε sont traités comme des flux réels.
          Quand leur flux descend à 0 lors d'un pivot, ils disparaissent naturellement de la base.
        </p>
      </div>
    </div> -->

    <!-- Rappel : la matrice est affichée à droite -->
    <!-- <div class="flex items-center gap-2 bg-indigo-50 dark:bg-indigo-900/20 border border-indigo-200
      dark:border-indigo-800 rounded-xl px-4 py-3 text-xs text-indigo-600 dark:text-indigo-400">
      <svg class="w-4 h-4 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
          d="M9 5l7 7-7 7"/>
      </svg>
      Consultez la <strong class="mx-1">Matrice</strong> et le <strong class="mx-1">Graphe</strong>
      à droite — les nœuds ε sont surlignés en jaune.
    </div> -->

  </div>
</template>

<script setup>
import { computed } from 'vue'
const props = defineProps({ etape: Object, config: Object })

const casesRequises = computed(() => {
  if (!props.etape.flux) return '?'
  return props.etape.flux.length + (props.etape.flux[0]?.length ?? 0) - 1
})
const casesRemplies = computed(() => casesRequises.value - (props.etape.cases_epsilon?.length ?? 0))
</script>