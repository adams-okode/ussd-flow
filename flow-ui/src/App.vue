<script setup lang="ts">
import HelloWorld from "./widgets/HelloWorld.vue";
import MainLayout from "./layout/MainLayout.vue";
import PhoneDialog from "./widgets/PhoneDialog.vue";
import SideBar from "./widgets/SideBar.vue";

import { mdiPlus, mdiEyeOutline, mdiDownloadBoxOutline } from "@mdi/js";
import SvgIcon from "@jamescoyle/vue-icon";

import { useMenuStore } from "./stores/menu";
import { storeToRefs } from "pinia";

const menuStore = useMenuStore();
const { previewSideNavToggle } = storeToRefs(menuStore);
const { showSideMenu, showPreviewSideNav, setSelectedMenuLevel, exportToJson } =
  menuStore;

function createMenuDialog() {
  showSideMenu();
  setSelectedMenuLevel(null);
}
</script>

<template>
  <div class="fixed right-3 top-20 z-50 block max-w-2xl rounded-lg">
    <button
      data-tooltip-target="tooltip-default"
      data-tooltip-placement="bottom"
      @click="createMenuDialog"
      class="text-white bg-[#24292F] hover:bg-[#24292F]/90 focus:ring-4 focus:outline-none focus:ring-[#24292F]/50 font-medium rounded-lg text-sm px-3 py-2.5 text-center inline-flex items-center dark:focus:ring-gray-500 dark:hover:bg-[#050708]/30 me-2 mb-2"
    >
      <svg-icon type="mdi" :path="mdiPlus" size="20"></svg-icon>
    </button>

    <div
      id="tooltip-default"
      role="tooltip"
      class="absolute z-10 invisible inline-block px-3 py-2 text-sm font-medium text-white transition-opacity duration-300 bg-gray-900 rounded-lg shadow-sm opacity-0 tooltip dark:bg-gray-700"
    >
      Create a new menu Item
      <div class="tooltip-arrow" data-popper-arrow></div>
    </div>

    <button
      v-if="!previewSideNavToggle"
      data-tooltip-target="tooltip-preview-button"
      data-tooltip-placement="bottom"
      @click="showPreviewSideNav"
      class="text-white bg-[#24292F] hover:bg-[#24292F]/90 focus:ring-4 focus:outline-none focus:ring-[#24292F]/50 font-medium rounded-lg text-sm px-3 py-2.5 text-center inline-flex items-center dark:focus:ring-gray-500 dark:hover:bg-[#050708]/30 me-2 mb-2"
    >
      <svg-icon type="mdi" :path="mdiEyeOutline" size="20"></svg-icon>
    </button>

    <div
      id="tooltip-preview-button"
      role="tooltip"
      class="absolute z-10 invisible inline-block px-3 py-2 text-sm font-medium text-white transition-opacity duration-300 bg-gray-900 rounded-lg shadow-sm opacity-0 tooltip dark:bg-gray-700"
    >
      Preview Menu
      <div class="tooltip-arrow" data-popper-arrow></div>
    </div>

    <button
      data-tooltip-target="tooltip-download-button"
      data-tooltip-placement="bottom"
      @click="exportToJson()"
      class="text-white bg-[#24292F] hover:bg-[#24292F]/90 focus:ring-4 focus:outline-none focus:ring-[#24292F]/50 font-medium rounded-lg text-sm px-3 py-2.5 text-center inline-flex items-center dark:focus:ring-gray-500 dark:hover:bg-[#050708]/30 me-2 mb-2"
    >
      <svg-icon type="mdi" :path="mdiDownloadBoxOutline" size="20"></svg-icon>
    </button>

    <div
      id="tooltip-download-button"
      role="tooltip"
      class="absolute z-10 invisible inline-block px-3 py-2 text-sm font-medium text-white transition-opacity duration-300 bg-gray-900 rounded-lg shadow-sm opacity-0 tooltip dark:bg-gray-700"
    >
      Download Menu
      <div class="tooltip-arrow" data-popper-arrow></div>
    </div>
  </div>

  <phone-dialog></phone-dialog>
  <main-layout>
    <template #side-bar>
      <side-bar></side-bar>
    </template>

    <template #flow>
      <hello-world></hello-world>
    </template>
  </main-layout>
</template>

<style scoped></style>
