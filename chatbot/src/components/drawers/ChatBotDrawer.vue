<template>
  <div class="chat-container">
    <div>
      <div
          v-for="(message, index) of messages"
          :key="index"
          class="message-container"
          :class="[message.sender === 'bot' ? 'left' : 'right']"
      >
        <div class="icon-container">
          <IconBase
              v-if="message.sender === 'bot' || error"
              type="fas"
              name="robot"
              size="xl"
              :color="error ? 'error': ''"
          />
        </div>
        <p v-if="error" class="left error">{{error}}</p>
        <p
            v-else
            class="text-container"
            :class="[message.sender === 'bot' ? 'left' : 'right']"
        >
          {{ message.text }}{{ isLoading ? dots : '' }}
        </p>
      </div>
    </div>
    <div class="ask-container">
      <div class="ask-content">
        <input
          v-model="text"
          type="text"
          placeholder="Ecrivez votre question..."
          class="input-container"
          @keyup.enter="isLoading ? null : send()"
        >
      </div>
      <button
        @click="send()"
        class="button-container"
        :disabled="isLoading"
      >
        envoyer
      </button>
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
      error: null,
      dotsCount: '',
      dotInterval: null,
      text: '',
      id: 0
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
      return this.chatStore.getChats || []
    },
    chat () {
      return this.chatStore.getChatById(this.id) || {}
    },
    messages () {
      return this.chat.messages || []
    },
    dots() {
      return '.'.repeat(this.dotsCount)
    },
    isLoading() {
      const lastMessage = this.messages[this.messages.length - 1]
      return lastMessage?.loading || false
    },
  },

  async mounted () {
    this.id = this.chats.length || 0
    try {
      this.startDotsAnimation()
      await this.chatStore.summarize(this.id, this.data)
    } catch (error) {
      this.stopDotsAnimation()
      this.error = error
    } finally {
      this.stopDotsAnimation()
    }
  },

  methods: {
    startDotsAnimation() {
      this.dotsInterval = setInterval(() => {
        this.dotsCount = (this.dotsCount + 1) % 3
      }, 500)
    },
    stopDotsAnimation() {
      clearInterval(this.dotsInterval)
      this.dotsInterval = null
      this.dotsCount = 0
    },
    async send() {
      const message = {
        sender: 'user',
        text: this.text
      }
      this.chatStore.updateChat({
        id: this.id,
        message
      })
      this.text = ''
      try {
        this.startDotsAnimation()
        await this.chatStore.send(this.id, message)
      } catch (error) {
        this.stopDotsAnimation()
        this.error = error
      } finally {
        this.stopDotsAnimation()
      }
    }
  }
}
</script>


<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  width: 100%;
  margin: .5rem;
}

.message-container {
  display: flex;
  align-items: center;
  width: 100%;
  margin-bottom: .1rem;
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

.left.error {
  color: #EF5350;
}

.ask-container {
  display: flex;
  justify-content: space-between;
}

.ask-content {
  display: flex;
  color: #949ED1;
  border: 1px solid #F0F2FC;
  border-radius: 5px;
  width: 100%;
  padding: .5rem;
  box-shadow: 0px 1px #F2F2F5;
  justify-content: start;
}


.input-container {
  border: none;
  width: 100%
}

.input-container:focus {
  outline: none;
}

.input-container::placeholder {
  color: #949ED1;
}

.input-container:focus::placeholder {
  color: transparent;
}

.button-container {
  margin-left: .2rem;
  padding: .5rem;
  color: white;
  background-color: #405BDD;
  border-radius: 5px;
  cursor: pointer;
}

.button-container:hover {
  background-color: #3048a6;
}

.button-container:disabled {
  cursor: not-allowed;
  opacity: 0.7;
}

.button-container:disabled:hover {
  background-color: #405BDD;
  cursor: not-allowed;
  opacity: 0.7;
}

</style>
