<script setup>
import { onMounted} from "vue";
import MessageComponent from "../components/MessageComponent.vue";
import SendMessageComponent from "../components/SendMessageComponent.vue";
import { useChatStore } from "../store/ChatStore.js";

const chatStore = useChatStore();

onMounted(() => {
  chatStore.init();
});
</script>

<template>
  <div class="m-2 flex-col min-h-full w-full relative">
    <div class="overflow-scroll">
      <MessageComponent :messages="chatStore.getMessages" />
    </div>

    <div class="w-full absolute bottom-0 z-10">
      <SendMessageComponent />
    </div>
  </div>


</template>

<style scoped>

</style>
