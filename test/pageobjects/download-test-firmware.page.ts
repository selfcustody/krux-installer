import Page from './page'

class DownloadTestFirmware extends Page {

  constructor () {
    super()
    this._main = '#download-test-firmware-page'
    this._cardTitle = '#download-test-firmware-page-card-title'
    this._cardSubtitle = '#download-test-firmware-page-card-subtitle'
    this._progressLinearText = '#download-test-firmware-page-card-progress-linear-test'
  }
 
  get cardTitle () { 
    // eslint-disable-next-line no-undef
    return $(this._cardTitle)
  }

  get cardSubtitle () { 
    // eslint-disable-next-line no-undef
    return $(this._cardSubtitle)
  }

  get progressLinearText () { 
    // eslint-disable-next-line no-undef
    return $(this._progressLinearText)
  }
}

export default new DownloadTestFirmware()
