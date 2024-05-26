import menu from "../data/menu.json";
import { MenuLevel, convertToCamelCase } from "../types/ussd";
import { Edge, Node, Position } from "@vue-flow/core";

export function loadMenus() {
  return generateGraph(convertToCamelCase(menu) as Record<string, MenuLevel>);
}

export function generateGraph(data: Record<string, MenuLevel>): {
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
