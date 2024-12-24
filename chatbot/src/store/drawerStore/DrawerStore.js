import { defineStore } from 'pinia';

export const useDrawerStore = defineStore('drawer', {
    state: () => ({
        drawer: {},
        showDrawer: false
    }),
    getters: {
        getDrawer: (state) => state.drawer || {},
        getShowDrawer: (state) => state.showDrawer
    },
    actions: {
        openDrawer (name, data) {
            this.drawer = {
                name,
                data
            }
            this.showDrawer = true
        },
        closeDrawer () {
            this.drawer =  null
            this.showDrawer = false
        }
    }
});
