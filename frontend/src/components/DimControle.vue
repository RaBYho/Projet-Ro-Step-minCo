<template>
  <div class="flex flex-col gap-1.5">
    <label
      class="text-xs font-medium"
      :class="isDark ? 'text-gray-400' : 'text-gray-500'"
      >{{ label }}</label
    >
    <div class="flex items-center gap-2">
      <button
        @click="$emit('decrementer')"
        :disabled="valeur <= min"
        class="w-9 h-9 rounded-xl border flex items-center justify-center text-gray-500 hover:text-indigo-600 disabled:opacity-30 disabled:cursor-not-allowed transition-all text-lg font-bold"
        :class="
          isDark
            ? 'border-gray-700 bg-gray-900 hover:border-indigo-500'
            : 'border-stone-200 bg-white hover:border-indigo-400'
        "
      >
        −
      </button>
      <span
        class="w-10 text-center text-xl font-bold text-indigo-600 dark:text-indigo-400 font-mono"
        >{{ valeur }}</span
      >
      <button
        @click="$emit('incrementer')"
        :disabled="valeur >= max"
        class="w-9 h-9 rounded-xl border flex items-center justify-center text-gray-500 hover:text-indigo-600 disabled:opacity-30 disabled:cursor-not-allowed transition-all text-lg font-bold"
        :class="
          isDark
            ? 'border-gray-700 bg-gray-900 hover:border-indigo-500'
            : 'border-stone-200 bg-white hover:border-indigo-400'
        "
      >
        +
      </button>
    </div>
  </div>
</template>

<script setup>
defineProps({
  label: String,
  valeur: Number,
  min: Number,
  max: Number,
  isDark: Boolean,
});
defineEmits(["incrementer", "decrementer"]);
</script>
