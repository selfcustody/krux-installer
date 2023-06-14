import Page from './page'

class App extends Page {

  constructor () {
    super()
    this._app = '#app'
    this._sideBanner = '#side-banner'
    this._sidePage = '#side-page'
  }

  get application () { 
    // eslint-disable-next-line no-undef
    return $(this._app)
  }

  get sideBanner () {
    // eslint-disable-next-line no-undef
    return $(this._sideBanner)
  }

  get sidePage () {
    // eslint-disable-next-line no-undef
    return $(this._sidePage)
  }

}

export default new App()

