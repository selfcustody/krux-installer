/**
 * Base class to handle actions
 */
class Handler {

  constructor (app) {
    this.app = app;
  }

  /**
   * Send message to specific channel
   *
   * @param channel: String
   * @param msg: Any
   */
  send (channel, msg) {
    this.app.webContents.send(channel, msg);
  }
}

export default Handler
