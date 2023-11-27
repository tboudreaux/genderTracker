<template>
  <div id="loginModal" style="background-color: rgba(0, 0, 0, 0.5);">
    <div class="fixed inset-0 z-10 overflow-y-auto">
        <div class="flex items-center justify-center min-h-screen">
            <div class="bg-white rounded-lg p-6 mx-4 text-left shadow-xl">
                <!-- Modal Content -->
                <div class="mb-4">
                    <label class="block text-gray-700 text-sm font-bold mb-2" for="username">Username</label>
                    <input type="text" id="username" class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline">
                </div>
                <div class="mb-6">
                    <label class="block text-gray-700 text-sm font-bold mb-2" for="password">Password</label>
                    <input type="password" id="password" class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline">
                </div>
                <div class="flex items-center justify-between">
                    <button @click="closeModal" class="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline" type="button">Close</button>
                    <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline" type="button">Login</button>
                    <button onclick="loginAsGuest()" class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline" type="button">Continue as Guest</button>
                </div>
            </div>
        </div>
    </div>
</div>
</template>

<script>
export default {
  methods: {
    login() {
      this.$store.commit('login', { isGuest: false });
      // Additional login logic...
    },
    loginAsGuest() {
      this.$store.commit('login', { isGuest: true });
      // Additional logic for guest mode...
    },
    closeModal() {
      this.$emit('close-login-modal');
    }
  }
}
</script>

