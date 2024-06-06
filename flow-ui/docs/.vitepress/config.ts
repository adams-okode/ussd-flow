import { defineConfig } from "vitepress";

// docs/.vitepress/config.js
export default defineConfig({
  base: process.env.VITE_DOCS_BASE_URL,
  title: "USSD Flow",
  description: "A VitePress site for my existing project",
  themeConfig: {
    nav: [
      {
        text: "Get started",
        link: "/guide/ussd-intro",
      },
      {
        text: "Menu Builder",
        link: "https://adams-okode.github.io/ussd-flow/",
      },
    ],
    sidebar: {
      "/guide": [
        {
          text: "USSD",
          items: [{ text: "USSD Intro", link: "/guide/ussd-intro" }],
        },
        {
          text: "Guide",
          items: [
            { text: "Intro to USSD Flow", link: "/guide/ussd-flow" },
            { text: "Fast API", link: "/guide/fast-api" },
            { text: "Django", link: "/guide/django-api" },
            { text: "Flask", link: "/guide/flask-api" },
          ],
        },
        {
          text: "Menus",
          items: [
            {
              text: "Intro to dynamic menus",
              link: "/guide/dynamic-menu-intro",
            },
            { text: "Menu builder", link: "/guide/menu-builder" },
          ],
        },
      ],
    },
  },
});
