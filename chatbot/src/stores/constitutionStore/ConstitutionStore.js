import { defineStore } from 'pinia';
import frenchConstitution from '@/assets/data/constitution-1958.json'

export const useConstitutionStore = defineStore('constitution', {
    state: () => ({
        isConstitution: frenchConstitution || [],
    }),
    getters: {
        getConstitution: (state) => state.isConstitution ||  []
    },
});
