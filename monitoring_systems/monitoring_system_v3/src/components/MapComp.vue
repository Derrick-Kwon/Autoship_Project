<script>
import { defineComponent } from 'vue'
import { Circle, GoogleMap, Marker } from 'vue3-google-map'
import voyageData from '../assets/voyage-data.json'
export default defineComponent({
  components: { GoogleMap, Marker, Circle },
  setup() {
    // const center = { lat: 36.3721, lng: 127.3604 };
    // const center = { lat: 37.300163057152, lng: 126.83771082564 }
    const p1 = { lat: 37.2978, lng: 126.83339 } // start - point1
    const p2 = { lat: 37.29788, lng: 126.83358 } // point2
    const p3 = { lat: 37.297865, lng: 126.83361 } // point3
    const p4 = { lat: 37.297905, lng: 126.833705 } // point 4
    const p5 = { lat: 37.29793, lng: 126.833705 } // point 5
    const p6 = { lat: 37.298015, lng: 126.833888 } // point 6
    const center = p1
    const points = [p1, p2, p3, p4, p5, p6]
    const markerOptions = { position: center, title: "destination", draggable: true, }
    const circleOptions = { center: center, radius: 0.2, fillColor: '#FF0000', fillOpacity: 0.8, strokeColor: '#FF0000', strokeOpacity: 0.8, strokeWeight: 2 }
    const initPath = { path: [center], geodesic: true, strokeColor: "#00FF00", strokeOpacity: 1.0, strokeWeight: 2 }
    const examplePath = { path: [center, { lat: center.lat + 1, lng: center.lng + 1 }], geodesic: true, strokeColor: "#FF0000", strokeOpacity: 1.0, strokeWeight: 2 }
    return { center, markerOptions, circleOptions, initPath, examplePath, points }
  },
  data() {
    return {
      circles: [],
      pathOptions: {},
      voyageData: voyageData,
      position: this.center,
    }
  },
  mounted() {
    this.pathOptions = this.initPath
    this.voyageData.max_indices.pop()
    this.max_indices = this.voyageData.max_indices
  },
  methods: {
    // move() {
    //   let option = this.circleOptions
    //   option.center.lat += 0.0001 + 0.0001 * (Math.random() - 0.5)
    //   option.center.lng += 0.0001 + 0.0001 * (Math.random() - 0.5)
    //   option.date = Date()

    //   console.log("voyagepath: ", this.pathOptons)
    //   console.log("circles: ", this.circles)

    //   this.pathOptions.path.push({ lat: option.center.lat, lng: option.center.lng })

    //   this.circles.push(option)
    // },
    move() {
      const data = this.voyageData.shift()
      if (typeof data === "undefined") {
        this.endMove()
        return
      }

      const p1 = this.points[data.level]
      const p2 = this.points[data.level + 1]
      console.log(p1)
      console.log(p2)

      const dlatTotal = p2.lat - p1.lat
      const dlngTotal = p2.lng - p1.lng
      const dlat = dlatTotal * data.progress
      const dlng = dlngTotal * data.progress

      const option = this.circleOptions
      option.date = Date()
      option.center.lat = p1.lat + dlat
      option.center.lng = p1.lng + dlng

      this.circles.push(option)
    },
    startMove() {
      this.interval = setInterval(this.move, 100)
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
    <Marker :options="markerOptions" @mouseup="console.log('marker position: ', this.markerOptions.position)" />
    <Circle v-for="circle in circles" :options="circle" :key="circle" v-bind="circles"></Circle>
    <!-- <Polyline :options="pathOptions" :key="pathOptions.path" /> -->

    <!-- <Polyline :options="examplePath" /> -->
  </GoogleMap>
</template>