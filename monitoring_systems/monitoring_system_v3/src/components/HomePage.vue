<script setup>
import MapComp from './MapComp.vue'
import { onMounted, ref } from 'vue'
import * as mysql from 'mysql'

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

const data = ref({})
const sample = {
  longitude: 36.3721,
  latitude: 127.3604,
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
  speed: 60,
  crash: 40,
  tilt: 2,
}

// database
async function testData() {
  // console.log("host: ", process.env.VUE_APP_DB_HOST)
  const conn = mysql.createConnection({
    host: process.env.VUE_APP_DB_HOST,
    user: process.env.VUE_APP_DB_USER,
    port: '3306',
    password: process.env.VUE_APP_DB_PW,
    database: 'raspi_db',
    connectionLimit: 5,
  })
  conn.connect()
  try {
    const rows = await conn.query("SELECT * from collect_data")
    console.log(rows)
    // rows: [ {val: 1}, meta: ... ]

    // const res = await conn.query("INSERT INTO  collect_data (?, ?, ?, ?)", ['gps', Date(), 36.3721, 127.3604])
    // if (res.affectedRows != 1) console.log("cannot insert value")
    // // res: { affectedRows: 1, insertId: 1, warningStatus: 0 }
  } finally {
    if (conn) conn.release()
  }
  return data
}

onMounted(() => {
  testData()
  // setInterval(getData, 1000)
})

</script>

<template>
  <div class="main-container">
    <div class="monitor">
      <div class="top-info-containter container">
        <div class="info" v-for="name in topInfoNames" v-bind:key="name">
          <div class="name">{{ nameToKor.get(name) }}</div>
          <div>
            <span v-if="name == 'longitude'" class="value">{{ sample[name] }}°N</span>
            <span v-else-if="name == 'latitude'" class="value">{{ sample[name] }}°E</span>
            <span v-else-if="name == 'progress'" class="value">{{ sample[name] }}%</span>
            <span v-else-if="name == 'communication' && sample[name] == 1" class="material-icons value">
              signal_cellular_alt_1_bar
            </span>
            <span v-else-if="name == 'communication' && sample[name] == 2" class="material-icons value">
              signal_cellular_alt_2_bar
            </span>
            <span v-else-if="name == 'communication' && sample[name] == 3" class="material-icons value">
              signal_cellular_alt
            </span>
            <span v-else-if="name == 'windSpeed'" class="value">{{ sample[name] }}m/s</span>
            <span v-else-if="name == 'windDirection'" class="material-icons value"
              :style="{ rotate: sample[name] + 'deg' }">north</span>
            <span v-else-if="name == 'temperature'" class="value">{{ sample[name] }}°C</span>
            <span v-else-if="name == 'precipitation'" class="value">{{ sample[name] }}mm</span>
          </div>
        </div>
      </div>
      <div class="monitor-body">
        <div class="body-left-banner">
          <div v-for="name in middleInfoNames" class="info middle-info" v-bind:key="name">
            <div class="name">{{ nameToKor.get(name) }}</div>
            <div>
              <span v-if="name == 'tilt'" class="value">{{ sample[name] }}°</span>
              <span v-else class="value">{{ sample[name] }}</span>
            </div>
          </div>
        </div>
        <div id="map" class="map" style="flex-grow: 1;">
          <MapComp></MapComp>
        </div>
        <div class="body-right-banner">
          <div class="rador">
            <img src="/rador.svg">
          </div>
          <div>
            <div style="text-align: center; margin: 5px">{{ sample['longitude'] }}°N {{ sample['latitude'] }}°E</div>
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
            <span v-if="name == 'speed'" class="value">{{ sample[name] }}km/h</span>
            <span v-else-if="name == 'fuel'" class="value">{{ sample[name] }}%</span>
            <span v-else-if="name == 'direction'" class="material-icons value"
              :style="{ rotate: sample[name] + 'deg' }">north</span>
            <span v-else class="value">{{ sample[name] }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
@import "../assets/style.css";
</style>
