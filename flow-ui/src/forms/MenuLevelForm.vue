<template>
  <Vueform v-model="menuLevel" sync :endpoint="false" @submit="handleSubmit">
    <text-element
      name="id"
      label="Menu Level"
      input-type="number"
      validation="required"
      description="The Generate"
      :readonly="true"
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
          <text-element
            :name="'nextMenuLevel'"
            label="Next Menu Level"
            input-type="number"
          />
          <text-element
            v-if="menuLevel?.menuOptions[index].action == 'action'"
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

  <!-- <pre>
    {{ menuLevel }}
  </pre> -->
</template>

<script setup lang="ts">
import { Ref, computed } from "vue";
import { MenuLevel } from "../types/ussd";
import { useMenuStore } from "../stores/menu";
import { useDialogStore } from "../stores/phone-dialog";

const dialogStore = useDialogStore();
const { hideDialog } = dialogStore;

const menuStore = useMenuStore();
const { getNextMenuLevelID, addNewMenuItem } = menuStore;

// Define props and emits for v-model
const props = defineProps({
  modelValue: {
    type: Object as () => MenuLevel,
    default: () => ({
      id: "",
      menuLevel: "",
      text: "",
      menuOptions: [],
      maxSelections: "",
      action: "",
    }),
  },
});
const emit = defineEmits(["update:modelValue"]);

const menuLevel: Ref<MenuLevel> = computed({
  get: () => {
    console.log(props.modelValue);
    return props.modelValue;
  },
  set: (value) => {
    if (value.id == null) {
      value.id = getNextMenuLevelID();
    }
    emit("update:modelValue", value);
  },
});

function handleSubmit() {
  addNewMenuItem(menuLevel.value);
  hideDialog();
}
</script>

<style scoped></style>
