<template>
  <form @submit.prevent="submitForm" class="space-y-6">
    <div class="mb-4">
      <label for="id" class="block text-xl font-medium text-gray-700"
        >Menu ID: {{ localMenuLevel.id }}</label
      >
    </div>

    <div class="mb-4">
      <label for="menuLevel" class="block text-sm font-medium text-gray-700"
        >Menu Level</label
      >
      <input
        type="number"
        id="menuLevel"
        v-model="localMenuLevel.menuLevel"
        required
        class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
      />
      <p class="mt-2 text-sm text-gray-500">
        The depth of the menu in the tree
      </p>
    </div>

    <div class="mb-4">
      <label for="text" class="block text-sm font-medium text-gray-700"
        >Text</label
      >
      <textarea
        id="text"
        v-model="localMenuLevel.text"
        required
        class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
        rows="6"
      ></textarea>
      <p class="mt-2 text-sm text-gray-500">
        The text to be displayed for the menu
      </p>
    </div>

    <div class="mb-4">
      <label for="maxSelections" class="block text-sm font-medium text-gray-700"
        >Max Selections</label
      >
      <input
        type="number"
        id="maxSelections"
        v-model="localMenuLevel.maxSelections"
        required
        class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
      />
      <p class="mt-2 text-sm text-gray-500">
        The max no of selections on the menu
      </p>
    </div>

    <div class="border border-gray-200 w-full mb-4"></div>

    <div class="mb-4">
      <label class="block text-sm font-medium text-gray-700"
        >Menu Options</label
      >
      <div
        v-for="(option, index) in localMenuLevel.menuOptions"
        :key="index"
        class="mt-2 border p-4 rounded-md relative"
      >
        <div class="absolute top-2 right-2">
          <button
            type="button"
            @click="removeMenuOption(index)"
            class="text-red-500 hover:text-red-700"
          >
            <svg
              class="w-6 h-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M6 18L18 6M6 6l12 12"
              ></path>
            </svg>
          </button>
        </div>
        <div class="mb-4">
          <label for="type" class="block text-sm font-medium text-gray-700"
            >Option Type</label
          >
          <select
            v-model="option.type"
            required
            class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
          >
            <option value="response">Response</option>
            <option value="action">Action</option>
          </select>
        </div>

        <div class="mb-4">
          <label for="response" class="block text-sm font-medium text-gray-700"
            >Response</label
          >
          <textarea
            v-model="option.response"
            class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
          ></textarea>
        </div>

        <div class="mb-4">
          <CustomSelect
            :id="'nextMenuLevel' + index"
            v-model="option.nextMenuLevel"
            :items="menusList"
            label="Next Menu Level"
            label-prop="text"
            value-prop="id"
          />
        </div>

        <div v-if="option.type === 'action'" class="mb-4">
          <label for="action" class="block text-sm font-medium text-gray-700"
            >Action</label
          >
          <input
            v-model="option.action"
            type="text"
            class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
          />
        </div>
      </div>
      <button
        type="button"
        @click="addMenuOption"
        class="mt-4 inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-lg text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
      >
        <svg-icon type="mdi" :path="mdiPlus"></svg-icon>
        Add Menu Option
      </button>
    </div>

    <div>
      <!-- <button
        type="submit"
        class="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
      >
        Save
      </button> -->
    </div>
  </form>
</template>

<script setup lang="ts">
import { Ref, computed, ref } from "vue";
import { MenuLevel, MenuOption } from "../types/ussd";
import { useMenuStore } from "../stores/menu";
import { storeToRefs } from "pinia";

import { mdiPlus } from "@mdi/js";

// @ts-ignore:next-line
import SvgIcon from "@jamescoyle/vue-icon";

import CustomSelect from "../components/CustomSelect.vue";

const menuStore = useMenuStore();
const { mainMenu } = storeToRefs(menuStore);
const { getNextMenuLevelID, setSelectedMenuLevel } = menuStore;

// Define props and emits for v-model
const props = defineProps<{
  modelValue: MenuLevel;
}>();
const emit = defineEmits(["update:modelValue", "submit"]);

const menusList = computed(() => Object.values(mainMenu.value));
const defaultMenuOption = ref<MenuOption>({
  type: "response",
  response: "",
  nextMenuLevel: null,
  action: "",
});

const localMenuLevel: Ref<MenuLevel> = computed({
  get: () => props.modelValue,
  set: (value) => {
    console.log(value);
    if (!value.id) {
      value.id = getNextMenuLevelID();
    }
    setSelectedMenuLevel(value.id);
    emit("update:modelValue", value);
  },
});

function addMenuOption() {
  localMenuLevel.value.menuOptions.push({ ...defaultMenuOption.value });
  emit("update:modelValue", localMenuLevel.value);
}

function removeMenuOption(index: number) {
  localMenuLevel.value.menuOptions.splice(index, 1);
  emit("update:modelValue", localMenuLevel.value);
}

function submitForm() {
  // Here you can add any additional logic you need to handle the form submission
  emit("submit", localMenuLevel.value);
}
</script>
