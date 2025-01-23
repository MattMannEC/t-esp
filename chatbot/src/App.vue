<template>
  <div id="app" :class="{ 'relative': drawerStore.getShowDrawer }">
    <SidebarComponent />
    <div class="router">
      <RouterView />
    </div>
    <template v-if="drawerStore.getShowDrawer">
      <DrawerBase :drawer="drawerStore.getDrawer.name" :data="drawerStore.getDrawer.data" />
    </template>
  </div>

</template>

<script>

import DrawerBase from "@/components/drawers/DrawerBase.vue";
import SidebarComponent from "@/components/sidebar/SidebarComponent.vue";
import { useDrawerStore } from "@/store/drawerStore/DrawerStore.js";

export default {

  components: {
    DrawerBase,
    SidebarComponent
  },

  computed: {
    drawerStore() {
      return useDrawerStore()
    }
  },
  data() {
    return {
      prompt: '',
      messages: [
        // { sender: 'bot', text: 'Hello! How can I assist you today?' },
        // { sender: 'user', text: 'Can you tell me a joke?' },
        // { sender: 'bot', text: 'Here is a really funny joke that i think that you will like. Tell me if you like it or not... Why don’t scientists trust atoms?\nBecause they make up everything!' },
      ],
      eventSource: null,
      userId: 0
    };
  },
  mounted() {
    this.userId = Math.floor(Math.random() * 1000000);
    this.eventSource = new EventSource('http://localhost:8001/stream');
    this.eventSource.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (this.messages.length === 0 || this.messages[this.messages.length - 1].sender !== 'bot') {
        this.messages.push({ sender: 'bot', text: data.value });
      } else {
        this.messages[this.messages.length - 1].text += data.value;
      }
    };
  },
  methods: {
    sendMessage() {
      if (this.prompt.trim() !== '') {
        this.messages.push({ sender: 'user', text: this.prompt });
        fetch(`http://localhost:8001/invoke?prompt=${encodeURIComponent(this.prompt)}&user_id=${this.userId}`)
          .then(response => response.json())
          .then(data => {
            // Handle the response data if needed
            console.log(data);
          })
          .catch(error => {
            console.error('Error:', error);
          });
        this.prompt = '';
      }
    },
    disconnect() {
      if (this.eventSource) {
        this.eventSource.close();
        this.eventSource = null;
      }
    },
    formatMessage(message) {
      return message.replace(/(?:\r\n|\r|\n)/g, '<br>');
    },
  },
};
</script>

<style scoped>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0;
  color: #949ED1;
  height: 100%;
  width: 100%;
  font-size: 12px;
  padding: 0;
  z-index: 0;
}

.relative {
  position: relative;
}

.router {
  padding: 0 1rem;
  width: 100%;
}
</style>
