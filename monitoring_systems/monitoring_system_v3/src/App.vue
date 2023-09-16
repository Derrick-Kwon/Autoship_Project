<template>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="true">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
  <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">

  <div class="logo">
    <div class="logo-img">
      <img src="/logo.svg">
    </div>
  </div>
  <div class="outside-page">
    <div class="page">
      <div class="menu-bar">
        <div class="menu main" @click="setIsmain">
          <span class="material-icons">home</span>
          <div>메인</div>
        </div>
        <div class="menu statistics" @click="unsetIsmain">
          <span class="material-icons">bar_chart</span>
          <div>통계</div>
        </div>
      </div>
      <HomePage v-if="ismain" />
      <!-- <StatisticsPage v-else /> -->
      <GrafanaComp v-else />
    </div>
  </div>
</template>

<script setup>
import HomePage from './components/HomePage.vue'
import GrafanaComp from './components/GrafanaComp.vue';
import { ref } from 'vue'

const ismain = ref(true)
function setIsmain() {
  ismain.value = true
}
function unsetIsmain() {
  ismain.value = false
}
</script>

<style scoped>
/* @import "./assets/style.css"; */
</style>
