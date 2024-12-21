import { defineStore } from 'pinia';
import frenchConstitution from '@/assets/data/constitution.json'

export const useConstitutionStore = defineStore('constitution', {
    state: () => ({
        isConstitution: frenchConstitution || [],
    }),
    getters: {
        getConstitution: (state) => state.isConstitution ||  []
    },
});
