/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
    "./node_modules/flowbite/**/*.js",
    "./vueform.config.js",
    "./node_modules/@vueform/vueform/themes/tailwind/**/*.vue",
    "./node_modules/@vueform/vueform/themes/tailwind/**/*.js",
  ],
  theme: {
    extend: {
        zIndex: {
            'on-top': '10000',
          }
    },
  },
  plugins: [require("flowbite/plugin"), require("@vueform/vueform/tailwind")],
  darkMode: "class",
};
