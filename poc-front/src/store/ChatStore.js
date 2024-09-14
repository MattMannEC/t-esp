import { defineStore } from "pinia";

export const useChatStore = defineStore('messageStore', {
    state: () => ({
        messages: [],
        currentId: 0,
        isStreaming: false,
        idChat: 0,
    }),

    getters: {
        getMessages() {
            return this.messages;
        },
        getIsStreaming() {
            return this.isStreaming;
        }
    },

    actions: {
        init() {
            if (localStorage.getItem('chat')) {
                const savedChat = JSON.parse(localStorage.getItem('chat'));
                this.idChat = savedChat.id;
                this.messages = savedChat.messages;
                this.currentId = this.messages[this.messages.length - 1].id + 1;
            } else {
                localStorage.setItem('chat', JSON.stringify({ id: this.idChat, messages: this.messages }));
            }
        },

        async sendMessage(message) {
            try {
                this.messages.push({
                    id: this.currentId++,
                    content: message,
                    sender: 'user'
                });

                const response = await fetch('http://localhost:9000/chat/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ message })
                });

                if (!response.ok) {
                    throw new Error(`Erreur HTTP : ${response.status}`);
                }

                const botMessageId = this.currentId++;
                this.messages.push({
                    id: botMessageId,
                    content: '',
                    sender: 'bot'
                });

                this.isStreaming = true;
                const reader = response.body.getReader();
                const decoder = new TextDecoder();
                let result = "";

                while (true) {
                    const { done, value } = await reader.read();
                    if (done) {
                        this.isStreaming = false;
                        break;
                    }

                    result += decoder.decode(value, { stream: true });

                    this.updateBotMessage(result, botMessageId);
                }

                localStorage.setItem('chat', JSON.stringify({ id: this.idChat, messages: this.messages }));

            } catch (e) {
                console.error("Erreur lors de l'envoi du message :", e);
            }
        },

        updateBotMessage(content, id) {
            const botMessage = this.messages.find(message => message.id === id);
            if (botMessage) {
                botMessage.content = content;
            }
        }
    },
});
