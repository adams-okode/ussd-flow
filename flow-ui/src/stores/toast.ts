import { defineStore } from "pinia";
import { Ref, ref } from "vue";

type ToastConfig = {
  toggle: boolean;
  closeDelay: number;
  severity: "info" | "warning" | "error" | "success";
  message: string;
};

export const useToastStore = defineStore("toast", () => {
  const defaultConfig: ToastConfig = {
    toggle: false,
    closeDelay: 5000,
    severity: "info",
    message: "",
  };

  const config: Ref<ToastConfig> = ref({ ...defaultConfig });

  function hideToast() {
    config.value.toggle = false;
  }

  function showToast(newConfig: Partial<ToastConfig>) {
    console.log(newConfig);
    Object.assign(config.value, {
      ...defaultConfig,
      ...newConfig,
      toggle: true,
    });
    if (config.value.closeDelay > 0) {
      setTimeout(() => {
        hideToast();
        Object.assign(config.value, defaultConfig);
      }, config.value.closeDelay);
    }
  }

  return {
    config,
    hideToast,
    showToast,
  };
});
