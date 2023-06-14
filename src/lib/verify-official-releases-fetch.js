'use strict'

import axios from 'axios'
import Handler from './base'

class VerifyOfficialReleasesFetchHandler extends Handler {

  constructor (win, store) {
    super('verify-official-releases-fetch', win, store)
    this.url = 'https://api.github.com/repos/selfcustody/krux/git/refs/tags'
    this.headers = {
      'User-Agent': `Chrome/${process.versions.chrome}`
    }
    this.store = store
  }

  async fetch() {
    try {
      this.log(`Fetching ${this.url}`)
      const response = await axios({
        method: 'get',
        url: this.url,
        headers: this.headers
      })
      if (response.status === 200) {
        this.log(response.data)
        this.releases = response.data
      } else {
        throw new Error(`${this.url} returned ${response.status} code`)
      }
    } catch (error) {
      this.log(error)
      this.send(`${this.name}:error`, error)
    }
  }

  save () {
    let list = this.store.get('versions')

    // verify for new releases if length of fetch is greater than the local list
    if (list.length === 0 || list.length < (Object.keys(this.releases)).length) {
      const __list__ = []
      const __v__ = this.releases[this.releases.length - 1]
      const version = __v__.ref.split('tags/')[1]
      __list__.push(`selfcustody/krux/releases/tag/${version}`)
      __list__.push('odudex/krux_binaries')
      this.store.set('versions', __list__)
      list = this.store.get('versions')
    }
    this.send(`${this.name}:success`, { releases: list })
  }

}


/**
 * Function to handle when
 * wants to verify official releases
 *
 * @param win
 * @apram store
 */
export default function (win, store) {
  // eslint-disable-next-line no-unused-vars
  return async function (_event, action) {
    const handler = new VerifyOfficialReleasesFetchHandler(win, store)
    await handler.fetch()
    handler.save()
  }
}
