import { defineStore } from 'pinia';

export const useChatStore = defineStore('chat', {
    state: () => ({
        chats: [],
    }),
    getters: {
        getChats: (state) => state.chats || [],
        getChatById: (state) => {
            return (id) => state.chats.find((chat) => chat.id === id) || null;
        },
    },
    actions: {
        updateChat(data) {
            const chat = this.getChatById(data.id);
            if (!chat) {
                this.chats.push({
                    id: data.id,
                    messages: data.messages || [],
                });
            } else {
                if (data.messages && data.messages.length > 0) {
                    chat.messages.push(...data.messages);
                }
            }
        },
        async summarize(id, articles) {
            let chat = this.getChatById(id);

            if (!chat) {
                chat = { id, messages: [] };
                this.chats.push(chat);
            }

            const text = articles
                .map((article) => `${article.title}\n${article.text}`)
                .join('\n');

            try {
                const response = await fetch('http://127.0.0.1:8001/summarize', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text }),
                });

                if (!response.ok) {
                    throw new Error(`Erreur API: ${response.status}`);
                }

                const result = await response.json();

                const botMessage = {
                    sender: 'bot',
                    text: result.summary,
                };

                this.updateChat({
                    id,
                    messages: [botMessage],
                });
            } catch (error) {
                console.error('Erreur lors de l’appel à l’API de résumé :', error);
            }
        },
    },
});
