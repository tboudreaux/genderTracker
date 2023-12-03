<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center">
    <!-- Modal content -->
    <div class="bg-white rounded-lg shadow-xl p-6 m-4 max-w-xl w-full">
      <!-- Close button -->
      <div class="flex justify-end">
        <button @click="closeSettingsModal" class="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline mx-2" type="button">Close</button>
      </div>
      <!-- Settings form content -->
      <h3 class="text-lg leading-6 font-medium text-gray-900" id="modal-headline">
        Settings
      </h3>
      <div class="mt-2">
          <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">Add New User</h3>
  <form @submit.prevent="addUser">
    <div class="mb-4">
      <label class="block text-gray-700 text-sm font-bold mb-2" for="username">
        Username
      </label>
      <input v-model="newUser.username" type="text" id="username" class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" required>
    </div>
    <div class="mb-4">
      <label class="block text-gray-700 text-sm font-bold mb-2" for="email">
        Email
      </label>
      <input v-model="newUser.email" type="email" id="email" class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" required>
    </div>
    <div class="mb-4">
      <label class="block text-gray-700 text-sm font-bold mb-2" for="password">
        Password
      </label>
      <input v-model="newUser.password" type="password" id="password" class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline" required>
    </div>
    <div class="flex items-center justify-between">
      <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline" type="submit">
        Add User
      </button>
    </div>
  </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Cookies from 'js-cookie';

export default {
  data() {
    return {
      newUser: {
        username: '',
        email: '',
        password: '',
      },
    };
  },
  emits: ['close-settings-form'],
  methods: {
    closeSettingsModal() {
      this.$emit('close-settings-modal');
    },
    addUser() {
      // Handle the user addition logic here
      console.log('Adding user:', this.newUser);
      const token = Cookies.get('gt_login_token');
      const payload = {
        'new_user': this.newUser.username,
        'new_pass': this.newUser.password,
        'new_email': this.newUser.email,
        'new_user_is_admin': false,
        'new_user_is_enabled': true
      }
      axios.post('/api/user/enroll_user', payload, {
        headers : {
        'x-access-tokens' : token,
        'Content-Type': 'application/json'
        },
      })
        .then((response) => {
          console.log(response);
          console.log("New User ", this.newUser.username, " enrolled");
          this.newUser = { username: '', email: '', password: '' };
        })
        .catch((error) => {
          console.log("Error Enrolling user: ", error);
        })
    },
  },
};
</script>

