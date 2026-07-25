<template>
  <div class="space-y-4">
    <!-- ── En-tête : coût avant / après / réduction ─────────────────────── -->
    <div
      :class="
        etape.optimal
          ? isDark
            ? 'bg-emerald-900/20 border-emerald-800'
            : 'bg-emerald-50 border-emerald-200'
          : isDark
            ? 'bg-gray-900 border-gray-800'
            : 'bg-white border-stone-200'
      "
      class="rounded-2xl border p-4 shadow-sm"
    >
      <div class="flex items-center gap-2 mb-3 flex-wrap">
        <span
          class="text-[11px] font-bold uppercase tracking-widest px-2.5 py-0.5 rounded-full"
          :class="
            etape.optimal
              ? isDark
                ? 'bg-emerald-800/60 text-emerald-300'
                : 'bg-emerald-100 text-emerald-700'
              : isDark
                ? 'bg-violet-900/50 text-violet-300'
                : 'bg-violet-100 text-violet-700'
          "
        >
          Itération {{ etape.iteration }}
        </span>
        <span
          v-if="etape.optimal"
          class="text-xs font-semibold"
          :class="isDark ? 'text-emerald-400' : 'text-emerald-600'"
        >
          ✓ Solution optimale
        </span>
      </div>

      <!-- Coût avant → après → réduction, empilé verticalement pour tenir dans une colonne étroite -->
      <div v-if="!etape.optimal" class="space-y-2.5">
        <div class="flex items-center gap-3">
          <div class="flex-1">
            <p
              class="text-[10px] uppercase tracking-wider mb-0.5"
              :class="isDark ? 'text-gray-500' : 'text-gray-400'"
            >
              Avant
            </p>
            <p
              class="text-lg font-bold font-mono tabular-nums"
              :class="isDark ? 'text-gray-200' : 'text-gray-700'"
            >
              {{ etape.cout_avant?.toFixed(2) }}
            </p>
          </div>
          <svg
            class="w-4 h-4 shrink-0"
            :class="isDark ? 'text-gray-600' : 'text-gray-300'"
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
          <div class="flex-1">
            <p
              class="text-[10px] uppercase tracking-wider mb-0.5"
              :class="isDark ? 'text-gray-500' : 'text-gray-400'"
            >
              Après
            </p>
            <p
              class="text-lg font-bold font-mono tabular-nums"
              :class="isDark ? 'text-indigo-400' : 'text-indigo-600'"
            >
              {{ etape.cout_apres?.toFixed(2) }}
            </p>
          </div>
        </div>
        <div
          class="rounded-xl px-3 py-2 flex items-center justify-between"
          :class="isDark ? 'bg-emerald-900/30' : 'bg-emerald-50'"
        >
          <span
            class="text-[10px] uppercase tracking-wider"
            :class="isDark ? 'text-emerald-500' : 'text-emerald-600'"
          >
            Réduction
          </span>
          <span
            class="text-base font-bold font-mono tabular-nums"
            :class="isDark ? 'text-emerald-300' : 'text-emerald-600'"
          >
            −{{ etape.reduction_cout?.toFixed(2) }}
          </span>
        </div>
      </div>

      <!-- Cas optimal -->
      <div v-else>
        <p
          class="text-[10px] uppercase tracking-wider mb-1"
          :class="isDark ? 'text-gray-500' : 'text-gray-400'"
        >
          Coût total minimal
        </p>
        <p
          class="text-2xl font-bold font-mono tabular-nums"
          :class="isDark ? 'text-emerald-300' : 'text-emerald-600'"
        >
          {{ etape.cout_apres?.toFixed(2) }}
        </p>
      </div>
    </div>

    <!-- ── Potentiels u, v ────────────────────────────────────────────────── -->
    <div
      class="rounded-2xl border p-4 shadow-sm"
      :class="
        isDark ? 'bg-gray-900 border-gray-800' : 'bg-white border-stone-200'
      "
    >
      <button
        @click="showPotentiels = !showPotentiels"
        class="w-full flex items-center justify-between text-left"
      >
        <h4
          class="text-[11px] font-semibold tracking-widest uppercase"
          :class="isDark ? 'text-gray-500' : 'text-gray-400'"
        >
          Potentiels u, v
        </h4>
        <svg
          class="w-3.5 h-3.5 transition-transform shrink-0"
          :class="[
            isDark ? 'text-gray-400' : 'text-gray-400',
            showPotentiels ? 'rotate-180' : '',
          ]"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M19 9l-7 7-7-7"
          />
        </svg>
      </button>
      <Transition name="collapse">
        <div v-if="showPotentiels" class="mt-3 space-y-2">
          <div class="flex flex-wrap gap-1.5">
            <span
              v-for="(val, i) in etape.potentiels?.u"
              :key="`u${i}`"
              class="rounded-lg px-2 py-1 text-[11px] font-mono"
              :class="isDark ? 'bg-indigo-900/30' : 'bg-indigo-50'"
            >
              <span class="text-gray-400"
                >u<sub>{{ i + 1 }}</sub
                >=</span
              >
              <span :class="isDark ? 'text-indigo-300' : 'text-indigo-600'">{{
                val?.toFixed(0) ?? "—"
              }}</span>
            </span>
          </div>
          <div class="flex flex-wrap gap-1.5">
            <span
              v-for="(val, j) in etape.potentiels?.v"
              :key="`v${j}`"
              class="rounded-lg px-2 py-1 text-[11px] font-mono"
              :class="isDark ? 'bg-teal-900/30' : 'bg-teal-50'"
            >
              <span class="text-gray-400"
                >v<sub>{{ j + 1 }}</sub
                >=</span
              >
              <span class="font-bold" :class=" isDark ? 'text-teal-300' : 'text-teal-600' " >{{
                val?.toFixed(0) ?? "—"
              }}</span>
            </span>
          </div>
          <p
            class="text-[11px] italic"
            :class="isDark ? 'text-gray-500' : 'text-gray-400'"
          >
            v<sub>j</sub> = u<sub>i</sub> + c<sub>ij</sub> pour chaque case de
            base
          </p>
        </div>
      </Transition>
    </div>

    <!-- ── Indices marginaux + Gains : cartes empilées au lieu d'un tableau 12-colonnes ── -->
    <div
      class="rounded-2xl border p-4 shadow-sm"
      :class="
        isDark ? 'bg-gray-900 border-gray-800' : 'bg-white border-stone-200'
      "
    >
      <button
        @click="showIndices = !showIndices"
        class="w-full flex items-center justify-between text-left"
      >
        <h4
          class="text-[11px] font-semibold tracking-widest uppercase"
          :class="isDark ? 'text-gray-500' : 'text-gray-400'"
        >
          Indices &amp; Gains
        </h4>
        <svg
          class="w-3.5 h-3.5 transition-transform shrink-0"
          :class="[
            isDark ? 'text-gray-400' : 'text-gray-400',
            showIndices ? 'rotate-180' : '',
          ]"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M19 9l-7 7-7-7"
          />
        </svg>
      </button>

      <p
        class="text-[10px] mt-1.5"
        :class="isDark ? 'text-gray-500' : 'text-gray-400'"
      >
        ρ<sub>ij</sub> = u<sub>i</sub> + c<sub>ij</sub> − v<sub>j</sub> · gain =
        ρ × θ
      </p>

      <Transition name="collapse">
        <div v-if="showIndices" class="mt-3 space-y-1.5">
          <div
            v-for="d in etape.details_indices"
            :key="`d-${d.i}-${d.j}`"
            :class="
              d.est_meilleur
                ? isDark
                  ? 'border-violet-500 bg-violet-900/30'
                  : 'border-violet-400 bg-violet-50'
                : d.gain < -1e-9
                  ? isDark
                    ? 'border-amber-800 bg-amber-900/20'
                    : 'border-amber-200 bg-amber-50'
                  : isDark
                    ? 'border-gray-800 bg-gray-800/40'
                    : 'border-stone-100 bg-stone-50'
            "
            class="rounded-xl border px-3 py-2"
          >
            <div class="flex items-center justify-between gap-2 mb-1">
              <div class="flex items-center gap-1.5 min-w-0">
                <span
                  v-if="d.est_meilleur"
                  class="text-[9px] font-bold px-1.5 py-0.5 rounded shrink-0 bg-violet-500 text-white"
                >
                  PIVOT
                </span>
                <span
                  class="text-xs font-semibold truncate"
                  :class="isDark ? 'text-gray-200' : 'text-gray-700'"
                >
                  U{{ d.i + 1 }} → C{{ d.j + 1 }}
                </span>
              </div>
              <span
                class="text-sm font-bold font-mono tabular-nums shrink-0"
                :class="isDark ? 'text-violet-300' : 'text-violet-600'"
              >
                ρ {{ d.indice >= 0 ? "+" : "" }}{{ d.indice.toFixed(2) }}
              </span>
            </div>
            <div
              class="flex items-center justify-between text-[11px]"
              :class="isDark ? 'text-gray-500' : 'text-gray-400'"
            >
              <span class="font-mono truncate">{{ d.formule }}</span>
              <span class="font-mono tabular-nums shrink-0 ml-2">
                θ={{ d.theta > 0 ? d.theta.toFixed(1) : "—" }} · gain={{
                  d.gain < -1e-9 ? d.gain.toFixed(2) : "—"
                }}
              </span>
            </div>
          </div>

          <!-- Légende compacte -->
          <div
            class="flex flex-wrap gap-x-3 gap-y-1 pt-2 text-[10px]"
            :class="isDark ? 'text-gray-500' : 'text-gray-400'"
          >
            <span class="flex items-center gap-1">
              <span
                class="w-2.5 h-2.5 rounded inline-block"
                :class="isDark ? 'bg-violet-800' : 'bg-violet-200'"
              ></span
              >Pivot
            </span>
            <span class="flex items-center gap-1">
              <span
                class="w-2.5 h-2.5 rounded inline-block"
                :class="isDark ? 'bg-amber-900/40' : 'bg-amber-100'"
              ></span
              >Amélioration
            </span>
            <span class="flex items-center gap-1">
              <span
                class="w-2.5 h-2.5 rounded inline-block"
                :class="isDark ? 'bg-gray-800' : 'bg-stone-100'"
              ></span
              >ρ ≥ 0
            </span>
          </div>
        </div>
      </Transition>
    </div>

    <!-- ── Cycle & Theta & Gain du pivot ─────────────────────────────────── -->
    <div
      v-if="!etape.optimal"
      class="rounded-2xl border p-4 shadow-sm"
      :class="
        isDark ? 'bg-gray-900 border-gray-800' : 'bg-white border-stone-200'
      "
    >
      <h4
        class="text-[11px] font-semibold tracking-widest uppercase mb-3"
        :class="isDark ? 'text-gray-500' : 'text-gray-400'"
      >
        Cycle Stepping Stone
      </h4>

      <!-- Cycle visuel -->
      <div
        class="rounded-xl p-2.5 mb-3 overflow-x-auto"
        :class="isDark ? 'bg-gray-800/60' : 'bg-stone-50'"
      >
        <div class="flex items-center gap-1 flex-wrap">
          <template v-for="(node, idx) in etape.cycle" :key="idx">
            <span
              class="border rounded-lg px-2 py-0.5 text-[11px] font-mono font-bold inline-flex items-center gap-1 shrink-0"
              :class="
                idx % 2 === 0
                  ? isDark
                    ? 'border-violet-600 bg-violet-900/50 text-violet-200'
                    : 'border-violet-300 bg-violet-100 text-violet-700'
                  : isDark
                    ? 'border-rose-600 bg-rose-900/50 text-rose-200'
                    : 'border-rose-300 bg-rose-100 text-rose-700'
              "
            >
              {{ idx % 2 === 0 ? "+" : "−" }}[{{ node[0] + 1 }},{{
                node[1] + 1
              }}]
            </span>
            <svg
              v-if="idx < etape.cycle.length - 1"
              class="w-2.5 h-2.5 shrink-0"
              :class="isDark ? 'text-gray-600' : 'text-gray-300'"
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
          </template>
        </div>
      </div>

      <!-- θ / case sortante / gain, empilés (au lieu d'un grid-cols-3 trop serré) -->
      <div class="grid grid-cols-3 gap-2 mb-3">
        <div
          class="rounded-xl p-2.5 text-center"
          :class="isDark ? 'bg-gray-800/60' : 'bg-stone-50'"
        >
          <p
            class="text-[9px] uppercase tracking-wider mb-1"
            :class="isDark ? 'text-gray-400' : 'text-gray-400'"
          >
            θ
          </p>
          <p
            class="text-base font-bold font-mono tabular-nums"
            :class="isDark ? 'text-violet-300' : 'text-violet-600'"
          >
            {{ etape.theta?.toFixed(2) }}
          </p>
        </div>
        <div
          class="rounded-xl p-2.5 text-center"
          :class="isDark ? 'bg-gray-800/60' : 'bg-stone-50'"
        >
          <p
            class="text-[9px] uppercase tracking-wider mb-1"
            :class="isDark ? 'text-gray-400' : 'text-gray-400'"
          >
            Sortante
          </p>
          <p
            v-if="etape.case_sortante"
            class="text-sm font-bold font-mono"
            :class="isDark ? 'text-rose-400' : 'text-rose-500'"
          >
            [{{ etape.case_sortante[0] + 1 }},{{ etape.case_sortante[1] + 1 }}]
          </p>
        </div>
        <div
          class="rounded-xl p-2.5 text-center"
          :class="isDark ? 'bg-violet-900/30' : 'bg-violet-50'"
        >
          <p
            class="text-[9px] uppercase tracking-wider mb-1"
            :class="isDark ? 'text-violet-500' : 'text-violet-500'"
          >
            Gain
          </p>
          <p
            class="text-base font-bold font-mono tabular-nums"
            :class="isDark ? 'text-violet-300' : 'text-violet-600'"
          >
            {{ etape.meilleur_indice?.gain?.toFixed(2) ?? "—" }}
          </p>
        </div>
      </div>

      <!-- Récap case entrante : formule condensée sur 2 lignes -->
      <div
        v-if="etape.meilleur_indice"
        class="rounded-xl p-3 text-xs font-mono leading-relaxed"
        :class="isDark ? 'bg-violet-900/20' : 'bg-violet-50'"
      >
        <p :class="isDark ? 'text-gray-300' : 'text-gray-700'">
          ρ(U{{ etape.meilleur_indice.i + 1 }},C{{
            etape.meilleur_indice.j + 1
          }}) = {{ etape.meilleur_indice.formule }} =
          <span
            class="font-bold"
            :class="isDark ? 'text-violet-300' : 'text-violet-600'"
            >{{ etape.meilleur_indice.valeur?.toFixed(2) }}</span
          >
        </p>
        <p class="mt-1" :class="isDark ? 'text-gray-400' : 'text-gray-500'">
          Gain = {{ etape.meilleur_indice.valeur?.toFixed(2) }} ×
          {{ etape.theta?.toFixed(2) }} =
          <span
            class="font-bold"
            :class="isDark ? 'text-violet-300' : 'text-violet-600'"
            >{{ etape.meilleur_indice.gain?.toFixed(2) }}</span
          >
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
const props = defineProps({ etape: Object, isDark: Boolean });
const showPotentiels = ref(true);
const showIndices = ref(true);
</script>

<style scoped>
.collapse-enter-active,
.collapse-leave-active {
  transition: all 0.3s ease;
  overflow: hidden;
}
.collapse-enter-from,
.collapse-leave-to {
  opacity: 0;
  max-height: 0;
}
.collapse-enter-to,
.collapse-leave-from {
  opacity: 1;
  max-height: 800px;
}
</style>
