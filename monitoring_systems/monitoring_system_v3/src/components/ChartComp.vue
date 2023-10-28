<script setup>
import { defineProps } from 'vue';
defineProps({
  selected: Object,
  selectedTotal: Number,
  selectedData: Object,
})
</script>

<template>
  <div v-if="selectedData.includes('wind')" class="chart">wind chart</div>
  <div v-if="selectedData.includes('temperature')" class="chart">temperature chart</div>
  <div v-if="selectedData.includes('precipitation')" class="chart">precipitation chart</div>
  <div v-if="selectedData.includes('speed')" class="chart">speed chart</div>
  <div v-if="selectedData.includes('RPM')" class="chart">RPM chart</div>
  <div v-if="selectedData.includes('fuel')" class="chart">fuel chart</div>
  <div v-if="selectedData.includes('danger')" class="chart">danger chart</div>
  <div v-if="selectedData.includes('status')" class="chart">status chart</div>
  <div v-if="selectedData.includes('crash')" class="chart">crash chart</div>
  <div v-if="selectedData.includes('tilt')" class="chart">tilt chart</div>
</template>
<style scoped>
@import "../assets/style.css";
</style>