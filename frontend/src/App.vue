<template>
  <div :class="isDark ? 'dark' : ''" class="min-h-screen transition-colors duration-300">
    <div class="min-h-screen bg-stone-50 dark:bg-gray-950 text-gray-800 dark:text-gray-100 transition-colors duration-300">

      <!-- Header -->
      <header class="sticky top-0 z-50 border-b border-stone-200 dark:border-gray-800 bg-stone-50/90 dark:bg-gray-950/90 backdrop-blur-md">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 py-3 flex items-center justify-between">
          <div class="flex items-center gap-3">
            <div class="w-9 h-9 rounded-xl bg-indigo-600 flex items-center justify-center shadow-md">
              <svg class="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7"/>
              </svg>
            </div>
            <div>
              <h1 class="text-base font-bold text-gray-900 dark:text-white tracking-tight">Problème de transport</h1>
              <!-- <p class="text-xs text-gray-400 dark:text-gray-500">Minimum · Stepping Stone · RO</p> -->
            </div>
          </div>
          <button @click="isDark = !isDark"
            class="flex items-center gap-2 px-3 py-2 rounded-xl border border-stone-200 dark:border-gray-700
              hover:bg-stone-100 dark:hover:bg-gray-800 transition-all text-xs text-gray-500 dark:text-gray-400">
            <svg v-if="isDark" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"/>
            </svg>
            <svg v-else class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"/>
            </svg>
            <span class="hidden sm:inline">{{ isDark ? 'Mode clair' : 'Mode sombre' }}</span>
          </button>
        </div>
      </header>

      <!-- Toast erreur -->
      <Transition name="toast">
        <div v-if="erreur"
          class="fixed top-20 left-1/2 -translate-x-1/2 z-50 bg-red-50 dark:bg-red-950 border border-red-200 dark:border-red-800
            rounded-2xl px-5 py-4 shadow-xl flex items-start gap-3 w-[90vw] max-w-md">
          <div class="w-8 h-8 rounded-full bg-red-100 dark:bg-red-900 flex items-center justify-center shrink-0">
            <svg class="w-4 h-4 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
          </div>
          <div class="flex-1 min-w-0">
            <p class="text-sm font-semibold text-red-700 dark:text-red-300">{{ erreur.titre }}</p>
            <p class="text-xs text-red-500 dark:text-red-400 mt-0.5 wrap-break-words">{{ erreur.detail }}</p>
          </div>
          <button @click="erreur = null" class="text-red-300 hover:text-red-500 transition-colors shrink-0">
            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>
      </Transition>

      <main class="max-w-7xl mx-auto px-4 sm:px-6 py-8">
        <Transition name="page" mode="out-in">
          <FormulaireTransport v-if="phase === 'formulaire'" @resoudre="lancerResolution" />
          <div v-else-if="phase === 'chargement'" class="flex items-center justify-center min-h-[60vh]">
            <LoaderAnimation :message="messageChargement" />
          </div>
          <AffichageEtapes v-else-if="phase === 'resultats'"
            :etapes="etapes" :config="config" :metadata="metadata" :final="resultatFinal"
            :is-dark="isDark" @recommencer="recommencer" />
        </Transition>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import FormulaireTransport from './components/FormulaireTransport.vue'
import AffichageEtapes from './components/AffichageEtapes.vue'
import LoaderAnimation from './components/LoaderAnimation.vue'

const isDark = ref(false)
const phase = ref('formulaire')
const etapes = ref([])
const config = ref(null)
const metadata = ref(null)
const resultatFinal = ref(null)
const messageChargement = ref('Initialisation...')
const erreur = ref(null)

function afficherErreur(titre, detail) {
  erreur.value = { titre, detail }
  setTimeout(() => { erreur.value = null }, 7000)
}

async function lancerResolution(donnees) {
  erreur.value = null
  phase.value = 'chargement'
  messageChargement.value = 'Connexion au serveur...'
  try {
    await new Promise(r => setTimeout(r, 300))
    messageChargement.value = 'Calcul de la solution initiale...'
    const response = await fetch('http://localhost:8000/resoudre', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(donnees)
    })
    if (!response.ok) {
      const txt = await response.text()
      throw new Error(`Erreur HTTP ${response.status} : ${txt}`)
    }
    const data = await response.json()
    if (data.erreur) {
      afficherErreur('Données invalides', data.erreur)
      phase.value = 'formulaire'
      return
    }
    messageChargement.value = 'Optimisation Stepping Stone...'
    await new Promise(r => setTimeout(r, 500))
    etapes.value = data.etapes
    config.value = data.config
    metadata.value = data.metadata
    resultatFinal.value = data.final
    await new Promise(r => setTimeout(r, 200))
    phase.value = 'resultats'
  } catch (e) {
    if (e.message.includes('fetch') || e.message.includes('network') || e.message.includes('Failed')) {
      afficherErreur('Serveur inaccessible', 'Vérifiez que FastAPI tourne sur http://localhost:8000 avec : uvicorn main:app --reload')
    } else {
      afficherErreur('Erreur', e.message)
    }
    phase.value = 'formulaire'
  }
}

function recommencer() {
  phase.value = 'formulaire'
  etapes.value = []
  config.value = null
}
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
*, *::before, *::after { box-sizing: border-box; }
html { font-family: 'Outfit', sans-serif; }
.font-mono { font-family: 'JetBrains Mono', monospace; }

.page-enter-active, .page-leave-active { transition: all 0.3s ease; }
.page-enter-from { opacity: 0; transform: translateY(12px); }
.page-leave-to   { opacity: 0; transform: translateY(-8px); }

.toast-enter-active, .toast-leave-active { transition: all 0.3s ease; }
.toast-enter-from { opacity: 0; transform: translate(-50%, -12px); }
.toast-leave-to   { opacity: 0; transform: translate(-50%, -12px); }

::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #c7d2fe; border-radius: 8px; }
.dark ::-webkit-scrollbar-thumb { background: #4338ca; }
</style>