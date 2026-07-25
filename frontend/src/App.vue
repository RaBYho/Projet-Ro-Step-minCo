<template>
  <div
    :class="isDark ? 'dark' : ''"
    class="flex h-screen overflow-hidden transition-colors duration-300"
  >
    <!-- Main Content -->
    <div
      class="flex-1 flex flex-col h-full overflow-hidden"
      :class="isDark ? 'bg-gray-950' : 'bg-stone-100'"
    >
      <!-- Header modernisé -->
      <header
        class="flex items-center justify-between px-8 py-4 backdrop-blur-md shadow-sm border-b shrink-0"
        :class="
          isDark
            ? 'bg-gray-900/80 border-gray-800/60 '
            : 'bg-white/80 border-stone-200/60'
        "
      >
        <div class="flex items-center gap-3">
          <div
            class="w-9 h-9 rounded-xl bg-indigo-600 flex items-center justify-center shadow-md shadow-indigo-500/25"
          >
            <svg
              class="w-5 h-5 text-white"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M9 17a2 2 0 11-4 0 2 2 0 014 0zM19 17a2 2 0 11-4 0 2 2 0 014 0z"
              />
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M13 16V6a1 1 0 00-1-1H4a1 1 0 00-1 1v10a1 1 0 001 1h1m8-1a1 1 0 01-1 1H9m4-1V8a1 1 0 011-1h2.586a1 1 0 01.707.293l3.414 3.414a1 1 0 01.293.707V16a1 1 0 01-1 1h-1m-6-1a1 1 0 001 1h1M5 17a2 2 0 104 0m-4 0a2 2 0 114 0m6 0a2 2 0 104 0m-4 0a2 2 0 114 0"
              />
            </svg>
          </div>
          <h1
            class="text-xl font-bold"
            :class="isDark ? 'text-white' : 'text-gray-900'"
          >
            Problème de transport
          </h1>
          <span
            v-if="phase !== 'formulaire'"
            class="px-3 py-1 text-xs font-medium rounded-full"
            :class="
              phase === 'chargement'
                ? isDark
                  ? 'bg-indigo-900/30 text-indigo-300'
                  : 'bg-indigo-50 text-indigo-700'
                : isDark
                  ? 'bg-emerald-900/30 text-emerald-300'
                  : 'bg-emerald-50 text-emerald-700'
            "
          >
            {{ phase === "chargement" ? "En cours" : "Résultats" }}
          </span>
        </div>

        <button
          @click="isDark = !isDark"
          class="flex items-center gap-2 px-4 py-2 rounded-xl transition-all"
          :class="
            isDark
              ? 'bg-gray-800 text-gray-200 hover:bg-gray-700'
              : 'bg-gray-200 text-gray-600 hover:bg-stone-100'
          "
        >
          <svg
            v-if="isDark"
            class="w-4 h-4"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"
            />
          </svg>
          <svg
            v-else
            class="w-4 h-4"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"
            />
          </svg>
          <span class="hidden sm:inline text-xs font-medium">
            {{ isDark ? "Mode clair" : "Mode sombre" }}
          </span>
        </button>
      </header>

      <!-- Toast moderne -->
      <Transition name="toast">
        <div
          v-if="erreur"
          class="fixed top-20 left-1/2 -translate-x-1/2 z-50 w-100 max-w-[90vw] rounded-2xl shadow-2xl backdrop-blur-xl border"
          :class="
            isDark
              ? 'bg-gray-900/90 border-red-800/50'
              : 'bg-white/90 border-red-200/50'
          "
        >
          <div class="flex items-start gap-4 p-5">
            <div
              class="w-10 h-10 rounded-full flex items-center justify-center shrink-0"
              :class="isDark ? 'bg-red-900/50' : 'bg-red-100'"
            >
              <svg
                class="w-5 h-5 text-red-500"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
            </div>
            <div class="flex-1 min-w-0">
              <p
                class="text-sm font-semibold"
                :class="isDark ? 'text-red-300' : 'text-red-700'"
              >
                {{ erreur.titre }}
              </p>
              <p
                class="text-xs mt-1 wrap-break-word"
                :class="isDark ? 'text-red-400' : 'text-red-500'"
              >
                {{ erreur.detail }}
              </p>
            </div>
            <button
              @click="erreur = null"
              class="shrink-0 p-1 rounded-lg transition-colors"
              :class="
                isDark
                  ? 'text-gray-500 hover:text-gray-300 hover:bg-gray-800'
                  : 'text-gray-400 hover:text-gray-600 hover:bg-gray-100'
              "
            >
              <svg
                class="w-4 h-4"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M6 18L18 6M6 6l12 12"
                />
              </svg>
            </button>
          </div>
        </div>
      </Transition>

      <!-- Main content area -->
      <main
        class="flex-1 overflow-y-auto p-8"
        :class="isDark ? 'text-gray-100' : 'text-gray-800'"
      >
        <Transition name="page" mode="out-in">
          <FormulaireTransport
            v-if="phase === 'formulaire'"
            @resoudre="lancerResolution"
            :is-dark="isDark"
          />
          <div
            v-else-if="phase === 'chargement'"
            class="flex items-center justify-center min-h-[60vh]"
          >
            <LoaderAnimation :message="messageChargement" :is-dark="isDark" />
          </div>
          <AffichageEtapes
            v-else-if="phase === 'resultats'"
            :etapes="etapes"
            :config="config"
            :metadata="metadata"
            :final="resultatFinal"
            :is-dark="isDark"
            @recommencer="recommencer"
          />
        </Transition>
      </main>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, watch } from "vue";
import { useRouter, useRoute } from "vue-router";
import FormulaireTransport from "./components/FormulaireTransport.vue";
import AffichageEtapes from "./components/AffichageEtapes.vue";
import LoaderAnimation from "./components/LoaderAnimation.vue";

// 1. URL dynamique de l'API (Render en prod, Localhost en dev)
const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

const isDark = ref(false);
const phase = ref("formulaire");
const etapes = ref([]);
const config = ref(null);
const metadata = ref(null);
const resultatFinal = ref(null);
const messageChargement = ref("Initialisation...");
const erreur = ref(null);

const router = useRouter();
const route = useRoute();

function afficherErreur(titre, detail) {
  erreur.value = { titre, detail };
  setTimeout(() => {
    erreur.value = null;
  }, 7000);
}

async function lancerResolution(donnees) {
  erreur.value = null;
  phase.value = "chargement";
  messageChargement.value = "Connexion au serveur...";
  try {
    await new Promise((r) => setTimeout(r, 300));
    messageChargement.value = "Calcul de la solution initiale...";

    // 2. Utilisation de la variable API_URL
    const response = await fetch(`${API_URL}/resoudre`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(donnees),
    });

    if (!response.ok) {
      const txt = await response.text();
      throw new Error(`Erreur HTTP ${response.status} : ${txt}`);
    }
    const data = await response.json();
    if (data.erreur) {
      afficherErreur("Données invalides", data.erreur);
      phase.value = "formulaire";
      return;
    }
    messageChargement.value = "Optimisation Stepping Stone...";
    await new Promise((r) => setTimeout(r, 500));
    etapes.value = data.etapes;
    config.value = data.config;
    metadata.value = data.metadata;
    resultatFinal.value = data.final;
    await new Promise((r) => setTimeout(r, 200));
    phase.value = "resultats";
  } catch (e) {
    if (
      e.message.includes("fetch") ||
      e.message.includes("network") ||
      e.message.includes("Failed")
    ) {
      afficherErreur(
        "Serveur inaccessible",
        `Impossible de contacter l'API sur ${API_URL}. Vérifiez que le backend tourne.`,
      );
    } else {
      afficherErreur("Erreur", e.message);
    }
    phase.value = "formulaire";
  }
}

function recommencer() {
  phase.value = "formulaire";
  etapes.value = [];
  config.value = null;
  router.push("/");
}

function loadDarkMode() {
  const saved = localStorage.getItem("dark-mode");
  if (saved !== null) {
    isDark.value = saved === "true";
  }
}

onMounted(loadDarkMode);
watch(isDark, (newValue) => {
  localStorage.setItem("dark-mode", String(newValue));
});
</script>
