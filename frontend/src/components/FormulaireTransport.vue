<template>
  <div class="h-full flex flex-col">
    <!-- Badge étape + titre -->
    <div class="flex items-center gap-3 shrink-0 mb-6">
      <span
        class="px-3 py-1 text-xs font-bold uppercase tracking-wider rounded-full"
        :class="
          isDark
            ? 'bg-indigo-900/40 text-indigo-300'
            : 'bg-indigo-100 text-indigo-600'
        "
      >
        Étape 1
      </span>
      <h2
        class="text-2xl font-bold"
        :class="isDark ? 'text-white' : 'text-stone-900'"
      >
        Saisie des données
      </h2>
    </div>

    <!-- Grille principale -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 flex-1 min-h-0">
      <!-- COLONNE GAUCHE : Matrice + Dimensions + Exemples -->
      <div class="lg:col-span-2 min-h-0">
        <div
          class="rounded-2xl p-6 ring-1 shadow-sm h-full flex flex-col"
          :class="
            isDark ? 'bg-gray-900 ring-gray-800' : 'bg-white ring-stone-200/60'
          "
        >
          <!-- En-tête : titre + dimensions côte à côte -->
          <div class="flex items-start justify-between gap-4 mb-4 flex-wrap">
            <h3
              class="text-sm font-semibold text-stone-500 dark:text-stone-400 uppercase tracking-wider pt-1.5"
            >
              Matrice des coûts, offres & demandes
            </h3>
            <div class="flex items-center gap-3 flex-wrap">
              <DimControle
                label="Sources"
                compact
                :valeur="nbLignes"
                :min="2"
                :max="6"
                :isDark="isDark"
                @incrementer="changerDim('lignes', 1)"
                @decrementer="changerDim('lignes', -1)"
              />
              <DimControle
                label="Destinations"
                compact
                :valeur="nbColonnes"
                :min="2"
                :max="6"
                :isDark="isDark"
                @incrementer="changerDim('colonnes', 1)"
                @decrementer="changerDim('colonnes', -1)"
              />
            </div>
          </div>

          <div class="overflow-auto">
            <table class="w-full border-collapse">
              <thead>
                <tr>
                  <th
                    class="w-20 p-2 sticky left-0 z-10"
                    :class="isDark ? 'bg-gray-900' : 'bg-white'"
                  ></th>
                  <th
                    v-for="j in nbColonnes"
                    :key="j"
                    class="p-2 text-xs font-semibold text-center min-w-20"
                    :class="isDark ? 'text-indigo-400' : 'text-indigo-600'"
                  >
                    Client {{ j }}
                  </th>
                  <th
                    class="p-2 text-xs font-semibold text-center min-w-20"
                    :class="isDark ? 'text-violet-400' : 'text-violet-600'"
                  >
                    Offre
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="i in nbLignes" :key="i" class="group">
                  <td
                    class="p-2 text-xs font-semibold text-right pr-4 whitespace-nowrap sticky left-0 z-10 transition-colors"
                    :class="[
                      isDark
                        ? 'text-indigo-400 bg-gray-900'
                        : 'text-indigo-600 bg-white',
                      'group-hover:text-indigo-500',
                    ]"
                  >
                    Usine {{ i }}
                  </td>
                  <td v-for="j in nbColonnes" :key="j" class="p-1.5">
                    <input
                      type="number"
                      v-model.number="couts[i - 1][j - 1]"
                      :class="[
                        'w-full rounded-xl px-3 py-3 text-center text-sm font-mono tabular-nums',
                        'border-0',
                        'focus:ring-2 focus:ring-indigo-500',
                        'transition-colors duration-150',
                        erreursCellules[`${i - 1}-${j - 1}`]
                          ? 'ring-2 ring-red-40'
                          : '',
                        backgroundColor(1),
                        isDark
                          ? 'bg-gray-800 focus:bg-gray-800'
                          : 'bg-stone-50 focus:bg-white',
                      ]"
                      placeholder="0"
                      min="0"
                      @blur="validerCellule(i - 1, j - 1)"
                    />
                  </td>
                  <td class="p-1.5">
                    <input
                      type="number"
                      v-model.number="offres[i - 1]"
                      :class="[
                        'w-full rounded-xl px-3 py-3 text-center text-sm font-mono tabular-nums',
                        'border-0',
                        'focus:ring-2 focus:ring-violet-500',
                        'transition-colors duration-150',
                        erreurs.offres ? 'ring-2 ring-red-400' : '',
                        isDark
                          ? 'text-violet-300 placeholder-violet-600/50 bg-violet-900/20 focus:bg-violet-900/30'
                          : 'text-violet-700 placeholder-violet-300 bg-violet-50 focus:bg-white',
                      ]"
                      placeholder="0"
                      min="0"
                    />
                  </td>
                </tr>

                <!-- Ligne Demandes -->
                <tr
                  class="border-t-2"
                  :class="isDark ? 'border-gray-800' : 'border-stone-200'"
                >
                  <td
                    class="p-2 text-xs font-semibold text-right pr-4 sticky left-0 z-10"
                    :class="
                      isDark
                        ? 'text-teal-400 bg-gray-900'
                        : 'text-teal-600 bg-white'
                    "
                  >
                    Demande
                  </td>
                  <td v-for="j in nbColonnes" :key="j" class="p-1.5">
                    <input
                      type="number"
                      v-model.number="demandes[j - 1]"
                      :class="[
                        'w-full rounded-xl px-3 py-3 text-center text-sm font-mono tabular-nums',
                        'border-0',
                        'focus:ring-2 focus:ring-teal-500 ',
                        'transition-colors duration-150',
                        erreurs.demandes ? 'ring-2 ring-red-400' : '',
                        isDark
                          ? 'text-teal-300 placeholder-teal-600/50 bg-teal-900/20 focus:bg-teal-900/30'
                          : 'text-teal-700 placeholder-teal-300 bg-teal-50 focus:bg-white',
                      ]"
                      placeholder="0"
                      min="0"
                    />
                  </td>
                  <td class="p-2 text-center">
                    <span
                      class="text-lg font-bold font-mono"
                      :class="
                        estEquilibre
                          ? isDark
                            ? 'text-emerald-400'
                            : 'text-emerald-600'
                          : isDark
                            ? 'text-amber-400'
                            : 'text-amber-600'
                      "
                    >
                      {{ estEquilibre ? "=" : "≠" }}
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Erreur coûts -->
          <div
            v-if="erreurs.couts"
            class="mt-4 flex items-center gap-2 text-xs rounded-lg p-3"
            :class="
              isDark ? 'text-red-400 bg-red-900/20' : 'text-red-600 bg-red-50'
            "
          >
            <svg
              class="w-4 h-4 shrink-0"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path
                fill-rule="evenodd"
                d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z"
                clip-rule="evenodd"
              />
            </svg>
            {{ erreurs.couts }}
          </div>

          <!-- Exemples : sous le tableau, même carte -->
          <div
            class="mt-5 pt-4 border-t"
            :class="isDark ? 'border-gray-800' : 'border-stone-200'"
          >
            <h3
              class="text-xs font-semibold uppercase tracking-wider mb-2.5"
              :class="isDark ? 'text-stone-400' : 'text-stone-500'"
            >
              Exemples
            </h3>
            <div class="flex flex-wrap gap-2">
              <button
                v-for="ex in exemples"
                :key="ex.label"
                @click="chargerExemple(ex)"
                class="px-3 py-1.5 rounded-full text-xs font-medium transition-all duration-200"
                :class="
                  isDark
                    ? 'bg-gray-800 text-gray-300 hover:bg-indigo-900/40 hover:text-indigo-300'
                    : 'bg-stone-100 text-stone-600 hover:bg-indigo-50 hover:text-indigo-700'
                "
              >
                {{ ex.label }}
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- COLONNE DROITE : Équilibre + Répartition + Résoudre -->
      <div class="flex flex-col gap-5 min-h-0">
        <!-- Carte Balance -->
        <div
          class="rounded-2xl p-5 shadow-sm shrink-0"
          :class="
            isDark ? 'bg-gray-900 ring-gray-800' : 'bg-white ring-stone-200/60'
          "
        >
          <h3
            class="text-xs font-semibold uppercase tracking-wider mb-3"
            :class="isDark ? 'text-stone-400' : 'text-stone-500'"
          >
            Équilibre
          </h3>
          <div class="flex items-center justify-between gap-4">
            <div class="flex-1 text-center">
              <p
                class="text-xs"
                :class="isDark ? 'text-stone-400' : 'text-stone-500'"
              >
                Offre totale
              </p>
              <p
                class="text-2xl font-bold font-mono tabular-nums text-violet-600 dark:text-violet-400"
                :class="isDark ? 'text-violet-400' : 'text-violet-600'"
              >
                {{ totalOffre }}
              </p>
            </div>
            <div class="flex-1 text-center">
              <p
                class="text-xs"
                :class="isDark ? 'text-stone-400' : 'text-stone-500'"
              >
                Demande totale
              </p>
              <p
                class="text-2xl font-bold font-mono tabular-nums text-teal-600 dark:text-teal-400"
                :class="isDark ? 'text-teal-400' : 'text-teal-600'"
              >
                {{ totalDemande }}
              </p>
            </div>
          </div>
          <div
            class="mt-4 flex items-center justify-center gap-2 px-3 py-2 rounded-full text-xs font-semibold transition-colors"
            :class="
              estEquilibre
                ? isDark
                  ? 'bg-emerald-900/30 text-emerald-400'
                  : 'bg-emerald-50 text-emerald-700'
                : isDark
                  ? 'bg-amber-900/30 text-amber-400'
                  : 'bg-amber-50 text-amber-700'
            "
          >
            <span
              class="w-2 h-2 rounded-full"
              :class="estEquilibre ? 'bg-emerald-500' : 'bg-amber-500'"
            ></span>
            {{
              estEquilibre
                ? "Équilibré"
                : `Écart de ${Math.abs(totalOffre - totalDemande)}`
            }}
          </div>
        </div>

        <!-- Carte Répartition : comble l'espace avec un vrai contenu utile,
       et grandit naturellement avec le nombre de sources/destinations -->
        <div
          class="rounded-2xl p-5 shadow-sm flex-1 min-h-0 overflow-y-auto"
          :class="
            isDark ? 'bg-gray-900 ring-gray-800' : 'bg-white ring-stone-200/60'
          "
        >
          <h3
            class="text-xs font-semibold uppercase tracking-wider mb-3"
            :class="isDark ? 'text-stone-400' : 'text-stone-500'"
          >
            Répartition
          </h3>

          <div class="space-y-3">
            <div>
              <p
                class="text-[11px] font-medium mb-1.5"
                :class="isDark ? 'text-violet-400' : 'text-violet-600'"
              >
                Offre par usine
              </p>
              <div class="space-y-1.5">
                <div
                  v-for="(v, i) in offres"
                  :key="'off-' + i"
                  class="flex items-center gap-2"
                >
                  <span
                    class="text-[11px] w-14 shrink-0"
                    :class="isDark ? 'text-stone-400' : 'text-stone-500'"
                    >Usine {{ i + 1 }}</span
                  >
                  <div
                    class="flex-1 h-2 rounded-full overflow-hidden"
                    :class="isDark ? 'bg-gray-800' : 'bg-stone-100'"
                  >
                    <div
                      class="h-full rounded-full transition-all duration-300"
                      :class="isDark ? 'bg-violet-500' : 'bg-violet-400'"
                      :style="{
                        width: `${totalOffre > 0 ? (v / totalOffre) * 100 : 0}%`,
                      }"
                    ></div>
                  </div>
                  <span
                    class="text-[11px] font-mono tabular-nums w-8 text-right"
                    :class="isDark ? 'text-violet-300' : 'text-violet-700'"
                  >
                    {{ v }}
                  </span>
                </div>
              </div>
            </div>

            <div>
              <p
                class="text-[11px] font-medium mb-1.5"
                :class="isDark ? 'text-teal-400' : 'text-teal-600'"
              >
                Demande par client
              </p>
              <div class="space-y-1.5">
                <div
                  v-for="(v, j) in demandes"
                  :key="'dem-' + j"
                  class="flex items-center gap-2"
                >
                  <span
                    class="text-[11px] w-14 shrink-0"
                    :class="isDark ? 'text-stone-400' : 'text-stone-500'"
                    >Client {{ j + 1 }}</span
                  >
                  <div
                    class="flex-1 h-2 rounded-full overflow-hidden"
                    :class="isDark ? 'bg-gray-800' : 'bg-stone-100'"
                  >
                    <div
                      class="h-full rounded-full transition-all duration-300"
                      :class="isDark ? 'bg-teal-500' : 'bg-teal-400'"
                      :style="{
                        width: `${totalDemande > 0 ? (v / totalDemande) * 100 : 0}%`,
                      }"
                    ></div>
                  </div>
                  <span
                    class="text-[11px] font-mono tabular-nums w-8 text-right"
                    :class="isDark ? 'text-teal-300' : 'text-teal-700'"
                  >
                    {{ v }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Bouton Résoudre -->
        <div class="space-y-3 shrink-0">
          <button
            @click="soumettre"
            class="w-full flex items-center justify-center gap-3 px-6 py-4 rounded-2xl font-semibold text-white transition-all duration-200"
            :class="buttonClass()"
          >
            <svg
              class="w-5 h-5"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M13 10V3L4 14h7v7l9-11h-7z"
              />
            </svg>
            Résoudre
          </button>
          <p
            v-if="!estValide && !estEquilibre && totalOffre > 0"
            class="text-xs text-center flex items-center justify-center gap-1"
            :class="isDark ? 'text-amber-400' : 'text-amber-600'"
          >
            <span>⚠</span> Le problème doit être équilibré
          </p>
          <p
            v-else-if="!estValide && estEquilibre && !coutsValides"
            class="text-xs text-center flex items-center justify-center gap-1"
            :class="isDark ? 'text-red-400' : 'text-red-600'"
          >
            <span>⚠</span> Certains coûts sont invalides
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, reactive } from "vue";
import DimControle from "./DimControle.vue";

const emit = defineEmits(["resoudre"]);

const props = defineProps({
  isDark: Boolean,
});

const nbLignes = ref(2);
const nbColonnes = ref(3);

const couts = ref([
  [2, 3, 1],
  [5, 4, 8],
]);
const offres = ref([100, 200]);
const demandes = ref([80, 120, 100]);

const erreurs = reactive({ couts: "", offres: false, demandes: false });
const erreursCellules = reactive({});

function backgroundColor(n) {
  if (n === 1) {
    return props.isDark ? "bg-stone-50" : "bg-gray-800";
  }
}

function buttonClass() {
  if (estValide.value) {
    return "bg-indigo-600 hover:bg-indigo-700 shadow-lg shadow-indigo-500/25 hover:shadow-xl hover:-translate-y-0.5";
  }
  return props.isDark
    ? "bg-gray-700 text-gray-400 cursor-not-allowed"
    : "bg-stone-300 text-stone-500 cursor-not-allowed";
}

function changerDim(type, delta) {
  if (type === "lignes") {
    const n = Math.max(2, Math.min(6, nbLignes.value + delta));
    if (n === nbLignes.value) return;
    nbLignes.value = n;
    if (delta > 0) {
      couts.value.push(Array(nbColonnes.value).fill(0));
      offres.value.push(0);
    } else {
      couts.value.pop();
      offres.value.pop();
    }
  } else {
    const n = Math.max(2, Math.min(6, nbColonnes.value + delta));
    if (n === nbColonnes.value) return;
    nbColonnes.value = n;
    if (delta > 0) {
      couts.value.forEach((r) => r.push(0));
      demandes.value.push(0);
    } else {
      couts.value.forEach((r) => r.pop());
      demandes.value.pop();
    }
  }
  // Nettoyage des erreurs de cellules devenues obsolètes
  Object.keys(erreursCellules).forEach((k) => {
    const [i, j] = k.split("-").map(Number);
    if (i >= nbLignes.value || j >= nbColonnes.value) delete erreursCellules[k];
  });
}

const totalOffre = computed(() =>
  offres.value.reduce((a, b) => a + (+b || 0), 0),
);
const totalDemande = computed(() =>
  demandes.value.reduce((a, b) => a + (+b || 0), 0),
);
const estEquilibre = computed(
  () =>
    totalOffre.value > 0 &&
    Math.abs(totalOffre.value - totalDemande.value) < 0.001,
);
const coutsValides = computed(() =>
  couts.value.every((row) =>
    row.every((v) => v !== null && v !== "" && +v >= 0),
  ),
);
const estValide = computed(() => estEquilibre.value && coutsValides.value);

function validerCellule(i, j) {
  const v = couts.value[i][j];
  erreursCellules[`${i}-${j}`] = v === null || v === "" || +v < 0;
}

const exemples = [
  {
    label: "2×3 Basique",
    couts: [
      [2, 3, 1],
      [5, 4, 8],
    ],
    offres: [100, 200],
    demandes: [80, 120, 100],
  },
  {
    label: "3×3 Classique",
    couts: [
      [4, 8, 8],
      [16, 24, 16],
      [8, 16, 24],
    ],
    offres: [76, 82, 77],
    demandes: [72, 102, 61],
  },
  {
    label: "3×4 Grand",
    couts: [
      [2, 3, 1, 5],
      [7, 3, 4, 2],
      [6, 1, 5, 4],
    ],
    offres: [120, 80, 80],
    demandes: [150, 70, 40, 20],
  },
  {
    label: "2×2 Minimal",
    couts: [
      [3, 1],
      [2, 4],
    ],
    offres: [50, 50],
    demandes: [60, 40],
  },
  {
    label: "5×4 Cas dégénéré",
    couts: [
      [2, 3, 5, 7],
      [1, 4, 6, 2],
      [3, 2, 4, 5],
      [4, 5, 2, 3],
      [6, 1, 3, 4],
    ],
    offres: [30, 40, 50, 20, 60],
    demandes: [50, 60, 40, 50],
  },
  {
    label: "TD n°7",
    couts: [
      [9, 12, 9, 6, 9, 10],
      [7, 3, 7, 7, 5, 5],
      [6, 5, 9, 11, 3, 11],
      [6, 8, 11, 2, 2, 10],
    ],
    offres: [50, 60, 20, 90],
    demandes: [40, 30, 70, 20, 40, 20],
  },
  {
    label: "TD n°8",
    couts: [
      [21, 11, 84, 49, 13],
      [27, 52, 43, 29, 42],
      [11, 47, 14, 80, 93],
      [52, 14, 76, 74, 54],
    ],
    offres: [896, 782, 943, 928],
    demandes: [800, 439, 50, 790, 1470],
  },
  {
    label: "TD n°9",
    couts: [
      [45, 60, 15, 30, 45, 40],
      [35, 15, 10, 35, 25, 5],
      [20, 15, 45, 55, 10, 55],
      [30, 40, 55, 10, 10, 50],
    ],
    offres: [25, 30, 10, 45],
    demandes: [20, 15, 35, 10, 20, 10],
  },
];

function chargerExemple(ex) {
  nbLignes.value = ex.couts.length;
  nbColonnes.value = ex.couts[0].length;
  couts.value = ex.couts.map((r) => [...r]);
  offres.value = [...ex.offres];
  demandes.value = [...ex.demandes];
  Object.keys(erreursCellules).forEach((k) => delete erreursCellules[k]);
}

function soumettre() {
  if (!estValide.value) return;
  emit("resoudre", {
    couts: couts.value,
    offres: offres.value,
    demandes: demandes.value,
  });
}
</script>
