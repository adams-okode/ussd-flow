<script setup lang="ts">
import { mdiAdjust } from "@mdi/js";
import { Handle, Position } from "@vue-flow/core";
import { toRef } from "vue";

import SvgIcon from "@jamescoyle/vue-icon";
import { useMenuStore } from "../stores/menu";

const props = defineProps([
  "data",
  "connectable",
  "data",
  "dimensions",
  "dragHandle",
  "dragging",
  "events",
  "id",
  "isValidSourcePos",
  "isValidTargetPos",
  "label",
  "parent",
  "parentNodeId",
  "position",
  "resizing",
  "selected",
  "sourcePosition",
  "targetPosition",
  "type",
  "zIndex",
]);

const menuStore = useMenuStore();

const { showSideMenu, setSelectedMenuLevel } = menuStore;

const data = toRef(props);

function openDialog() {
  showSideMenu();
  setSelectedMenuLevel(data.value.data.id);
}
</script>

<template>
  <div class="process-node" @click="openDialog">
    <div class="preformatted">{{ data.label }}</div>
    <Handle type="target" :position="Position.Left">
      <span>
        <svg-icon type="mdi" :path="mdiAdjust" size="10"></svg-icon>
      </span>
    </Handle>
    <Handle type="source" :position="Position.Right">
      <span>
        <svg-icon type="mdi" :path="mdiAdjust" size="10"></svg-icon>
      </span>
    </Handle>
  </div>
</template>

<style scoped>
.process-node {
  border-radius: 99px;
  width: auto;
  height: auto;
  display: flex;
  align-items: center;
  justify-content: center;
}

.process-node .vue-flow__handle {
  border: none;
  height: unset;
  width: unset;
  background: transparent;
  font-size: 12px;
}

.preformatted {
  white-space: pre-wrap; /* CSS property to preserve whitespace and new lines */
}
</style>
