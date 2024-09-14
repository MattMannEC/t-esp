import { defineStore } from "pinia";

export const useLocalStorageStore = defineStore('messageStore', {
    state: () => ({
        chats: [],
    }),
    actions: {
       onLoad () {
              const chats = localStorage.getItem('chats');
              if (chats) {
                this.chats = JSON.parse(chats);
              }
       }
    },
});
