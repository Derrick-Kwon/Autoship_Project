<script setup>
import { ref } from 'vue'
import { ChartComp } from './ChartComp.vue'

const nameToKor = new Map([
  ['longitude', '위도'],
  ['langitude', '경도'],
  ['progress', '진행상황'],
  ['communication', '통신상태'],
  ['windSpeed', '풍속'],
  ['windDirection', '풍향'],
  ['wind', '바람'],
  ['temperature', '기온'],
  ['precipitation', '강수량'],
  ['speed', '속도'],
  ['RPM', 'RPM'],
  ['fuel', '연료량'],
  ['direction', '방향'],
  ['mode', '작동모드'],
  ['danger', '위험도'],
  ['status', '상태'],
  ['crash', '충돌위험'],
  ['tilt', '기울기'],
])
const topInfoNames = ['wind', 'temperature', 'precipitation', 'speed', 'RPM']
const bottomInfoNames = ['fuel', 'danger', 'status', 'crash', 'tilt']
let selected =
{
  'wind': false,
  'temperature': false,
  'precipitation': false,
  'speed': false,
  'RPM': false,
  'fuel': false,
  'danger': false,
  'status': false,
  'crash': false,
  'tilt': false,
}
const selectedTotal = ref(0)

// const sample = {
//   longitude: 36.3721,
//   langitude: 127.3604,
//   progress: 50,
//   communication: 3,
//   windSpeed: 2.7,
//   windDirection: 40,
//   temperature: 30,
//   precipitation: 0.1,
//   RPM: 3000,
//   fuel: 60,
//   direction: 50,
//   mode: 'autonomous',
//   danger: 40,
//   status: 'safe',
//   speed: 60,
//   crash: 40,
//   tilt: 2,
// }

function toggleSelected(event, name) {
  console.log("toggle: ", name)
  if (selectedTotal.value >= 4 && selected[name] == false) return
  if (selected[name] == false) {
    selected[name] = true
    selectedTotal.value++
  }
  else {
    selected[name] = false
    selectedTotal.value--
  }
  event.currentTarget.classList.toggle('selected')
}
</script>

<template>
  <div class="statistics-container">
    <div class="container">
      <div :class="{ info: true, 'chart-name': true }" v-for="name in topInfoNames" v-bind:key="name"
        @click="toggleSelected($event, name)">
        <div class="name">{{ nameToKor.get(name) }}</div>
      </div>
    </div>
    <div class="statistics-display">
      <ChartComp :selected="selected" :selectedTotal="selectedTotal" />
    </div>
    <div class="container">
      <div :class="{ info: true, 'chart-name': true }" v-for="name in bottomInfoNames" v-bind:key="name"
        @click="toggleSelected($event, name)">
        <div class="name">{{ nameToKor.get(name) }}</div>
      </div>
    </div>
  </div>
</template>

<style scoped>
@import "../assets/style.css";
</style>
