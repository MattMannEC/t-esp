import './assets/main.css'
import App from './App.vue'
import router from './router/index.js'
import {FontAwesomeIcon} from "./plugin/font-awesome.js"



import { createApp } from 'vue'
import { createPinia } from 'pinia'

createApp(App).component('FontAwesomeIcon', FontAwesomeIcon).use(createPinia()).use(router).mount('#app')
