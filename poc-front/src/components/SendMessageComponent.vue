<script setup>
import { ref } from "vue";
import {useChatStore} from "../store/ChatStore.js";
const message = ref("");
const chatStore = useChatStore;

function updateMessage(event) {
  message.value = event.target.innerText;
}

async function send() {
  try {
    if(message.value === "") {
      return;
    }
    await chatStore().sendMessage(message.value);
    message.value = "";
  } catch (error) {
    console.error(error);
  }

}

</script>

<template>
  <div class="m-2 flex-col justify-end">
    <div @keydown.enter.prevent="send" @input="updateMessage" contenteditable="true" class="textarea-div border border-gray-300 p-2 rounded-md  overflow-auto focus:outline-none focus:ring-2 focus:ring-blue-500" style="min-height: 100px;" />
    <div class="flex w-full justify-end">
      <button @click="send" class="m-4 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
        Envoyer
      </button>
    </div>

  </div>
</template>

<style scoped>
</style>
