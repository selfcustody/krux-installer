const { $ } = require('@wdio/globals')

class Page {

  protected __main__: string

  get title (): typeof $ {
    return $('title')
  }
}

module.exports = Page
