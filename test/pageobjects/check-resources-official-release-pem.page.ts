import Page from './page'

class CheckResourcesOfficialReleasePem extends Page {

  constructor () {
    super()
    this._main = '#check-resources-official-release-pem-page'
    this._cardTitleChecking = '#check-resources-official-release-pem-page-card-title-checking'
    this._cardTitleChecked = '#check-resources-official-release-pem-page-card-title-checked' 
    this._cardSubtitleChecked = '#check-resources-official-release-pem-page-card-subtitle-checked' 
    this._cardContentChecked = '#check-resources-official-release-pem-page-card-content-checked' 
    this._buttonDownload = '#check-resources-official-release-pem-page-button-download-checked'
    this._buttonProceed = '#check-resources-official-release-pem-page-button-proceed-checked'
  }
 
  get cardTitleChecking () { 
    // eslint-disable-next-line no-undef
    return $(this._cardTitleChecking)
  }

  get cardTitleChecked () { 
    // eslint-disable-next-line no-undef
    return $(this._cardTitleChecked)
  }

  get cardSubtitleChecked () { 
    // eslint-disable-next-line no-undef
    return $(this._cardSubtitleChecked)
  }

  get cardContentChecked () { 
    // eslint-disable-next-line no-undef
    return $(this._cardContentChecked)
  }

  get buttonDownload () { 
    // eslint-disable-next-line no-undef
    return $(this._buttonDownload)
  }

  get buttonProceed () { 
    // eslint-disable-next-line no-undef
    return $(this._buttonProceed)
  }
 
}

export default new CheckResourcesOfficialReleasePem()
