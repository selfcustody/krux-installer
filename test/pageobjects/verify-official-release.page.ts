import Page from './page'

class VerifyOfficialRelease extends Page {

  constructor () {
    super()
    this._main = '#verify-official-release-page'
    this._cardTitleChecking = '#verify-official-release-page-card-title-checking'
    this._cardTitleChecked = '#verify-official-release-page-card-title-checked' 
    this._cardSubtitleSha256sumChecked = '#verify-official-release-page-card-subtitle-sha256sum-checked'
    this._cardSubtitleSigChecked = '#verify-official-release-page-card-subtitle-sig-checked' 
    this._cardContent = '#verify-official-release-page-card-content'
    this._signatureCommand = '#verify-official-release-page-console-command'
    this._signatureResult = '#verify-official-release-page-chip-sig-result'
  }
 
  get cardTitleChecking () { 
    // eslint-disable-next-line no-undef
    return $(this._cardTitleChecking)
  }

  get cardTitleChecked () { 
    // eslint-disable-next-line no-undef
    return $(this._cardTitleChecked)
  }

  get cardSubtitleSha256sumChecked () { 
    // eslint-disable-next-line no-undef
    return $(this._cardSubtitleSha256sumChecked)
  }

  get cardSubtitleSigChecked () { 
    // eslint-disable-next-line no-undef
    return $(this._cardSubtitleSigChecked)
  }

  get cardContent () { 
    // eslint-disable-next-line no-undef
    return $(this._cardContent)
  }

  get cardContentFilenameTxt () {
    return this.cardContent.$$('.v-card-text')[0].$('b')
  }

  get cardContentFilenameSha256 () {
    return this.cardContent.$$('.v-card-text')[1].$('b')
  }

  get chipHashTxt () {
    return this.cardContent.$$('.v-card-text')[0].$('span')
  }

  get chipHashSha256 () {
    return this.cardContent.$$('.v-card-text')[1].$('span')
  }
  
  get consoleSignatureCommand () { 
    // eslint-disable-next-line no-undef
    return $(this._signatureCommand)
  }

  get chipSignatureResult () { 
    // eslint-disable-next-line no-undef
    return $(this._signatureResult)
  }
}
export default new VerifyOfficialRelease()
