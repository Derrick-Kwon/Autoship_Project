<script setup>
import { defineProps } from 'vue';
defineProps({
  selected: Object,
  selectedTotal: Number,
})

</script>

<template>
  <div>
    selectedTotal: {{ selectedTotal }}
  </div>
  <div class="example-chart">
    this is an example chart.
  </div>
</template>

<style scoped>
@import "../assets/style.css";
</style>