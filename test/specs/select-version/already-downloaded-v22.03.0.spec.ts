import { exists, stat } from 'fs'
import { promisify } from 'util'
import { join } from 'path'
import { expect as expectChai } from 'chai'
import { name } from '../../../package.json'
import { expect as expectWDIO } from '@wdio/globals'
import delay from '../delay'
import formatBytes from '../format-bytes'
import Main from '../../pageobjects/main.page'
import SelectVersion from '../../pageobjects/select-version.page'
import CheckResourcesOfficialRelease from '../../pageobjects/check-resources-official-release.page'

const existsAsync = promisify(exists)
const statAsync = promisify(stat)

// eslint-disable-next-line no-undef
describe('SelectVersionPage: warn before download \'selfcustody/krux/releases/tag/v22.03.0\' again', () => {
  
  let api
  let dir
  let zip

  // eslint-disable-next-line no-undef
  before(async () => {
    // eslint-disable-next-line no-undef
    api = await browser.electronAPI()
    dir = join(api.documents, name, 'v22.03.0')
    zip = join(dir, 'krux-v22.03.0.zip')
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
    await SelectVersion.formSelectButton.waitForExist()
    await SelectVersion.formSelectButton.click()  
    await SelectVersion.page.waitForExist({ reverse: true }) 
    await CheckResourcesOfficialRelease.page.waitForExist() 
    await CheckResourcesOfficialRelease.cardTitleChecking.waitForExist()
    await CheckResourcesOfficialRelease.cardTitleChecking.waitForExist({ reverse: true }) 
    await CheckResourcesOfficialRelease.cardTitleChecked.waitForExist()
    await CheckResourcesOfficialRelease.cardSubtitleChecked.waitForExist()
    await CheckResourcesOfficialRelease.cardContentChecked.waitForExist()
    await CheckResourcesOfficialRelease.buttonDownload.waitForExist()
    await CheckResourcesOfficialRelease.buttonProceed.waitForExist()
    await delay(1000)
  })

    
  // eslint-disable-next-line no-undef
  it('should card title be \'v22.03.0/krux-v22.03.0.zip\'', async () => {
    await expectWDIO(CheckResourcesOfficialRelease.cardTitleChecked).toHaveText('v22.03.0/krux-v22.03.0.zip')
  })

  // eslint-disable-next-line no-undef
  it('should card subtitle be \'Already downloaded\'', async () => {
    await expectWDIO(CheckResourcesOfficialRelease.cardSubtitleChecked).toHaveText('Already downloaded')
  })

  // eslint-disable-next-line no-undef
  it('should have downloaded release zip file on disk', async () => {
    const zipExists = await existsAsync(zip)
    expectChai(zipExists).to.be.equal(true)
  })

  // eslint-disable-next-line no-undef
  it('should downloaded release zip file on disk have correct size', async () => {
    const zipStat = await statAsync(zip)
    const bytes = formatBytes(zipStat.size)
    expectChai(bytes).to.be.equal('31.4 MB')
  })

  // eslint-disable-next-line no-undef
  it('should card content be \'Click "Download" to download again or "Proceed" to proceed with the downloaded version.\'', async () => {
    await expectWDIO(CheckResourcesOfficialRelease.cardContentChecked)
      .toHaveText('Click "Download" to download again or "Proceed" to proceed with the downloaded version.')
  })

  // eslint-disable-next-line no-undef
  it('should have a \'DOWNLOAD\' button', async () => { 
    await expectWDIO(CheckResourcesOfficialRelease.buttonDownload).toHaveText('DOWNLOAD')
  })

  // eslint-disable-next-line no-undef
  it('should have a \'PROCEED\' button', async () => { 
    await expectWDIO(CheckResourcesOfficialRelease.buttonProceed).toHaveText('PROCEED')
  })
})
