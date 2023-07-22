import { $ } from '@wdio/globals'

export default class Page {

  protected __title__: string
  protected __main__: string

  constructor () {
    this.__title__ = 'krux-installer'
  }

  get title (): typeof $ {
    return $('title')
  }

  get page (): typeof $ {
    return $(this.__main__)
  }
}