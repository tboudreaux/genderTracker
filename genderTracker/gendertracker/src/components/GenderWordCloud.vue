<template>
  <div id="genderWorldCloud"></div>
</template>

<script>
import * as d3 from 'd3';
// import d3Cloud from 'd3-cloud';
import axios from 'axios';
import Cookies from 'js-cookie';

export default {
  name: 'GenderWorldCloud',
  mounted() {
    this.fetchDataAndRenderCloud();
  },
  methods: {
    async fetchDataAndRenderCloud() {
      try {
        const response = await axios.get('/api/gender/history', {
          headers: { 'x-access-token': Cookies.get('gt_login_token') }
        });
        console.log(response.data);

        const formattedData = this.prepareDataForWordCloud(response.data);
        console.log(formattedData);
         
        this.renderWorldCloud(formattedData);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    },
    renderWorldCloud(wordsArray) {
      /* eslint-disable no-unused-vars */

      var layout = d3.layout.cloud()
                     .size([800, 400])
                     .words(wordsArray.map(function(d) {
                       return {text: d.word, size: d.size};
                     }))
                     .padding(5)
                     .rotate(function() { return ~~(Math.random() * 2) * 90; })
                     .font("Impact")
                     .fontSize(function(d) { return d.size; })
                     .on("end", draw);
      layout.start();
      function draw(words) {
        d3.select("#genderWordCloud").append("svg")
            .attr("width", layout.size()[0])
            .attr("height", layout.size()[1])
          .append("g")
            .attr("transform", "translate(" + layout.size()[0] / 2 + "," + layout.size()[1] / 2 + ")")
          .selectAll("text")
            .data(words)
          .enter().append("text")
            .style("font-size", function(d) { return d.size + "px"; })
            .style("font-family", "Impact")
            .attr("text-anchor", "middle")
            .attr("transform", function(d) {
              return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
            })
            .text(function(d) { return d.text; });
      }
    },
    prepareDataForWordCloud(jsonData) {
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
 }
};
</script>
