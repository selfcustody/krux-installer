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
    }
  }
}