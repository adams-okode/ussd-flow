<template>
  <div
    ref="content"
    contenteditable="true"
    class="mt-1 min-h-12 p-4 block w-full border border-gray-300 dark:bg-slate-600 dark:text-gray-200 dark:border-slate-500 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
    @input="onInput"
  >
    <div
      class="min-h-3 mb-2"
      style="white-space: pre-wrap"
      v-html="parsedModelValue"
    ></div>
  </div>
</template>

<script setup lang="ts">
import { PropType, ref, computed } from "vue";
import { MenuOption } from "../types/ussd";
import { onMounted } from "vue";

const content = ref<HTMLDivElement | null>(null);

const props = defineProps({
  modelValue: {
    type: String,
    required: true,
  },
  options: {
    type: Array as PropType<MenuOption[]>,
  },
});

const emit = defineEmits(["update:modelValue"]);

const parseModelValue = (value: string) => {
  return value.replace(
    /(\d+)\. ([^\n]+)/g,
    '<span class="option">$1. $2</span>'
  );
};

const parsedModelValue = computed(() => parseModelValue(props.modelValue));

const onInput = () => {
  try {
    if (content.value) {
      emit("update:modelValue", content.value.innerHTML);
    }
  } catch (error) {
    console.error("Error in onInput:", error);
  }
};

onMounted(() => {
  console.log(props.modelValue);
});
</script>

<style scoped>
.option {
  background-color: yellow; /* Just for visual distinction */
}
</style>
