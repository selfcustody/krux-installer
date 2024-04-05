import { Ref } from "vue"

function wipeOrFlash(data: Ref<Record<string, any>>, kind: string): string {
  let click = ''
  if (data.value.os === 'linux') {
    click =  `${kind} with ktool-linux`
  }
  else if (data.value.os === 'win32') {
    click = `${kind} with ktool-win.exe`
  }
  else if (data.value.os === 'darwin' && !data.value.isMac10) {
    click = `${kind} with ktool-mac`
  }
  else if (data.value.os === 'darwin' && data.value.isMac10) {
    click = `${kind} with ktool-mac-10`
  }
  return click
}

export default function (data: Ref<Record<string, any>>): Function {
  return function (_: Event, result: Record<'showFlash', boolean>): void {
    data.value.showFlash = result.showFlash
    if (!data.value.showFlash && data.value.device !== 'Select device') {
      if (data.value.version === 'Select version') {
        if(data.value.showWipe) {
          const click = wipeOrFlash(data, 'Wipe')
          data.value.clickMessage = `Click 'Select version' or '${click}'`
        } else {
          data.value.clickMessage = `Click 'Select version'`
        }
      } else {
        const click = wipeOrFlash(data, 'Wipe')
        data.value.clickMessage = `Click 'Version: ${data.value.version}' or ${click} for ${data.value.device}`
      }
    } else {
      const click = wipeOrFlash(data, 'Wipe/Flash')
      data.value.clickMessage = `Connect your ${data.value.device} device and power on it before click '${click}'`
    }
  }
}
