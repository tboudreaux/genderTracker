<template>
  <div class="bg-gray-100">
    <TopBanner @auth-button-clicked="showModal=true"/>
    <LoginForm v-if="showModal" @close-login-modal="showModal = false"/>
    <MainContent />
  </div>
</template>

<script>
import TopBanner from './components/TopBanner.vue'
import LoginForm from './components/LoginForm.vue'
import MainContent from './components/MainContent.vue'

export default {
  components: {
    TopBanner,
    LoginForm,
    MainContent
  },
  data() {
    return {
      showModal: false,
    };
  }
};
</script>
