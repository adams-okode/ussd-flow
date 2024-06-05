<script setup lang="ts">
import { mdiAdjust } from "@mdi/js";
import { Handle, Position } from "@vue-flow/core";
import { toRef } from "vue";
import { storeToRefs } from "pinia";

// @ts-ignore:next-line
import { NodeToolbar } from "@vue-flow/node-toolbar";
import { mdiPlus, mdiTrashCan, mdiPencil } from "@mdi/js";

// @ts-ignore:next-line
import SvgIcon from "@jamescoyle/vue-icon";

import { useMenuStore } from "../stores/menu";
import "flowbite";

const props = defineProps([
  "data",
  "connectable",
  "data",
  "dimensions",
  "dragHandle",
  "dragging",
  "events",
  "id",
  "isValidSourcePos",
  "isValidTargetPos",
  "label",
  "parent",
  "parentNodeId",
  "position",
  "resizing",
  "selected",
  "sourcePosition",
  "targetPosition",
  "type",
  "zIndex",
  "toolbarVisible",
]);

const menuStore = useMenuStore();
const { mainMenu } = storeToRefs(menuStore);
const { showSideMenu, setSelectedMenuLevel, addNewMenuItem, removeMenuLevel } =
  menuStore;

const data = toRef(props);

function newMenu() {
  setSelectedMenuLevel(data.value.data.id);
  const mewMenu = addNewMenuItem();
  setSelectedMenuLevel(mewMenu.id);
  showSideMenu();
}

function edit() {
  showSideMenu();
  setSelectedMenuLevel(data.value.data.id);
}

function remove() {
  removeMenuLevel(data.value.data.id);
}
</script>

<template>
  <div class="relative">
    <div class="process-node">
      <div class="preformatted">{{ mainMenu[data.id]?.text }}</div>
      <Handle type="target" :position="Position.Left">
        <span>
          <svg-icon type="mdi" :path="mdiAdjust" size="10"></svg-icon>
        </span>
      </Handle>
      <Handle type="source" :position="Position.Right">
        <span>
          <svg-icon type="mdi" :path="mdiAdjust" size="10"></svg-icon>
        </span>
      </Handle>
    </div>

    <NodeToolbar
      style="display: flex; gap: 0.5rem; align-items: center"
      :is-visible="data?.toolbarVisible"
      :position="Position.Right"
    >
      <div
        class="max-w-md bg-white border border-gray-200 rounded-lg shadow dark:bg-gray-800 dark:border-gray-700"
      >
        <ul
          class="py-1 text-sm text-gray-700 dark:text-gray-200"
          aria-labelledby="dropdownMenuIconHorizontalButton"
        >
          <li>
            <a
              @click="edit()"
              class="relative cursor-pointer inline-flex items-center w-full px-4 py-2 text-sm font-medium hover:bg-gray-100 hover:text-blue-700 focus:z-10 focus:ring-2 focus:ring-blue-700 focus:text-blue-700 dark:border-gray-600 dark:hover:bg-gray-600 dark:hover:text-white dark:focus:ring-gray-500 dark:focus:text-white"
            >
              <svg-icon :path="mdiPencil" type="mdi"></svg-icon>
              Edit
            </a>
          </li>
          <li>
            <a
              @click="newMenu()"
              class="relative cursor-pointer inline-flex border-b border-gray-200 items-center w-full px-4 py-2 text-sm font-medium hover:bg-gray-100 hover:text-blue-700 focus:z-10 focus:ring-2 focus:ring-blue-700 focus:text-blue-700 dark:border-gray-600 dark:hover:bg-gray-600 dark:hover:text-white dark:focus:ring-gray-500 dark:focus:text-white"
            >
              <svg-icon :path="mdiPlus" type="mdi"></svg-icon>
              New Menu item
            </a>
          </li>
          <li>
            <a
              @click="remove()"
              class="relative cursor-pointer inline-flex items-center w-full px-4 py-2 text-sm font-medium hover:bg-gray-100 hover:text-blue-700 focus:z-10 focus:ring-2 focus:ring-blue-700 focus:text-blue-700 dark:border-gray-600 dark:hover:bg-gray-600 dark:hover:text-white dark:focus:ring-gray-500 dark:focus:text-white"
            >
              <svg-icon :path="mdiTrashCan" type="mdi"></svg-icon> Remove</a
            >
          </li>
        </ul>
      </div>
    </NodeToolbar>
  </div>
</template>

<style scoped>
.process-node {
  border-radius: 99px;
  width: auto;
  height: auto;
  display: flex;
  align-items: center;
  justify-content: center;
}

.process-node .vue-flow__handle {
  border: none;
  height: unset;
  width: unset;
  background: transparent;
  font-size: 12px;
}

.preformatted {
  white-space: pre-wrap; /* CSS property to preserve whitespace and new lines */
}

.context-menu {
  position: absolute;
  z-index: 1000;
  width: 200px;
  background-color: white;
  border: 1px solid #ccc;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}
</style>
