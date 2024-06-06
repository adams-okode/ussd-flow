import { createRouter, createWebHashHistory } from "vue-router";

import DesignerPage from "../src/pages/DesignerPage.vue";

const routes = [{ path: "/", component: DesignerPage }];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router;
