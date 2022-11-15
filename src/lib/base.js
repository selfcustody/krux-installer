import createDebug from 'debug'

/**
 * Base class to handle actions
 */
class Handler {

  constructor (name, win, store) {
    this.win = win
    this.store = store
    this.name = name
    this.debug = createDebug(`krux:${name}`)
  }

  /**
   * Send message to specific channel
   *
   * @param channel: String
   * @param msg: Any
   */
  send (channel, msg) {
    if (typeof msg == 'object') {
      this.debug(`| ${channel} | ${JSON.stringify(msg)}`)
    } else {
      this.debug(`| ${channel} | ${msg}`)
    }
    this.win.webContents.send(channel, msg);
  }

  /**
   * Send log to debug module and to window
   *
   * @param msg: String
   */
  log (msg) {
    if (typeof msg == 'object') {
      msg = JSON.stringify(msg)
    }
    this.send('window:log:info', msg)
  }
}

export default Handler
