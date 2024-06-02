<template>
  <div v-show="showMenuSidenav">
    <side-bar @close="hideSideMenu">
      <template #content>
        <div class="relative p-4 md:p-5 h-full">
          <div class="flex flex-row h-full">
            <div class="basis-2/3 relative h-full flex flex-col px-2">
              <div class="flex-1 overflow-y-auto mb-16 p-6">
                <template v-if="metadata">
                  <menu-level-form v-model="metadata" />
                </template>
              </div>
              <div class="absolute bottom-0 left-0 w-full p-2 bg-white">
                <button
                  @click="saveMenuItem"
                  type="button"
                  class="w-full text-white bg-green-700 hover:bg-green-800 focus:outline-none focus:ring-4 focus:ring-green-300 font-medium rounded-xl text-sm px-5 py-2.5 text-center mb-2 dark:bg-green-600 dark:hover:bg-green-700 dark:focus:ring-green-800"
                >
                  Save Item
                </button>
              </div>
            </div>

            <div class="basis-1/3 h-full overflow-y-auto border-r px-2">
              <pre class="language-json">{{ metadata }}</pre>
            </div>
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
