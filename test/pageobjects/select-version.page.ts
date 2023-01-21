import Page from './page'

class SelectVersion extends Page {

  constructor () {
    super()
    this._main = '#select-version-page' 
    this._cardContent = '#select-version-page-card-content' 
    this._cardTitleChecking = '#select-version-page-card-title-checking'
    this._cardTitleChecked = '#select-version-page-card-title-checked'   
    this._cardSubtitleOfficial = '#select-version-page-card-subtitle-official'
    this._cardSubtitleTest = '#select-version-page-card-subtitle-test'  
    this._formSelect = '#select-version-page-form-select-versions' 
    this._selectButton = '#select-version-page-form-select-versions-button'
    this._backButton = '#select-device-page-form-select-versions-back-button' 
    this._selected = '.v-select__selection-text'
  }

  get page () { 
    // eslint-disable-next-line no-undef
    return $(this._main)
  }

  get cardTitleChecking () { 
    // eslint-disable-next-line no-undef
    return $(this._cardTitleChecking)
  }

  get cardTitleChecked () { 
    // eslint-disable-next-line no-undef
    return $(this._cardTitleChecked)
  }

  get cardSubtitleOfficial () { 
    // eslint-disable-next-line no-undef
    return $(this._cardSubtitleOfficial)
  }

  get cardSubtitleTest () { 
    // eslint-disable-next-line no-undef
    return $(this._cardSubtitleTest)
  }

  get cardContent () {
    // eslint-disable-next-line no-undef
    return $(this._cardContent)
  }

  get formSelect () {
    // eslint-disable-next-line no-undef
    return $(this._formSelect)
  }

  get formSelectLabel () {
    // eslint-disable-next-line no-undef
    return $(`${this._formSelect}>label`)
  }

  get formSelectButton () {
    // eslint-disable-next-line no-undef
    return $(this._selectButton)
  }

  get formBackButton () {
    // eslint-disable-next-line no-undef
    return $(this._backButton)
  }

  get formArrowContainer () {
    return this.cardContent.$('div.v-input')
  }

  get formArrowWrapper () {
    return this.formArrowContainer.$('div.v-input__control').$('div.v-field')
  }

  get formArrow () {
    return this.formArrowWrapper.$('div.v-field__append-inner').$('i')
  }

  get formOverlayContainer () {
    // eslint-disable-next-line no-undef
    return $('.v-overlay-container')
  }

  get list_item_22_03_0 () { 
    // eslint-disable-next-line no-undef
    return $$('.v-list>.v-list-item')[0]
  }

  get list_item_22_08_0 () { 
    // eslint-disable-next-line no-undef
    return $$('.v-list>.v-list-item')[1]
  }

  get list_item_22_08_1 () { 
    // eslint-disable-next-line no-undef
    return $$('.v-list>.v-list-item')[2]
  }

  get list_item_22_08_2 () { 
    // eslint-disable-next-line no-undef
    return $$('.v-list>.v-list-item')[3]
  }

  get list_item_krux_binaries () { 
    // eslint-disable-next-line no-undef
    return $$('.v-list>.v-list-item')[4]
  }

  get selected () { 
    // eslint-disable-next-line no-undef
    return $(this._selected)
  }
}

export default new SelectVersion()
