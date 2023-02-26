import Page from './page'

class DownloadTestKtool extends Page {

  constructor () {
    super()
    this._main = '#download-test-ktool-page'
    this._cardTitle = '#download-test-ktool-page-card-title'
    this._cardSubtitle = '#download-test-ktool-page-card-subtitle'
    this._progressLinearText = '#download-test-ktool-page-card-progress-linear-test'
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

export default new DownloadTestKtool()
