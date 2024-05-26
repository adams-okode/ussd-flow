<script setup lang="ts">
import { onMounted, ref } from "vue";
import {
  initAccordions,
  initCarousels,
  initCollapses,
  initDials,
  initDismisses,
  initDrawers,
  initDropdowns,
  initModals,
  initPopovers,
  initTabs,
  initTooltips,
} from "flowbite";
import SvgIcon from "@jamescoyle/vue-icon";
import { mdiMoonWaxingCrescent, mdiWeatherSunny } from "@mdi/js";

const isDarkMode = ref(false);
const themeToggleBtn = ref<HTMLButtonElement | null>(null);

const toggleTheme = () => {
  isDarkMode.value = !isDarkMode.value;
  if (isDarkMode.value) {
    document.documentElement.classList.add("dark");
    localStorage.setItem("color-theme", "dark");
  } else {
    document.documentElement.classList.remove("dark");
    localStorage.setItem("color-theme", "light");
  }
};
// initialize components based on data attribute selectors
onMounted(() => {
  initAccordions();
  initCarousels();
  initCollapses();
  initDials();
  initDismisses();
  initDrawers();
  initDropdowns();
  initModals();
  initPopovers();
  initTabs();
  initTooltips();

  const savedTheme = localStorage.getItem("color-theme");
  if (
    savedTheme === "dark" ||
    (!savedTheme && window.matchMedia("(prefers-color-scheme: dark)").matches)
  ) {
    isDarkMode.value = true;
    document.documentElement.classList.add("dark");
  }
});
</script>

<template>
  <div>
    <nav
      class="fixed z-50 top-0 w-full bg-white border-b border-gray-200 dark:bg-gray-800 dark:border-gray-700"
    >
      <div class="px-3 py-3 lg:px-5 lg:pl-3">
        <div
          class="flex flex-wrap justify-between items-center mx-auto max-w-screen-xl"
        >
          <a href="https://flowbite.com" class="flex items-center">
            <img
              src="https://flowbite.com/docs/images/logo.svg"
              class="mr-3 h-6 sm:h-9"
              alt="Flowbite Logo"
            />
            <span
              class="self-center text-xl font-semibold whitespace-nowrap dark:text-white"
              >Flowbite</span
            >
          </a>
          <div class="flex items-center lg:order-2">
            <a
              href="#"
              class="text-gray-800 dark:text-white hover:bg-gray-50 focus:ring-4 focus:ring-gray-300 font-medium rounded-lg text-sm px-4 lg:px-5 py-2 lg:py-2.5 mr-2 dark:hover:bg-gray-700 focus:outline-none dark:focus:ring-gray-800"
              >Docs</a
            >
            <a
              href="#"
              class="text-gray-800 dark:text-white hover:bg-gray-50 focus:ring-4 focus:ring-gray-300 font-medium rounded-lg text-sm px-4 lg:px-5 py-2 lg:py-2.5 mr-2 dark:hover:bg-gray-700 focus:outline-none dark:focus:ring-gray-800"
              >Get started</a
            >

            <button
              ref="themeToggleBtn"
              class="text-gray-800 dark:text-white hover:bg-gray-50 focus:ring-4 focus:ring-gray-300 font-medium rounded-lg text-sm px-4 lg:px-5 py-2 lg:py-2.5 mr-2 dark:hover:bg-gray-700 focus:outline-none dark:focus:ring-gray-800"
              @click="toggleTheme"
            >
              <svg-icon
                v-show="isDarkMode"
                type="mdi"
                :path="mdiWeatherSunny"
              ></svg-icon>

              <svg-icon
                v-show="!isDarkMode"
                type="mdi"
                :path="mdiMoonWaxingCrescent"
              ></svg-icon>
            </button>
          </div>
        </div>
      </div>
    </nav>

    <slot name="side-bar"> </slot>

    <main>
      <slot name="flow">
        <!-- Main modal -->
      </slot>
    </main>
  </div>
</template>

<style scoped></style>
