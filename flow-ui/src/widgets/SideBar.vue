<template>
  <!-- drawer component -->
  <div v-if="previewSideNavToggle">
    <aside
      id="logo-sidebar"
      class="fixed left-0 z-40 resizable shadow-md bg-white border-r border-gray-200 sm:translate-x-0 dark:bg-gray-800 dark:border-gray-700"
      aria-label="Sidebar"
      :style="{
        width: width + 'px',
        height: 'calc(100vh - 70px)',
        top: '70px',
        overflowY: 'scroll',
      }"
      ref="resizableBox"
    >
      <slot name="content">
        <div
          class="block w-full p-6 bg-white border border-gray-200 rounded-lg shadow hover:bg-gray-100 dark:bg-gray-800 dark:border-gray-700 dark:hover:bg-gray-700"
        >
          <h5
            class="text-2xl font-bold tracking-tight text-gray-900 dark:text-white"
          >
            Noteworthy technology acquisitions 2021
          </h5>
          <p class="font-normal text-gray-700 dark:text-gray-400">
            Here are the biggest enterprise technology acquisitions of 2021 so
            far, in reverse chronological order.
          </p>
        </div>

        <div>
          <pre ref="codeBlock" class="language-json h-full">
              {{ formattedMenu }}
            </pre
          >
          <div class="handle shadow-sm" @mousedown="startResize"></div>
        </div>
      </slot>
    </aside>

    <button
      type="button"
      class="fixed top-20 z-50 text-red-700 border border-red-700 hover:bg-red-700 hover:text-white focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-full text-sm p-2.5 text-center inline-flex items-center dark:border-blue-500 dark:text-blue-500 dark:hover:text-white dark:focus:ring-blue-800 dark:hover:bg-blue-500"
      :style="{ left: `${width + 10}px` }"
      @click="hidePreviewSideNav"
    >
      <svg
        class="w-4 h-4"
        aria-hidden="true"
        xmlns="http://www.w3.org/2000/svg"
        fill="currentColor"
        viewBox="0 0 18 18"
      >
        <path
          d="M3 7H1a1 1 0 0 0-1 1v8a2 2 0 0 0 4 0V8a1 1 0 0 0-1-1Zm12.954 0H12l1.558-4.5a1.778 1.778 0 0 0-3.331-1.06A24.859 24.859 0 0 1 6 6.8v9.586h.114C8.223 16.969 11.015 18 13.6 18c1.4 0 1.592-.526 1.88-1.317l2.354-7A2 2 0 0 0 15.954 7Z"
        />
      </svg>
      <span class="sr-only">Icon description</span>
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted, onBeforeUnmount, Ref } from "vue";
import { useMenuStore } from "../stores/menu";
import { storeToRefs } from "pinia";
import Prism from "prismjs";

const menuStore = useMenuStore();
const { mainMenu, previewSideNavToggle } = storeToRefs(menuStore);
const { hidePreviewSideNav } = menuStore;

const codeBlock = ref<HTMLElement | null>(null);
const formattedMenu = ref("");

const width = ref(1000); // Initial width of the resizable div
const isResizing = ref(false);
const resizableBox: Ref<any> = ref(null);

const startResize = (event: any) => {
  isResizing.value = true;
  document.addEventListener("mousemove", resize);
  document.addEventListener("mouseup", stopResize);
};

const resize = (event: any) => {
  if (isResizing.value) {
    width.value = event.clientX - resizableBox.value?.offsetLeft;
  }
};

const stopResize = () => {
  isResizing.value = false;
  document.removeEventListener("mousemove", resize);
  document.removeEventListener("mouseup", stopResize);
};

function highlightCode() {
  if (codeBlock.value) {
    Prism.highlightElement(codeBlock.value);
  }
}

// watch(
//   mainMenu,
//   (newMenu) => {
//     formattedMenu.value = JSON.stringify(newMenu, null, "\t"); // Format JSON with indentation
//     highlightCode();
//   },
//   { immediate: true, deep: true }
// );

onMounted(() => {
  highlightCode();
});

onBeforeUnmount(() => {
  document.removeEventListener("mouseup", stopResize);
});
</script>

<style scoped>
.resizable {
  transition: width 0.5s ease;
  overflow: hidden;
}
.handle {
  width: 10px;
  cursor: ew-resize;
  position: absolute;
  right: 0;
  top: 0;
  bottom: 0;
}
</style>
