import Page from './page'

class CheckResourcesOfficialRelease extends Page {

  constructor () {
    super()
    this._main = '#check-resources-official-release-page'
    this._cardTitleChecking = '#check-resources-official-release-page-card-title-checking'
  }
 
  get page () { 
    // eslint-disable-next-line no-undef
    return $(this._main)
  }

  get cardTitleChecking () { 
    // eslint-disable-next-line no-undef
    return $(this._cardTitleChecking)
  }
}

export default new CheckResourcesOfficialRelease()
