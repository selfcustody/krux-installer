export default class Page {

  constructor () {
    this._title = 'krux-installer'
  }

  get title () {
    return $('title')
  }

}
