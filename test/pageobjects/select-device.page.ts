import Page from './page'

class SelectDevice extends Page {

  constructor () {
    super()
    this._main = '#select-device-page'
    this._cardTitle = '#select-device-page-card-title'  
    this._cardContent = '#select-device-page-card-content' 
    this._formSelect = '#select-device-page-form-select'  
    this._overlayContainer = '#' 
    this._selectButton = '#select-device-page-form-select-button'
    this._backButton = '#select-device-page-form-back-button'
  }

  get page () { 
    // eslint-disable-next-line no-undef
    return $(this._main)
  }

  get cardTitle () { 
    // eslint-disable-next-line no-undef
    return $(this._cardTitle)
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

  get selectButton () {
    // eslint-disable-next-line no-undef
    return $(`${this._selectButton}`)
  }

  get backButton () {
    // eslint-disable-next-line no-undef
    return $(`${this._backButton}`)
  }
}

export default new SelectDevice()
