/// <reference path="../node_modules/electron/electron.d.ts" />
/// <reference path="../node_modules/electron-store/index.d.ts" />

/**
 * The KruxInstaller namespace:
 * 
 * @see DebugName
 * @see JsonValue
 * @see JsonArray
 */
declare namespace KruxInstaller {

    /**
     * The specific format `string:string` to debug in terminal or console
     */
    export type DebugName = `${string}:${string}`
  
    // 
    /**
     * Arbitrary value for json objects
     * see https://stackoverflow.com/questions/64921660/dealing-with-arbitrary-objects-in-typescript
     * 
     * @see JsonArray
     */
    export type JsonValue = null | string | number | boolean | JsonArray | JsonDict;
  
    /**
     * Arbitrary array of values for json objects
     * see https://stackoverflow.com/questions/64921660/dealing-with-arbitrary-objects-in-typescript
     * 
     * @see JsonValue
     */
    export type JsonArray = JsonValue[];
    
    /**
     * An arbitrary json in form {string: JsonValue}
     * 
     * @see JsonValue
     */
    export interface JsonDict extends Record<string, JsonValue> { }

    export interface StartedApp {
      app: Electron.App;
      ipcMain: Electron.IpcMain;
      win: Electron.BrowserWindow;
    }

    export interface FetchedGithubTags {
      ref: string;
      node_id: string;
      url: string;
      object: {
        sha: string;
        type: string;
        url: string;
      }
    }
}