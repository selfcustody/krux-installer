import Page from './page'

class Logo extends Page {

  constructor () {
    super()
    this._krux_banner = '#krux-banner'
    this._asciiart = 'pre.__asciimorph__'
    this._title = 'h1=Krux Installer'
  }

  get banner () { 
    // eslint-disable-next-line no-undef
    return $(this._krux_banner)
  }

  get asciiart () {
    // eslint-disable-next-line no-undef
    return $(this._asciiart)
  }

  get title () {
    // eslint-disable-next-line no-undef
    return $(this._title)
  }

}

export default new Logo()

