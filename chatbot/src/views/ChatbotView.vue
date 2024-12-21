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
          <template v-if="msg.sender === 'bot'" class="received-container">
            <img src="./assets/image.png" alt="Bot Icon" class="icon" />
            <div v-if="loading && messages.length - 1 === index" class="received-text">{{msg.text}}{{dots}}</div>
            <div v-else v-html="formatMessage(msg.text)" class="received-text"></div>
          </template>
          <div v-else v-html="formatMessage(msg.text)"></div>

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
        <IconPlus @click="resumeText" class="summarize-button-container"/>
      </div>
    </div>
  </div>
</template>

<script>

import IconPlus from "@/components/icons/IconPlus.vue";

export default {
  components: {
    IconPlus
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
      loading: false,
      dots: ''
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
    formatMessage(message) {
      return message.replace(/(?:\r\n|\r|\n)/g, '<br>');
    },
    resumeText() {
      if(this.loading === true) return
      this.loading = true
      this.messages.push( {
        sender: 'bot',
        text: 'Traitement de la requête en cours.'
      })
      this.dot()
      const text = 'PRÉAMBULE\n' +
          'Le peuple français proclame solennellement son attachement aux Droits de l\'homme et aux principes de la souveraineté nationale tels qu\'ils ont été définis par la Déclaration de 1789, confirmée et complétée par le préambule de la Constitution de 1946, ainsi qu\'aux droits et devoirs définis dans la Charte de l\'environnement de 2004.\n' +
          '\n' +
          'En vertu de ces principes et de celui de la libre détermination des peuples, la République offre aux territoires d\'outre-mer qui manifestent la volonté d\'y adhérer des institutions nouvelles fondées sur l\'idéal commun de liberté, d\'égalité et de fraternité et conçues en vue de leur évolution démocratique.\n' +
          '\n' +
          'ARTICLE PREMIER.\n' +
          'La France est une République indivisible, laïque, démocratique et sociale. Elle assure l\'égalité devant la loi de tous les citoyens sans distinction d\'origine, de race ou de religion. Elle respecte toutes les croyances. Son organisation est décentralisée.\n' +
          '\n' +
          'La loi favorise l\'égal accès des femmes et des hommes aux mandats électoraux et fonctions électives, ainsi qu\'aux responsabilités professionnelles et sociales.\n' +
          '\n' +
          'Titre premier - DE LA SOUVERAINETÉ\n' +
          'ARTICLE 2.\n' +
          'La langue de la République est le français.\n' +
          '\n' +
          'L\'emblème national est le drapeau tricolore, bleu, blanc, rouge.\n' +
          '\n' +
          'L\'hymne national est « La Marseillaise ».\n' +
          '\n' +
          'La devise de la République est « Liberté, Égalité, Fraternité ».\n' +
          '\n' +
          'Son principe est : gouvernement du peuple, par le peuple et pour le peuple.\n' +
          '\n' +
          'ARTICLE 3.\n' +
          'La souveraineté nationale appartient au peuple qui l\'exerce par ses représentants et par la voie du référendum.\n' +
          '\n' +
          'Aucune section du peuple ni aucun individu ne peut s\'en attribuer l\'exercice.\n' +
          '\n' +
          'Le suffrage peut être direct ou indirect dans les conditions prévues par la Constitution. Il est toujours universel, égal et secret.\n' +
          '\n' +
          'Sont électeurs, dans les conditions déterminées par la loi, tous les nationaux français majeurs des deux sexes, jouissant de leurs droits civils et politiques.\n' +
          '\n' +
          'ARTICLE 4.\n' +
          'Les partis et groupements politiques concourent à l\'expression du suffrage. Ils se forment et exercent leur activité librement. Ils doivent respecter les principes de la souveraineté nationale et de la démocratie.\n' +
          '\n' +
          'Ils contribuent à la mise en œuvre du principe énoncé au second alinéa de l\'article 1er dans les conditions déterminées par la loi.\n' +
          '\n' +
          'La loi garantit les expressions pluralistes des opinions et la participation équitable des partis et groupements politiques à la vie démocratique de la Nation.\n' +
          '\n' +
          'Titre II - LE PRÉSIDENT DE LA RÉPUBLIQUE\n' +
          'ARTICLE 5.\n' +
          'Le Président de la République veille au respect de la Constitution. Il assure, par son arbitrage, le fonctionnement régulier des pouvoirs publics ainsi que la continuité de l\'État.\n' +
          '\n' +
          'Il est le garant de l\'indépendance nationale, de l\'intégrité du territoire et du respect des traités.\n' +
          '\n' +
          'ARTICLE 6.\n' +
          'Le Président de la République est élu pour cinq ans au suffrage universel direct.\n' +
          '\n' +
          'Nul ne peut exercer plus de deux mandats consécutifs.\n' +
          '\n' +
          'Les modalités d\'application du présent article sont fixées par une loi organique.'
      fetch('http://127.0.0.1:8001/summarize', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: text }),
      })
          .then(response => response.json())
          .then(data => {
            this.loading = false
            this.stopDots()
            this.messages[this.messages.length - 1].text = data.summary
          })
          .catch((error) => {
            this.loading = false
            this.stopDots()
            console.error('Erreur:', error)
          });
    }
  }
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
  display: flex;
  flex-direction: column;
}

.message {
  padding: 10px;
  margin: 5px 0;
  border-radius: 5px;
  word-wrap: break-word;
}

.sent {
  background: #74747430;
  text-align: right;
  align-self: flex-end;
}

.received {
  display: flex;
  width: 100%;
}
.received-text {
  text-align: left
}
.received-container {
  display: flex;
  align-items: center;
  align-self: flex-start;
}
.input-container {
  display: flex;
  gap: 10px;
  align-items: center;
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

.icon {
  width: 30px;
  height: 30px;
  margin-right: 10px;
}

.summarize-button-container:hover {
  background: #74747430;
  border-radius: 5px;
  cursor: pointer;
}
</style>
