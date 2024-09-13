<script setup>
import MessageComponent from "../components/MessageComponent.vue";
import SendMessageComponent from "../components/SendMessageComponent.vue";
</script>

<template>
  <div class="flex-col min-h-full w-full relative">
    <div class="m-2 flex justify-end">
      <MessageComponent />
    </div>

    <div class="m-2 w-full absolute bottom-0">
      <SendMessageComponent />
    </div>
  </div>


</template>

<style scoped>

</style>
