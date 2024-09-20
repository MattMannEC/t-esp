<script setup>
import { onMounted, onUpdated, ref } from "vue";
import MessageComponent from "../components/MessageComponent.vue";
import SendMessageComponent from "../components/SendMessageComponent.vue";
import { useChatStore } from "../store/ChatStore.js";

const chatStore = useChatStore();
const messageAreaRef = ref(null);

onMounted(() => {
  chatStore.init();
});

onUpdated(() => {
  if (messageAreaRef.value) {
    messageAreaRef.value.scrollTop = messageAreaRef.value.scrollHeight;
  }
});
</script>

<template>
  <div class="flex flex-col h-screen">
    <div class="flex-1 overflow-y-auto p-4" :ref="messageAreaRef">
      <MessageComponent :messages="chatStore.getMessages" />
    </div>

    <div class="w-full p-4  bg-white">
      <SendMessageComponent />
    </div>
  </div>
</template>

<style scoped>
</style>
