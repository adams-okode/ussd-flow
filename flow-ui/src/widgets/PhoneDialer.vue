<template>
  <div
    class="flex flex-col items-center justify-center py-6 bg-gray-100 dark:bg-gray-900 rounded-lg"
  >
    <p
      v-if="metadata?.text != undefined"
      class="text-xl font-normal bg-gray-100 dark:bg-gray-900 text-gray-500 dark:text-gray-400 rounded-lg px-6 my-2"
      style="white-space: pre-wrap"
    >
      {{ textTransformer(metadata?.text) }}
    </p>
    <div class="mb-4">
      <input
        type="text"
        v-model="phoneNumber"
        class="w-64 p-2 text-lg text-center border-0 focus:border-0 active:border-0 text-gray-500 dark:text-gray-400 bg-gray-100 dark:bg-gray-900 rounded-lg"
        placeholder="Enter number"
        readonly
      />
    </div>
    <div class="grid grid-cols-3 gap-4 mb-4">
      <button
        v-for="num in numbers"
        :key="num"
        @click="addNumber(num)"
        class="p-4 text-xl bg-white border rounded-lg shadow"
      >
        {{ num }}
      </button>
      <button
        @click="addNumber('*')"
        class="p-4 text-xl bg-white border rounded-lg shadow"
      >
        *
      </button>
      <button
        @click="addNumber('0')"
        class="p-4 text-xl bg-white border rounded-lg shadow"
      >
        0
      </button>
      <button
        @click="addNumber('#')"
        class="p-4 text-xl bg-white border rounded-lg shadow"
      >
        #
      </button>
    </div>
    <button
      @click="callNumber"
      class="px-8 py-2 text-white bg-green-500 rounded-lg"
    >
      Call
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";

import { useDialogStore } from "../stores/phone-dialog";
import { storeToRefs } from "pinia";

const dialogStore = useDialogStore();
const { metadata } = storeToRefs(dialogStore);

const phoneNumber = ref("");
const numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9];

const addNumber = (num: number | string) => {
  phoneNumber.value += num;
};

const callNumber = () => {
  alert(`Calling ${phoneNumber.value}`);
  phoneNumber.value = "";
};

function textTransformer(text: string) {
  const regex = /^(?<notifier>CON|END)(\s+)?/gim;
  const match = regex.exec(text);
  if (match) {
    return text.replace(regex, "");
  }
  return null;
}
</script>

<style scoped>
button {
  transition: background-color 0.3s;
}
button:hover {
  background-color: #e2e8f0;
}
</style>
