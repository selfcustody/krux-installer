import axios from 'axios'
import Handler from './base'

export default class VerifyOfficialReleasesHandler extends Handler {

  constructor (win, store) {
    super(win)
    this.url = 'https://api.github.com/repos/selfcustody/krux/git/refs/tags'
    this.headers = {
      'User-Agent': `Chrome/${process.versions.chrome}`
    }
    this.store = store
  }

  async fetchReleases() {
    try {
      this.send('window:log:info', `fetching ${this.url}`)
      const response = await axios({
        method: 'get',
        url: this.url,
        headers: this.headers
      })
      if (response.status === 200) {
        return response.data
      } else {
        throw new Error(`${this.url} returned ${response.status} code`)
      }
    } catch (error) {
      throw error
    }
  }

}
