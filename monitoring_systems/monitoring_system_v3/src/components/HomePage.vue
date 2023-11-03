<script setup>
import MapComp from './MapComp.vue'
import RadorComp from './RadorComp.vue';
import { onMounted, ref, computed, defineEmits } from 'vue'
import axios from 'axios'
import { emit } from 'process';

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
  ['wave', '파고'],
  ['fuel', '연료량'],
  ['direction', '방향'],
  ['mode', '작동모드'],
  ['danger', '위험도'],
  ['status', '상태'],
  ['crash', '충돌위험'],
  ['tilt', '기울기']
])
const topInfoNames = ['longitude', 'latitude', 'progress', 'communication', 'windSpeed', 'windDirection', 'temperature', 'precipitation']
const bottomInfoNames = ['speed', 'wave', 'fuel', 'direction']
const middleInfoNames = ['mode', 'danger', 'status', 'crash', 'tilt']

const data = ref()
const weather = ref()
const sample = {
  longitude: 37.2978,
  latitude: 126.83339,
  progress: 50,
  communication: 3,
  windSpeed: 2.7,
  windDirection: 40,
  temperature: 30,
  precipitation: 0.1,
  wave: 5,
  fuel: 80,
  direction: 50,
  mode: 'autonomous',
  danger: 40,
  status: 'safe',
  speed: 5,
  crash: 40,
  tilt: "",
  ridar: [],
  pitch: 0,
  roll: 0
}
const sampleWeather = {'id': 139, 'basetime': '202310310300', 'nx': 67, 'ny': 101, 'T1H': 0, 'RN1': 0, 'UUU': 0, 'VVV': 0, 'REH': 0, 'PTY': 0, 'VEC': 0, 'WSD': 0}

const tilt = computed(() => {
  let p = parseFloat(data.value['pitch'])
  let r = parseFloat(data.value['roll'])
  return Math.floor(100*Math.atan(Math.sqrt(Math.tan(r)**2+Math.tan(p)**2)))/100
})

const crash = computed(() => {
  let minlen = 300
  for (let i=0; i<data.value.ridar.length; i++) {
    if (data.value.ridar[i][1]<minlen) {
      minlen = data.value.ridar[i][1]
    }
  }
  return Math.floor(Math.min((-1)*Math.log(minlen/300), 100))
})
const danger = computed(() => {
  let tiltDanger = Math.min(tilt.value/40*100, 100)
  return Math.floor(Math.max(crash.value, tiltDanger))
})  
const status = computed(() => {
  let message = ""
  if (danger.value>70) message = "danger"
  else if (danger.value>50) message = "caution"
  else message = "safe"

  return message
})


data.value = sample
weather.value = sampleWeather

// database

async function testData() {
  axios.get('/api/fetch')
    .then((res) => {
      console.log('fetch: ', res.data)
      const dlat = data.value.latitude -  res.data.latitude
      const dlng = data.value.longitude -  res.data.longitude
      data.value.direction = Math.atan(dlng/dlat)
      data.value.latitude = res.data.latitude
      data.value.longitude = res.data.longitude
      data.value.roll = res.data.roll
      data.value.pitch = res.data.pitch
      data.value.ridar = res.data.ridar
      data.value.speed = res.data.speed
    })
    .catch((err) => {
      console.error(err)
    })
    .finally(console.log("data: ", data.value))
}

async function getWeather() {
  axios.get('/api/weather')
    .then((res) => {
      console.log('weather: ', res.data)
      weather.value = res.data
    })
    .catch((err) => {
      console.error(err)
    })
    .finally(console.log('getWeather executed'))
}

onMounted(() => {
  // testData()
  setInterval(testData, 5000)
  setInterval(getWeather, 5000)
})

</script>

<template>
  <div class="main-container">
    <div class="monitor">
      <div class="top-info-containter container">
        <div class="info" v-for="name in topInfoNames" v-bind:key="name">
          <div class="name">{{ nameToKor.get(name) }}</div>
          <div>
            <span v-if="name == 'longitude'" class="value longitude">{{ Math.round(100000*data[name])/100000 }}°N</span>
            <span v-else-if="name == 'latitude'" class="value latitude">{{ Math.round(100000*data[name])/100000 }}°E</span>
            <span v-else-if="name == 'progress'" class="value progress">{{ data[name] }}%</span>
            <span v-else-if="name == 'communication' && data[name] == 1" class="material-icons value communication">
              signal_cellular_alt_1_bar
            </span>
            <span v-else-if="name == 'communication' && data[name] == 2" class="material-icons value communication">
              signal_cellular_alt_2_bar
            </span>
            <span v-else-if="name == 'communication' && data[name] == 3" class="material-icons value communication">
              signal_cellular_alt
            </span>
            <span v-else-if="name == 'windSpeed'" class="value windSpeed">{{ weather.WSD }}m/s</span>
            <span v-else-if="name == 'windDirection'" class="material-icons value windDirection"
              :style="{ rotate: weather.VEC + 'deg' }">north</span>
            <span v-else-if="name == 'temperature'" class="value temperature">{{ weather.T1H }}°C</span>
            <span v-else-if="name == 'precipitation'" class="value precipitation">{{ weather.RN1 }}mm</span>
          </div>
        </div>
      </div>
      <div class="monitor-body">
        <div class="body-left-banner">
          <div v-for="name in middleInfoNames" class="info middle-info" v-bind:key="name">
            <div class="name">{{ nameToKor.get(name) }}</div>
            <div>
              <span v-if="name == 'tilt'" class="value tilt">{{ tilt }}°</span>
              <span v-if="name == 'crash'" class="value crash">{{ crash }}</span>
              <span v-if="name == 'danger'" class="value danger">{{ danger }}</span>
              <span v-if="name == 'status'" class="value status">{{ status }}</span>
              <span v-else :class="'value '+ name">{{ data[name] }}</span>
            </div> 
          </div>
        </div>
        <div id="map" class="map" style="flex-grow: 1;">
          <MapComp :data="data"></MapComp> 
        </div>
        <div class="body-right-banner">
          <div>
            <RadorComp :ridar="data.ridar"></RadorComp>
            <!-- <div style="text-align: center; margin: 5px">{{ data['longitude'] }}°N {{ data['latitude'] }}°E</div> -->
          </div>
          <div class="camera">
            <!-- <iframe width="240" height="180" frameBorder="0" src="http://192.168.137.73:9090/?action=stream">
              </iframe> -->
            <!-- <img src="http://192.168.137.73:9090/?action=stream"> -->
            <img src="http://192.168.137.9:8081/" width="300" height="200">
          </div>
        </div>
      </div>
      <div class="bottom-info-containter container">
        <div v-for="name in bottomInfoNames" class="info" v-bind:key="name">
          <div class="name">{{ nameToKor.get(name) }} </div>
          <div>
            <span v-if="name == 'speed'" class="value speed">{{ data[name] }}km/h</span>
            <span v-else-if="name == 'fuel'" class="value fuel">{{ data[name] }}%</span>
            <span v-else-if="name == 'direction'" class="material-icons value direction"
              :style="{ rotate: '60' + 'deg' }">north</span>
            <span v-else :class="'value '+name">{{ data[name] }}m</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
@import "../assets/style.css";
</style>
