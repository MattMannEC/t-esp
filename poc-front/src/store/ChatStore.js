import { defineStore } from "pinia";

export const useChatStore = defineStore('messageStore', {
    state: () => ({
        messages: [],
        currentId: 0
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

                const data = await response.json();

                this.messages.push({
                    id: this.currentId++,
                    content: data.response,
                    sender: 'bot'
                });
                console.log('data', data.response);
            } catch (e) {
                console.error("Erreur lors de l'envoi du message :", e);
            }
        },
    },
});
