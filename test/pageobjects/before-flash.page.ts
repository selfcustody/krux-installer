import Page from './page'

class BeforeFlash extends Page {

  constructor () {
    super()
    this._main = '#before-flash-device-page'
    this._cardTitle = '#before-flash-device-page-card-title'
    this._cardSubtitleVersion = '#before-flash-device-page-card-subtitle-version' 
    this._cardSubtitleDevice = '#before-flash-device-page-card-subtitle-device'
    this._flashButton = '#before-flash-device-page-flash-button'
    this._backButton = '#before-flash-device-page-back-button'
  }

  get cardTitle () { 
    // eslint-disable-next-line no-undef
    return $(this._cardTitle)
  }

  get cardSubtitleVersion () { 
    // eslint-disable-next-line no-undef
    return $(this._cardSubtitleVersion)
  }

  get cardSubtitleDevice() { 
    // eslint-disable-next-line no-undef
    return $(this._cardSubtitleDevice)
  }

  get flashButton() { 
    // eslint-disable-next-line no-undef
    return $(this._flashButton)
  }

  get backButton() { 
    // eslint-disable-next-line no-undef
    return $(this._backButton)
  }
}

export default new BeforeFlash()

