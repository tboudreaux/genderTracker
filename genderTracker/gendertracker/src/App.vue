<template>
  <div class="bg-gray-100">
    <TopBanner />
    <LoginForm v-if="!$store.state.isAuthenticated" />
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
  }
}
</script>
