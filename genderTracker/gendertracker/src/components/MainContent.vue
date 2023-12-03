<template>
  <div class="container mx-auto p-4">
    <div class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
      <form>
        <!-- Name Input -->
        <div v-if="this.$store.state.isGuest" class="mb-4">
          <label class="block text-gray-700 text-sm font-bold mb-2" for="username">
            Name
          </label>
          <input class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" id="username" type="text" placeholder="Enter name">
        </div>

        <!-- Gender Selection with Other option -->
        <div class="mb-4">
          <label class="block text-gray-700 text-sm font-bold mb-2">
            Gender
          </label>
          <select v-model="selectedGender" id="genderSelect" class="block appearance-none w-full bg-white border border-gray-400 hover:border-gray-500 px-4 py-2 pr-8 rounded shadow leading-tight focus:outline-none focus:shadow-outline" @change="showOtherField">
            <option v-for="gender in this.$store.state.genderList" :key=gender[0]>
              {{ gender[0] }} ({{ gender[1].join('/') }})
            </option>
            <option>Other</option>
          </select>
        </div>

        <div class="mb-4" :class="{'hidden': !showOtherGenderField}" id="otherGender">
          <label class="block text-gray-700 text-sm font-bold mb-2" for="otherGenderInput">
            Please specify
          </label>
          <div class="flex space-x-2">
            <input ref="genderName" type="text" id="otherGenderInput1" class="shadow appearance-none border rounded w-1/4 py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" placeholder="Enter your gender*">
            <input ref="pronouns" type="text" id="otherGenderInput2" class="shadow appearance-none border rounded w-1/4 py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" placeholder="Enter your pronouns*">
            <input ref="genderDescription" type="text" id="otherGenderInput3" class="shadow appearance-none border rounded w-1/2 py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" placeholder="Enter a description">
          </div>
        </div>


        <!-- Description Area -->
        <div class="mb-6">
          <label class="block text-gray-700 text-sm font-bold mb-2" for="description">
            Description
          </label>
          <textarea ref="dailyDescription" class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" id="description" placeholder="Enter description"></textarea>
        </div>

        <!-- Submit Button -->
        <div v-if="this.$store.state.isAuthenticated" class="flex items-center justify-between">
          <button @click="submitData" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline" type="button">
            Submit
          </button>
        </div>
      </form>
    </div>

    <!-- Placeholder for Graphical Visualization -->
    <div class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
    <h2 class="text-xl mb-4">Graphical Visualizations of Gender</h2>
    <div class="flex flex-col md:flex-row">
      <div class="md:w-1/2 h-96">
        <GenderTimeline />
      </div>
      <div class="md:w-1/2 h-96" >
        <GenderWordCloud />
      </div>
    </div>
  </div>
  </div>
</template>

<script>
import GenderTimeline from './GenderTimeline.vue'
import GenderWordCloud from './GenderWordCloud.vue'
import axios from 'axios';
import Cookies from 'js-cookie';

export default {
  components: {
    GenderTimeline,
    GenderWordCloud,

  },
  data() {
    return {
      showOtherGenderField: false,
      selectedGender: '',
    
    };
  },
  methods: {
    showOtherField(event) {
      this.showOtherGenderField = event.target.value === 'Other';
    },
    submitData() {
      const token = Cookies.get('gt_login_token');
      const dayDs = this.$refs.dailyDescription.value;
      var gender = '';
      var pronouns = '';
      var genderDescription = '';
      
      if (this.selectedGender === 'Other'){
        gender = this.$refs.genderName.value;

        // eslint-disable-next-line no-useless-escape
        pronouns = this.$refs.pronouns.value;
        genderDescription = this.$refs.genderDescription.value;
        
      } else{
        gender = this.selectedGender.split('(')[0].trim();
        pronouns = this.selectedGender.split('(')[1].split(')')[0].trim();
      }
      const payload = {
        'gender': gender,
        'pronouns': pronouns,
        'genderDescription': genderDescription,
        'dayDescription': dayDs,
      }
      axios.post('/api/gender/day', payload, {
        headers : {
        'x-access-tokens' : token,
        'Content-Type': 'application/json'
        },
      })
      .then((response) => {
        console.log(response);
        this.$emit('submission-button-pressed');
        this.$refs.dailyDescription.value = '';
        this.$store.state.submissions += 1;
        if (this.selectedGender === 'Other') {
            this.$refs.genderName.value = '';
            this.$refs.pronouns.value = '';
            this.$refs.genderDescription.value = '';
          }
        this.selectedGender = '';
      }, (error) => {
        console.log(error);
      })
    }
  },
};
</script>

