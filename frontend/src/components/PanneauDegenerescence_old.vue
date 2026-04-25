<template>
  <div class="space-y-4">

    <!-- ── Alerte principale ─────────────────────────────────────────────── -->
    <div class="bg-amber-50 dark:bg-amber-900/20 border-2 border-amber-400 dark:border-amber-600 rounded-2xl p-5 shadow-md">
      <div class="flex items-start gap-3">
        <div class="w-10 h-10 rounded-xl bg-amber-100 dark:bg-amber-900/60 border border-amber-300
          dark:border-amber-700 flex items-center justify-center shrink-0">
          <svg class="w-5 h-5 text-amber-600 dark:text-amber-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
          </svg>
        </div>
        <div class="flex-1">
          <h3 class="text-base font-bold text-amber-800 dark:text-amber-200 mb-1">
            Cas dégénéré détecté
          </h3>
          <p class="text-sm text-amber-700 dark:text-amber-300">
            {{ etape.message }}
          </p>
        </div>
      </div>
    </div>

    <!-- ── Explication théorique ─────────────────────────────────────────── -->
    <div class="bg-white dark:bg-gray-900 rounded-2xl border border-stone-200 dark:border-gray-800 p-5 shadow-sm">
      <h4 class="text-xs font-semibold tracking-widest uppercase text-gray-400 dark:text-gray-500 mb-3">
        Pourquoi ce cas se produit-il ?
      </h4>
      <div class="space-y-2 text-sm text-gray-600 dark:text-gray-300">
        <p>
          Un problème de transport de taille <strong>m × n</strong> doit avoir exactement
          <strong>m + n − 1</strong> cases de base (variables de base) pour que les
          potentiels u<sub>i</sub>, v<sub>j</sub> soient calculables.
        </p>
        <p>
          La <strong>dégénérescence</strong> survient quand une ligne et une colonne
          s'épuisent <em>simultanément</em> lors de l'initialisation, réduisant le nombre
          de cases remplies en dessous du minimum requis.
        </p>
      </div>

      <!-- Comptage cases -->
      <div class="grid grid-cols-3 gap-3 mt-4">
        <div class="bg-stone-50 dark:bg-gray-800 rounded-xl p-3 text-center border border-stone-200 dark:border-gray-700">
          <p class="text-[10px] text-gray-400 uppercase tracking-wider mb-1">Cases remplies</p>
          <p class="text-2xl font-bold font-mono text-red-500 dark:text-red-400">{{ casesRemplies }}</p>
        </div>
        <div class="bg-stone-50 dark:bg-gray-800 rounded-xl p-3 text-center border border-stone-200 dark:border-gray-700">
          <p class="text-[10px] text-gray-400 uppercase tracking-wider mb-1">Requises (m+n−1)</p>
          <p class="text-2xl font-bold font-mono text-gray-700 dark:text-gray-200">{{ casesRequises }}</p>
        </div>
        <div class="bg-amber-50 dark:bg-amber-900/30 rounded-xl p-3 text-center border border-amber-200 dark:border-amber-700">
          <p class="text-[10px] text-amber-600 uppercase tracking-wider mb-1">Epsilon ajoutés</p>
          <p class="text-2xl font-bold font-mono text-amber-600 dark:text-amber-300">
            {{ etape.cases_epsilon?.length ?? 0 }}
          </p>
        </div>
      </div>
    </div>

    <!-- ── Cases epsilon ajoutées ─────────────────────────────────────────── -->
    <div class="bg-white dark:bg-gray-900 rounded-2xl border-2 border-dashed border-amber-300
      dark:border-amber-700 p-5 shadow-sm">
      <h4 class="text-xs font-semibold tracking-widest uppercase text-amber-600 dark:text-amber-400 mb-3 flex items-center gap-2">
        <span class="inline-block w-3 h-3 rounded-sm bg-amber-400 animate-pulse"></span>
        Nœuds epsilon ε ajoutés
      </h4>

      <div class="flex flex-wrap gap-3 mb-4">
        <div v-for="([i, j]) in etape.cases_epsilon" :key="`eps-${i}-${j}`"
          class="flex items-center gap-2 bg-amber-50 dark:bg-amber-900/30 border-2 border-amber-400
            dark:border-amber-500 rounded-xl px-4 py-2.5 shadow-sm">
          <!-- Icône ε -->
          <span class="text-lg font-bold text-amber-500 dark:text-amber-300 leading-none">ε</span>
          <div>
            <p class="text-sm font-bold font-mono text-amber-700 dark:text-amber-200">
              [U{{ i+1 }}, C{{ j+1 }}]
            </p>
            <p class="text-[10px] text-amber-500 dark:text-amber-400">flux = ε ≈ 0</p>
          </div>
        </div>
      </div>

      <div class="bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800 rounded-xl p-3">
        <p class="text-xs text-amber-700 dark:text-amber-300">
          <strong>Rôle de ε :</strong> Ces cases fictives avec un flux infinitésimal (≈ 10⁻¹⁰)
          permettent de lier la base et de calculer tous les potentiels u<sub>i</sub>, v<sub>j</sub>.
          Elles n'affectent pas le coût total et disparaîtront naturellement lors de l'optimisation.
        </p>
      </div>
    </div>

    <!-- ── Matrice avec epsilon surlignés ─────────────────────────────────── -->
    <div class="bg-white dark:bg-gray-900 rounded-2xl border border-stone-200 dark:border-gray-800 p-5 shadow-sm overflow-x-auto">
      <h4 class="text-xs font-semibold tracking-widest uppercase text-gray-400 dark:text-gray-500 mb-3">
        État de la matrice après correction
      </h4>
      <table class="border-collapse w-full text-sm">
        <thead>
          <tr>
            <th class="p-1.5 w-14"></th>
            <th v-for="(_, j) in etape.flux[0]" :key="j"
              class="p-1.5 text-xs font-semibold text-indigo-500 dark:text-indigo-400 text-center min-w-15">
              C{{ j+1 }}
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, i) in etape.flux" :key="i">
            <td class="p-1.5 text-xs font-semibold text-indigo-500 dark:text-indigo-400">U{{ i+1 }}</td>
            <td v-for="(val, j) in row" :key="j" class="p-1">
              <div :class="estEpsilon(i, j)
                  ? 'bg-amber-100 dark:bg-amber-900/40 border-2 border-amber-400 dark:border-amber-500 scale-105 shadow-md'
                  : val > 1e-6
                    ? 'bg-emerald-50 dark:bg-emerald-900/20 border-emerald-200 dark:border-emerald-800'
                    : 'bg-stone-50 dark:bg-gray-800/60 border-stone-200 dark:border-gray-700'"
                class="relative min-w-13 h-12 rounded-xl border flex flex-col items-center justify-center transition-all">
                <!-- Valeur -->
                <span class="text-sm font-bold font-mono"
                  :class="estEpsilon(i, j)
                    ? 'text-amber-700 dark:text-amber-300'
                    : val > 1e-6 ? 'text-emerald-700 dark:text-emerald-300' : 'text-gray-300 dark:text-gray-600'">
                  {{ estEpsilon(i, j) ? 'ε' : val > 1e-6 ? val.toFixed(0) : '—' }}
                </span>
                <!-- Badge ε -->
                <span v-if="estEpsilon(i, j)"
                  class="absolute -top-1.5 -right-1.5 w-4 h-4 rounded-full bg-amber-500 text-white
                    flex items-center justify-center text-[9px] font-bold shadow animate-pulse">
                  ε
                </span>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({ etape: Object, config: Object })

const casesEpsilonSet = computed(() => {
  return new Set((props.etape.cases_epsilon ?? []).map(([i, j]) => `${i}-${j}`))
})

function estEpsilon(i, j) {
  return casesEpsilonSet.value.has(`${i}-${j}`)
}

// Comptage pour l'affichage
const casesRequises = computed(() => {
  if (!props.etape.flux) return '?'
  const m = props.etape.flux.length
  const n = props.etape.flux[0]?.length ?? 0
  return m + n - 1
})

const casesRemplies = computed(() => {
  return casesRequises.value - (props.etape.cases_epsilon?.length ?? 0)
})
</script>