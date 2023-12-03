<template>
  <div id="genderWordCloud" class="w-full h-full"></div>
</template>

<script>
import * as d3 from 'd3';
import d3Cloud from 'd3-cloud';
import axios from 'axios';
import Cookies from 'js-cookie';
import { watch, computed, onMounted } from 'vue';
import { useStore } from 'vuex';


export default {
  name: 'GenderWordCloud',
  setup() {
    const store = useStore();
    const isAuthenticated = computed(() => store.state.isAuthenticated);
    const submissions = computed(() => store.state.submissions);

    const fetchDataAndRenderCloud = async () => {
      console.log("Fetch and Render starting for world cloud");
      try {
        console.log("GET request with token ", Cookies.get('gt_login_token'));
        const response = await axios.get('/api/gender/history', {
          headers: { 'x-access-tokens': Cookies.get('gt_login_token') }
        });

        const formattedData = prepareDataForWordCloud(response.data);
        renderWordCloud(formattedData);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    const renderWordCloud = (data) => {
      const svgDiv = d3.select('#genderWordCloud');
      svgDiv.selectAll("svg").remove();
      const width = svgDiv.node().getBoundingClientRect().width;
      const height = svgDiv.node().getBoundingClientRect().height;

      const layout = d3Cloud()
                      .size([width, height])
                      .words(data.map(d => ({text: d.text, size: d.size * 10})))
                      .padding(5)
                      .rotate(() => ~~(Math.random() * 2) * 90)
                      .font('Impact')
                      .fontSize(d => d.size)
                      .on('end', words => {
      // Render the word cloud
      const svg = svgDiv.append('svg')
         .attr('width', layout.size()[0])
         .attr('height', layout.size()[1])
         .append('g')
         .attr('transform', `translate(${layout.size()[0] / 2}, ${layout.size()[1] / 2})`);

      svg.selectAll('text')
         .data(words)
         .enter().append('text')
         .style('font-size', d => `${d.size}px`)
         .style('font-family', 'Impact')
         .attr('text-anchor', 'middle')
         .attr('transform', d => `translate(${d.x}, ${d.y}) rotate(${d.rotate})`)
         .text(d => d.text);
        });

      layout.start();
    };

    const prepareDataForWordCloud = (jsonData) => {
      let allDescriptions = jsonData.map(item => item.description).join(" ");
      let words = allDescriptions.match(/\b(\w+)\b/g);
      let wordCounts = words.reduce((acc, word) => {
          word = word.toLowerCase(); // Convert to lower case
          acc[word] = (acc[word] || 0) + 1;
          return acc;
      }, {});

      return Object.keys(wordCounts).map(word => {
          return {text: word, size: wordCounts[word]};
      });
    }


    watch(isAuthenticated, (newValue, oldValue) => {
      fetchDataAndRenderCloud();
      console.log("Updating Word Cloud due to user change. (", oldValue, " -> ", newValue, ')');
    });

    watch(submissions, (newValue, oldValue) => {
      fetchDataAndRenderCloud();
      console.log("Updating World Cloud due to submission (", oldValue, " -> ", newValue, ')');
    });

    onMounted(() => {
      fetchDataAndRenderCloud();
    });

    return {
      isAuthenticated
    };
  }

}
</script>
