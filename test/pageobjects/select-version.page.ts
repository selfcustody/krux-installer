import SelectOptions from './select-options.page'

class SelectVersion extends SelectOptions {

  constructor () {
    super()
    this._main = '#select-version-page'  
    this._formSelect = '#select-version-page-form-select-versions' 
    this._cardTitleChecking = '#select-version-page-card-title-checking'
    this._cardTitleChecked = '#select-version-page-card-title-checked'   
    this._cardSubtitleOfficial = '#select-version-page-card-subtitle-official'
    this._cardSubtitleTest = '#select-version-page-card-subtitle-test'   
    this._cardContent = '#select-version-page-card-content' 
    this._selectButton = '#select-version-page-form-select-versions-button'
    this._backButton = '#select-device-page-form-select-versions-back-button' 
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

  get list_item_22_08_2 () { 
    // eslint-disable-next-line no-undef
    return $$('.v-list>.v-list-item')[0]
  }

  get list_item_krux_binaries () { 
    // eslint-disable-next-line no-undef
    return $$('.v-list>.v-list-item')[1]
  }
}

export default new SelectVersion()
