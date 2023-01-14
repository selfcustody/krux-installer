import { exists, readFile } from 'fs'
import { promisify } from 'util'
//import { join } from 'path'
import { expect as expectChai } from 'chai'
import { expect as expectWDIO } from '@wdio/globals'
import { name, version } from '../../package.json'
import App from '../pageobjects/app.page'
import Logo from '../pageobjects/logo.page'
import Main from '../pageobjects/main.page'

const existsAsync = promisify(exists)
const readFileAsync = promisify(readFile)

// eslint-disable-next-line no-undef
describe('KruxInstaller', () => {


  // eslint-disable-next-line no-undef
  describe('Initialization', () => {

    // eslint-disable-next-line no-undef
    it('should created a \'krux-installer\' folder in \'documents\' directory', async () => {

      // eslint-disable-next-line no-undef
      let docsPath = ''
      if (process.platform === 'linux') {
        docsPath = `${process.env.HOME}/.config/${name}/config.json`
      }
      if (process.platform === 'win32') {
        docsPath = `${process.env.APPDATA}\\${name}\\config.json`
      }
      if (process.platform === 'darwin') {
        docsPath = `${process.env.HOME}/Library/Application Support/${name}/config.json`
      }

      console.log(docsPath)
      const existsConfig = await existsAsync(docsPath) 
      expectChai(existsConfig).to.equal(true)

    })

    // eslint-disable-next-line no-undef
    it('should launch with correct title', () => { 
      expectWDIO(App.title).toHaveText(name)
    })

    // eslint-disable-next-line no-undef
    it('should configuration file to be correct', async () => {

      let docsPath = ''
      if (process.platform === 'linux') {
        docsPath = `${process.env.HOME}/.config/${name}/config.json`
      }
      if (process.platform === 'win32') {
        docsPath = `${process.env.APPDATA}/${name}/config.json`
      }
      if (process.platform === 'darwin') {
        docsPath = `${process.env.HOME}/Library/Application Support/${name}/config.json`
      }

      const configString = await readFileAsync(docsPath, 'utf8')
      expectChai(configString).to.be.a('string')

      const config = JSON.parse(configString)
      expectChai(config).to.be.an('object')
      expectChai(config).to.have.property('appVersion', version)
      expectChai(config).to.have.property('resources')
      expectChai(config).to.have.property('os', process.platform) 

      const docs = 'Documents|Documentos|Documenten|Documenti|Unterlagen'
      if (process.platform === 'linux') {
        const regexp = new RegExp(`/home/[a-zA-Z0-9]+/(${docs})/${name}`, 'g')
        expectChai(config.resources).to.match(regexp)
        expectChai(config).to.have.property('isMac10', false)
      }
      if (process.platform === 'win32') {
        const regexp = new RegExp(`[A-Z]:\\Users\\[a-zA-Z0-9]+\\(${docs})\\${name}`, 'g')
        expectChai(config.resources).to.match(regexp)
        expectChai(config).to.have.property('isMac10', false)
      }
      if (process.platform === 'darwin') {
        const regexp = new RegExp(`/Users/[a-zA-Z0-9]+/(${docs})/${name}`, 'g')
        expectChai(config.resources).to.match(regexp)
        expectChai(config.os).to.be.equal('isMac10', false)
      }

      expectChai(config).to.have.property('versions')
      expectChai(config.versions).to.be.an('Array')
      expectChai(config.versions.length).to.equal(0)
      expectChai(config).to.have.property('version', 'Select version')
      expectChai(config).to.have.property('device', 'Select device')
      expectChai(config).to.have.property('sdcard') 
    })

  })

  // eslint-disable-next-line no-undef
  describe('Lateral logo', () => {

    // eslint-disable-next-line no-undef
    it('should have banner', () => { 
      expectWDIO(Logo.banner).toBeDisplayed()
    })

    // eslint-disable-next-line no-undef
    it('should have asciiart', () => { 
      expectWDIO(Logo.asciiart).toBeDisplayed()
      expectWDIO(Logo.asciiart).toHaveText([ 
        "     ██        ",
        "     ██        ",
        "     ██        ",
        "   ██████      ",
        "     ██        ",
        "     ██  ██    ",
        "     ██ ██     ",
        "     ████      ",
        "     ██ ██     ",
        "     ██  ██    ",
        "     ██   ██   "
      ].join('\n'))
    })

    // eslint-disable-next-line no-undef
    it('should have title text', () => {
      expectWDIO(Logo.title).toBeDisplayed()
      expectWDIO(Logo.title).toHaveText('Krux Installer')
    })
  })

  // eslint-disable-next-line no-undef
  describe('Main page', () => {

    // eslint-disable-next-line no-undef
    it('should to be displayed', () => {
      expectWDIO(Main.page).toBeDisplayed()
    })

    // eslint-disable-next-line no-undef
    describe('\'Select device\' Menu', () => {
      
      // eslint-disable-next-line no-undef
      it('should to be displayed', () => { 
        expectWDIO(Main.selectDeviceCard).toBeDisplayed() 
        expectWDIO(Main.selectDeviceCardSubtitle).toBeDisplayed() 
        expectWDIO(Main.selectDeviceButton).toBeDisplayed() 
      })

      // eslint-disable-next-line no-undef
      it('should subtitle have correct text', () => { 
        expectWDIO(Main.selectDeviceCardSubtitle).toHaveText(
          'Select between available devices (m5stickV, amigo, bit, dock)')
      })

      // eslint-disable-next-line no-undef
      it('should have a clickable button', () => {
        expectWDIO(Main.selectDeviceButton).toBeClickable()
      })

      // eslint-disable-next-line no-undef
      it('should button have correct initial text', async () => {
        const deviceButtonText = await Main.selectDeviceButton.$('span.v-btn__content').getText()  
        expectChai(deviceButtonText).to.be.equal(' SELECT DEVICE')
      })
    })


    // eslint-disable-next-line no-undef
    describe('\'Select version\' menu', () => {

      // eslint-disable-next-line no-undef
      it('should to be displayed', () => {
        expectWDIO(Main.selectVersionCard).toBeDisplayed() 
        expectWDIO(Main.selectVersionCardSubtitle).toBeDisplayed() 
        expectWDIO(Main.selectVersionButton).toBeDisplayed() 
      })

      // eslint-disable-next-line no-undef
      it('should subtitle have correct text', () => { 
        expectWDIO(Main.selectVersionCardSubtitle).toHaveText(
          'Select between selfcustody (official) or odudex (test) releases')
      })

      // eslint-disable-next-line no-undef
      it('should have a clickable button', () => {
        expectWDIO(Main.selectVersionButton).toBeClickable()
      })
    
      // eslint-disable-next-line no-undef
      it('should button have correct initial text', async () => {
        const versionButtonText = await Main.selectVersionButton.$('span.v-btn__content').getText() 
        expectChai(versionButtonText).to.be.equal(' SELECT VERSION')
      })
    })


    // eslint-disable-next-line no-undef
    describe('\'Flash\' menu', () => {
      
      // eslint-disable-next-line no-undef
      it('should to be displayed', () => {
        expectWDIO(Main.selectWriteCard).toBeDisplayed()
        expectWDIO(Main.selectWriteCardSubtitle).toBeDisplayed()
        expectWDIO(Main.selectWriteButton).toBeDisplayed()
      })

      // eslint-disable-next-line no-undef
      it('should subtitle have correct initial text', async () => {
        if (process.platform === 'linux') {      
          expectWDIO(Main.selectDeviceCardSubtitle).toHaveText('Flash to device with ktool-linux')
        }
        if (process.platform === 'win32') {
          expectWDIO(Main.selectDeviceCardSubtitle).toHaveText('Flash to device with ktool-win.exe')
        }
        if (process.platform === 'darwin') {
          expectWDIO(Main.selectDeviceCardSubtitle).toHaveText('Flash to device with ktool-mac')
        }
      })
    
      // eslint-disable-next-line no-undef
      it('should have a clickable button', () => {
        expectWDIO(Main.selectWriteButton).toBeClickable()
      })

      // eslint-disable-next-line no-undef
      it('should button have correct initial text', async () => {
        const writeButtonText = await Main.selectWriteButton.$('span.v-btn__content').getText() 
        expectChai(writeButtonText).to.be.equal(' FLASH')
      })
    })
  })
})
