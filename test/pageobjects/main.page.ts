import Page from './page'

class Main extends Page {

  constructor () {
    super()
    this._main = '#main-page'
    this._selectDeviceCard = '#select-device-card'
    this._selectVersionCard = '#select-version-card'
    this._selectWriteCard = '#select-write-card'
    this._selectDeviceCardSubtitle = '#select-device-card-subtitle'
    this._selectVersionCardSubtitle = '#select-version-card-subtitle'
    this._selectWriteCardSubtitle = '#select-write-card-subtitle'
  }

  get page () { 
    // eslint-disable-next-line no-undef
    return $(this._main)
  }

  get selectDeviceCard () { 
    // eslint-disable-next-line no-undef
    return $(this._selectDeviceCard)
  }

  get selectVersionCard () { 
    // eslint-disable-next-line no-undef
    return $(this._selectVersionCard)
  }

  get selectWriteCard () { 
    // eslint-disable-next-line no-undef
    return $(this._selectWriteCard)
  }
 
  get selectDeviceCardSubtitle () { 
    // eslint-disable-next-line no-undef
    return $(this._selectDeviceCardSubtitle)
  }

  get selectVersionCardSubtitle () { 
    // eslint-disable-next-line no-undef
    return $(this._selectVersionCardSubtitle)
  }

  get selectWriteCardSubtitle () { 
    // eslint-disable-next-line no-undef
    return $(this._selectWriteCardSubtitle)
  }
}

export default new Main()

