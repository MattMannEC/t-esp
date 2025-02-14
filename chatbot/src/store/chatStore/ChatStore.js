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
                    messages: [data.message],
                });
            } else {
                const lastMessage = chat.messages[chat.messages.length - 1]
                if (lastMessage?.loading) {
                    chat.messages[chat.messages.length - 1] = {
                        ...data.message,
                        loading: undefined,
                    }
                } else {
                    chat.messages.push(data.message)
                }
            }
        },
        async summarize(id, articles) {
            this.loading(id)
            const text = articles
                .map((article) => `${article.title}\n${article.text}`)
                .join('\n')
            try {
                const response = await fetch('http://127.0.0.1:8001/summarize', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text }),
                });
                if (!response.ok) {
                    throw new Error(`Erreur API: ${response.status}`);
                }
                const result = await response.json()
                const messageBot = {
                    sender: 'bot',
                    text: result.summary,
                };
                this.updateChat({
                    id,
                    message: messageBot,
                });
            } catch (error) {
                console.error('Erreur lors du résumé :', error);
                this.updateChat({
                    id,
                    message: {
                        sender: 'bot',
                        text: error,
                    }
                })
            }
        },
        async send (id, data) {
            this.loading(id)
            const text = data.text
            try {
                const response = await fetch(`http://127.0.0.1:8001/simulate_llm?prompt=${encodeURIComponent(text)}`)
                const result = response.json
                console.log(result)
            } catch (error) {
                console.log(error)
            }
        },
        loading (id) {
            const loadingMessage = {
                sender: 'bot',
                text: 'Résumé en cours.',
                loading: true
            }
            let chat = this.getChatById(id) || {id, messages: [loadingMessage]}
            if (!chat || chat.length === 0) {
                this.chats.push(chat)
            }
            else {
                this.updateChat({id, message: loadingMessage})
            }
        }
    },
});
