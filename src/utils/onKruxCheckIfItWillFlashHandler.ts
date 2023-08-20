import { Ref } from "vue"

export default function (data: Ref<Record<string, any>>): Function {
  return function (_: Event, result: Record<'showFlash', boolean>): void {
    data.value.showFlash = result.showFlash
    if (!data.value.showFlash && data.value.device !== 'Select device') {
      if (data.value.version === 'Select version') {
        data.value.clickMessage = `Please click 'Select version' to download sources`
      } else {
        data.value.clickMessage = `Please click 'Version: ${data.value.version}' to download sources for ${data.value.device}`
      }
    } else {
      let click = ''
      if (data.value.os === 'linux') {
        click =  'Flash with ktool-linux'
      }
      else if (data.value.os === 'win32') {
        click = 'Flash with ktool-win.exe'
      }
      else if (data.value.os === 'darwin' && !data.value.isMac10) {
        click = 'Flash with ktool-mac'
      }
      else if (data.value.os === 'darwin' && data.value.isMac10) {
        click = 'Flash with ktool-mac-10'
      }
      data.value.clickMessage = `Connect your ${data.value.device} device and power on it before click '${click}'`
    }
  }
}