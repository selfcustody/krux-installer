import Page from './page'

class CheckResourcesOfficialReleaseSHA256 extends Page {

  constructor () {
    super()
    this._main = '#check-resources-official-release-sha256-page'
    this._cardTitleChecking = '#check-resources-official-release-sha256-page-card-title-checking'
    this._cardTitleChecked = '#check-resources-official-release-sha256-page-card-title-checked'
  }
 
  get cardTitleChecking () { 
    // eslint-disable-next-line no-undef
    return $(this._cardTitleChecking)
  }

  get cardTitleChecked () { 
    // eslint-disable-next-line no-undef
    return $(this._cardTitleChecked)
  }
 
}

export default new CheckResourcesOfficialReleaseSHA256()
