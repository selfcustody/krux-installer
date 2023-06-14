export default class Page {

  constructor () {
    this._title = 'krux-installer'
  }

  get title () {
    // eslint-disable-next-line no-undef
    return $('title')
  }

  get page () {
    // eslint-disable-next-line no-undef
    return $(this._main)
  }
}
