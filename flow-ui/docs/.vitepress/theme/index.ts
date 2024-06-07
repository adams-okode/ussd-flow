import DefaultTheme from "vitepress/theme";
import HomeDoc from "../../../src/components/HomeDoc.vue";

import { createPinia } from "pinia";

const pinia = createPinia();

export default {
  ...DefaultTheme,
  enhanceApp({ app }) {
    app.component("HomeDoc", HomeDoc);

    app.use(pinia);
  },
};
