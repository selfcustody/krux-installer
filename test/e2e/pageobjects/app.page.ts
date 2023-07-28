import { $ } from '@wdio/globals'
import Page from './page'

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

export default new App()