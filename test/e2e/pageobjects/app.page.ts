
const Page = require('./page')

class App extends Page {

  private __app__: string;

  constructor () {
    super()
    this.__app__ = '#app'
  }

  get application () {
    return $(this.__app__)
  }

}

module.exports = App