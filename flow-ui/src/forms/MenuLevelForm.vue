<template>
  <form @submit.prevent="submitForm" class="space-y-6">
    <div class="mb-4">
      <label
        for="id"
        class="block text-xl font-medium text-gray-700 dark:text-gray-200"
        >Menu ID: {{ localMenuLevel.id }}</label
      >
    </div>

    <div class="mb-4">
      <label
        for="menuLevel"
        class="block text-sm font-medium text-gray-700 dark:text-gray-200"
        >Menu Level</label
      >
      <input
        type="number"
        id="menuLevel"
        v-model="localMenuLevel.menuLevel"
        required
        class="mt-1 block w-full border border-gray-300 dark:bg-slate-600 dark:text-gray-200 dark:border-slate-500 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
      />
      <p class="mt-2 text-sm text-gray-500 dark:text-gray-100">
        The depth of the menu in the tree
      </p>
    </div>

    <div class="mb-4">
      <label
        for="text"
        class="block text-sm font-medium text-gray-700 dark:text-gray-200"
        >Text</label
      >
      <textarea
        id="text"
        v-model="localMenuLevel.text"
        required
        class="mt-1 block w-full border border-gray-300 dark:bg-slate-600 dark:text-gray-200 dark:border-slate-500 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
        rows="6"
      ></textarea>
      <p class="mt-2 text-sm text-gray-500 dark:text-gray-100">
        The text to be displayed for the menu
      </p>
      <div class="flex items-center mt-2">
        <input
          id="conEnd"
          type="checkbox"
          v-model="localMenuLevel.conEnd"
          class="h-4 w-4 text-indigo-600 border-gray-300 dark:border-slate-500 rounded focus:ring-indigo-500"
        />
        <label
          for="conEnd"
          class="ml-2 block text-sm text-gray-900 dark:text-gray-500"
          >CON (Checked) / END (Unchecked)</label
        >
      </div>
    </div>

    <div class="mb-4">
      <label
        for="maxSelections"
        class="block text-sm font-medium text-gray-700 dark:text-gray-200"
        >Max Selections</label
      >
      <input
        type="number"
        id="maxSelections"
        v-model="localMenuLevel.maxSelections"
        required
        class="mt-1 block w-full border border-gray-300 dark:bg-slate-600 dark:text-gray-200 dark:border-slate-500 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
      />
      <p class="mt-2 text-sm text-gray-500 dark:text-gray-100">
        The max no of selections on the menu
      </p>
    </div>

    <div class="border border-gray-200 dark:border-gray-700 w-full mb-4"></div>

    <div class="mb-4">
      <label class="block text-sm font-medium text-gray-700 dark:text-gray-200"
        >Menu Options</label
      >
      <div
        v-for="(option, index) in localMenuLevel.menuOptions"
        :key="index"
        class="mt-2 border border-gray-200 dark:border-gray-700 p-4 rounded-md relative"
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
          <label
            for="type"
            class="block text-sm font-medium text-gray-700 dark:text-gray-200"
            >Option Type</label
          >
          <select
            v-model="option.type"
            required
            class="mt-1 block w-full border border-gray-300 dark:bg-slate-600 dark:text-gray-200 dark:border-slate-500 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
          >
            <option value="response">Response</option>
            <option value="action">Action</option>
          </select>
        </div>

        <div class="mb-4">
          <label
            for="response"
            class="block text-sm font-medium text-gray-700 dark:text-gray-200"
            >Response</label
          >
          <textarea
            v-model="option.response"
            class="mt-1 block w-full border border-gray-300 dark:bg-slate-600 dark:text-gray-200 dark:border-slate-500 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
          ></textarea>
          <div class="flex items-center mt-2">
            <input
              :id="'conEnd' + index"
              type="checkbox"
              v-model="option.conEnd"
              class="h-4 w-4 text-indigo-600 border-gray-300 dark:border-slate-500 rounded focus:ring-indigo-500"
            />
            <label
              :for="'conEnd' + index"
              class="ml-2 block text-sm text-gray-900 dark:text-gray-500"
              >CON (Checked) / END (Unchecked)</label
            >
          </div>
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
          <label
            for="action"
            class="block text-sm font-medium text-gray-700 dark:text-gray-200"
            >Action</label
          >
          <input
            v-model="option.action"
            type="text"
            class="mt-1 block w-full border border-gray-300 dark:bg-slate-600 dark:text-gray-200 dark:border-slate-500 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
          />
        </div>
      </div>
      <button
        type="button"
        @click="addMenuOption"
        class="mt-4 inline-flex justify-center py-1 px-4 border border-transparent shadow-sm text-sm font-medium rounded-lg text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
      >
        <svg-icon type="mdi" :path="mdiPlus" :size="20"></svg-icon>
        Add Menu Option
      </button>
    </div>

    <!-- <div>
      <button
        type="submit"
        class="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
      >
        Save
      </button>
    </div> -->
  </form>
</template>

<script setup lang="ts">
import { Ref, computed, ref, watch } from "vue";
import { MenuLevel, MenuOption } from "../types/ussd";
import { useMenuStore } from "../stores/menu";
import { storeToRefs } from "pinia";
import { mdiPlus } from "@mdi/js";

// @ts-ignore: next-line
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
  conEnd: true,
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

// Watchers to update text and response based on conEnd checkbox
// watch(
//   () => localMenuLevel.value.conEnd,
//   (newValue) => {
//     console.log(newValue);
//     let text = localMenuLevel.value?.text ?? "";

//     // Remove any initial undefined values or extra spaces
//     text = text.replace(/^undefined\s*/, "").trim();

//     const prefix = /^(CON|END)\b/i.test(text) ? "" : newValue ? "CON" : "END";

//     localMenuLevel.value.text = `${prefix} ${text}`.trim();
//   }
// );

function updateOptionConEnd(option: MenuOption) {
  option.response = `${option.conEnd ? "CON" : "END"} ${option.response}`;
}

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
  // Append CON or END based on the checkbox value
  emit("submit", localMenuLevel.value);
}
</script>
