import Page from './page'

class DownloadOfficialRelease extends Page {

  constructor () {
    super()
    this._main = '#download-official-release-page'
    this._cardTitle = '#download-official-release-page-card-title'
    this._cardSubtitle = '#download-official-release-page-card-subtitle'
  }
 
  get page () { 
    // eslint-disable-next-line no-undef
    return $(this._main)
  }

  get cardTitle () { 
    // eslint-disable-next-line no-undef
    return $(this._cardTitle)
  }

  get cardSubtitle () { 
    // eslint-disable-next-line no-undef
    return $(this._cardSubtitle)
  }
}

export default new DownloadOfficialRelease()
