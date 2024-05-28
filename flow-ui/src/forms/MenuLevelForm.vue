<template>
  <Vueform
    v-model="localMenuLevel"
    sync
    :endpoint="false"
    @submit="handleSubmit"
  >
    <text-element
      name="id"
      label="Menu ID"
      input-type="number"
      validation="required"
      description="The Generate"
      :disabled="true"
    />

    <text-element
      name="menuLevel"
      label="Menu Level"
      input-type="number"
      validation="required"
      description="The depth of the menu in the tree"
    />

    <textarea-element
      name="text"
      label="Text"
      validation="required"
      description="The text to be displayed for the menu"
    />

    <text-element
      name="maxSelections"
      label="Max Selections"
      input-type="number"
      validation="required"
      description="The max no of selections on the menu"
    />

    <div class="border border-gray-200 w-full"></div>

    <ListElement label="Menu Options" name="menuOptions" view="blocks">
      <template #default="{ index }">
        <ObjectElement :name="index">
          <select-element
            :name="'type'"
            :native="false"
            :items="['response', 'action']"
            label="Option Type"
            validation="required"
          />
          <textarea-element
            :name="'response'"
            label="Response"
            input-type="text"
          />
          <select-element
            :name="'nextMenuLevel'"
            label="Next Menu Level"
            label-prop="text"
            value-prop="id"
            :items="menusList"
            :truncate="true"
            :native="false"
          />
          <text-element
            v-if="localMenuLevel?.menuOptions[index]?.type === 'action'"
            :name="'action'"
            label="Action"
            type="text"
          />
        </ObjectElement>
      </template>
    </ListElement>

    <button-element
      name="register"
      :submits="true"
      :full="true"
      button-label="Add Menu Level"
      size="lg"
    />
  </Vueform>
</template>

<script setup lang="ts">
import { Ref, computed } from "vue";
import { MenuLevel } from "../types/ussd";
import { useMenuStore } from "../stores/menu";
import { useDialogStore } from "../stores/phone-dialog";
import { storeToRefs } from "pinia";

const dialogStore = useDialogStore();
const { hideDialog } = dialogStore;

const menuStore = useMenuStore();
const { mainMenu } = storeToRefs(menuStore);
const { getNextMenuLevelID, addNewMenuItem } = menuStore;

// Define props and emits for v-model
const props = defineProps<{
  modelValue: MenuLevel;
}>();
const emit = defineEmits(["update:modelValue"]);

const menusList = computed(() => Object.values(mainMenu.value));

const localMenuLevel: Ref<MenuLevel> = computed({
  get: () => props.modelValue,
  set: (value) => {
    if (!value.id) {
      value.id = getNextMenuLevelID();
    }
    emit("update:modelValue", value);
  },
});

function handleSubmit() {
  addNewMenuItem(localMenuLevel.value);
  hideDialog();
}
</script>

<style scoped></style>
