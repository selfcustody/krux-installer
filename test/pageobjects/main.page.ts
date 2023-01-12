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
    return $(this._main)
  }

  get selectDeviceCard () {
    return $(this._selectDeviceCard)
  }

  get selectVersionCard () {
    return $(this._selectVersionCard)
  }

  get selectWriteCard () {
    return $(this._selectWriteCard)
  }
 
  get selectDeviceCardSubtitle () {
    return $(this._selectDeviceCardSubtitle)
  }

  get selectVersionCardSubtitle () {
    return $(this._selectVersionCardSubtitle)
  }

  get selectWriteCardSubtitle () {
    return $(this._selectWriteCardSubtitle)
  }
}

export default new Main()

