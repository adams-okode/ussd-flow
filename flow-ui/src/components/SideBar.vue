<template>
  <!-- drawer component -->
  <aside
    id="logo-sidebar"
    class="fixed left-0 z-40 resizable shadow-md bg-white border-r border-slate-800 sm:translate-x-0 dark:bg-gray-400 dark:border-gray-700"
    aria-label="Sidebar"
    :style="{
      width: width + 'px',
      height: 'calc(100vh - 70px)',
      top: '70px',
      overflowY: 'hidden',
    }"
    ref="resizableBox"
  >
    <slot name="content"> </slot>
    <div class="handle shadow-sm" @mousedown="startResize"></div>
  </aside>

  <button
    type="button"
    class="fixed top-20 z-50 cursor-pointer bg-gray-700 text-gray-100 border border-gray-900 hover:bg-red-700 hover:text-white focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-full text-sm p-2.5 text-center inline-flex items-center dark:border-blue-500 dark:text-blue-500 dark:hover:text-white dark:focus:ring-blue-800 dark:hover:bg-blue-500"
    :style="{ left: `${width + 10}px` }"
    @click="emit('close')"
  >
    <svg-icon type="mdi" :path="mdiClose" size="28"></svg-icon>
  </button>
</template>

<script setup lang="ts">
import { ref, onBeforeUnmount } from "vue";
import { mdiClose } from "@mdi/js";
import SvgIcon from "@jamescoyle/vue-icon";

const emit = defineEmits(["close"]);

const width = ref(1000); // Initial width of the resizable div
const isResizing = ref(false);
const resizableBox = ref(null);

const startResize = (event: Event) => {
  isResizing.value = true;
  document.addEventListener("mousemove", resize);
  document.addEventListener("mouseup", stopResize);
};

const resize = (event) => {
  if (isResizing.value) {
    width.value = event.clientX - resizableBox.value.offsetLeft;
  }
};

const stopResize = () => {
  isResizing.value = false;
  document.removeEventListener("mousemove", resize);
  document.removeEventListener("mouseup", stopResize);
};

onBeforeUnmount(() => {
  document.removeEventListener("mouseup", stopResize);
});
</script>

<style scoped>
.resizable {
  /* transition: width 0.5s ease; */
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
