<template>
  <div class="bg-gray-100">
    <TopBanner @auth-button-clicked="showModal=true" @settings-button-clicked="showSettings=true"/>
    <LoginForm v-if="showModal" @close-login-modal="showModal = false"/>
    <SettingsForm v-if="showSettings" @close-settings-modal="showSettings = false"/>
    <SubmissionResult v-if="showSubmissionResuts" @close-result-modal="showSubmissionResuts=false"/>
    <MainContent @submission-button-pressed="showSubmissionResuts=true"/>
  </div>
</template>

<script>
import TopBanner from './components/TopBanner.vue'
import LoginForm from './components/LoginForm.vue'
import MainContent from './components/MainContent.vue'
import SettingsForm from './components/SettingsForm.vue'
import SubmissionResult from './components/SubmissionResult.vue'

export default {
  components: {
    TopBanner,
    LoginForm,
    MainContent,
    SettingsForm,
    SubmissionResult,
  },
  data() {
    return {
      showModal: false,
      showSettings: false,
      showSubmissionResuts: false,
    };
  }
};
</script>
