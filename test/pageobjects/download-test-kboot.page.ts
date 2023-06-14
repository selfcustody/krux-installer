import Page from './page'

class DownloadTestKboot extends Page {

  constructor () {
    super()
    this._main = '#download-test-kboot-page'
    this._cardTitle = '#download-test-kboot-page-card-title'
    this._cardSubtitle = '#download-test-kboot-page-card-subtitle'
    this._progressLinearText = '#download-test-kboot-page-card-progress-linear-test'
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

export default new DownloadTestKboot()
