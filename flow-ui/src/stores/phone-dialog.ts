import { defineStore } from "pinia";
import { ref } from "vue";
import { MenuLevel } from "../types/ussd";

type IPhoneDialog = {
  show: boolean;
  metadata: MenuLevel | null;
};

export const useDialogStore = defineStore("dialog", () => {
  const show = ref<IPhoneDialog["show"]>(false);
  const metadata = ref<IPhoneDialog["metadata"]>(null);

  function toggle() {
    show.value = !show.value;
  }

  function showDialog() {
    show.value = true;
  }

  function hideDialog() {
    show.value = false;
  }

  function setMenuData(menu: MenuLevel) {
    metadata.value = menu;
  }

  return { show, metadata, toggle, showDialog, hideDialog, setMenuData };
});
