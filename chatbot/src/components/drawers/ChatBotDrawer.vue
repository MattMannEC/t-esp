<template>
  <div class="chat-container">
    <div
      v-for="(message, index) of messages"
      :key="index"
      class="message-container"
      :class="[message.sender === 'bot' ? 'left' : 'right']"
    >
      <IconBase v-if="message.sender === 'bot'" type="fas" name="robot" size="xl" />
      <p
        class="text-container"
        :class="[message.sender === 'bot' ? 'left' : 'right']"
      >
        {{ message.text }}{{loading ? dots : ''}}
      </p>
    </div>
  </div>
</template>

<script>
import IconBase from "@/components/icons/IconBase.vue";
import {useChatStore} from "@/store/chatStore/ChatStore.js";

export default {
  components: {
    IconBase
  },

  data () {
    return {
      messages: [],
      error: null,
      loading: false,
      dots: '',
      dotInterval: null
    }
  },

  props: {
    data: {
      type: Object,
      required: true,
      default: {}
    }
  },

  computed: {
    chatStore () {
      return useChatStore()
    },
    chats () {
      return this.chatStore.getChats
    }
  },

  async mounted () {
    const id = this.chats.length || 0
    try {
      this.loading = true
      this.messages.push({
        sender: 'bot',
        text: 'Résumé en cours.'
      })
      this.dot()
      await this.chatStore.summarize(id, this.data)
    } catch (error) {
      this.loading = false
      this.stopDots()
      this.error = error
      this.messages.push({
        sender: 'bot',
        text: error
      })
    } finally {
      this.loading = false
      this.stopDots()
      if (this.chatStore.getChatById(id)) {
        this.messages = this.chatStore.getChatById(id).messages
      }
    }
  },

  methods: {
    dot() {
      const maxDots = 2;
      this.dotInterval = setInterval(() => {
        this.dots = this.dots.length < maxDots ? this.dots + '.' : '';
      }, 500);
    },
    stopDots() {
      clearInterval(this.dotInterval);
      this.dots = '';
    },
  }
}
</script>


<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  width: 100%;
  margin: .5rem;
}

.message-container {
  display: flex;
  align-items: center;
  width: 100%;
}

.text-container {
  display: flex;
  padding: .5rem;
  border-radius: 5px;
  max-width: 60%;
  width: fit-content;
  word-wrap: break-word;
  word-break: break-word;
  text-align: start;
}

.text-container.right {
  background-color: #405BDD;
  color: white;
}

.right {
  justify-content: end;
}

.left {
  justify-content: start;
}



</style>
