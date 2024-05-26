<template>
  <div
    tabindex="-1"
    aria-hidden="true"
    v-show="show"
    class="overflow-y-auto overflow-x-hidden fixed top-0 right-auto left-auto z-50 flex justify-center items-center w-full md:inset-0 h-[calc(100%-1rem)] max-h-full bg-gray-700 bg-opacity-50"
  >
    <div class="relative mx-auto p-4 w-full max-w-4xl max-h-full">
      <!-- Modal content -->
      <div class="relative bg-white rounded-lg shadow dark:bg-gray-700">
        <!-- Modal header -->
        <div
          class="flex items-center justify-between p-4 md:p-5 border-b rounded-t dark:border-gray-600"
        >
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
            Connect wallet
          </h3>
          <button
            type="button"
            class="text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm h-8 w-8 ms-auto inline-flex justify-center items-center dark:hover:bg-gray-600 dark:hover:text-white"
            @click="toggle"
          >
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
            <span class="sr-only">Close modal</span>
          </button>
        </div>
        <!-- Modal body -->
        <div class="p-4 overflow-y-scroll max-h-[800px] md:p-5">
          <!-- <phone-dialer /> -->
          <menu-level-form v-model="metadata" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// import PhoneDialer from "./PhoneDialer.vue";
import MenuLevelForm from "../forms/MenuLevelForm.vue";
import { useDialogStore } from "../stores/phone-dialog";
import { storeToRefs } from "pinia";

const dialogStore = useDialogStore();
const { show, metadata } = storeToRefs(dialogStore);
const { toggle } = dialogStore;
</script>

<style scoped></style>
