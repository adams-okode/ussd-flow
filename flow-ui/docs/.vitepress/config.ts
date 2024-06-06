import { defineConfig } from "vitepress";

// docs/.vitepress/config.js
export default defineConfig({
  base: process.env.VITE_DOCS_BASE_URL,
  title: "My Project Documentation",
  description: "A VitePress site for my existing project",
  themeConfig: {
    nav: [{ text: "Guide", link: "/guide/getting-started" }],
    sidebar: {
      "/guide/": [
        {
          text: "Guide",
          items: [{ text: "Fast API", link: "/guide/fast-api" }],
        },
      ],
    },
  },
});
