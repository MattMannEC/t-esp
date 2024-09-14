<script setup>
import { defineProps } from "vue";

const props = defineProps({
  messages: {
    type: Array,
    required: true,
    default: () => [],
  },
});
</script>

<template>
<div v-for="(message, index) in messages" class="my-4 flex w-full" :class="[message.sender === 'user'? 'justify-end': 'justify-start']">
  <div class="rounded p-2" :class="[message.sender === 'user' ? 'bg-gray-200': 'bg-gray-100']">
    {{message.content}}
  </div>
</div>
</template>

<style scoped>

</style>
