<template>
  <div>
    <svg class="rador"></svg>
  </div>
</template>
<script>
import * as d3 from "d3";
import voyageData from '../assets/voyage-data.json'
export default {
  data() {
    const width = 250
    const height = 250
    return { width, height, voyageData: voyageData }
  },
  methods: {
    showRador: function () {
      // const randAngle = Math.random() * 360
      // const randDist = Math.random() * 10
      if (this.voyageData.length < 1) {
        return
      }
      const data = this.voyageData.shift().ridar_points
      for (let i = 0; i < data.length; i++) {
        const point = data[i]
        console.log("point: ")
        console.log(point)
        const noisex = Math.random() - 0.5
        const noisey = Math.random() - 0.5
        const center = this.width / 2
        const cx = center + Math.cos(point.angle * Math.PI / 180) * point.distance / 25 * center / 10 + noisex
        const cy = center + Math.sin(point.angle * Math.PI / 180) * point.distance / 25 * center / 10 + noisey

        d3.select('svg').append('circle')
          .attr('cx', cx)
          .attr('cy', cy)
          .attr('r', 2)
          .attr('fill', 'red')
          .attr("fill-opacity", 1)
          .attr("stroke-opacity", 1)
          .transition()
          .duration(1000)
          //change fill and stroke opacity to avoid CSS conflicts
          .attr("fill-opacity", 0)
          .attr("stroke-opacity", 0)
          .remove() //remove after transitions are complete
      }
      setTimeout(this.showRador, 500)
    },
  },
  mounted() {
    d3.select('svg').append("svg:image").attr("xlink:href", "/rador.svg")
    setTimeout(this.showRador, 5000)

    // const g = svg.append("g");

    // //2. Parse the dates
    // const parseTime = d3.timeParse("%d-%b-%y");

    // //3. Creating the Chart Axes
    // const x = d3
    //   .scaleTime()
    //   .domain(
    //     d3.extent(data, function (d) {
    //       return parseTime(d.date);
    //     })
    //   )
    //   .rangeRound([0, width]);

    // const y = d3
    //   .scaleLinear()
    //   .domain(
    //     d3.extent(data, function (d) {
    //       return d.amount;
    //     })
    //   )
    //   .rangeRound([height, 0]);

    // //4. Creating a Line
    // const line = d3
    //   .line()
    //   .x(function (d) {
    //     return x(parseTime(d.date));
    //   })
    //   .y(function (d) {
    //     return y(d.amount);
    //   });

    // //5. Appending the Axes to the Chart
    // g.append("g")
    //   .attr("transform", "translate(0," + height + ")")
    //   .call(d3.axisBottom(x));

    // g.append("g")
    //   .call(d3.axisLeft(y))
    //   .append("text")
    //   .attr("fill", "#000")
    //   .attr("transform", "rotate(-90)")
    //   .attr("y", 6)
    //   .attr("dy", "0.71em")
    //   .attr("text-anchor", "end")
    //   .text("Price ($)");

    // //6. Appending a path to the Chart
    // g.append("path")
    //   .datum(data)
    //   .attr("fill", "none")
    //   .attr("stroke", "steelblue")
    //   .attr("stroke-width", 1.5)
    //   .attr("d", line);
  },
};
</script>