<template>
  <div class="flex items-center justify-between py-2 border-b border-slate-800">
    <span class="text-xs text-slate-500 tracking-wider">{{ label }}</span>
    <span :class="`text-${couleur}-300`" class="text-sm font-bold font-mono">{{ valeur }}</span>
  </div>
</template>

<script setup>
defineProps({
  label: String,
  valeur: [String, Number],
  couleur: { type: String, default: 'cyan' }
})
</script>
