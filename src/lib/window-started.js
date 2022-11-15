import Handler from './base'

class WindowStartedHandler extends Handler {

  constructor(win, store) {
    super('window-started', win, store)
  }

  ready() {
    const version = this.store.get('appVersion')
    const msg = `KruxInstaller ${version} running`
    this.log(msg)
  }
}

export default function (win, store) {
  // eslint-disable-next-line no-unused-vars
  return function (_event, action) {
    const handler = new WindowStartedHandler(win, store)
    handler.ready()
  }
}
