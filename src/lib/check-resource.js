import { join } from 'path'
import { existsAsync } from './utils/fs-async'
import Handler from './base'

class CheckResourcesHandler extends Handler {

  constructor (win, store, resource) {
    super('check-resource', win, store)
    this.resources = store.get('resources')
    this.relativeResource = resource
    this.destinationResource = join(this.resources, this.relativeResource)
  }

  async exists () {
    this.log(`Checking if ${this.destinationResource} exists`)
    const __exists__ = await existsAsync(this.destinationResource)
    this.log(`${this.destinationResource} ${__exists__ ? '' : 'not'} exists`)
    this.send(`${this.name}:${__exists__ ? 'success' : 'error'}`)
  }

}

export default function (win, store) {
  return async function (_event, options) {
    const handler = new CheckResourcesHandler(win, store, options)
    await handler.exists()
  }
}
