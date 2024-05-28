<template>
  <div v-show="showMenuSidenav">
    <side-bar @close="hideSideMenu">
      <template #content>
        <div class="relative p-4 md:p-5">
          <div class="flex flex-row h-full">
            <div class="basis-1/2 h-full overflow-y-auto border-r px-2">
              <pre class="language-json">{{ metadata }}</pre>
            </div>
            <div class="basis-1/2 h-full overflow-y-auto px-2 pb-16">
              <template v-if="metadata">
                <menu-level-form v-model="metadata" />
              </template>
            </div>
          </div>
          <div class="absolute bottom-0 left-0 w-full p-2 bg-white">
            <button
              type="button"
              class="w-full text-white bg-green-700 hover:bg-green-800 focus:outline-none focus:ring-4 focus:ring-green-300 font-medium rounded-full text-sm px-5 py-2.5 text-center mb-2 dark:bg-green-600 dark:hover:bg-green-700 dark:focus:ring-green-800"
            >
              Green
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

const menuStore = useMenuStore();
const { showMenuSidenav, selectedMenuLevelId, mainMenu } =
  storeToRefs(menuStore);
const { hideSideMenu, getNextMenuLevelID } = menuStore;

const metadata = computed({
  get() {
    if (!selectedMenuLevelId.value) {
      return { id: getNextMenuLevelID() } as MenuLevel;
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
    console.log("Setting metadata:", value);
  },
});
</script>

<style lang="scss" scoped>
/* Ensure the button container has a higher z-index */
.relative > .absolute {
  z-index: 10;
}
</style>
