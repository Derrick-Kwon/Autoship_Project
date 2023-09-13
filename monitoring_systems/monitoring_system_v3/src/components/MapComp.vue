<script>
import { defineComponent } from 'vue'
import { Circle, GoogleMap, Marker, Polyline } from 'vue3-google-map'
export default defineComponent({
  components: { GoogleMap, Marker, Circle, Polyline },
  setup() {
    const center = { lat: 36.3721, lng: 127.3604 };
    const markerOptions = { position: center, title: "destination", draggable: true, };
    const circleOptions = { center: center, radius: 3, fillColor: '#FF0000', fillOpacity: 0.8, strokeColor: '#FF0000', strokeOpacity: 0.8, strokeWeight: 2 }
    const initPath = { path: [center], geodesic: true, strokeColor: "#00FF00", strokeOpacity: 1.0, strokeWeight: 2 }
    const examplePath = { path: [center, { lat: center.lat + 1, lng: center.lng + 1 }], geodesic: true, strokeColor: "#FF0000", strokeOpacity: 1.0, strokeWeight: 2 }
    return { center, markerOptions, circleOptions, initPath, examplePath }
  },
  data() {
    return {
      circles: [],
      pathOptions: {},
    }
  },
  mounted() {
    this.pathOptions = this.initPath
  },
  methods: {
    move() {
      let option = this.circleOptions
      option.center.lat += 0.0001 + 0.0001 * (Math.random() - 0.5)
      option.center.lng += 0.0001 + 0.0001 * (Math.random() - 0.5)
      option.date = Date()

      console.log("voyagepath: ", this.pathOptons)
      console.log("circles: ", this.circles)

      this.pathOptions.path.push({ lat: option.center.lat, lng: option.center.lng })

      this.circles.push(option)
    },
    startMove() {
      this.interval = setInterval(this.move, 500)
    },
    endMove() {
      clearInterval(this.interval)
    }
  }
})
</script>

<template>
  <GoogleMap api-key="AIzaSyAzKCIGiO7ODgLmp5ZhPLb4p3TVG8vBVEc" style="width: 100%; height: 100%;" :center="center"
    :zoom="15" language="kor" id="map" @mouseenter="startMove" @mouseleave="endMove">
    <Marker :options="markerOptions" />
    <Circle v-for="circle in circles" :options="circle" :key="circle" v-bind="circles"></Circle>
    <Polyline :options="pathOptions" :key="pathOptions.path" />
    <!-- <Polyline :options="examplePath" /> -->
  </GoogleMap>
</template>