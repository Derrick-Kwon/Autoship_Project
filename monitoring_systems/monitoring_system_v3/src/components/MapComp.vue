<script>
import { defineComponent } from 'vue'
import { Circle, GoogleMap, Marker } from 'vue3-google-map'
export default defineComponent({
  components: { GoogleMap, Marker, Circle },
  setup() {
    const center = { lat: 36.3721, lng: 127.3604 };
    const markerOptions = { position: center, title: "destination", draggable: true, };
    const circleOptions = { center: center, radius: 3, fillColor: '#FF0000', fillOpacity: 0.8, strokeColor: '#FF0000', strokeOpacity: 0.8, strokeWeight: 2 }

    return { center, markerOptions, circleOptions }
  },
  data() {
    return {
      circles: [],
    }
  },
  mounted() {
    setInterval(this.move, 500)
  },
  methods: {
    move() {
      let option = this.circleOptions
      option.center.lat += 0.0001 + 0.0001 * (Math.random() - 0.5)
      option.center.lng += 0.0001 + 0.0001 * (Math.random() - 0.5)
      option.date = Date()
      this.circles.push(option)
    },
    showDate() {

    }
  }
})


</script>

<template>
  <GoogleMap api-key="AIzaSyAzKCIGiO7ODgLmp5ZhPLb4p3TVG8vBVEc" style="width: 100%; height: 100%;" :center="center"
    :zoom="15" language="kor" id="map">
    <Marker :options="markerOptions" />
    <Circle :options="circleOptions">
    </Circle>
    <Circle v-for="circle in circles" :options="circle" :key="circle" v-bind="circles" @mouseover="showDate"></Circle>
  </GoogleMap>
</template>

