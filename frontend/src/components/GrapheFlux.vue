<template>
  <div class="w-full">
    <!-- Toggle potentiels / offre-demande -->
    <div class="flex items-center gap-2 mb-3 flex-wrap">
      <span
        class="text-[10px] uppercase tracking-wider text-gray-400 dark:text-gray-500"
        >Nœuds</span
      >
      <div
        class="relative inline-flex p-0.5 rounded-lg"
        :class="isDark ? 'bg-gray-800' : 'bg-stone-100'"
      >
        <div
          class="absolute top-0.5 bottom-0.5 rounded-md transition-all duration-200 ease-out shadow-sm"
          :class="isDark ? 'bg-gray-900' : 'bg-white'"
          :style="
            mode === 'potentiels'
              ? { left: '2px', width: 'calc(50% - 2px)' }
              : { left: 'calc(50% + 0px)', width: 'calc(50% - 2px)' }
          "
        />
        <button
          @click="mode = 'potentiels'"
          :disabled="!aPotentiels"
          class="relative z-10 px-2.5 py-0.5 rounded-md text-[11px] font-semibold transition-colors"
          :class="
            mode === 'potentiels'
              ? isDark
                ? 'text-white'
                : 'text-gray-800'
              : 'text-gray-400 dark:text-gray-500 disabled:opacity-40 disabled:cursor-not-allowed'
          "
        >
          Potentiels u, v
        </button>
        <button
          @click="mode = 'offre'"
          class="relative z-10 px-2.5 py-0.5 rounded-md text-[11px] font-semibold transition-colors"
          :class="
            mode === 'offre'
              ? isDark
                ? 'text-white'
                : 'text-gray-800'
              : 'text-gray-400 dark:text-gray-500'
          "
        >
          Offre / Demande
        </button>
      </div>
      <span
        v-if="nbEpsilon > 0"
        class="ml-auto flex items-center gap-1.5 text-[11px] font-medium text-amber-600 dark:text-amber-400"
      >
        <span
          class="w-1.5 h-1.5 rounded-full bg-amber-400 animate-pulse inline-block"
        ></span>
        {{ nbEpsilon }} ε actif{{ nbEpsilon > 1 ? "s" : "" }}
      </span>
    </div>

    <!--
      Conteneur à HAUTEUR FIXE : c'est ce qui force le graphe à rétrécir
      (et non plus juste "se resserrer") quand il y a beaucoup de nœuds.
      Le SVG interne, avec preserveAspectRatio, scale tout son contenu
      pour tenir dans cette boîte, quel que soit le nombre de sources/destinations.
    -->
    <div class="w-full h-56">
      <svg
        :viewBox="`0 0 ${W} ${H}`"
        preserveAspectRatio="xMidYMid meet"
        width="100%"
        height="100%"
        class="block"
      >
        <!-- ── Arêtes ──────────────────────────────────────────────────────── -->
        <line
          v-for="lien in liens"
          :key="`l-${lien.i}-${lien.j}`"
          :x1="SX"
          :y1="ySrc(lien.i)"
          :x2="DX"
          :y2="yDst(lien.j)"
          :stroke="strokeLien(lien)"
          :stroke-width="epaisLien(lien)"
          :stroke-dasharray="lienEstInactif(lien) ? '3 3' : 'none'"
          stroke-linecap="round"
          class="transition-all duration-500"
        />

        <!-- Label au milieu des arêtes actives ou epsilon -->
        <template v-for="lien in liensVisibles" :key="`lf-${lien.i}-${lien.j}`">
          <text
            :x="(SX + DX) / 2"
            :y="(ySrc(lien.i) + yDst(lien.j)) / 2 - labelOffset"
            text-anchor="middle"
            dominant-baseline="middle"
            :fill="
              lienEstEpsilon(lien)
                ? '#f59e0b'
                : estDansCycle(lien.i, lien.j)
                  ? '#a78bfa'
                  : '#9ca3af'
            "
            :stroke="isDark ? '#111827' : '#ffffff'"
            stroke-width="3"
            paint-order="stroke"
            stroke-linejoin="round"
            :font-size="fontLabel"
            font-weight="700"
            class="select-none"
          >
            {{ valAr(lien) }}
          </text>
        </template>

        <!-- Flèches -->
        <polygon
          v-for="lien in liensActifsReels"
          :key="`a-${lien.i}-${lien.j}`"
          :points="arrowPoints(ySrc(lien.i), yDst(lien.j))"
          :fill="strokeLien(lien)"
          class="transition-all duration-500"
        />

        <!-- ── Nœuds sources (gauche) ──────────────────────────────────────── -->
        <g v-for="(src, i) in metadata.sources" :key="`s-${i}`">
          <circle
            v-if="srcAEpsilon(i)"
            :cx="SX"
            :cy="ySrc(i)"
            :r="R"
            fill="none"
            stroke="#f59e0b"
            stroke-width="1.5"
            opacity="0.5"
            class="animate-ping-slow"
          />
          <circle
            :cx="SX"
            :cy="ySrc(i)"
            :r="R"
            :fill="couleurCercleSrc(i)"
            :stroke="bordureCercleSrc(i)"
            stroke-width="2"
            class="transition-all duration-300"
          />
          <title>
            Source {{ i + 1 }} · offre {{ config?.offres?.[i] ?? "—" }}
          </title>
          <text
            :x="SX"
            :y="ySrc(i) - nodeLabelOffset"
            text-anchor="middle"
            dominant-baseline="middle"
            :fill="
              srcActif(i) ? '#ffffff' : srcAEpsilon(i) ? '#92400e' : '#6366f1'
            "
            :font-size="fontTag"
            font-weight="700"
            class="select-none"
          >
            U{{ i + 1 }}
          </text>
          <text
            :x="SX"
            :y="ySrc(i) + nodeValueOffset"
            text-anchor="middle"
            dominant-baseline="middle"
            :fill="
              srcAEpsilon(i)
                ? '#d97706'
                : srcActif(i)
                  ? '#e0e7ff'
                  : mode === 'potentiels'
                    ? '#4f46e5'
                    : '#6b7280'
            "
            :font-size="fontValue"
            font-weight="700"
            class="select-none"
          >
            {{ valSrc(i) }}
          </text>
        </g>

        <!-- ── Nœuds destinations (droite) ────────────────────────────────── -->
        <g v-for="(dst, j) in metadata.destinations" :key="`d-${j}`">
          <circle
            v-if="dstAEpsilon(j)"
            :cx="DX"
            :cy="yDst(j)"
            :r="R"
            fill="none"
            stroke="#f59e0b"
            stroke-width="1.5"
            opacity="0.5"
            class="animate-ping-slow"
          />
          <circle
            :cx="DX"
            :cy="yDst(j)"
            :r="R"
            :fill="couleurCercleDst(j)"
            :stroke="bordureCercleDst(j)"
            stroke-width="2"
            class="transition-all duration-300"
          />
          <title>
            Destination {{ j + 1 }} · demande {{ config?.demandes?.[j] ?? "—" }}
          </title>
          <text
            :x="DX"
            :y="yDst(j) - nodeLabelOffset"
            text-anchor="middle"
            dominant-baseline="middle"
            :fill="
              dstActif(j) ? '#ffffff' : dstAEpsilon(j) ? '#92400e' : '#0d9488'
            "
            :font-size="fontTag"
            font-weight="700"
            class="select-none"
          >
            C{{ j + 1 }}
          </text>
          <text
            :x="DX"
            :y="yDst(j) + nodeValueOffset"
            text-anchor="middle"
            dominant-baseline="middle"
            :fill="
              dstAEpsilon(j)
                ? '#d97706'
                : dstActif(j)
                  ? '#ccfbf1'
                  : mode === 'potentiels'
                    ? '#0d9488'
                    : '#6b7280'
            "
            :font-size="fontValue"
            font-weight="700"
            class="select-none"
          >
            {{ valDst(j) }}
          </text>
        </g>
      </svg>
    </div>

    <!-- Bandeau potentiels pas encore dispo -->
    <div
      v-if="mode === 'potentiels' && !aPotentiels"
      class="mt-2 flex items-center gap-2 rounded-lg px-2.5 py-1.5 text-[11px] border"
      :class="
        isDark
          ? 'bg-amber-900/20 border-amber-800 text-amber-400'
          : 'bg-amber-50 border-amber-200 text-amber-600'
      "
    >
      <svg
        class="w-3 h-3 shrink-0"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
        />
      </svg>
      Potentiels disponibles pendant l'optimisation
    </div>

    <!-- Légende -->
    <div
      class="flex flex-wrap gap-x-3 gap-y-1 mt-3 pt-2 text-[11px] border-t"
      :class="
        isDark
          ? 'text-gray-500 border-gray-800'
          : 'text-gray-400 border-stone-200'
      "
    >
      <span class="flex items-center gap-1">
        <span class="inline-block w-4 h-0.5 bg-indigo-300 rounded"></span>Actif
      </span>
      <span class="flex items-center gap-1">
        <span
          class="inline-block w-4 h-0.5 border-t border-dashed border-stone-400 dark:border-gray-600"
        ></span
        >Nul
      </span>
      <span v-if="nbEpsilon > 0" class="flex items-center gap-1">
        <span class="inline-block w-4 h-0.5 bg-amber-400 rounded"></span>ε
      </span>
      <span v-if="hasCycle" class="flex items-center gap-1">
        <span class="inline-block w-4 h-0.5 bg-violet-400 rounded"></span>Cycle
        +
      </span>
      <span v-if="hasCycle" class="flex items-center gap-1">
        <span class="inline-block w-4 h-0.5 bg-rose-400 rounded"></span>Cycle -
      </span>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, watch } from "vue";

const props = defineProps({
  flux: Array,
  metadata: Object,
  config: Object,
  caseActive: Array,
  cycle: Array,
  potentiels: Object,
  casesEpsilon: Array,
  isDark: Boolean,
});

const mode = ref("potentiels");

// ── Dimensions du viewBox ──────────────────────────────────────────────────
// Ces valeurs définissent l'espace "logique" du dessin. Comme le SVG est
// maintenant contraint par un conteneur à hauteur fixe (h-56) avec
// preserveAspectRatio="xMidYMid meet", le navigateur scale TOUT le viewBox
// (cercles, textes, traits) pour qu'il tienne dans cette boîte — donc plus
// il y a de nœuds, plus H grandit, plus le rendu final rétrécit réellement,
// au lieu de pousser la hauteur de la page.
const W = 300;
const SX = 66;
const DX = computed(() => W - 66);

const nbS = computed(() => props.metadata?.sources?.length ?? 0);
const nbD = computed(() => props.metadata?.destinations?.length ?? 0);
const maxN = computed(() => Math.max(nbS.value, nbD.value, 1));

function clamp(v, min, max) {
  return Math.max(min, Math.min(max, v));
}

// Espacement et rayon "logiques" : gardés raisonnablement généreux, puisque
// c'est le scaling global du SVG (via le conteneur h-56) qui gère la vraie
// compacité à l'écran, pas ces valeurs en elles-mêmes.
const R = computed(() => clamp(26 - (maxN.value - 2) * 1.2, 16, 26));
const STEP = computed(() => clamp(64 - (maxN.value - 2) * 3, 40, 64));

const PAD_TOP = 20;
const PAD_BOT = 12;

const H = computed(
  () => PAD_TOP + PAD_BOT + (maxN.value - 1) * STEP.value + R.value * 2,
);

function yPositions(n) {
  const start = PAD_TOP + R.value;
  return (i) => (n === 1 ? H.value / 2 : start + i * STEP.value);
}
const ySrc = computed(() => yPositions(nbS.value));
const yDst = computed(() => yPositions(nbD.value));

const fontTag = computed(() => clamp(R.value * 0.36, 7, 9));
const fontValue = computed(() => clamp(R.value * 0.44, 8.5, 11));
const fontLabel = computed(() => clamp(R.value * 0.36, 7.5, 9));
const nodeLabelOffset = computed(() => R.value * 0.32);
const nodeValueOffset = computed(() => R.value * 0.36);
const labelOffset = computed(() => Math.max(5, R.value * 0.3));

// ── Potentiels ───────────────────────────────────────────────────────────────
const arrU = computed(() => props.potentiels?.u ?? []);
const arrV = computed(() => props.potentiels?.v ?? []);
const aPotentiels = computed(() => {
  const arr = arrU.value;
  if (!Array.isArray(arr) || arr.length === 0) return false;
  return arr.some((x) => x !== null && x !== undefined);
});
watch(
  aPotentiels,
  (ok) => {
    mode.value = ok ? "potentiels" : "offre";
  },
  { immediate: true },
);

function fmt(val) {
  if (val === null || val === undefined) return "—";
  const n = Number(val);
  if (isNaN(n)) return "—";
  return Number.isInteger(n) ? String(n) : n.toFixed(1);
}

// ── Epsilon ──────────────────────────────────────────────────────────────────
const epsSet = computed(
  () => new Set((props.casesEpsilon ?? []).map(([i, j]) => `${i}-${j}`)),
);
const nbEpsilon = computed(() => (props.casesEpsilon ?? []).length);

function estEpsilonCase(i, j) {
  return epsSet.value.has(`${i}-${j}`);
}
function srcAEpsilon(i) {
  return (props.casesEpsilon ?? []).some(([r]) => r === i);
}
function dstAEpsilon(j) {
  return (props.casesEpsilon ?? []).some(([, c]) => c === j);
}

// ── Valeurs affichées sur les nœuds ──────────────────────────────────────────
function valSrc(i) {
  if (mode.value === "potentiels" && aPotentiels.value)
    return fmt(arrU.value[i]);
  return String(props.config?.offres?.[i] ?? "");
}
function valDst(j) {
  if (mode.value === "potentiels" && aPotentiels.value)
    return fmt(arrV.value[j]);
  return String(props.config?.demandes?.[j] ?? "");
}

function valAr(lien) {
  const cij = props.config?.couts?.[lien.i]?.[lien.j];
  if (mode.value === "potentiels") {
    return cij !== undefined ? String(cij) : "—";
  }
  if (estEpsilonCase(lien.i, lien.j)) return "ε";
  if (lien.flux < 1e-6) return "—";
  return Number.isInteger(lien.flux) ? String(lien.flux) : lien.flux.toFixed(1);
}

// ── Couleurs des cercles ──────────────────────────────────────────────────────
function couleurCercleSrc(i) {
  if (srcActif(i)) return "#6366f1";
  if (srcAEpsilon(i)) return props.isDark ? "#451a03" : "#fef3c7";
  return props.isDark ? "#1f2937" : "#eef2ff";
}
function bordureCercleSrc(i) {
  if (srcActif(i)) return "#4f46e5";
  if (srcAEpsilon(i)) return "#f59e0b";
  return "#a5b4fc";
}
function couleurCercleDst(j) {
  if (dstActif(j)) return "#14b8a6";
  if (dstAEpsilon(j)) return props.isDark ? "#451a03" : "#fef3c7";
  return props.isDark ? "#1f2937" : "#f0fdfa";
}
function bordureCercleDst(j) {
  if (dstActif(j)) return "#0d9488";
  if (dstAEpsilon(j)) return "#f59e0b";
  return "#5eead4";
}

// ── Liens ─────────────────────────────────────────────────────────────────────
const liens = computed(() => {
  const res = [];
  for (let i = 0; i < nbS.value; i++)
    for (let j = 0; j < nbD.value; j++)
      res.push({ i, j, flux: props.flux?.[i]?.[j] ?? 0 });
  return res;
});

const liensVisibles = computed(() =>
  liens.value.filter((l) => l.flux > 1e-6 || estEpsilonCase(l.i, l.j)),
);
const liensActifsReels = computed(() =>
  liens.value.filter((l) => l.flux > 1e-6 || estEpsilonCase(l.i, l.j)),
);

const hasCycle = computed(
  () => Array.isArray(props.cycle) && props.cycle.length > 0,
);

// ── Helpers ──────────────────────────────────────────────────────────────────
function lienEstEpsilon(lien) {
  return estEpsilonCase(lien.i, lien.j);
}
function lienEstInactif(lien) {
  return lien.flux <= 1e-6 && !estEpsilonCase(lien.i, lien.j);
}

function estDansCycle(i, j) {
  return props.cycle?.some(([r, c]) => r === i && c === j) ?? false;
}
function posCycle(i, j) {
  return props.cycle?.findIndex(([r, c]) => r === i && c === j) ?? -1;
}
function estActive(i, j) {
  return props.caseActive?.[0] === i && props.caseActive?.[1] === j;
}

function srcActif(i) {
  if (props.caseActive?.[0] === i) return true;
  return props.cycle?.some(([r]) => r === i) ?? false;
}
function dstActif(j) {
  if (props.caseActive?.[1] === j) return true;
  return props.cycle?.some(([, c]) => c === j) ?? false;
}

// ── Couleur des arêtes ────────────────────────────────────────────────────────
function strokeLien({ i, j, flux }) {
  if (estDansCycle(i, j))
    return posCycle(i, j) % 2 === 0 ? "#a78bfa" : "#f87171";
  if (estActive(i, j)) return "#6366f1";
  if (estEpsilonCase(i, j)) return "#f59e0b";
  if (flux > 1e-6) return "#a5b4fc";
  return "#e2e8f0";
}
function epaisLien({ i, j, flux }) {
  if (estDansCycle(i, j) || estActive(i, j)) return 2.2;
  if (estEpsilonCase(i, j)) return 1.8;
  if (flux > 1e-6) return Math.max(0.8, Math.min(3, flux / 35));
  return 0.095;
}

// ── Flèches ───────────────────────────────────────────────────────────────────
function arrowPoints(y1, y2) {
  const dx = DX.value - SX;
  const dy = y2 - y1;
  const len = Math.sqrt(dx * dx + dy * dy);
  const ux = dx / len,
    uy = dy / len;
  const mx = (SX + DX.value) / 2;
  const my = (y1 + y2) / 2;
  const s = clamp(R.value * 0.2, 3.5, 5);
  return [
    `${mx + ux * s},${my + uy * s}`,
    `${mx - ux * s + uy * s * 0.5},${my - uy * s - ux * s * 0.5}`,
    `${mx - ux * s - uy * s * 0.5},${my - uy * s + ux * s * 0.5}`,
  ].join(" ");
}
</script>

<style scoped>
@keyframes ping-slow {
  0%,
  100% {
    transform: scale(1);
    opacity: 0.5;
  }
  50% {
    transform: scale(1.15);
    opacity: 0.15;
  }
}
.animate-ping-slow {
  animation: ping-slow 2s ease-in-out infinite;
  transform-origin: center;
}
</style>
