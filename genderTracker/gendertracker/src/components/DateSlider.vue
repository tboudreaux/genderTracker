<template>
  <div class="slider-container my-4">
    <input
      type="range"
      class="slider w-full"
      :min="0"
      :max="dateRange"
      v-model="sliderValue"
    />
    <div class="text-center mt-2">Selected Date: {{ formattedSelectedDate }}</div>
  </div>
</template>

<script>
import { ref, computed } from 'vue';
import { differenceInCalendarDays, addDays, format } from 'date-fns';

export default {
  props: {
    initialDate: {
      type: Date,
      required: true
    },
    finalDate: {
      type: Date,
      required: true
    }
  },
  setup(props) {
    const sliderValue = ref(0);

    const dateRange = computed(() => {
      return differenceInCalendarDays(props.finalDate, props.initialDate);
    });

    const selectedDate = computed(() => {
      return addDays(props.initialDate, sliderValue.value);
    });

    const formattedSelectedDate = computed(() => {
      return format(selectedDate.value, 'PPP'); // e.g., Jun 7, 2020
    });

    return { sliderValue, dateRange, formattedSelectedDate };
  }
};
</script>

<style scoped>
.slider-container {
  /* Custom container styles */
}
.slider {
  /* Custom slider styles */
  -webkit-appearance: none; /* Override default appearance */
  appearance: none;
  width: 100%;
  height: 15px;
  background: #ddd; /* Slider background */
  outline: none; /* Remove outline */
  opacity: 0.7; /* Set transparency (cross-browser) */
  -webkit-transition: .2s; /* Transition for smooth effect */
  transition: opacity .2s;
}
.slider:hover {
  opacity: 1; /* Fully opaque on hover */
}
</style>
