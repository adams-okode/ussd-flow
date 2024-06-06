import { createApp } from "vue";
import { createPinia } from "pinia";
import "./style.scss";
import App from "./App.vue";
import Vueform from "@vueform/vueform";
import vueformConfig from "../vueform.config";
import Prism from "prismjs";
// import "prismjs/themes/prism.css";
import "prismjs/themes/prism-okaidia.min.css";

import router from "./router";

const pinia = createPinia();
const app = createApp(App);

app.use(router);
app.use(pinia);
app.use(Vueform, vueformConfig);
app.config.globalProperties.$prism = Prism; // Register Prism globally
app.mount("#app");
