<template>
  <div id="submissionResult" style="background-color: rgba(0, 0, 0, 0.5);">
    <div class="fixed inset-0 z-10 overflow-y-auto">
        <div class="flex items-center justify-center min-h-screen">
            <div class="bg-white rounded-lg p-6 mx-4 text-left shadow-xl">
                <!-- Modal Content -->
                Gender Record Submitted! 
                <div class="mt-4 flex justify-right">
                    <button @click="closeResultModal" class="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline mx-2" type="button">Close</button>
                </div>
            </div>
        </div>
    </div>
</div>
</template>

<script>

export default {
  methods: {
    closeResultModal() {
      this.$emit('close-result-modal');
    }
  }
}
</script>

