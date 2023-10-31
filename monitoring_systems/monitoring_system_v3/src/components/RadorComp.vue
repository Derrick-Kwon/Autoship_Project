<template>
  <div>
    <svg class="rador" style="margin: 25px;"></svg>
  </div>
</template>
<script>
import * as d3 from "d3";
import voyageData from '../assets/voyage-data.json'
export default {
  props: ['ridar'],
  name: 'RadorComp',
  data() {
    const width = 250
    const height = 250
    return { width, height, voyageData: voyageData }
  },
  methods: {
    showRador: function () {
      console.log("ridar: ", this.ridar)
      // const randAngle = Math.random() * 360
      // const randDist = Math.random() * 10
      if (this.ridar == null) {
        setTimeout(this.showRador, 500)
        return
      }
      for (let i = 0; i < 50; i++) {
        const point = this.ridar[i]
        const center = this.width / 2
        const cx = center + Math.cos((180-parseInt(point[0])) * Math.PI / 180) * center * parseInt(point[1]) / 250
        const cy = center + Math.sin((-1)*(180-parseInt(point[0])) * Math.PI / 180) * center * parseInt(point[1]) / 250

        d3.select('svg').append('circle')
          .attr('cx', cx)
          .attr('cy', cy)
          .attr('r', 2)
          .attr('fill', 'red')
          .attr("fill-opacity", 1)
          .attr("stroke-opacity", 1)
          .transition()
          .duration(3000)
          //change fill and stroke opacity to avoid CSS conflicts
          .attr("fill-opacity", 0)
          .attr("stroke-opacity", 0)
          .remove() //remove after transitions are complete
      }
      setTimeout(this.showRador, 3000)
    },
  },
  mounted() {
    d3.select('svg').append("svg:image").attr("xlink:href", "/rador.svg")
    setTimeout(this.showRador,6000)
  },
};
</script>