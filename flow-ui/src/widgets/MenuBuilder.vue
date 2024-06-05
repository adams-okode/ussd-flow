<script setup lang="ts">
import { ref, onMounted, Ref, watch } from "vue";

import { PanelPosition, VueFlow, useVueFlow } from "@vue-flow/core";
import { Background } from "@vue-flow/background";
import { ControlButton, Controls } from "@vue-flow/controls";

import Icon from "./Icon.vue";
import CustomNode from "./CustomNode.vue";
import { Edge, Node } from "@vue-flow/core";

import { useMenuStore } from "../stores/menu";
import { storeToRefs } from "pinia";

const menuStore = useMenuStore();
const { menuGraph, mainMenu } = storeToRefs(menuStore);
const { generateGraph, setMenuGraph } = menuStore;

/**
 * useVueFlow provides all event handlers and store properties
 * You can pass the composable an object that has the same properties as the VueFlow component props
 */
const {
  onPaneReady,
  onNodeDragStop,
  onConnect,
  addNodes,
  addEdges,
  project,
  setViewport,
  toObject,
} = useVueFlow();

const nodes: Ref<Node[]> = ref(menuGraph.value.nodes);

const edges: Ref<Edge[]> = ref(menuGraph.value.edges);

// our dark mode toggle flag
const dark = ref(false);

/**
 * This is a Vue Flow event-hook which can be listened to from anywhere you call the composable, instead of only on the main component
 * Any event that is available as `@event-name` on the VueFlow component is also available as `onEventName` on the composable and vice versa
 *
 * onPaneReady is called when viewpane & nodes have visible dimensions
 */
onPaneReady(({ fitView }) => {
  fitView();
});

/**
 * onNodeDragStop is called when a node is done being dragged
 *
 * Node drag events provide you with:
 * 1. the event object
 * 2. the nodes array (if multiple nodes are dragged)
 * 3. the node that initiated the drag
 * 4. any intersections with other nodes
 */
onNodeDragStop(({ event, nodes, node, intersections }) => {
  console.log("Node Drag Stop", { event, nodes, node, intersections });
});

/**
 * onConnect is called when a new connection is created.
 *
 * You can add additional properties to your new edge (like a type or label) or block the creation altogether by not calling `addEdges`
 */
onConnect((connection) => {
  addEdges(connection);
});

/**
 * To update a node or multiple nodes, you can
 * 1. Mutate the node objects *if* you're using `v-model`
 * 2. Use the `updateNode` method (from `useVueFlow`) to update the node(s)
 * 3. Create a new array of nodes and pass it to the `nodes` ref
 */
function updatePos() {
  nodes.value = nodes.value.map((node: any) => {
    return {
      ...node,
      position: {
        x: Math.random() * 400,
        y: Math.random() * 400,
      },
    };
  });
}

/**
 * toObject transforms your current graph data to an easily persist-able object
 */
function logToObject() {
  console.log(toObject());
}

/**
 * Resets the current viewport transformation (zoom & pan)
 */
function resetTransform() {
  setViewport({ x: 0, y: 0, zoom: 1 });
}

function toggleDarkMode() {
  dark.value = !dark.value;
}

const onDrop = (event: any) => {
  const node = JSON.parse(event.dataTransfer?.getData("application/vueflow"));
  const position = project({ x: event.clientX - 60, y: event.clientY - 18 });
  const newNode = {
    id: "",
    type: node.type,
    position,
    data: {
      ...node,
    },
    label: `${node.type} node`,
  };
  addNodes([newNode]);
};

// Helper function to find new items
function findNewItems(newItems: any[], oldItems: any[], idKey = "id") {
  return newItems.filter(
    (newItem) => !oldItems.some((oldItem) => oldItem[idKey] === newItem[idKey])
  );
}

watch(
  mainMenu,
  (newMenu, oldMenu) => {
    if (!oldMenu) return;
    const menuGraph = generateGraph(newMenu);
    setMenuGraph(menuGraph);
  },
  { deep: true }
);

// Watcher to detect changes in the graph
watch(
  menuGraph,
  (newGraph, oldGraph) => {
    if (!oldGraph) return;

    const newNodes = findNewItems(newGraph.nodes, oldGraph.nodes);
    const newEdges = findNewItems(newGraph.edges, oldGraph.edges);

    if (newNodes.length > 0) {
      console.log("New nodes added:", newNodes);
      addNodes(newNodes);
    }
    if (newEdges.length > 0) {
      console.log("New edges added:", newEdges);
      addEdges(newEdges);
    }
  },
  { deep: true }
);

onMounted(() => {});
</script>

<template>
  <div class="dashboard-map-wrapper">
    <div class="dashboard-map-wrapper-inner">
      <div
        style="
          position: absolute;
          top: 70px;
          left: 0;
          width: 100vw;
          height: calc(100vh - 70px);
        "
        @drop="onDrop"
      >
        <VueFlow
          :nodes="nodes"
          :edges="edges"
          :class="{ dark }"
          class="basicflow"
        >
          <template #node-input="props">
            <CustomNode v-bind="props" />
          </template>
          <template #node-output="props">
            <CustomNode v-bind="props" />
          </template>
          <Background />

          <Controls :position="PanelPosition.BottomRight">
            <ControlButton title="Reset Transform" @click="resetTransform">
              <Icon name="reset" />
            </ControlButton>

            <ControlButton title="Shuffle Node Positions" @click="updatePos">
              <Icon name="update" />
            </ControlButton>

            <ControlButton title="Toggle Dark Mode" @click="toggleDarkMode">
              <Icon v-if="dark" name="sun" />
              <Icon v-else name="moon" />
            </ControlButton>

            <ControlButton title="Log `toObject`" @click="logToObject">
              <Icon name="log" />
            </ControlButton>
          </Controls>
        </VueFlow>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
html,
body,
#app {
  margin: 0;
  height: 100%;
  text-transform: uppercase;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

.vue-flow__handle {
  position: absolute;
  width: 10px;
  height: 10px;
  background: var(--vf-handle);
  border: 1px solid #fff;
  border-radius: 100%;
}

.vue-flow-drag-item {
  padding: 10px;
  border-radius: 10px;
  cursor: pointer;
}

.vue-flow__minimap {
  transform: scale(75%);
  transform-origin: bottom right;
}

.dndflow {
  flex-direction: column;
  display: flex;
  height: 100%;
}

.dndflow aside {
  color: #fff;
  font-weight: 700;
  border-right: 1px solid #eee;
  padding: 15px 10px;
  font-size: 12px;
  background: rgba(16, 185, 129, 0.75);
  box-shadow: 0 5px 10px #0000004d;
}

.dndflow aside .nodes > * {
  margin-bottom: 10px;
  cursor: -webkit-grab;
  cursor: grab;
  font-weight: 500;
  box-shadow: 5px 5px 10px 2px #00000040;
}

.dndflow aside .description {
  margin-bottom: 10px;
}

.dndflow .vue-flow-wrapper {
  flex-grow: 1;
  height: 100%;
}

@media screen and (min-width: 640px) {
  .dndflow {
    flex-direction: row;
  }

  .dndflow aside {
    min-width: 25%;
  }
}

@media screen and (max-width: 639px) {
  .dndflow aside .nodes {
    display: flex;
    flex-direction: row;
    gap: 5px;
  }
}

.has-top-nav {
  .dashboard-map-wrapper {
    top: 80px;
    height: calc(100% - 80px);
  }
}

.is-dark {
  .dashboard-map-wrapper {
    .dashboard-map-wrapper-inner {
      .content-section {
        background: var(--dark-sidebar-dark-3);

        .content-section-body {
          .map-box {
            background: var(--dark-sidebar-light-3);
            border-color: var(--dark-sidebar-light-10);

            &.is-active {
              border-color: var(--primary) !important;
            }
          }
        }
      }
    }
  }
}

@media only screen and (max-width: 767px) {
  .has-top-nav {
    .dashboard-map-wrapper {
      top: 0;
      height: 100%;
    }
  }

  .dashboard-map-wrapper {
    overflow-x: hidden;

    .dashboard-map-wrapper-inner {
      flex-direction: column;

      &.is-reversed {
        flex-direction: column;
      }

      .map-section {
        min-height: 30vh;
        width: 100%;
      }

      .content-section {
        height: 70vh;
      }
    }
  }

  .geocoder {
    padding: 0 2rem;
  }
}

@media only screen and (min-width: 768px) and (max-width: 1024px) and (orientation: portrait) {
  .has-top-nav {
    .dashboard-map-wrapper {
      top: 0;
      height: 100%;
    }
  }

  .dashboard-map-wrapper {
    overflow-x: hidden;

    .dashboard-map-wrapper-inner {
      flex-direction: column;

      &.is-reversed {
        flex-direction: column;
      }

      .map-section {
        min-height: 30vh;
        width: 100%;
      }

      .content-section {
        height: calc(70vh - 60px);
        width: 100%;
      }
    }
  }

  .geocoder {
    padding: 0 2rem;
  }
}
</style>
