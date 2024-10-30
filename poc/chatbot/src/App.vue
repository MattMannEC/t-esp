<template>
  <div id="app">
    <h1>Chatbot</h1>
    <div class="chat-container">
      <div class="messages">
        <div
          v-for="(msg, index) in messages"
          :key="index"
          :class="['message', msg.sender === 'user' ? 'sent' : 'received']"
        >
          {{ msg.text }}
        </div>
      </div>
      <div class="input-container">
        <input
          v-model="prompt"
          @keyup.enter="sendMessage"
          placeholder="Ask a question..."
        />
        <button @click="sendMessage">Send</button>
        <button @click="disconnect" v-if="eventSource">Disconnect</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      prompt: '',
      messages: [],
      eventSource: null,
    };
  },
  mounted() {
    this.eventSource = new EventSource('http://localhost:8001/stream');
    this.eventSource.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (this.messages.length === 0 || this.messages[this.messages.length - 1].sender !== 'bot') {
        this.messages.push({ sender: 'bot', text: data.message });
      } else {
        this.messages[this.messages.length - 1].text += data.message;
      }
    };
  },
  methods: {
    sendMessage() {
      if (this.prompt.trim() !== '') {
        this.messages.push({ sender: 'user', text: this.prompt });
        fetch(`http://127.0.0.1:8001/simulate_llm?prompt=${encodeURIComponent(this.prompt)}`)
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
  },
};
</script>

<style scoped>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  margin: 0;
}

h1 {
  color: #2c3e50;
  margin-bottom: 20px;
}

.chat-container {
  width: 90%;
  height: 70%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  background: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.messages {
  flex: 1;
  overflow-y: auto;
  margin-bottom: 20px;
}

.message {
  padding: 10px;
  margin: 5px 0;
  border-radius: 5px;
  word-wrap: break-word;
}

.sent {
  background: #e0f7fa;
  text-align: right;
  align-self: flex-end;
}

.received {
  background: #fff9c4;
  text-align: left;
  align-self: flex-start;
}

.input-container {
  display: flex;
  gap: 10px;
}

input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
}

button {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  background: #42b983;
  color: white;
  cursor: pointer;
}

button:hover {
  background: #369f6b;
}

button:disabled {
  background: #ccc;
  cursor: not-allowed;
}
</style>