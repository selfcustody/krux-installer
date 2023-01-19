import Page from './page'

class SelectDevice extends Page {

  constructor () {
    super()
    this._main = '#select-device-page'
    this._cardTitle = '#select-device-page-card-title'
  }

  get page () { 
    // eslint-disable-next-line no-undef
    return $(this._main)
  }

  get cardTitle () { 
    // eslint-disable-next-line no-undef
    return $(this._cardTitle)
  }
}

export default new SelectDevice()

