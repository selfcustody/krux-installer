const { $ } = require('@wdio/globals')

class App {

  private __app__: string;

  constructor () {
    this.__app__ = '#app'
    this.__main__ = '#app>div>main'
  }

  get title () {
    return $('head>title')
  }

  get app () {
    return $(this.__app__)
  }

  get main () {
    return $(this.__main__)
  }

}

module.exports = App
