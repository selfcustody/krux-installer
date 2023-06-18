/// <reference path="../typings/index.d.ts"/>

import createDebug from 'debug'

/**
 * Base class for initializing KruxInstaller application,
 * wdioTest runner and handlers. The `name` property will be used
 * as identification for `debugger` object,as well a identification
 * for ipcMain/ipcRenderer channel messages.
 * 
 * @example
 * ```
 * const base = new Base('krux:myClass')
 * ```
 * 
 * @see WdioTest
 * @see Storage
 * @see Handler
 */
export default class Base {
  /**
   * Identificator to use as a attributed debugger and ipcMain/ipcRenderer channel messages
   */
  protected name: KruxInstaller.DebugName;
  
  /**
   * The attributed debuger
   * 
   * @see debug.Debugger
   */
  protected debug: debug.Debugger;

  /**
   * The attributed electron browser window
   * 
   * @see Electron.BrowserWindow
   */
  protected win?: Electron.BrowserWindow;
  
  /**
   * The attributed electron application
   * 
   * @see Electron.App
   */
  protected app?: Electron.App;

  /**
   * If the environment variable DEBUG is attributed to 'background', any of the messages will be displayed only for this module; can use wildcards.
   * 
   * @param name 
   * @example
   * ```
   * $> DEBUG=background yarn run electron:<serve|build>
   * $> DEBUG=background:* yarn run electron:<serve|build>
   * ```
   */
  constructor(name: KruxInstaller.DebugName) {
    this.name = name;
    this.debug = createDebug(name);
    this.log(`Initializing ${name}`);
  }

  /**
   * Send a message to debugger and to client
   * window logger channel
   *
   * @param msg
   * @example
   * ```
   * log('Hello World')
   * log({ hello: 'World' })
   * ```
   */ 
  log(msg: string | KruxInstaller.JsonDict): void {
    this.send(null, msg)
  }

  /**
   * Send a message to a specific channel
   *
   * @param channel
   * @param msg
   * @example 
   * ```
   * send('my:channel', 'Hello World')
   * send('my:channel', { hello: 'World' })
   * ```
   */ 
  send(channel: string | null, msg: KruxInstaller.JsonValue | KruxInstaller.JsonDict | string[]): void {
    const __date__ = (new Date()).toLocaleString()
    let __msg__ = ''
    if (typeof msg === 'object') {
      __msg__ = `[ ${__date__} ] ${JSON.stringify(msg)}`
    } else { 
      __msg__ = `[ ${__date__} ] ${msg}`
    }
    this.debug(__msg__)
    if (this.win !== null && this.win !== undefined) {
      this.win.webContents.send('main-process-message', __msg__)
      if (channel) {
        this.win.webContents.send(channel, msg)
      }
    }
  }
}
