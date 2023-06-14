import Page from './page'

class WriteFirmwareToDevice extends Page {

  constructor () {
    super()
    this._main = '#write-firmware-to-device-page'
    this._cardTitle = '#write-firmware-to-device-page-card-title'
    this._cardSubtitle = '#write-firmware-to-device-page-card-subtitle' 
    this._cardContent = '#write-firmware-to-device-page-card-content'
    this._console = '#write-firmware-to-device-console'
  }

  get cardTitle () { 
    // eslint-disable-next-line no-undef
    return $(this._cardTitle)
  }

  get cardSubtitle () { 
    // eslint-disable-next-line no-undef
    return $(this._cardSubtitle)
  }

  get console() { 
    // eslint-disable-next-line no-undef
    return $(this._console)
  }
}

export default new WriteFirmwareToDevice()

