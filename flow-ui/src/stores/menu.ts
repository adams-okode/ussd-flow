import { defineStore } from "pinia";
import menu from "../data/menu.json";
import { MenuLevel, convertToCamelCase } from "../types/ussd";
import { Edge, Node, Position } from "@vue-flow/core";
import { Ref, ref } from "vue";

// Extending the Navigator type to include msSaveOrOpenBlob
interface Navigator {
  msSaveOrOpenBlob?: (blob: Blob, defaultName?: string) => boolean;
}

export const useMenuStore = defineStore("menu", () => {
  const showMenuSidenav = ref(false);
  const previewSideNavToggle = ref(false);

  const mainMenu: Ref<Record<string, MenuLevel>> = ref(
    convertToCamelCase(menu)
  );
  const menuGraph = ref(loadMenus());

  const selectedMenuLevelId: Ref<string | null> = ref(null);

  function loadMenus() {
    return generateGraph(convertToCamelCase(menu) as Record<string, MenuLevel>);
  }

  function generateGraph(data: Record<string, MenuLevel>): {
    nodes: Node[];
    edges: Edge[];
  } {
    const nodes: Node[] = [];
    const edges: Edge[] = [];
    const targetPositions = new Set<string | number>();
    const sourcePositions = new Set<string | number>();

    for (const key in data) {
      if (data.hasOwnProperty(key)) {
        const menuLevel = data[key];

        // Create edges for each menu option
        for (const option of menuLevel.menuOptions) {
          if (
            option.nextMenuLevel !== null &&
            option.nextMenuLevel !== undefined
          ) {
            edges.push({
              id: `e${menuLevel.id}-${option.nextMenuLevel}`,
              source: `${menuLevel.id}`,
              target: `${option.nextMenuLevel}`,
              label: `Responded with option ${option.nextMenuLevel}`,
              updatable: true,
              type: "smoothstep",
            });
            targetPositions.add(option.nextMenuLevel);
            sourcePositions.add(menuLevel.id);
          }
        }
      }
    }

    for (const key in data) {
      if (data.hasOwnProperty(key)) {
        const menuLevel = data[key];
        const hasOptions = menuLevel.menuOptions.length > 0;
        const isOutput =
          !hasOptions ||
          menuLevel.menuOptions.every((option) => !option.nextMenuLevel);

        const nodeType = isOutput ? "output" : "input";
        const nodeSourcePosition = sourcePositions.has(menuLevel.id)
          ? Position.Right
          : undefined;
        const nodeTargetPosition = targetPositions.has(menuLevel.id)
          ? Position.Left
          : undefined;

        // Create a node for the menu level
        nodes.push({
          id: menuLevel.id,
          label: menuLevel.text,
          type: nodeType,
          position: {
            x: 250 + Number(menuLevel.id) * 250,
            y: 50 + Number(menuLevel.id) * 100,
          },
          class: "light",
          sourcePosition: nodeSourcePosition,
          targetPosition: nodeTargetPosition,
          data: menuLevel,
        });
      }
    }

    return { nodes, edges };
  }

  function getNextMenuLevelID(): string {
    const menuKeys = Object.keys(mainMenu.value);

    if (menuKeys.length === 0) {
      throw new Error("The main menu is empty.");
    }

    menuKeys.sort((a, b) => parseInt(a) - parseInt(b));

    return (parseInt(menuKeys[menuKeys.length - 1]) + 1).toString();
  }

  function addNewMenuItem(menuLevel: MenuLevel) {
    mainMenu.value = {
      ...mainMenu.value,
      [menuLevel.id]: menuLevel,
    };
    menuGraph.value = generateGraph(mainMenu.value);
  }

  function hideSideMenu() {
    showMenuSidenav.value = false;
  }

  function showSideMenu() {
    showMenuSidenav.value = true;
  }

  function hidePreviewSideNav() {
    previewSideNavToggle.value = false;
  }

  function showPreviewSideNav() {
    previewSideNavToggle.value = true;
  }

  function setSelectedMenuLevel(menuId: string | null) {
    selectedMenuLevelId.value = menuId;
  }

  function exportToJson(fileName: string = "export.json") {
    const contentType = "application/json;charset=utf-8;";
    console.log(fileName);

    const jsonString = JSON.stringify(mainMenu.value, null, 2); // Pretty print JSON

    if (window.navigator && window.navigator.msSaveOrOpenBlob) {
      // For IE browser
      const blob = new Blob([jsonString], { type: contentType });
      window.navigator.msSaveOrOpenBlob(blob, fileName);
    } else {
      //   console.log(jsonString, fileName);
      const blob = new Blob([jsonString], { type: contentType });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");

      a.href = url;
      a.download = fileName;

      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    }
  }

  return {
    mainMenu,
    menuGraph,
    showMenuSidenav,
    previewSideNavToggle,
    selectedMenuLevelId,
    setSelectedMenuLevel,
    hidePreviewSideNav,
    showPreviewSideNav,
    getNextMenuLevelID,
    loadMenus,
    exportToJson,
    generateGraph,
    addNewMenuItem,
    hideSideMenu,
    showSideMenu,
  };
});
