import Page from './page'

class App extends Page {

  constructor () {
    super()
    this._app = '#app'
    this._sideBanner = '#side-banner'
    this._sidePage = '#side-page'
  }

  get application () {
    return $(this._app)
  }

  get sideBanner () {
    return $(this._sideBanner)
  }

  get sidePage () {
    return $(this._sidePage)
  }

}

export default new App()

