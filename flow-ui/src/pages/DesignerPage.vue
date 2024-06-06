<script setup lang="ts">
import MenuBuilder from "../widgets/MenuBuilder.vue";

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

const isDarkMode = ref(false);

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
    <main style="height: calc(100vh - 70px)">
      <menu-builder></menu-builder>
    </main>
  </div>
</template>

<style scoped></style>
