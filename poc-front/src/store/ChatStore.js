import { defineStore } from "pinia";

export const useChatStore = defineStore('messageStore', {
    state: () => ({
        messages: [],
        currentId: 0,
        isStreaming: false
    }),

    actions: {
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

                this.isStreaming = true;
                const reader = response.body.getReader();
                const decoder = new TextDecoder();
                let result = "";

                const botID = this.currentId;


                while (true) {
                    const { done, value } = await reader.read();
                    if (done) {
                        this.isStreaming = false;
                        break;
                    }
                    result += decoder.decode(value, { stream: true });

                    this.updateBotMessage(result, botID);
                }

            } catch (e) {
                console.error("Erreur lors de l'envoi du message :", e);
            }
        },

        updateBotMessage(content, id) {
            const botMessage = this.messages.find(message => message.id === id);
            if (botMessage) {
                botMessage.content = content;
            } else {
                this.messages.push({
                    id: this.currentId++,
                    content: content,
                    sender: 'bot'
                });
            }
        }
    },
});
