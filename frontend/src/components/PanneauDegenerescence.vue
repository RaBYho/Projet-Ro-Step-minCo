<template>
  <div class="space-y-4">
    <!-- Alerte principale -->
    <div
      class="rounded-2xl p-4 shadow-sm border-2"
      :class="
        isDark
          ? 'bg-amber-900/20 border-amber-700'
          : 'bg-amber-50 border-amber-300'
      "
    >
      <div class="flex items-start gap-3">
        <div
          class="w-9 h-9 rounded-xl flex items-center justify-center shrink-0"
          :class="isDark ? 'bg-amber-900/60' : 'bg-amber-100'"
        >
          <svg
            class="w-4.5 h-4.5 shrink-0"
            :class="isDark ? 'text-amber-400' : 'text-amber-600'"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
            />
          </svg>
        </div>
        <div class="flex-1 min-w-0">
          <h3
            class="text-sm font-bold mb-1"
            :class="isDark ? 'text-amber-200' : 'text-amber-800'"
          >
            Cas dégénéré détecté
          </h3>
          <p
            class="text-xs leading-relaxed"
            :class="isDark ? 'text-amber-300' : 'text-amber-700'"
          >
            {{ etape.message }}
          </p>
        </div>
      </div>
    </div>

    <!-- Explication théorique + comptage -->
    <div
      class="rounded-2xl border p-4 shadow-sm"
      :class="
        isDark ? 'bg-gray-900 border-gray-800' : 'bg-white border-stone-200'
      "
    >
      <h4
        class="text-[11px] font-semibold tracking-widest uppercase mb-2.5"
        :class="isDark ? 'text-gray-500' : 'text-gray-400'"
      >
        Pourquoi ce cas se produit
      </h4>
      <p
        class="text-xs leading-relaxed mb-4"
        :class="isDark ? 'text-gray-300' : 'text-gray-600'"
      >
        Un problème <strong>m × n</strong> requiert exactement
        <strong>m + n − 1</strong> cases de base pour calculer les potentiels
        u<sub>i</sub>, v<sub>j</sub>. La dégénérescence survient quand une ligne
        et une colonne s'épuisent <em>simultanément</em>, faisant tomber le
        nombre de cases actives sous ce seuil.
      </p>
      <div class="grid grid-cols-3 gap-2">
        <div
          class="rounded-xl p-2.5 text-center"
          :class="isDark ? 'bg-gray-800' : 'bg-stone-50'"
        >
          <p
            class="text-[9px] uppercase tracking-wider mb-1"
            :class="isDark ? 'text-gray-400' : 'text-gray-400'"
          >
            Remplies
          </p>
          <p
            class="text-lg font-bold font-mono tabular-nums"
            :class="isDark ? 'text-red-400' : 'text-red-500'"
          >
            {{ casesRemplies }}
          </p>
        </div>
        <div
          class="rounded-xl p-2.5 text-center"
          :class="isDark ? 'bg-gray-800' : 'bg-stone-50'"
        >
          <p
            class="text-[9px] uppercase tracking-wider mb-1"
            :class="isDark ? 'text-gray-400' : 'text-gray-400'"
          >
            Requises
          </p>
          <p
            class="text-lg font-bold font-mono tabular-nums"
            :class="isDark ? 'text-gray-200' : 'text-gray-700'"
          >
            {{ casesRequises }}
          </p>
        </div>
        <div
          class="rounded-xl p-2.5 text-center"
          :class="isDark ? 'bg-amber-900/30' : 'bg-amber-50'"
        >
          <p
            class="text-[9px] uppercase tracking-wider mb-1"
            :class="isDark ? 'text-amber-600' : 'text-amber-600'"
          >
            ajoutés
          </p>
          <p
            class="text-lg font-bold font-mono tabular-nums"
            :class="isDark ? 'text-amber-300' : 'text-amber-600'"
          >
            {{ etape.cases_epsilon?.length ?? 0 }}
          </p>
        </div>
      </div>
    </div>

    <!-- Nœuds epsilon -->
    <div
      class="rounded-2xl border p-4 shadow-sm"
      :class="
        isDark
          ? 'bg-gray-900 border-gray-700'
          : 'bg-white border-amber-300 border-dashed'
      "
    >
      <h4
        class="text-[11px] font-semibold tracking-widest uppercase mb-3 flex items-center gap-2"
        :class="isDark ? 'text-amber-400' : 'text-amber-600'"
      >
        <span
          class="w-2 h-2 rounded-sm inline-block animate-pulse bg-amber-400"
        ></span>
        Nœuds ε insérés
      </h4>

      <div class="flex flex-wrap gap-2 mb-3">
        <div
          v-for="[i, j] in etape.cases_epsilon"
          :key="`eps-${i}-${j}`"
          class="flex items-center gap-2 rounded-xl px-3 py-2"
          :class="isDark ? 'bg-amber-900/30' : 'bg-amber-50'"
        >
          <span
            class="text-base font-bold leading-none font-mono"
            :class="isDark ? 'text-amber-300' : 'text-amber-500'"
          >
            ε
          </span>
          <div>
            <p
              class="text-xs font-bold font-mono"
              :class="isDark ? 'text-amber-200' : 'text-amber-700'"
            >
              U{{ i + 1 }} → C{{ j + 1 }}
            </p>
            <p
              class="text-[9px]"
              :class="isDark ? 'text-amber-400' : 'text-amber-500'"
            >
              flux ≈ 0
            </p>
          </div>
        </div>
      </div>

      <div
        class="rounded-xl p-3 space-y-1.5"
        :class="isDark ? 'bg-amber-900/20' : 'bg-amber-50'"
      >
        <p
          class="text-[11px] leading-relaxed"
          :class="isDark ? 'text-amber-300' : 'text-amber-700'"
        >
          <strong>Matrice →</strong> surlignées en jaune avec le badge
          <strong>ε</strong>.
        </p>
        <p
          class="text-[11px] leading-relaxed"
          :class="isDark ? 'text-amber-300' : 'text-amber-700'"
        >
          <strong>Graphe →</strong> nœuds sources/destinations concernés en
          jaune.
        </p>
        <p
          class="text-[11px] leading-relaxed"
          :class="isDark ? 'text-amber-300' : 'text-amber-700'"
        >
          <strong>Élimination →</strong> traités comme flux réels ;
          disparaissent quand leur flux atteint 0 lors d'un pivot.
        </p>
      </div>
    </div>

    <!-- Rappel navigation -->
    <div
      class="flex items-center gap-2 rounded-xl px-3 py-2.5 text-[11px]"
      :class="
        isDark
          ? 'bg-indigo-900/20 text-indigo-400'
          : 'bg-indigo-50 text-indigo-600'
      "
    >
      <svg
        class="w-3.5 h-3.5 shrink-0"
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
      Voir <strong class="mx-0.5">Matrice</strong> et
      <strong class="mx-0.5">Graphe</strong> à droite — nœuds ε en jaune.
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";
const props = defineProps({ etape: Object, config: Object, isDark: Boolean });

const casesRequises = computed(() => {
  if (!props.etape.flux) return "?";
  return props.etape.flux.length + (props.etape.flux[0]?.length ?? 0) - 1;
});

// Compte réel des cases non-nulles dans le flux (hors epsilon), au lieu de
// la déduire arithmétiquement de casesRequises — sinon l'affichage reste
// toujours cohérent avec lui-même mais jamais avec la vraie matrice.
const epsSet = computed(
  () => new Set((props.etape.cases_epsilon ?? []).map(([i, j]) => `${i}-${j}`)),
);
const casesRemplies = computed(() => {
  if (!props.etape.flux) return "?";
  let count = 0;
  for (let i = 0; i < props.etape.flux.length; i++) {
    for (let j = 0; j < props.etape.flux[i].length; j++) {
      const isEps = epsSet.value.has(`${i}-${j}`);
      if (!isEps && (props.etape.flux[i][j] ?? 0) > 1e-6) count++;
    }
  }
  return count;
});
</script>
