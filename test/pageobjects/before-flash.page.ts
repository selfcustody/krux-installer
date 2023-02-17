import Page from './page'

class BeforeFlash extends Page {

  constructor () {
    super()
    this._main = '#before-flash-device-page'
    this._cardTitle = '#before-flash-device-page-card-title'
    this._cardSubtitleVersion = '#before-flash-device-page-card-subtitle-version' 
    this._cardSubtitleDevice = '#before-flash-device-page-card-subtitle-device'
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
}

export default new BeforeFlash()

