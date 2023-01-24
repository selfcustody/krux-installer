import Page from './page'

export default class SelectOptions extends Page {

  constructor () {
    super()
    this._overlayContainer = '.v-overlay-container'
    this._selected = '.v-select__selection-text'
  }

  get cardContent () {
    // eslint-disable-next-line no-undef
    return $(this._cardContent)
  }
  
  get formSelectContainer () {
    return this.cardContent.$('.v-input')
  }

  get formSelectControl () {
    return this.formSelectContainer.$('.v-input__control')
  }

  get formSelectFieldContainer () {
    return this.formSelectControl.$('.v-field')
  }

  get formSelectField () {
    return this.formSelectFieldContainer.$('.v-field__field')
  }

  get formSelectLabel () {
    return this.formSelectFieldContainer.$('label')
  }

  get formArrowContainer () {
    return this.formSelectFieldContainer.$('.v-field__append-inner')
  }

  get formArrow () {
    return this.formArrowContainer.$('i')
  }

  get formOverlayContainer () {
    // eslint-disable-next-line no-undef
    return $(this._overlayContainer)
  }

  get formSelected () { 
    // eslint-disable-next-line no-undef
    return $(this._selected)
  }

  get formSelectButton () {
    // eslint-disable-next-line no-undef
    return $(this._selectButton)
  }

  get formBackButton () {
    // eslint-disable-next-line no-undef
    return $(this._backButton)
  }
}
