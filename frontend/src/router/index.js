import { createRouter, createWebHistory } from "vue-router";
import App from "../App.vue"; // ou un composant racine

const routes = [
  { path: "/", component: App }, // une seule page pour l'instant
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
