<script>
import { defineComponent, ref } from 'vue'
import { Circle, GoogleMap, Marker, InfoWindow, Polyline } from 'vue3-google-map'
import voyageData from '../assets/voyage-data.json'
import axios from 'axios'
export default defineComponent({
  components: { GoogleMap, Marker, Circle, InfoWindow, Polyline },
  setup() {
    // const center = { lat: 37.300163057152, lng: 126.83771082564 }
    const p1 = { lat: 37.2978, lng: 126.83339 } // start - point1
    const p2 = { lat: 37.29788, lng: 126.83358 } // point2
    const p3 = { lat: 37.297865, lng: 126.83361 } // point3
    const p4 = { lat: 37.297905, lng: 126.833705 } // point 4
    const p5 = { lat: 37.29793, lng: 126.833705 } // point 5
    const p6 = { lat: 37.298015, lng: 126.833888 } // point 6
    const initCenter = {lat: p1.lat, lng: p1.lng}
    const center = p1
    const points = [p1, p2, p3, p4, p5, p6]
    const markerOption = {position: {lat: center.lat, lng: center.lng}, draggable: true}
    const circleOptions = { center: center, radius: 0.2, fillColor: '#FF0000', fillOpacity: 0.8, strokeColor: '#FF0000', strokeOpacity: 0.8, strokeWeight: 2 }
    const initPath = { path: [center], geodesic: true, strokeColor: "#00FF00", strokeOpacity: 1.0, strokeWeight: 2, zIndex: -1 }
    const examplePath = { path: [center, { lat: center.lat + 1, lng: center.lng + 1 }], geodesic: true, strokeColor: "#FF0000", strokeOpacity: 1.0, strokeWeight: 2 }
    return { center, circleOptions, initPath, examplePath, points, initCenter, markerOption }
  },
  data() {
    return {
      circles: [],
      pathOptions: ref(this.initPath),
      voyageData: voyageData,
      position: this.center,
      mlat: ref(this.center.lat),
      mlng: ref(this.center.lng),
      dlat: ref(this.center.lat),
      dlng: ref(this.center.lng),
      destination: ref()
    }
  },
  mounted() {
    this.pathOptions = this.initPath
    // this.max_indices = this.voyageData.max_indices
    setInterval(this.move, 2000)
  },
  methods: {
    testmove() {
      const data = this.voyageData.shift()
      if (typeof data === "undefined") {
        return
      }

      const p1 = this.points[data.level]
      const p2 = this.points[data.level + 1]
      // console.log(p1)
      // console.log(p2)

      const dlatTotal = p2.lat - p1.lat
      const dlngTotal = p2.lng - p1.lng
      const dlat = dlatTotal / (data.max_index + 1)
      const dlng = dlngTotal / (data.max_index + 1)

      const option = this.circleOptions
      option.date = Date()
      option.center.lat = p1.lat + (dlat * data.index) + (dlat * data.progress) + Math.random() * 0.000005 - 0.0000025
      option.center.lng = p1.lng + (dlng * data.index) + (dlng * data.progress) + Math.random() * 0.000005 - 0.0000025

      this.circles.push(option)
      this.pathOptions.path.push(this.pathOptions.path[this.pathOptions.path.length-1])
      this.pathOptions.path[this.pathOptions.path.length-2] = {lat: option.center.lat, lng: option.center.lng}
    },
    startMove() {
      this.interval = setInterval(this.testmove, 500)
    },
    endMove() {
      clearInterval(this.interval)
    },
    move() {
      axios.get('/api/getPosition')
        .then((res) => {
          console.log('getPosition: ', res.data)
          const point = res.data
          const option = this.circleOptions
          option.date = Date()
          option.center.lat = point.lat
          option.center.lng = point.lng
          
          this.circles.push(option)
          this.pathOptions.path.push(this.pathOptions.path[this.pathOptions.path.length-1])
          this.pathOptions.path[this.pathOptions.path.length-2] = {lat: option.center.lat, lng: option.center.lng}
        })
        .catch((err) => {
          console.error(err)
        })
    },
    setDestination(location) {
      const lat = location.latLng.lat()
      const lng = location.latLng.lng()
      console.log('lat: ', lat, ", lng: ",  lng)
      const text = `위도: ${lat} 경도: ${lng} 목적지를 설정하시겠습니까?`
      if (confirm(text)==true) {
        this.dlat = lat
        this.dlng = lng
        // Change destination circle
        const option = {
          center: {lat, lng},
          radius: 0.3,
          fillColor: '#00FF00',
          fillOpacity: 0.8,
          strokeColor: '#00FF00',
          strokeOpacity: 0.8,
          strokeWeight: 2
        }
        this.destination = option

        const pathlen = this.pathOptions.path.length
        this.pathOptions.path[pathlen-1] = {lat, lng}
      }
      else {
        this.mlat = this.dlat
        this.mlng = this.dlng
      }
    },
  }
})
</script>

<template>
  <div class="destination-box" style="width: 100%; height:10%;">
    <div class="destination-label">목적지:</div>
    <div class="destination-label">위도</div>
    <input class="destination-input" type="text" v-model="dlat">
    <div class="destination-label">경도</div>
    <input class="destination-input" type="text" v-model="dlng">
    <!-- <button class="destination-button"><div>목적지 변경</div></button> -->
  </div>
  <GoogleMap api-key="AIzaSyAzKCIGiO7ODgLmp5ZhPLb4p3TVG8vBVEc" style="width: 100%; height: 90%;" :center="points[2]"
    :zoom="20" language="kor" id="map">
    <Marker :options="markerOption" @mouseup="setDestination" v-bind:ref="mlat" />
    <InfoWindow :options="{ position: {lat: initCenter.lat+0.00005, lng: initCenter.lng}, content: '목적지 설정을 위해 마커를 옮겨 주세요.' }" />
    <Circle v-for="circle in circles" :options="circle" :key="circle" v-bind="circles"></Circle>
    <Circle v-bind="destination" :options="destination"></Circle>
    <Polyline :key="pathOptions.path[pathOptions.path.length-2]" :options="pathOptions"></Polyline>
    <!-- <Polyline :options="examplePath" /> -->
  </GoogleMap>
</template>
