<template>
  <div class="bg-blue-500 text-white text-center p-4 flex justify-between items-center">
    <h1 class="text-lg sm:text-xl md:text-2xl font-bold">Welcome to the Gender Tracking App</h1>
    <button @click="handleAuthButton" class="bg-white text-blue-500 font-bold py-2 px-4 rounded">
      {{ $store.state.isAuthenticated ? 'Logout' : 'Login' }}
    </button>
  </div>
</template>

<script>
export default {
  methods: {
    handleAuthButton() {
      if (this.$store.state.isAuthenticated) {
        this.$store.commit('logout');
      } else {
        console.log("Login button pressed");
        this.$emit("auth-button-clicked");
      }
    }
  }
}
</script>

