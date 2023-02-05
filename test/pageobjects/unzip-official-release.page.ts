import Page from './page'

class UnzipOfficialRelease extends Page {

  constructor () {
    super()
    this._main = '#unzip-official-release-page'
    this._cardTitleUnzipping = '#unzip-official-release-page-card-title-unzipping'
    this._cardSubtitleUnzipping = '#unzip-official-release-page-card-subtitle-unzipping' 
    this._cardProgressLinearTextUnzipping = '#unzip-official-release-page-progress-linear-text-unzipping'
    this._cardTitleUnzipped = '#unzip-official-release-page-card-title-unzipped' 
    this._cardSubtitleUnzipped = '#unzip-official-release-page-card-subtitle-unzipped'
    this._cardContentTextUnzipped = '#unzip-official-release-page-card-content-text-unzipped'
    this._buttonDone = '#unzip-official-release-page-card-action-button-done-unzipped' 
    this._buttonBack = '#unzip-official-release-page-card-action-button-back-unzipped' 
  }
 
  get cardTitleUnzipping () {
    // eslint-disable-next-line no-undef
    return $(this._cardTitleUnzipping)
  }

  get cardTitleUnzipped () { 
    // eslint-disable-next-line no-undef
    return $(this._cardTitleUnzipped)
  }

  get cardSubtitleUnzipping () {
    // eslint-disable-next-line no-undef
    return $(this._cardSubtitleUnzipping)
  }

  get cardSubitleUnzipped () { 
    // eslint-disable-next-line no-undef
    return $(this._cardSubtitleUnzipped)
  }

  get cardProgressLinearTextUnzipping () { 
    // eslint-disable-next-line no-undef
    return $(this._cardProgressLinearTextUnzipping)
  }

  get cardContentTextUnzipped () { 
    // eslint-disable-next-line no-undef
    return $(this._cardContentTextUnzipped)
  }

  get buttonDone () { 
    // eslint-disable-next-line no-undef
    return $(this._buttonDone)
  }

  get buttonBack () { 
    // eslint-disable-next-line no-undef
    return $(this._buttonBack)
  }

}
export default new UnzipOfficialRelease()
