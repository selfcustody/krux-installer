import { exists } from 'fs'
import { promisify } from 'util'
import { join } from 'path'
import { expect as expectChai } from 'chai'
import { name } from '../../../package.json'
import { expect as expectWDIO } from '@wdio/globals'
import delay from '../delay'
import Main from '../../pageobjects/main.page'
import SelectVersion from '../../pageobjects/select-version.page'
import DownloadOfficialRelease from '../../pageobjects/download-official-release.page'

const existsAsync = promisify(exists)

// eslint-disable-next-line no-undef
describe('SelectVersionPage: download \'selfcustody/krux/releases/tag/v22.03.0\' option', () => {
 
  // eslint-disable-next-line no-undef
  before(async () => {
    await Main.selectVersionButton.click()
    await SelectVersion.cardTitleChecked.waitForExist({ timeout: 5000 }) 
    await delay(1000)
    await SelectVersion.formArrow.click()
    await delay(1000)
    await SelectVersion.list_item_22_03_0.waitForExist({ timeout: 5000 })
    await delay(1000)
  })

  // eslint-disable-next-line no-undef
  it('should be selected', async () => {    
    await SelectVersion.list_item_22_03_0.click()
    await expectWDIO(SelectVersion.formSelected).toHaveText('selfcustody/krux/releases/tag/v22.03.0')
    await delay(1000)
  })

  // eslint-disable-next-line no-undef
  it('should click \'select\' and start to download', async () => {   
    await SelectVersion.formSelectButton.click() 
    await DownloadOfficialRelease.page.waitForExist({ timeout: 5000 })
    await delay(1000)
  })

  // eslint-disable-next-line no-undef
  it('should card title be \'Downloading...\'', async () => {
    await expectWDIO(DownloadOfficialRelease.cardTitle).toHaveText('Downloading...')
  })

  // eslint-disable-next-line no-undef
  it('should card subtitle be \'selfcustody/krux/releases/download/v22.03.0/krux-v22.03.0.zip\'', async () => { 
    await expectWDIO(DownloadOfficialRelease.cardSubtitle)
      .toHaveText('selfcustody/krux/releases/download/v22.03.0/krux-v22.03.0.zip')
  })

  // eslint-disable-next-line no-undef
  it('should download release zip file', async () => {
    await DownloadOfficialRelease.progressLinearText.waitUntil(async function () {
      const percentText = await this.getText()
      const percent = parseFloat(percentText.split('%')[0])
      return percent > 90.0
    }, {
      timeout: 60000,
      interval: 50
    })
    await DownloadOfficialRelease.page.waitForExist({ reverse: true })
  })

  // eslint-disable-next-line no-undef
  it('should have downloaded release zip file on disk', async () => {
    const api = await browser.electronAPI()
    const zip = join(api.documents, name, 'v22.03.0', 'krux-v22.03.0.zip')
    const exists = await existsAsync(zip)
    expectChai(exists).to.be.equal(true)
  })
})
