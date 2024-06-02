import menu from "../data/menu.json";
import { MenuLevel, convertToCamelCase } from "../types/ussd";
import { Edge, Node, Position } from "@vue-flow/core";

export function loadMenus() {
  return generateGraph(convertToCamelCase(menu) as Record<string, MenuLevel>);
}

export function calculateNextMenuLevel(
  data: Record<string, MenuLevel>
): number {
  let maxMenuLevel = 0;

  for (const key in data) {
    if (data.hasOwnProperty(key)) {
      const menuLevel = data[key];
      const level =
        typeof menuLevel.menuLevel === "string"
          ? parseInt(menuLevel.menuLevel)
          : menuLevel.menuLevel;
      if (level > maxMenuLevel) {
        maxMenuLevel = level;
      }
    }
  }

  return maxMenuLevel + 1;
}

export function generateGraph(data: Record<string, MenuLevel>): {
  nodes: Node[];
  edges: Edge[];
} {
  const nodes: Node[] = [];
  const edges: Edge[] = [];
  const targetPositions = new Set<string | number>();
  const sourcePositions = new Set<string | number>();

  const levels: Record<number, MenuLevel[]> = {};

  // Group nodes by their menuLevel
  for (const key in data) {
    if (data.hasOwnProperty(key)) {
      const menuLevel = data[key];
      const level =
        typeof menuLevel.menuLevel === "string"
          ? parseInt(menuLevel.menuLevel)
          : menuLevel.menuLevel;
      if (!levels[level]) {
        levels[level] = [];
      }
      levels[level].push(menuLevel);
    }
  }

  // Create edges for each menu option
  for (const key in data) {
    if (data.hasOwnProperty(key)) {
      const menuLevel = data[key];
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

  const nodePositions: Record<string, { x: number; y: number }> = {};

  // Function to calculate y position based on parent node
  function calculateYPosition(
    parentId: string,
    index: number,
    total: number
  ): number {
    const parentNode = nodePositions[parentId];
    if (!parentNode) return index * 100;
    const parentY = parentNode.y;
    const offset = (index - (total - 1) / 2) * 100;
    return parentY + offset;
  }

  // Create nodes with calculated positions
  for (const level in levels) {
    if (levels.hasOwnProperty(level)) {
      const menuLevels = levels[level];
      for (let i = 0; i < menuLevels.length; i++) {
        const menuLevel = menuLevels[i];
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

        // Calculate y position based on parent node
        const parentNode = edges.find((edge) => edge.target === menuLevel.id);
        const parentId = parentNode ? parentNode.source : null;
        const yPos = parentId
          ? calculateYPosition(parentId, i, menuLevels.length)
          : i * 100;

        const xPos = parseInt(level) * 250;

        nodePositions[menuLevel.id] = { x: xPos, y: yPos };

        nodes.push({
          id: menuLevel.id,
          label: menuLevel.text,
          type: nodeType,
          position: {
            x: xPos,
            y: yPos,
          },
          class: "light",
          sourcePosition: nodeSourcePosition,
          targetPosition: nodeTargetPosition,
          data: menuLevel,
        });
      }
    }
  }

  return { nodes, edges };
}
