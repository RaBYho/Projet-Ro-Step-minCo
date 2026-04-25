<template>
  <div class="max-w-4xl mx-auto">

    <!-- Titre -->
    <div class="text-center mb-10">
      <span class="inline-block bg-indigo-100 dark:bg-indigo-900/40 text-indigo-600 dark:text-indigo-400
        text-xs font-semibold tracking-widest uppercase px-3 py-1 rounded-full mb-3">
        Problème de transport
      </span>
      <h2 class="text-3xl sm:text-4xl font-bold text-gray-900 dark:text-white mb-2">
        Saisie des données
      </h2>
      <p class="text-gray-500 dark:text-gray-400 text-sm">
        Configurez la taille du tableau, puis renseignez coûts, offres et demandes.
      </p>
    </div>

    <!-- Card dimensions -->
    <div class="bg-white dark:bg-gray-900 rounded-2xl border border-stone-200 dark:border-gray-800 p-5 shadow-sm mb-5">
      <h3 class="text-xs font-semibold tracking-widest uppercase text-gray-400 dark:text-gray-500 mb-4">Dimensions</h3>
      <div class="flex flex-wrap gap-6 items-start">
        <DimControle label="Sources (usines)" :valeur="nbLignes" :min="2" :max="6"
          @incrementer="changerDim('lignes', 1)" @decrementer="changerDim('lignes', -1)" />
        <DimControle label="Destinations (clients)" :valeur="nbColonnes" :min="2" :max="6"
          @incrementer="changerDim('colonnes', 1)" @decrementer="changerDim('colonnes', -1)" />

        <!-- Badge équilibre -->
        <div class="ml-auto self-end">
          <div :class="estEquilibre
              ? 'bg-emerald-50 dark:bg-emerald-900/30 border-emerald-200 dark:border-emerald-700 text-emerald-700 dark:text-emerald-300'
              : 'bg-amber-50 dark:bg-amber-900/30 border-amber-200 dark:border-amber-700 text-amber-700 dark:text-amber-300'"
            class="flex items-center gap-2 border rounded-xl px-4 py-2.5 text-xs font-medium transition-all">
            <span :class="estEquilibre ? 'bg-emerald-500' : 'bg-amber-500'" class="w-2 h-2 rounded-full shrink-0"></span>
            <span v-if="estEquilibre">Équilibré ✓ (Σ = {{ totalOffre }})</span>
            <span v-else>Déséquilibré — Offre <strong>{{ totalOffre }}</strong> ≠ Demande <strong>{{ totalDemande }}</strong></span>
          </div>
        </div>
      </div>
    </div>

    <!-- Tableau de saisie -->
    <div class="bg-white dark:bg-gray-900 rounded-2xl border border-stone-200 dark:border-gray-800 p-5 shadow-sm mb-5 overflow-x-auto">
      <h3 class="text-xs font-semibold tracking-widest uppercase text-gray-400 dark:text-gray-500 mb-4">
        Matrice des coûts · Offres · Demandes
      </h3>

      <table class="border-collapse min-w-full">
        <thead>
          <tr>
            <th class="w-20 p-2"></th>
            <th v-for="j in nbColonnes" :key="j"
              class="p-2 text-xs font-semibold text-indigo-500 dark:text-indigo-400 text-center min-w-20">
              Client {{ j }}
            </th>
            <th class="p-2 text-xs font-semibold text-violet-500 dark:text-violet-400 text-center min-w-20">
              Offre
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="i in nbLignes" :key="i">
            <td class="p-2 text-xs font-semibold text-indigo-500 dark:text-indigo-400 pr-3 whitespace-nowrap">
              Usine {{ i }}
            </td>
            <td v-for="j in nbColonnes" :key="j" class="p-1.5">
              <input type="number" v-model.number="couts[i-1][j-1]"
                :class="erreursCellules[`${i-1}-${j-1}`]
                  ? 'border-red-400 bg-red-50 dark:bg-red-900/20 focus:border-red-500'
                  : 'border-stone-200 dark:border-gray-700 bg-white dark:bg-gray-900 focus:border-indigo-400'"
                class="w-full rounded-xl border px-2 py-2 text-center text-sm font-mono
                  focus:outline-none focus:ring-2 focus:ring-indigo-200 dark:focus:ring-indigo-900 transition-all"
                placeholder="0" min="0"
                @blur="validerCellule(i-1, j-1)"
              />
            </td>
            <td class="p-1.5">
              <input type="number" v-model.number="offres[i-1]"
                :class="erreurs.offres
                  ? 'border-red-400 bg-red-50 dark:bg-red-900/20'
                  : 'border-violet-200 dark:border-violet-800 bg-white dark:bg-gray-900 focus:border-violet-400'"
                class="w-full rounded-xl border px-2 py-2 text-center text-sm font-mono
                  text-violet-600 dark:text-violet-300 focus:outline-none focus:ring-2 focus:ring-violet-200 dark:focus:ring-violet-900 transition-all"
                placeholder="0" min="0" />
            </td>
          </tr>

          <!-- Ligne demandes -->
          <tr class="border-t-2 border-stone-200 dark:border-gray-700">
            <td class="p-2 text-xs font-semibold text-teal-500 dark:text-teal-400">Demande</td>
            <td v-for="j in nbColonnes" :key="j" class="p-1.5">
              <input type="number" v-model.number="demandes[j-1]"
                :class="erreurs.demandes
                  ? 'border-red-400 bg-red-50 dark:bg-red-900/20'
                  : 'border-teal-200 dark:border-teal-800 bg-white dark:bg-gray-900 focus:border-teal-400'"
                class="w-full rounded-xl border px-2 py-2 text-center text-sm font-mono
                  text-teal-600 dark:text-teal-300 focus:outline-none focus:ring-2 focus:ring-teal-200 dark:focus:ring-teal-900 transition-all"
                placeholder="0" min="0" />
            </td>
            <td class="p-2 text-center text-sm font-bold" :class="estEquilibre ? 'text-emerald-500' : 'text-amber-500'">
              {{ estEquilibre ? '=' : '≠' }}
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Erreur coûts -->
      <div v-if="erreurs.couts" class="mt-3 text-xs text-red-500 flex items-center gap-1">
        <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
        </svg>
        {{ erreurs.couts }}
      </div>
    </div>

    <!-- Exemples -->
    <div class="bg-white dark:bg-gray-900 rounded-2xl border border-stone-200 dark:border-gray-800 p-5 shadow-sm mb-6">
      <h3 class="text-xs font-semibold tracking-widest uppercase text-gray-400 dark:text-gray-500 mb-3">
        Exemples prédéfinis
      </h3>
      <div class="flex flex-wrap gap-2">
        <button v-for="ex in exemples" :key="ex.label" @click="chargerExemple(ex)"
          class="px-4 py-2 text-xs font-medium rounded-xl border border-stone-200 dark:border-gray-700
            text-gray-600 dark:text-gray-300 hover:border-indigo-400 hover:text-indigo-600
            dark:hover:border-indigo-500 dark:hover:text-indigo-400 hover:bg-indigo-50 dark:hover:bg-indigo-900/20
            transition-all">
          {{ ex.label }}
        </button>
      </div>
    </div>

    <!-- Bouton résoudre -->
    <div class="flex flex-col items-center gap-3">
      <button @click="soumettre" :disabled="!estValide"
        :class="estValide
          ? 'bg-indigo-600 hover:bg-indigo-700 shadow-lg shadow-indigo-200 dark:shadow-indigo-900 text-white cursor-pointer'
          : 'bg-stone-100 dark:bg-gray-800 text-gray-400 cursor-not-allowed'"
        class="flex items-center gap-3 px-10 py-3.5 rounded-2xl font-semibold text-sm tracking-wide transition-all">
        <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
        </svg>
        Résoudre le problème
      </button>
      <p v-if="!estValide && !estEquilibre && totalOffre > 0" class="text-xs text-amber-500">
        ⚠ Le problème doit être équilibré avant résolution
      </p>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, reactive } from 'vue'
import DimControle from './DimControle.vue'

const emit = defineEmits(['resoudre'])

const nbLignes   = ref(2)
const nbColonnes = ref(3)

const couts   = ref([[2,3,1],[5,4,8]])
const offres  = ref([100, 200])
const demandes = ref([80, 120, 100])

const erreurs = reactive({ couts: '', offres: false, demandes: false })
const erreursCellules = reactive({})

function changerDim(type, delta) {
  if (type === 'lignes') {
    const n = Math.max(2, Math.min(6, nbLignes.value + delta))
    if (n === nbLignes.value) return
    nbLignes.value = n
    if (delta > 0) { couts.value.push(Array(nbColonnes.value).fill(0)); offres.value.push(0) }
    else           { couts.value.pop(); offres.value.pop() }
  } else {
    const n = Math.max(2, Math.min(6, nbColonnes.value + delta))
    if (n === nbColonnes.value) return
    nbColonnes.value = n
    if (delta > 0) { couts.value.forEach(r => r.push(0)); demandes.value.push(0) }
    else           { couts.value.forEach(r => r.pop()); demandes.value.pop() }
  }
}

const totalOffre   = computed(() => offres.value.reduce((a, b)  => a + (+b || 0), 0))
const totalDemande = computed(() => demandes.value.reduce((a, b) => a + (+b || 0), 0))
const estEquilibre = computed(() => totalOffre.value > 0 && Math.abs(totalOffre.value - totalDemande.value) < 0.001)
const coutsValides = computed(() => couts.value.every(row => row.every(v => v !== null && v !== '' && +v >= 0)))
const estValide    = computed(() => estEquilibre.value && coutsValides.value)

function validerCellule(i, j) {
  const v = couts.value[i][j]
  erreursCellules[`${i}-${j}`] = (v === null || v === '' || +v < 0)
}

const exemples = [
  { label: '2×3 Basique',   couts: [[2,3,1],[5,4,8]],                offres: [100,200],    demandes: [80,120,100] },
  { label: '3×3 Classique', couts: [[4,8,8],[16,24,16],[8,16,24]],   offres: [76,82,77],   demandes: [72,102,61] },
  { label: '3×4 Grand',     couts: [[2,3,1,5],[7,3,4,2],[6,1,5,4]], offres: [120,80,80],  demandes: [150,70,40,20] },
  { label: '2×2 Minimal',   couts: [[3,1],[2,4]],                    offres: [50,50],      demandes: [60,40] },
  { label: '4×6 Tres Grand',   couts: [[45,60,15,30,45,40],[35,15,10,35,25,5],[20,15,45,55,10,55],[30,40,55,10,10,50]], offres: [25,30,10,45],  demandes: [20,15,35,10,20,10] }
]

function chargerExemple(ex) {
  nbLignes.value   = ex.couts.length
  nbColonnes.value = ex.couts[0].length
  couts.value    = ex.couts.map(r => [...r])
  offres.value   = [...ex.offres]
  demandes.value = [...ex.demandes]
  Object.keys(erreursCellules).forEach(k => delete erreursCellules[k])
}

function soumettre() {
  if (!estValide.value) return
  emit('resoudre', { couts: couts.value, offres: offres.value, demandes: demandes.value })
}
</script>