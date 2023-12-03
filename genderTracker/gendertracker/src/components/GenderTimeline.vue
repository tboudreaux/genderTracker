<template>
  <div id="genderPieChart" class="w-full h-full"></div>
</template>

<script>
import * as d3 from 'd3';
import axios from 'axios';
import Cookies from 'js-cookie';
import { watch, computed, onMounted } from 'vue';
import { useStore } from 'vuex';

export default {
  name: 'GenderPieChart',
  setup() {
    const store = useStore();
    const isAuthenticated = computed(() => store.state.isAuthenticated);
    const submissions = computed(() => store.state.submissions);

    const fetchDataAndRenderChart = async () => {
      console.log("Fetch and Render starting");
      try {
        console.log("GET request with token ", Cookies.get('gt_login_token'));
        const response = await axios.get('/api/gender/pie', {
          headers: { 'x-access-tokens': Cookies.get('gt_login_token') }
        });

        const formattedData = Object.keys(response.data).map(key => {
          return { gender: key, count: response.data[key] };
        });
        renderTimelineChart(formattedData);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    const renderTimelineChart = (data) => {
      const svgDiv = d3.select('#genderPieChart');
      svgDiv.selectAll("svg").remove();
      /* eslint-disable no-unused-vars */
      const width = svgDiv.node().getBoundingClientRect().width;
      const height = svgDiv.node().getBoundingClientRect().height;
      console.log("box dimensions are ", width, height);

      // if (height === 0) {
      //   height = 500;
      // })


      const margin = width / 10;
      const radius = Math.min(width, height) / 2 - margin;
      const hoverRadius = radius + 10;

      const svg = svgDiv.append("svg")
                        .attr("width", width)
                        .attr("height", height)
                        .append("g")
                        .attr("transform", `translate(${width / 2}, ${height / 2})`);

      const color = d3.scaleOrdinal()
                      .domain(data)
                      .range(d3.schemeCategory10);

      const pie = d3.pie().value(d => d.count);
      const data_ready = pie(data);

      const arcGenerator = d3.arc()
                              .innerRadius(0)
                              .outerRadius(radius);

      const arcHover = d3.arc()
                          .innerRadius(0)
                          .outerRadius(hoverRadius);
      // Tooltip setup
      const tooltip = d3.select("body").append("div")
                        .attr("class", "tooltip")
                        .style("opacity", 0);

      svg.selectAll('path')
        .data(data_ready)
        .enter()
        .append('path')
        .attr('d', arcGenerator)
        .attr('fill', d => color(d.data.gender))
        .attr("stroke", "white")
        .style("stroke-width", "2px")
        .style("opacity", 0.7)
        .on('mouseover', function (event, d) {
          d3.select(this)
            .transition()
            .duration(200)
            .attr('d', arcHover);
          tooltip.transition()
                 .duration(200)
                 .style("opacity", 1);
          tooltip.html(`Percentage: ${(d.data.count / d3.sum(data, d => d.count) * 100).toFixed(2)}%`)
                 .style("left", (event.pageX) + "px")
                 .style("top", (event.pageY - 28) + "px");
          })
          .on('mouseout', function (d) {
            d3.select(this)
              .transition()
              .duration(200)
              .attr('d', arcGenerator);

            tooltip.transition()
              .duration(500)
              .style("opacity", 0);
          });

          // Adding text labels
      svg.selectAll('text')
        .data(data_ready)
        .enter()
        .append('text')
        .text(d => d.data.gender)
        .attr("transform", function(d) {
          let pos = arcGenerator.centroid(d);
          return `translate(${pos[0]}, ${pos[1]})`;
        })
        .style("text-anchor", "middle")
        .style("font-size", 14);
    };

    watch(isAuthenticated, (newValue, oldValue) => {
      fetchDataAndRenderChart();
      console.log("Updating Pie Chart due to user change.");
    });

    watch(submissions, (newValue, oldValue) => {
      fetchDataAndRenderChart();
      console.log("Updating Pie Chart due to new submission of data.");
    });

    onMounted(() => {
      fetchDataAndRenderChart();
    });

    return {
      isAuthenticated
    };
  }
};
</script>
