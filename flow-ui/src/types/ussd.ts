export interface MenuOption {
  id: number;
  numberedDisplayText?: string;
  type: string;
  response?: string;
  nextMenuLevel?: string | null;
  action?: string;
  conEnd?: boolean;
}

export interface MenuLevel {
  id: string;
  menuLevel: number | string;
  intro?: string;
  text: string;
  menuOptions: MenuOption[];
  maxSelections: number | string;
  action?: string;
  conEnd?: boolean;
}

export interface USSDSession {
  id: string;
  sessionId: string;
  serviceCode: string;
  phoneNumber: string;
  text: string;
  previousMenuLevel: string;
  currentMenuLevel: string;
}

export interface IngressData {
  sessionId: string;
  serviceCode: string;
  phoneNumber: string;
  text: string;
  networkCode: string;
}

/**
 *
 * @param key
 * @returns
 */
export function toCamelCase(key: string): string {
  return key.replace(/_([a-z])/g, (_, letter) => letter.toUpperCase());
}

/**
 *
 * @param obj
 * @returns
 */
export function convertToCamelCase(obj: any): any {
  if (Array.isArray(obj)) {
    return obj.map((v) => convertToCamelCase(v));
  } else if (obj !== null && obj.constructor === Object) {
    return Object.keys(obj).reduce((result: any, key: string) => {
      const camelCaseKey = toCamelCase(key);
      result[camelCaseKey] = convertToCamelCase(obj[key]);
      return result;
    }, {});
  }
  return obj;
}
