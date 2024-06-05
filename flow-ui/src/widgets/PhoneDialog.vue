<template>
  <div v-show="showMenuSidenav">
    <side-bar @close="hideSideMenu">
      <template #content>
        <div
          class="relative p-4 md:p-5 h-full dark:bg-slate-800 dark:border-slate-800"
        >
          <div class="absolute right-5 z-50 block max-w-2xl rounded-lg">
            <!-- <button
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
            </div> -->
          </div>

          <div
            class="flex-1 overflow-y-scroll mb-16 p-6 pb-10 dark:bg-slate-800"
            style="height: calc(100vh - 80px)"
          >
            <template v-if="metadata">
              <menu-level-form v-model="metadata" />
            </template>
          </div>
          <div
            class="absolute bottom-0 left-0 w-full p-2 bg-white dark:bg-slate-800 flex justify-center"
          >
            <button
              @click="saveMenuItem"
              type="button"
              class="inline-flex justify-center w-auto text-white bg-green-700 hover:bg-green-800 border border-green-800 focus:outline-none focus:ring-4 focus:ring-green-300 font-medium rounded-xl text-sm px-5 py-2.5 text-center mb-2 dark:border-green-700 dark:bg-slate-600 dark:hover:bg-slate-700 dark:focus:ring-slate-800"
            >
              <svg-icon :path="mdiContentSave" type="mdi" :size="20"></svg-icon>
              Save Item
            </button>
          </div>
        </div>
      </template>
    </side-bar>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import SideBar from "../components/SideBar.vue";
import MenuLevelForm from "../forms/MenuLevelForm.vue";
import { useMenuStore } from "../stores/menu";
import { storeToRefs } from "pinia";
import { MenuLevel } from "../types/ussd";
import { useToastStore } from "../stores/toast";

import { mdiContentSave } from "@mdi/js";

// @ts-ignore:next-line
import SvgIcon from "@jamescoyle/vue-icon";

const toastStore = useToastStore();
const { showToast } = toastStore;
// Example usage

const menuStore = useMenuStore();
const { showMenuSidenav, selectedMenuLevelId, mainMenu } =
  storeToRefs(menuStore);
const { hideSideMenu, getNextMenuLevelID, addNewMenuItem } = menuStore;

const metadata = computed({
  get() {
    if (!selectedMenuLevelId.value) {
      return {
        id: getNextMenuLevelID(),
        menuLevel: 3,
        text: "",
        menuOptions: [],
        maxSelections: 3,
        action: "sample_action_function",
      } as MenuLevel;
    }

    const menuLevel = mainMenu.value[selectedMenuLevelId.value];
    if (!menuLevel) {
      console.error(
        `Menu level with id ${selectedMenuLevelId.value} not found`
      );
      return { id: getNextMenuLevelID() } as MenuLevel;
    }

    return menuLevel;
  },
  set(value) {
    if (!value.id) {
      value.id = getNextMenuLevelID();
    }
    // Update the store or handle the new value appropriately
    return value;
  },
});

function saveMenuItem() {
  addNewMenuItem(metadata.value);
  hideSideMenu();
  showToast({
    toggle: true,
    severity: "success",
    message: `Menu level ${metadata.value.id} saved`,
    closeDelay: 3000,
  });
}
</script>

<style scoped>
/* Ensure the button container has a higher z-index */
.relative > .absolute {
  z-index: 10;
}
</style>
