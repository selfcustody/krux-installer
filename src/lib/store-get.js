import Handler from './base'

class StoreGetHandler extends Handler {

  constructor (win, store) {
    super('store-get', win, store)
  }

  run (key) {
    const val = this.store.get(key)
    const msg = `${key} = '${val}'`
    this.log(msg)
    this.send(`${this.name}:${key}`, val)
  }
}

/**
 * Function to handle the capture of many config values
 *
 * @param win
 * @param store
 */
export default function (win, store) {
  // eslint-disable-next-line no-unused-vars
  return function (_event, options) {
    const handler = new StoreGetHandler(win, store)
    handler.run(options.key)
  }
}
