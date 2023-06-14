import Page from './page'

class DownloadOfficialReleaseSig extends Page {

  constructor () {
    super()
    this._main = '#download-official-release-sig-page'
    this._cardTitle = '#download-official-release-sig-page-card-title'
    this._cardSubtitle = '#download-official-release-sig-page-card-subtitle'
    this._progressLinearText = '#download-official-release-sig-page-card-progress-linear-text'
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

export default new DownloadOfficialReleaseSig()
