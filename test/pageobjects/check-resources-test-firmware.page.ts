import Page from './page'

class CheckResourcesTestFirmware extends Page {

  constructor () {
    super()
    this._main = '#check-resources-test-firmware-page'
    this._cardTitleChecking = '#check-resources-page-card-title-checking'
    this._cardTitleChecked = '#check-resources-page-card-title-checked'
    this._cardSubtitleChecked = '#check-resources-page-card-subtitle-checked'
    this._cardContentChecked = '#check-resources-page-card-content-checked' 
    this._buttonDownload = '#check-resources-page-button-download-checked'
    this._buttonProceed = '#check-resources-page-button-proceed-checked'
  }
 
  get page () { 
    // eslint-disable-next-line no-undef
    return $(this._main)
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

export default new CheckResourcesTestFirmware()
