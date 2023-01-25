import { exists, stat } from 'fs'
import { promisify } from 'util'
import { join } from 'path'
import { expect as expectChai } from 'chai'
import { name } from '../../../package.json'
import { expect as expectWDIO } from '@wdio/globals'
import delay from '../delay'
import Main from '../../pageobjects/main.page'
import SelectVersion from '../../pageobjects/select-version.page'
import CheckResourcesOfficialRelease from '../../pageobjects/check-resources-official-release.page'
import DownloadOfficialRelease from '../../pageobjects/download-official-release.page'

const existsAsync = promisify(exists)
const statAsync = promisify(stat)

// Correct way to convert size in bytes to KB, MB, GB in JavaScript
// https://gist.github.com/lanqy/5193417?permalink_comment_id=4225701#gistcomment-4225701
function formatBytes(bytes: number): string {
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
  if (bytes === 0) return 'n/a';
  const i = Math.min(Math.floor(Math.log(bytes) / Math.log(1024)), sizes.length - 1);
  if (i === 0) return `${bytes} ${sizes[i]}`;
  return `${(bytes / (1024 ** i)).toFixed(1)} ${sizes[i]}`;
}

// eslint-disable-next-line no-undef
describe('SelectVersionPage: download \'selfcustody/krux/releases/tag/v22.03.0\' option', () => {
 
  // eslint-disable-next-line no-undef
  before(async () => {
    await Main.selectVersionButton.waitForExist()
    await delay(1000)
    await Main.selectVersionButton.click()
    await SelectVersion.cardTitleChecking.waitForExist()
    await delay(1000)
    await SelectVersion.cardTitleChecked.waitForExist()  
    await SelectVersion.cardSubtitleOfficial.waitForExist()  
    await SelectVersion.cardSubtitleTest.waitForExist()  
    await SelectVersion.formArrow.waitForExist()
    await SelectVersion.formBackButton.waitForExist()  
    await delay(1000)
    await SelectVersion.formArrow.click()
    await delay(1000)
    await SelectVersion.list_item_22_03_0.waitForExist()
    await SelectVersion.list_item_22_08_0.waitForExist()
    await SelectVersion.list_item_22_08_1.waitForExist()
    await SelectVersion.list_item_22_08_2.waitForExist()
    await SelectVersion.list_item_krux_binaries.waitForExist()
    await delay(1000) 
    await SelectVersion.list_item_22_03_0.click()
  })

  // eslint-disable-next-line no-undef
  it('should be selected', async () => {    
    await expectWDIO(SelectVersion.formSelected).toHaveText('selfcustody/krux/releases/tag/v22.03.0')
  })

  describe('download zip release', () => {

    // eslint-disable-next-line no-undef
    before(async () => {
      await SelectVersion.formSelectButton.waitForExist()
      await SelectVersion.formSelectButton.click() 
      await DownloadOfficialRelease.page.waitForExist()
      await delay(1000)
    })

    // eslint-disable-next-line no-undef
    it('should card title be \'Downloading...\'', async () => {
      await expectWDIO(DownloadOfficialRelease.cardTitle).toHaveText('Downloading...')
    })

    // eslint-disable-next-line no-undef
    it('should card subtitle be \'selfcustody/krux/releases/download/v22.03.0/krux-v22.03.0.zip\'', async () => { 
      await expectWDIO(DownloadOfficialRelease.cardSubtitle).toHaveText('selfcustody/krux/releases/download/v22.03.0/krux-v22.03.0.zip')
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

    // eslint-disable-next-line no-undef
    it('should downloaded release zip file on disk have correct size', async () => {
      const api = await browser.electronAPI()
      const zip = join(api.documents, name, 'v22.03.0', 'krux-v22.03.0.zip')
      const zipStat = await statAsync(zip)
      const bytes = formatBytes(zipStat.size)
      expectChai(bytes).to.be.equal('31.4 MB')
    })
  })
})
