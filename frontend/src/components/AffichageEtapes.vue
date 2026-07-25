<template>
  <div class="h-full flex flex-col gap-6">
    <!-- Barre de progression -->
    <div class="shrink-0 flex items-center gap-5">
      <span
        class="text-[11px] font-medium uppercase tracking-wide whitespace-nowrap"
        :class="isDark ? 'text-stone-500' : 'text-stone-400'"
      >
        Progression
      </span>
      <div class="flex-1 flex gap-2 group">
        <button
          v-for="(e, i) in etapes"
          :key="i"
          @click="allerA(i)"
          class="relative h-2 rounded-full flex-1 transition-all duration-300 ease-out"
          :class="[
            i <= etapeIndex
              ? 'opacity-100 scale-y-100'
              : 'opacity-25 scale-y-75 hover:opacity-50',
            i === etapeIndex
              ? 'ring-2 ring-offset-2 ring-offset-transparent'
              : '',
            e.type === 'INITIALISATION'
              ? 'bg-indigo-500 ring-indigo-400/40'
              : e.type === 'DEGENERESCENCE'
                ? 'bg-amber-500 ring-amber-400/40'
                : 'bg-violet-500 ring-violet-400/40',
          ]"
          :title="`Étape ${i + 1} · ${labelType(e.type)}`"
        />
        <button
          @click="allerA(etapes.length)"
          class="h-2 rounded-full flex-1 transition-all duration-300 ease-out"
          :class="
            etapeIndex === etapes.length
              ? 'opacity-100 scale-y-100 bg-emerald-500 ring-2 ring-emerald-400/40 ring-offset-2 ring-offset-transparent'
              : 'opacity-25 scale-y-75 hover:opacity-50 bg-emerald-500'
          "
          title="Résultat final"
        />
      </div>

      <span
        class="text-[11px] font-mono tabular-nums whitespace-nowrap"
        :class="isDark ? 'text-stone-500' : 'text-stone-400'"
      >
        {{ etapeIndex < etapes.length ? etapeIndex + 1 : "F" }} /
        {{ etapes.length }}
      </span>
      <button
        @click="$emit('recommencer')"
        class="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-all duration-200 whitespace-nowrap"
        :class="
          isDark
            ? 'bg-gray-800 text-gray-300 hover:bg-gray-700 hover:text-white border border-gray-700'
            : 'bg-white text-stone-600 hover:bg-stone-100 hover:text-stone-800 border border-stone-200'
        "
        title="Revenir au formulaire pour un nouveau problème"
      >
        <svg
          class="w-3.5 h-3.5"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M12 4v16m8-8H4"
          />
        </svg>
        <span class="hidden sm:inline">Nouveau problème</span>
      </button>
    </div>

    <!-- Contenu principal : 2 colonnes 30/70 -->
    <div class="flex-1 flex gap-6 min-h-0">
      <!-- COLONNE GAUCHE (30%) : Détails de l'étape -->
      <div class="w-[30%] overflow-y-auto pr-1 -mr-1">
        <Transition name="panel" mode="out-in">
          <!-- Bloc INITIALISATION -->
          <div
            v-if="
              etapeIndex < etapes.length &&
              etapeActuelle.type === 'INITIALISATION'
            "
            :key="'init-' + etapeIndex"
            class="rounded-2xl border p-5 shadow-sm shadow-black/5"
            :class="
              isDark
                ? 'border-gray-800 bg-gray-900'
                : 'border-stone-200 bg-white'
            "
          >
            <StepEyebrow
              tone="indigo"
              :index="etapeIndex + 1"
              label="Initialisation"
              :isDark="isDark"
            />
            <h3
              class="text-sm font-semibold mt-3 mb-1"
              :class="isDark ? 'text-white' : 'text-gray-900'"
            >
              Affectation au minimum
            </h3>
            <p
              class="text-xs leading-relaxed mb-5"
              :class="isDark ? 'text-gray-400' : 'text-gray-500'"
            >
              {{ etapeActuelle.message }}
            </p>

            <div
              class="rounded-xl px-4 py-3.5 flex items-center justify-between mb-5"
              :class="
                isDark
                  ? 'bg-indigo-950/40 border border-indigo-900/50'
                  : 'bg-indigo-50 border border-indigo-100'
              "
            >
              <span
                class="text-[11px] uppercase tracking-wider"
                :class="isDark ? 'text-indigo-300/70' : 'text-indigo-600/70'"
              >
                Case allouée
              </span>
              <span
                class="font-semibold font-mono text-sm"
                :class="isDark ? 'text-indigo-300' : 'text-indigo-600'"
              >
                U{{ etapeActuelle.case_active[0] + 1 }} → C{{
                  etapeActuelle.case_active[1] + 1
                }}
              </span>
            </div>

            <div class="space-y-3">
              <div>
                <p
                  class="text-[11px] uppercase tracking-wider mb-1.5"
                  :class="isDark ? 'text-stone-500' : 'text-stone-400'"
                >
                  Offres restantes
                </p>
                <div class="flex flex-wrap gap-3">
                  <span
                    v-for="(v, i) in etapeActuelle.offre_restante"
                    :key="'o' + i"
                    class="text-xs font-mono px-2 py-0.5 rounded-md"
                    :class="
                      isDark
                        ? 'bg-violet-900/25 text-violet-300'
                        : 'bg-violet-50 text-violet-700'
                    "
                    >U{{ i + 1 }}: {{ v.toFixed(0) }}</span
                  >
                </div>
              </div>
              <div>
                <p
                  class="text-[11px] uppercase tracking-wider mb-1.5"
                  :class="isDark ? 'text-stone-500' : 'text-stone-400'"
                >
                  Demandes restantes
                </p>
                <div class="flex flex-wrap gap-3">
                  <span
                    v-for="(v, j) in etapeActuelle.demande_restante"
                    :key="'d' + j"
                    class="text-xs font-mono px-2 py-0.5 rounded-md"
                    :class="
                      isDark
                        ? 'bg-teal-900/25 text-teal-300'
                        : 'bg-teal-50 text-teal-700'
                    "
                    >C{{ j + 1 }}: {{ v.toFixed(0) }}</span
                  >
                </div>
              </div>
            </div>
          </div>

          <!-- Bloc DEGENERESCENCE -->
          <PanneauDegenerescence
            v-else-if="
              etapeIndex < etapes.length &&
              etapeActuelle.type === 'DEGENERESCENCE'
            "
            :key="'deg-' + etapeIndex"
            :etape="etapeActuelle"
            :config="config"
            :isDark="isDark"
          />

          <!-- Bloc OPTIMISATION -->
          <PanneauOptimisation
            v-else-if="
              etapeIndex < etapes.length &&
              etapeActuelle.type === 'OPTIMISATION'
            "
            :key="'opt-' + etapeIndex"
            :etape="etapeActuelle"
            :isDark="isDark"
          />

          <!-- Solution finale -->
          <div
            v-else
            key="final"
            class="rounded-2xl border p-5 shadow-sm shadow-black/5"
            :class="
              isDark
                ? 'border-gray-800 bg-gray-900'
                : 'border-stone-200 bg-white'
            "
          >
            <StepEyebrow
              tone="emerald"
              label="Solution optimale"
              :isDark="isDark"
            />
            <h3
              class="text-sm font-semibold mt-3 mb-1"
              :class="isDark ? 'text-white' : 'text-gray-900'"
            >
              Optimisation terminée
            </h3>
            <p
              class="text-xs leading-relaxed mb-5"
              :class="isDark ? 'text-gray-400' : 'text-gray-500'"
            >
              Tous les indices marginaux sont ≥ 0 — la solution est optimale.
            </p>
            <div
              class="rounded-xl p-5 text-center border"
              :class="
                isDark
                  ? 'bg-emerald-950/30 border-emerald-900/50'
                  : 'bg-emerald-50 border-emerald-200'
              "
            >
              <p
                class="text-[11px] uppercase tracking-widest mb-1"
                :class="isDark ? 'text-emerald-400' : 'text-emerald-600'"
              >
                Coût total minimal
              </p>
              <p
                class="text-3xl font-bold font-mono tabular-nums"
                :class="isDark ? 'text-emerald-300' : 'text-emerald-600'"
              >
                {{ final.cout_total.toFixed(2) }}
              </p>
            </div>
          </div>
        </Transition>
      </div>

      <!-- COLONNE DROITE (70%) : Matrice / Graphe -->
      <div class="flex-1 flex flex-col min-w-0">
        <!-- Segmented control -->
        <div
          class="relative inline-flex self-start mb-3 p-1 rounded-xl"
          :class="
            isDark ? 'bg-gray-900 border border-gray-800' : 'bg-stone-100'
          "
        >
          <div
            class="absolute top-1 bottom-1 rounded-lg transition-all duration-200 ease-out shadow-sm"
            :class="isDark ? 'bg-gray-800' : 'bg-white'"
            :style="
              onglet === 'matrice'
                ? { left: '4px', width: 'calc(50% - 4px)' }
                : { left: 'calc(50% + 0px)', width: 'calc(50% - 4px)' }
            "
          />
          <button
            @click="onglet = 'matrice'"
            class="relative z-10 flex items-center gap-3.5 px-4 py-1.5 rounded-lg text-xs font-semibold transition-colors"
            :class="
              onglet === 'matrice'
                ? isDark
                  ? 'text-white'
                  : 'text-gray-800'
                : isDark
                  ? 'text-gray-400'
                  : 'text-gray-500'
            "
          >
            <svg
              class="w-3.5 h-3.5"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M3 3h18v18H3zM3 9h18M3 15h18M9 3v18M15 3v18"
              />
            </svg>
            Matrice
          </button>
          <button
            @click="onglet = 'graphe'"
            class="relative z-10 flex items-center gap-3.5 px-4 py-1.5 rounded-lg text-xs font-semibold transition-colors"
            :class="
              onglet === 'graphe'
                ? isDark
                  ? 'text-white'
                  : 'text-gray-800'
                : isDark
                  ? 'text-gray-400'
                  : 'text-gray-500'
            "
          >
            <svg
              class="w-3.5 h-3.5"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <circle cx="6" cy="6" r="2.5" />
              <circle cx="18" cy="6" r="2.5" />
              <circle cx="6" cy="18" r="2.5" />
              <circle cx="18" cy="18" r="2.5" />
              <path
                stroke-linecap="round"
                d="M8.2 7.3L15.8 16.7M15.8 7.3L8.2 16.7"
              />
            </svg>
            Graphe
          </button>
        </div>

        <!-- Contenu matrice/graphe -->
        <div
          class="flex-1 rounded-2xl border overflow-hidden shadow-sm shadow-black/5"
          :class="
            isDark ? 'border-gray-800 bg-gray-900' : 'border-stone-200 bg-white'
          "
        >
          <div class="h-full overflow-auto p-5">
            <Transition name="tab" mode="out-in">
              <div :key="onglet + '-' + etapeIndex">
                <MatriceFlux
                  v-if="onglet === 'matrice'"
                  :flux="fluxCourant"
                  :config="config"
                  :metadata="metadata"
                  :case-active="caseActiveActuelle"
                  :cycle="cycleActuel"
                  :potentiels="potentielsActuels"
                  :cases-epsilon="casesEpsilonActuelles"
                  :isDark="isDark"
                />
                <GrapheFlux
                  v-else
                  :flux="fluxCourant"
                  :metadata="metadata"
                  :config="config"
                  :case-active="caseActiveActuelle"
                  :cycle="cycleActuel"
                  :potentiels="potentielsActuels"
                  :cases-epsilon="casesEpsilonActuelles"
                  :isDark="isDark"
                />
              </div>
            </Transition>
          </div>
        </div>
      </div>
    </div>

    <!-- Navigation en bas -->
    <div
      class="shrink-0 flex items-center justify-between gap-5 rounded-xl px-4 py-3 border"
      :class="
        isDark
          ? 'bg-gray-900/60 border-gray-800'
          : 'bg-stone-50 border-stone-200'
      "
    >
      <div class="flex items-center gap-3">
        <button
          @click="precedent"
          :disabled="etapeIndex === 0"
          class="p-2 rounded-lg text-stone-500 dark:text-stone-400 hover:bg-white dark:hover:bg-gray-800 hover:text-stone-800 dark:hover:text-white disabled:opacity-30 disabled:hover:bg-transparent disabled:cursor-not-allowed transition-colors"
          title="Précédent"
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
              d="M15 19l-7-7 7-7"
            />
          </svg>
        </button>
        <button
          @click="lectureAuto ? arreterLecture() : demarrerLecture()"
          class="p-2 rounded-lg transition-colors"
          :class="
            lectureAuto
              ? 'bg-indigo-500/10 text-indigo-500'
              : 'text-stone-500 dark:text-stone-400 hover:bg-white dark:hover:bg-gray-800 hover:text-stone-800 dark:hover:text-white'
          "
          :title="lectureAuto ? 'Arrêter' : 'Lecture auto'"
        >
          <svg
            v-if="!lectureAuto"
            class="w-4 h-4"
            fill="currentColor"
            viewBox="0 0 24 24"
          >
            <path d="M8 5v14l11-7z" />
          </svg>
          <svg v-else class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
            <rect x="6" y="4" width="4" height="16" />
            <rect x="14" y="4" width="4" height="16" />
          </svg>
        </button>
        <button
          @click="suivant"
          :disabled="etapeIndex === etapes.length"
          class="p-2 rounded-lg text-stone-500 dark:text-stone-400 hover:bg-white dark:hover:bg-gray-800 hover:text-stone-800 dark:hover:text-white disabled:opacity-30 disabled:hover:bg-transparent disabled:cursor-not-allowed transition-colors"
          title="Suivant"
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
              d="M9 5l7 7-7 7"
            />
          </svg>
        </button>
      </div>

      <div class="flex items-center gap-3">
        <!-- <Transition name="fade">
          <div v-if="lectureAuto" class="flex items-center gap-2">
            <span
              class="text-[11px]"
              :class="isDark ? 'text-stone-500' : 'text-stone-400'"
              >Vitesse</span
            >
            <input
              type="range"
              v-model.number="vitesse"
              min="500"
              max="3000"
              step="250"
              class="w-20 accent-indigo-500"
            />
            <span
              class="text-[11px] font-mono tabular-nums w-8"
              :class="isDark ? 'text-stone-500' : 'text-stone-400'"
            >
              {{ (vitesse / 1000).toFixed(1) }}s
            </span>
          </div>
        </Transition> -->
        <span
          class="text-[11px] font-mono tabular-nums"
          :class="isDark ? 'text-stone-500' : 'text-stone-400'"
        >
          {{ etapeIndex + 1 }} / {{ etapes.length + 1 }}
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onUnmounted, h } from "vue";
import MatriceFlux from "./MatriceFlux.vue";
import GrapheFlux from "./GrapheFlux.vue";
import PanneauOptimisation from "./PanneauOptimisation.vue";
import PanneauDegenerescence from "./PanneauDegenerescence.vue";

const props = defineProps({
  etapes: Array,
  config: Object,
  metadata: Object,
  final: Object,
  isDark: Boolean,
});
const emit = defineEmits(["recommencer"]);
const etapeIndex = ref(0);
const onglet = ref("matrice");
const lectureAuto = ref(false);
const vitesse = ref(1500);
let timerAuto = null;

const etapeActuelle = computed(() => props.etapes[etapeIndex.value]);

const fluxCourant = computed(() => {
  if (etapeIndex.value === props.etapes.length) return props.final.flux;
  const e = props.etapes[etapeIndex.value];
  if (e.type === "OPTIMISATION") return e.flux_avant ?? e.flux_apres;
  return e.flux ?? [];
});

const caseActiveActuelle = computed(() => {
  if (etapeIndex.value >= props.etapes.length) return null;
  const e = props.etapes[etapeIndex.value];
  return e.type === "INITIALISATION" ? e.case_active : null;
});

const potentielsActuels = computed(() => {
  if (etapeIndex.value >= props.etapes.length) return null;
  return props.etapes[etapeIndex.value].potentiels ?? null;
});

const casesEpsilonActuelles = computed(() => {
  if (etapeIndex.value >= props.etapes.length) return [];
  return props.etapes[etapeIndex.value].cases_epsilon ?? [];
});

const cycleActuel = computed(() => {
  if (etapeIndex.value >= props.etapes.length) return null;
  return props.etapes[etapeIndex.value].type === "OPTIMISATION"
    ? props.etapes[etapeIndex.value].cycle
    : null;
});

function labelType(type) {
  return type === "INITIALISATION"
    ? "Initialisation"
    : type === "DEGENERESCENCE"
      ? "Dégénérescence"
      : "Optimisation";
}

function precedent() {
  if (etapeIndex.value > 0) etapeIndex.value--;
}
function suivant() {
  if (etapeIndex.value < props.etapes.length) etapeIndex.value++;
}
function allerA(i) {
  etapeIndex.value = i;
}

function demarrerLecture() {
  lectureAuto.value = true;
  timerAuto = setInterval(() => {
    if (etapeIndex.value >= props.etapes.length) {
      arreterLecture();
      return;
    }
    etapeIndex.value++;
  }, vitesse.value);
}
function arreterLecture() {
  lectureAuto.value = false;
  clearInterval(timerAuto);
}

onUnmounted(() => clearInterval(timerAuto));

// Petit composant inline pour l'eyebrow des cartes (évite la répétition de markup)
const StepEyebrow = (props) =>
  h("div", { class: "flex items-center gap-2" }, [
    h(
      "span",
      {
        class: [
          "text-[11px] font-bold uppercase tracking-widest px-2 py-0.5 rounded-full",
          props.tone === "indigo" &&
            (props.isDark
              ? "bg-indigo-900/50 text-indigo-300"
              : "bg-indigo-100 text-indigo-700"),
          props.tone === "emerald" &&
            (props.isDark
              ? "bg-emerald-900/50 text-emerald-300"
              : "bg-emerald-100 text-emerald-700"),
        ],
      },
      props.label,
    ),
    props.index &&
      h(
        "span",
        { class: "text-[11px] font-mono text-stone-400 dark:text-stone-500" },
        `Étape ${props.index}`,
      ),
  ]);
</script>

<style scoped>
.tab-enter-active,
.tab-leave-active {
  transition: all 0.15s ease;
}
.tab-enter-from {
  opacity: 0;
}
.tab-leave-to {
  opacity: 0;
}

.panel-enter-active,
.panel-leave-active {
  transition: all 0.18s ease;
}
.panel-enter-from {
  opacity: 0;
  transform: translateY(4px);
}
.panel-leave-to {
  opacity: 0;
  transform: translateY(-4px);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.15s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
