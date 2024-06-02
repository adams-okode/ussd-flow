<template>
  <div>
    <div
      v-if="config.toggle"
      class="fixed z-999 top-5 right-5 flex items-center w-full max-w-xs p-4 space-x-4 text-gray-500 bg-white divide-x rtl:divide-x-reverse divide-gray-200 rounded-lg shadow dark:text-gray-400 dark:divide-gray-700 space-x dark:bg-gray-800"
      role="alert"
    >
      <div class="flex">
        <div
          class="w-8 h-8 rounded-full"
          :class="themeClasses[config.severity]"
          alt="Jese Leos image"
        />

        <div class="ms-3 text-sm font-normal">
          <span
            class="mb-1 text-sm font-semibold text-gray-900 dark:text-white"
            >{{ config.severity }}</span
          >
          <div class="mb-2 text-sm font-normal">
            {{ config.message }}
          </div>
        </div>

        <button
          type="button"
          class="ms-auto -mx-1.5 -my-1.5 bg-white justify-center items-center flex-shrink-0 text-gray-400 hover:text-gray-900 rounded-lg focus:ring-2 focus:ring-gray-300 p-1.5 hover:bg-gray-100 inline-flex h-8 w-8 dark:text-gray-500 dark:hover:text-white dark:bg-gray-800 dark:hover:bg-gray-700"
          @click="hideToast"
        >
          <span class="sr-only">Close</span>
          <svg
            class="w-3 h-3"
            aria-hidden="true"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 14 14"
          >
            <path
              stroke="currentColor"
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6"
            />
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { storeToRefs } from "pinia";
import { useToastStore } from "../stores/toast";
import { Ref, ref } from "vue";

const store = useToastStore();
const { config } = storeToRefs(store);
const { hideToast } = store;

const themeClasses: Ref<any> = ref({
  success: "bg-green-500",
  error: "bg-red-500",
  warning: "fbg-orange-500",
});
</script>

<style scoped>
.icon {
  display: inline-flex;
  align-items: center;
  flex-shrink: 0;
  width: 8px;
  height: 8px;
  border-radius: 50%;
}
</style>
