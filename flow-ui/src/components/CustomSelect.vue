<!-- src/components/CustomSelect.vue -->
<template>
  <div class="relative cursor-pointer">
    <label :for="id" class="block text-sm font-medium text-gray-700">{{
      label
    }}</label>
    <div class="mt-1 relative">
      <input
        type="text"
        v-model="searchQuery"
        placeholder="Search..."
        @focus="showDropdown = true"
        @blur="hideDropdown"
        class="block w-full py-2 pl-3 pr-10 mt-1 text-base border border-gray-300 rounded-md dark:bg-slate-600 dark:text-gray-200 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
      />
      <span
        class="absolute inset-y-0 right-0 flex items-center pr-3 cursor-pointer pointer-events-none"
      >
        <SvgIcon type="mdi" :path="mdiChevronDown" />
      </span>
      <span
        v-if="modelValue !== null && modelValue !== undefined"
        class="absolute inset-y-0 right-6 flex items-center pr-3 cursor-pointer"
        @click="clearSelection"
      >
        <SvgIcon type="mdi" :path="mdiClose" />
      </span>
      <div v-if="showDropdown" class="relative mt-1">
        <ul
          class="absolute z-10 w-full py-1 mt-1 overflow-auto text-base bg-white border border-gray-300 rounded-md shadow-lg max-h-60 focus:outline-none sm:text-sm dark:bg-slate-600 dark:text-gray-200"
          tabindex="-1"
        >
          <li
            v-for="item in filteredItems"
            :key="item[valueProp]"
            :class="{
              'bg-indigo-600 text-white': item[valueProp] === modelValue,
              'text-gray-900': item[valueProp] !== modelValue,
            }"
            @mousedown.prevent="selectItem(item)"
            class="cursor-pointer select-none relative py-2 pl-3 pr-9 hover:bg-indigo-600 hover:text-indigo-200 dark:text-gray-200"
          >
            <span
              :class="{
                'font-semibold': item[valueProp] === modelValue,
                'font-normal': item[valueProp] !== modelValue,
              }"
              class="preformatted"
            >
              {{ item[labelProp] }}
            </span>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps, defineEmits, ref, computed, watch } from "vue";
import { mdiClose, mdiChevronDown } from "@mdi/js";

// @ts-ignore: next-line
import SvgIcon from "@jamescoyle/vue-icon";

const props = defineProps<{
  id: string;
  modelValue: string | number | null | undefined;
  label: string;
  items: Array<Record<string, any>>;
  labelProp?: string;
  valueProp?: string;
}>();

const emit = defineEmits(["update:modelValue"]);

const searchQuery = ref("");
const showDropdown = ref(false);
const labelProp = props.labelProp || "text";
const valueProp = props.valueProp || "id";

const filteredItems = computed(() => {
  if (!searchQuery.value) {
    return props.items;
  }
  return props.items.filter((item) =>
    item[labelProp].toLowerCase().includes(searchQuery.value.toLowerCase())
  );
});

const selectItem = (item: Record<string, any>) => {
  emit("update:modelValue", item[valueProp]);
  searchQuery.value = item[labelProp];
  showDropdown.value = false;
};

const clearSelection = () => {
  emit("update:modelValue", null);
  searchQuery.value = "";
};

const hideDropdown = () => {
  setTimeout(() => {
    showDropdown.value = false;
  }, 200); // Delay to allow click event to register
};

// Watch for external changes to modelValue to update the search query
watch(
  () => props.modelValue,
  (newVal) => {
    const selectedItem = props.items.find((item) => item[valueProp] === newVal);
    if (selectedItem) {
      searchQuery.value = selectedItem[labelProp];
    } else {
      searchQuery.value = "";
    }
  },
  { immediate: true }
);
</script>

<style scoped>
/* Add any additional custom styling here */
</style>
