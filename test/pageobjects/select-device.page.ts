import SelectOptions from './select-options.page'

class SelectDevice extends SelectOptions {

  constructor () {
    super()
    this._main = '#select-device-page' 
    this._formSelect = '#select-device-page-form-select'  
    this._cardTitle = '#select-device-page-card-title'  
    this._cardContent = '#select-device-page-card-content' 
    this._selectButton = '#select-device-page-form-select-button'
    this._backButton = '#select-device-page-form-back-button'
  }

  get cardTitle () { 
    // eslint-disable-next-line no-undef
    return $(this._cardTitle)
  }

  get list_item_m5stickv () { 
    // eslint-disable-next-line no-undef
    return $$('.v-list>.v-list-item')[0]
  }

  get list_item_amigo_ips () { 
    // eslint-disable-next-line no-undef
    return $$('.v-list>.v-list-item')[1]
  }

  get list_item_amigo_tft () { 
    // eslint-disable-next-line no-undef
    return $$('.v-list>.v-list-item')[2]
  }

  get list_item_bit () { 
    // eslint-disable-next-line no-undef
    return $$('.v-list>.v-list-item')[3]
  }

  get list_item_dock () { 
    // eslint-disable-next-line no-undef
    return $$('.v-list>.v-list-item')[4]
  }

}

export default new SelectDevice()
