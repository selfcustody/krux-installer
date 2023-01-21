import Page from './page'

class CheckResources extends Page {

  constructor () {
    super()
    this._main = '#check-resources-page'
    this._cardTitle = '#check-resources-page-card-title'
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

export default new CheckResources()
