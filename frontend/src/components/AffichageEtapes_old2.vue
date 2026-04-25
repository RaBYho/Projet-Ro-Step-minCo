<template>
  <div class="max-w-6xl mx-auto">

    <!-- Header -->
    <div class="flex flex-wrap items-start justify-between gap-4 mb-6">
      <div>
        <p class="text-xs font-semibold tracking-widest uppercase text-indigo-500 dark:text-indigo-400 mb-1">
          Résolution complète
        </p>
        <h2 class="text-2xl sm:text-3xl font-bold text-gray-900 dark:text-white">
          {{ etapes.length }} étapes ·
          <span class="text-indigo-600 dark:text-indigo-400">Coût = {{ final.cout_total.toFixed(2) }}</span>
        </h2>
      </div>
      <button @click="$emit('recommencer')"
        class="flex items-center gap-2 px-4 py-2 rounded-xl border border-stone-200 dark:border-gray-700
          text-gray-500 dark:text-gray-400 hover:text-indigo-600 dark:hover:text-indigo-400
          hover:border-indigo-300 dark:hover:border-indigo-600 text-xs font-medium transition-all
          bg-white dark:bg-gray-900">
        ← Nouvelle saisie
      </button>
    </div>

    <!-- Barre de progression globale -->
    <div class="bg-white dark:bg-gray-900 rounded-2xl border border-stone-200 dark:border-gray-800 p-5 shadow-sm mb-5">
      <div class="flex items-center justify-between mb-2">
        <span class="text-xs text-gray-400 dark:text-gray-500 font-medium tracking-wider uppercase">Avancement</span>
        <span class="text-xs font-mono text-indigo-600 dark:text-indigo-400 font-semibold">
          {{ etapeIndex < etapes.length ? etapeIndex + 1 : 'Final' }} / {{ etapes.length }}
        </span>
      </div>
      <div class="flex gap-1 mb-2.5">
        <button v-for="(e, i) in etapes" :key="i" @click="allerA(i)"
          :title="`Étape ${i+1} — ${e.type}`"
          :class="[
            i <= etapeIndex ? 'opacity-100' : 'opacity-25 hover:opacity-50',
            e.type === 'INITIALISATION' ? 'bg-indigo-400' : 'bg-violet-400'
          ]"
          class="h-2 rounded-full flex-1 transition-all hover:scale-y-150 cursor-pointer">
        </button>
        <button @click="allerA(etapes.length)"
          :class="etapeIndex === etapes.length ? 'opacity-100' : 'opacity-25 hover:opacity-50'"
          class="h-2 rounded-full flex-1 bg-emerald-400 transition-all hover:scale-y-150 cursor-pointer"
          title="Solution finale">
        </button>
      </div>
      <div class="flex flex-wrap gap-4 text-xs text-gray-400 dark:text-gray-500">
        <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-indigo-400 inline-block"></span>Init ({{ nbInit }})</span>
        <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-violet-400 inline-block"></span>Optim ({{ nbOpti }})</span>
        <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-emerald-400 inline-block"></span>Final</span>
      </div>
    </div>

    <!-- Contenu principal -->
    <div class="grid grid-cols-1 xl:grid-cols-2 gap-5 mb-5">

      <!-- Panneau gauche : infos de l'étape -->
      <Transition name="slide" mode="out-in">
        <div :key="etapeIndex" class="min-h-0">

          <!-- Étape INITIALISATION -->
          <div v-if="etapeIndex < etapes.length && etapeActuelle.type === 'INITIALISATION'"
            class="bg-white dark:bg-gray-900 rounded-2xl border border-stone-200 dark:border-gray-800 p-5 shadow-sm">
            <div class="flex items-center gap-2 mb-4">
              <span class="bg-indigo-100 dark:bg-indigo-900/50 text-indigo-600 dark:text-indigo-400
                text-xs font-bold uppercase tracking-widest px-3 py-1 rounded-full">
                Initialisation
              </span>
              <span class="text-xs text-gray-400 font-mono">Étape {{ etapeIndex + 1 }}</span>
            </div>
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-1">Affectation au minimum</h3>
            <p class="text-sm text-gray-500 dark:text-gray-400 mb-4">{{ etapeActuelle.message }}</p>
            <div class="space-y-4">
              <div class="flex items-center justify-between py-2.5 border-b border-stone-100 dark:border-gray-800">
                <span class="text-xs text-gray-400 uppercase tracking-wider">Case allouée</span>
                <span class="text-sm font-mono font-semibold text-indigo-600 dark:text-indigo-400">
                  Usine {{ etapeActuelle.case_active[0]+1 }} → Client {{ etapeActuelle.case_active[1]+1 }}
                </span>
              </div>
              <div>
                <p class="text-xs text-gray-400 uppercase tracking-wider mb-2">Offres restantes</p>
                <div class="flex flex-wrap gap-2">
                  <div v-for="(v, i) in etapeActuelle.offre_restante" :key="i"
                    :class="v <= 0 ? 'opacity-30' : ''"
                    class="bg-stone-50 dark:bg-gray-800 border border-stone-200 dark:border-gray-700 rounded-xl px-3 py-2 text-xs">
                    <span class="text-gray-400">U{{ i+1 }}</span>
                    <span class="text-violet-600 dark:text-violet-300 ml-2 font-mono font-bold">{{ v.toFixed(0) }}</span>
                  </div>
                </div>
              </div>
              <div>
                <p class="text-xs text-gray-400 uppercase tracking-wider mb-2">Demandes restantes</p>
                <div class="flex flex-wrap gap-2">
                  <div v-for="(v, j) in etapeActuelle.demande_restante" :key="j"
                    :class="v <= 0 ? 'opacity-30' : ''"
                    class="bg-stone-50 dark:bg-gray-800 border border-stone-200 dark:border-gray-700 rounded-xl px-3 py-2 text-xs">
                    <span class="text-gray-400">C{{ j+1 }}</span>
                    <span class="text-teal-600 dark:text-teal-300 ml-2 font-mono font-bold">{{ v.toFixed(0) }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Étape OPTIMISATION -->
          <PanneauOptimisation
            v-else-if="etapeIndex < etapes.length && etapeActuelle.type === 'OPTIMISATION'"
            :etape="etapeActuelle"
          />

          <!-- Solution finale -->
          <div v-else
            class="bg-white dark:bg-gray-900 rounded-2xl border border-stone-200 dark:border-gray-800 p-5 shadow-sm">
            <div class="flex items-center gap-2 mb-4">
              <span class="bg-emerald-100 dark:bg-emerald-900/50 text-emerald-600 dark:text-emerald-400
                text-xs font-bold uppercase tracking-widest px-3 py-1 rounded-full">
                Solution optimale
              </span>
            </div>
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-1">Optimisation terminée</h3>
            <p class="text-sm text-gray-500 dark:text-gray-400 mb-5">
              Tous les indices marginaux sont ≥ 0. La solution est optimale.
            </p>
            <div class="bg-emerald-50 dark:bg-emerald-900/20 border border-emerald-200 dark:border-emerald-800 rounded-2xl p-5 text-center">
              <p class="text-xs text-emerald-600 dark:text-emerald-400 uppercase tracking-widest mb-1">Coût total minimal</p>
              <p class="text-4xl font-bold text-emerald-600 dark:text-emerald-300 font-mono">
                {{ final.cout_total.toFixed(2) }}
              </p>
            </div>
          </div>

        </div>
      </Transition>

      <!-- Panneau droit : matrice / graphe -->
      <div class="bg-white dark:bg-gray-900 rounded-2xl border border-stone-200 dark:border-gray-800 p-5 shadow-sm flex flex-col">
        <div class="flex gap-1 mb-4 bg-stone-100 dark:bg-gray-800 p-1 rounded-xl w-fit self-start">
          <button @click="onglet = 'matrice'"
            :class="onglet === 'matrice' ? 'bg-white dark:bg-gray-900 shadow text-gray-800 dark:text-white' : 'text-gray-500 dark:text-gray-400'"
            class="px-4 py-1.5 rounded-lg text-xs font-semibold transition-all">Matrice</button>
          <button @click="onglet = 'graphe'"
            :class="onglet === 'graphe' ? 'bg-white dark:bg-gray-900 shadow text-gray-800 dark:text-white' : 'text-gray-500 dark:text-gray-400'"
            class="px-4 py-1.5 rounded-lg text-xs font-semibold transition-all">Graphe</button>
        </div>
        <Transition name="tab" mode="out-in">
          <div :key="onglet + '-' + etapeIndex" class="flex-1 overflow-auto">
            <MatriceFlux v-if="onglet === 'matrice'"
              :flux="fluxCourant" :config="config" :metadata="metadata"
              :case-active="caseActiveActuelle" :cycle="cycleActuel" />
            <GrapheFlux v-else
              :flux="fluxCourant" :metadata="metadata" :config="config"
              :case-active="caseActiveActuelle" :cycle="cycleActuel" />
          </div>
        </Transition>
      </div>
    </div>

    <!-- Navigation -->
    <div class="bg-white dark:bg-gray-900 rounded-2xl border border-stone-200 dark:border-gray-800 p-5 shadow-sm">
      <div class="flex items-center justify-between gap-3 flex-wrap">
        <button @click="precedent" :disabled="etapeIndex === 0"
          :class="etapeIndex === 0 ? 'opacity-30 cursor-not-allowed' : 'hover:bg-stone-100 dark:hover:bg-gray-800 hover:text-indigo-600 dark:hover:text-indigo-400'"
          class="flex items-center gap-2 px-5 py-2.5 border border-stone-200 dark:border-gray-700 rounded-xl
            text-sm text-gray-500 dark:text-gray-400 transition-all bg-white dark:bg-gray-900">
          <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
          </svg>
          Précédent
        </button>

        <div class="flex items-center gap-3">
          <button v-if="!lectureAuto" @click="demarrerLecture"
            class="flex items-center gap-1.5 px-4 py-2 bg-indigo-50 dark:bg-indigo-900/30 border border-indigo-200
              dark:border-indigo-700 text-indigo-600 dark:text-indigo-400 rounded-xl text-xs font-medium
              hover:bg-indigo-100 dark:hover:bg-indigo-900/50 transition-all">
            ▶ Lecture auto
          </button>
          <button v-else @click="arreterLecture"
            class="flex items-center gap-1.5 px-4 py-2 bg-red-50 dark:bg-red-900/30 border border-red-200
              dark:border-red-700 text-red-500 dark:text-red-400 rounded-xl text-xs font-medium
              hover:bg-red-100 dark:hover:bg-red-900/50 transition-all">
            ■ Stop
          </button>
          <span class="text-xs font-mono text-gray-400 dark:text-gray-500">
            <strong class="text-gray-700 dark:text-gray-200">{{ etapeIndex + 1 }}</strong> / {{ etapes.length + 1 }}
          </span>
        </div>

        <button @click="suivant" :disabled="etapeIndex === etapes.length"
          :class="etapeIndex === etapes.length ? 'opacity-30 cursor-not-allowed' : 'hover:bg-stone-100 dark:hover:bg-gray-800 hover:text-indigo-600 dark:hover:text-indigo-400'"
          class="flex items-center gap-2 px-5 py-2.5 border border-stone-200 dark:border-gray-700 rounded-xl
            text-sm text-gray-500 dark:text-gray-400 transition-all bg-white dark:bg-gray-900">
          Suivant
          <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
          </svg>
        </button>
      </div>

      <div v-if="lectureAuto" class="mt-4 flex items-center gap-3 pt-4 border-t border-stone-100 dark:border-gray-800">
        <span class="text-xs text-gray-400">Vitesse</span>
        <input type="range" v-model.number="vitesse" min="500" max="3000" step="250" class="flex-1 accent-indigo-500"/>
        <span class="text-xs font-mono text-indigo-500 w-14">{{ (vitesse/1000).toFixed(1) }}s</span>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onUnmounted } from 'vue'
import MatriceFlux from './MatriceFlux.vue'
import GrapheFlux from './GrapheFlux.vue'
import PanneauOptimisation from './PanneauOptimisation.vue'

const props = defineProps({ etapes: Array, config: Object, metadata: Object, final: Object })
defineEmits(['recommencer'])

const etapeIndex  = ref(0)
const onglet      = ref('matrice')
const lectureAuto = ref(false)
const vitesse     = ref(1500)
let timerAuto = null

const etapeActuelle = computed(() => props.etapes[etapeIndex.value])
const nbInit = computed(() => props.etapes.filter(e => e.type === 'INITIALISATION').length)
const nbOpti = computed(() => props.etapes.filter(e => e.type === 'OPTIMISATION').length)

const fluxCourant = computed(() => {
  if (etapeIndex.value === props.etapes.length) return props.final.flux
  const e = props.etapes[etapeIndex.value]
  return e.flux || e.flux_avant
})

const caseActiveActuelle = computed(() => {
  if (etapeIndex.value >= props.etapes.length) return null
  const e = props.etapes[etapeIndex.value]
  return e.type === 'INITIALISATION' ? e.case_active : null
})

const cycleActuel = computed(() => {
  if (etapeIndex.value >= props.etapes.length) return null
  const e = props.etapes[etapeIndex.value]
  return e.type === 'OPTIMISATION' ? e.cycle : null
})

function precedent() { if (etapeIndex.value > 0) etapeIndex.value-- }
function suivant()   { if (etapeIndex.value < props.etapes.length) etapeIndex.value++ }
function allerA(i)   { etapeIndex.value = i }

function demarrerLecture() {
  lectureAuto.value = true
  timerAuto = setInterval(() => {
    if (etapeIndex.value >= props.etapes.length) { arreterLecture(); return }
    etapeIndex.value++
  }, vitesse.value)
}
function arreterLecture() { lectureAuto.value = false; clearInterval(timerAuto) }
onUnmounted(() => clearInterval(timerAuto))
</script>

<style scoped>
.slide-enter-active, .slide-leave-active { transition: all 0.25s ease; }
.slide-enter-from { opacity: 0; transform: translateX(10px); }
.slide-leave-to   { opacity: 0; transform: translateX(-10px); }
.tab-enter-active, .tab-leave-active { transition: all 0.2s ease; }
.tab-enter-from { opacity: 0; }
.tab-leave-to   { opacity: 0; }
</style>