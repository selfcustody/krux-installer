import Page from './page'

class CheckResourcesTestKboot extends Page {

  constructor () {
    super()
    this._main = '#check-resources-test-kboot-page'
    this._cardTitleChecking = '#check-resources-test-kboot-page-card-title-checking'
    this._cardTitleChecked = '#check-resources-test-kboot-page-card-title-checked'
    this._cardSubtitleChecked = '#check-resources-test-kboot-page-card-subtitle-checked'
    this._cardContentChecked = '#check-resources-test-kboot-page-card-content-checked' 
    this._buttonDownload = '#check-resources-test-kboot-page-button-download-checked'
    this._buttonProceed = '#check-resources-test-kboot-page-button-proceed-checked'
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

export default new CheckResourcesTestKboot()