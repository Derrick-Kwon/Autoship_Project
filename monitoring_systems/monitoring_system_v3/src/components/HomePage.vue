<script setup>
import MapComp from './MapComp.vue'
import RadorComp from './RadorComp.vue';
import { onMounted, ref } from 'vue'
import axios from 'axios'

// const topInfoNamesKor: Array<string> = ['경도', '위도', '진행률', '통신상태', '풍속', '풍향', '기온', '강수']
// const bottomInfoNamesKor: Array<string> = ['속도', 'RPM', '연료량', '방향']
// const middleInfoNamesKor: Array<string> = ['작동모드', '충돌위험', '상태', '속도', '위험도', '기울기']
// const infoNames: Array<string> = ['longitude', 'latitude', 'progress', 'communication', 'windSpeed', 'windDirection', 'temperature', 'precipitation', 'speed', 'speed', 'RPM', 'fuel', 'direction', 'mode', 'danger', 'status', 'speed', 'crash', 'tilt']
const nameToKor = new Map([
  ['longitude', '위도'],
  ['latitude', '경도'],
  ['progress', '진행상황'],
  ['communication', '통신상태'],
  ['windSpeed', '풍속'],
  ['windDirection', '풍향'],
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
  ['tilt', '기울기']
])
const topInfoNames = ['longitude', 'latitude', 'progress', 'communication', 'windSpeed', 'windDirection', 'temperature', 'precipitation']
const bottomInfoNames = ['speed', 'RPM', 'fuel', 'direction']
const middleInfoNames = ['mode', 'danger', 'status', 'crash', 'tilt']

const data = ref()
const sample = {
  longitude: 37.2978,
  latitude: 126.83339,
  progress: 50,
  communication: 3,
  windSpeed: 2.7,
  windDirection: 40,
  temperature: 30,
  precipitation: 0.1,
  RPM: 3000,
  fuel: 60,
  direction: 50,
  mode: 'autonomous',
  danger: 40,
  status: 'safe',
  speed: 5,
  crash: 40,
  tilt: 2,
}
data.value = sample

// database
async function testData() {
  axios.get('/api/fetch')
    .then((res) => {
      console.log('fetch: ', res.data)
      data.value = res.data[0]
    })
    .catch((err) => {
      console.error(err)
    })
    .finally(console.log('testData executed'))
}

async function getWeather() {
  axios.get('/api/weather')
    .then((res) => {
      console.log('weather: ', res.data)
    })
    .catch((err) => {
      console.error(err)
    })
    .finally(console.log('getWeather executed'))
}

onMounted(() => {
  // testData()
  setInterval(testData, 5000)
  getWeather()
})

</script>

<template>
  <div class="main-container">
    <div class="monitor">
      <div class="top-info-containter container">
        <div class="info" v-for="name in topInfoNames" v-bind:key="name">
          <div class="name">{{ nameToKor.get(name) }}</div>
          <div>
            <span v-if="name == 'longitude'" class="value">{{ data[name] }}°N</span>
            <span v-else-if="name == 'latitude'" class="value">{{ data[name] }}°E</span>
            <span v-else-if="name == 'progress'" class="value">{{ data[name] }}%</span>
            <span v-else-if="name == 'communication' && data[name] == 1" class="material-icons value">
              signal_cellular_alt_1_bar
            </span>
            <span v-else-if="name == 'communication' && data[name] == 2" class="material-icons value">
              signal_cellular_alt_2_bar
            </span>
            <span v-else-if="name == 'communication' && data[name] == 3" class="material-icons value">
              signal_cellular_alt
            </span>
            <span v-else-if="name == 'windSpeed'" class="value">{{ data[name] }}m/s</span>
            <span v-else-if="name == 'windDirection'" class="material-icons value"
              :style="{ rotate: data[name] + 'deg' }">north</span>
            <span v-else-if="name == 'temperature'" class="value">{{ data[name] }}°C</span>
            <span v-else-if="name == 'precipitation'" class="value">{{ data[name] }}mm</span>
          </div>
        </div>
      </div>
      <div class="monitor-body">
        <div class="body-left-banner">
          <div v-for="name in middleInfoNames" class="info middle-info" v-bind:key="name">
            <div class="name">{{ nameToKor.get(name) }}</div>
            <div>
              <span v-if="name == 'tilt'" class="value">{{ data[name] }}°</span>
              <span v-else class="value">{{ data[name] }}</span>
            </div>
          </div>
        </div>
        <div id="map" class="map" style="flex-grow: 1;">
          <MapComp></MapComp>
        </div>
        <div class="body-right-banner">
          <div>
            <RadorComp></RadorComp>
            <div style="text-align: center; margin: 5px">{{ data['longitude'] }}°N {{ data['latitude'] }}°E</div>
          </div>
          <div class="camera">
            <!-- <iframe width="240" height="180" frameBorder="0" src="http://192.168.137.73:9090/?action=stream">
              </iframe> -->
            <!-- <img src="http://192.168.137.73:9090/?action=stream"> -->
            <img src="http://192.168.137.177:8081" width="240" height="180">
          </div>
        </div>
      </div>
      <div class="bottom-info-containter container">
        <div v-for="name in bottomInfoNames" class="info" v-bind:key="name">
          <div class="name">{{ nameToKor.get(name) }} </div>
          <div>
            <span v-if="name == 'speed'" class="value">{{ data[name] }}km/h</span>
            <span v-else-if="name == 'fuel'" class="value">{{ data[name] }}%</span>
            <span v-else-if="name == 'direction'" class="material-icons value"
              :style="{ rotate: data[name] + 'deg' }">north</span>
            <span v-else class="value">{{ data[name] }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
@import "../assets/style.css";
</style>
