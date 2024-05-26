<script setup lang="ts">
import HelloWorld from "./components/HelloWorld.vue";
import MainLayout from "./layout/MainLayout.vue";
import PhoneDialog from "./components/PhoneDialog.vue";
import SideBar from "./components/SideBar.vue";

import { useMenuStore } from "./stores/menu";
import { storeToRefs } from "pinia";

const menuStore = useMenuStore();
const { showMenuSidenav } = storeToRefs(menuStore);
const { showSideMenu } = menuStore;
</script>

<template>
  <button
    v-if="!showMenuSidenav"
    @click="showSideMenu"
    type="button"
    class="fixed right-2 top-20 z-50 text-white bg-green-700 hover:bg-green-800 focus:outline-none focus:ring-4 focus:ring-green-300 font-medium rounded-full text-sm px-5 py-2.5 text-center me-2 mb-2 dark:bg-green-600 dark:hover:bg-green-700 dark:focus:ring-green-800"
  >
    Preview Menu
  </button>

  <phone-dialog></phone-dialog>
  <main-layout>
    <template #flow>
      <hello-world></hello-world>
    </template>

    <template #side-bar>
      <side-bar></side-bar>
    </template>
  </main-layout>
</template>

<style scoped></style>
