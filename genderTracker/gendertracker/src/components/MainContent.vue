<template>
  <div class="container mx-auto p-4">
    <div class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
      <form>
        <!-- Name Input -->
        <div class="mb-4">
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
          <select id="genderSelect" class="block appearance-none w-full bg-white border border-gray-400 hover:border-gray-500 px-4 py-2 pr-8 rounded shadow leading-tight focus:outline-none focus:shadow-outline" @change="showOtherField">
            <option>Female</option>
            <option>Male</option>
            <option>Non-binary</option>
            <option>Other</option>
          </select>
        </div>

        <!-- Other Gender Text Field (Initially Hidden) -->
        <div class="mb-4" :class="{'hidden': !showOtherGenderField}" id="otherGender">
          <label class="block text-gray-700 text-sm font-bold mb-2" for="otherGenderInput">
            Please specify
          </label>
          <input type="text" id="otherGenderInput" class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" placeholder="Enter your gender">
        </div>

        <!-- Pronouns Input -->
        <div class="mb-4">
          <label class="block text-gray-700 text-sm font-bold mb-2" for="pronouns">
            Pronouns
          </label>
          <input class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" id="pronouns" type="text" placeholder="e.g., She/Her, They/Them">
        </div>

        <!-- Description Area -->
        <div class="mb-6">
          <label class="block text-gray-700 text-sm font-bold mb-2" for="description">
            Description
          </label>
          <textarea class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" id="description" placeholder="Enter description"></textarea>
        </div>

        <!-- Submit Button -->
        <div class="flex items-center justify-between">
          <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline" type="button">
            Submit
          </button>
        </div>
      </form>
    </div>

    <!-- Placeholder for Graphical Visualization -->
    <div class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
      <h2 class="text-xl mb-4">Graphical Visualization Placeholder</h2>
      <p>Content will be displayed here in the future.</p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      showOtherGenderField: false,
    };
  },
  methods: {
    showOtherField(event) {
      this.showOtherGenderField = event.target.value === 'Other';
    },
  },
};
</script>

