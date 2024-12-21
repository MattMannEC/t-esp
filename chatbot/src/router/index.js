import { createRouter, createWebHistory } from 'vue-router';
import ChatbotView from "@/views/ChatbotView.vue";
import ArticleView from "@/views/ArticleView.vue";

const routes = [
    { path: '/chat', name: 'chatbot', component: ChatbotView },
    { path: '/article', name: 'article', component: ArticleView }
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
