import { defineStore } from "pinia";
import menu from "../data/menu.json";
import { MenuLevel, MenuOption, convertToCamelCase } from "../types/ussd";
import { generateGraph, calculateNextMenuLevel } from "../services/menu";
import { Ref, ref } from "vue";

// Extending the Navigator type to include msSaveOrOpenBlob

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

  function getNextMenuLevelID(): string {
    const menuKeys = Object.keys(mainMenu.value);

    if (menuKeys.length === 0) {
      throw new Error("The main menu is empty.");
    }

    menuKeys.sort((a, b) => parseInt(a) - parseInt(b));

    return (parseInt(menuKeys[menuKeys.length - 1]) + 1).toString();
  }

  function addNewMenuItem(menuLevel: MenuLevel = <MenuLevel>{}) {
    if (!menuLevel.id) {
      menuLevel.id = getNextMenuLevelID();
      menuLevel.menuOptions = [<MenuOption>{}];
      menuLevel.menuLevel = calculateNextMenuLevel(mainMenu.value);
      selectedMenuLevelId.value = menuLevel.id;
    }

    mainMenu.value = {
      ...mainMenu.value,
      [menuLevel.id]: menuLevel,
    };

    menuGraph.value = generateGraph(mainMenu.value);

    return menuLevel;
  }

  function setMenuGraph(menuGraph: any) {
    menuGraph.value = menuGraph;
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
    setMenuGraph,
    setSelectedMenuLevel,
    hidePreviewSideNav,
    showPreviewSideNav,
    getNextMenuLevelID,
    loadMenus,
    exportToJson,
    generateGraph,
    calculateNextMenuLevel,
    addNewMenuItem,
    hideSideMenu,
    showSideMenu,
  };
});
