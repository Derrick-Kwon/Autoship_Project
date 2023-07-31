<script>
import { defineComponent } from 'vue'
import { GoogleMap, Marker } from 'vue3-google-map'
export default defineComponent({
  components: { GoogleMap, Marker },
  setup() {
    const center = { lat: 36.3721, lng: 127.3604 };
    const markerOptions = { position: center, title: "destination", draggable: true, };
    return { center, markerOptions, }
  },
})

</script>

<template>
  <GoogleMap api-key="AIzaSyAzKCIGiO7ODgLmp5ZhPLb4p3TVG8vBVEc" style="width: 100%; height: 100%;" :center="center"
    :zoom="15" language="kor">
    <Marker :options="markerOptions" />
  </GoogleMap>
</template>

