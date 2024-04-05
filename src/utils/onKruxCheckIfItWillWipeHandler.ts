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
  return function (_: Event, result: Record<'showWipe', boolean>): void {
    data.value.showWipe = result.showWipe
  }
}
