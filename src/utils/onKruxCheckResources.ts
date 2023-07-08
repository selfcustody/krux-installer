import { Ref } from "vue"
import messages from "./messages"

async function onResourceExist (
  data: Ref<Record<string, any>>,
  result: Record<'from' | 'exists' | 'baseUrl' | 'resourceFrom' | 'resourceTo', any>
) {
  let checked
  if (result.resourceTo.match(/^.*(zip|sha256.txt|sig|pem)$/g)){
    checked = result.resourceTo.split('krux-installer/')[1]
  } else if (result.resourceTo.match(/^.*(firmware|kboot|ktool).*$/g)) {
    checked = result.resourceTo.split('/main/')[1]
  }
  await messages.add(data, `${checked} found`)
  data.value.proceedTo = 'ConsoleLoad'
  data.value.backTo = 'GithubChecker'
  await messages.close(data)
  await window.api.invoke('krux:change:page', { page: 'WarningDownload' })
}

async function onResourceNotExist (
  data: Ref<Record<string, any>>,
  result: Record<'from' | 'exists' | 'baseUrl' | 'resourceFrom' | 'resourceTo', any>,
  page: string
) {
  let checked
  if (result.resourceTo.match(/^.*(zip|sha256.txt|sig|pem)$/g)){
    checked = result.resourceTo.split('krux-installer/')[1]
  } else if (result.resourceTo.match(/^.*(firmware|kboot|ktool).*$/g)) {
    checked = result.resourceTo.split('/main/')[1]
  }
  await messages.add(data, `${checked} not found`)
  data.value.progress = 0.0
  await messages.close(data)
  await window.api.invoke('krux:change:page', { page: page })
}

async function onDownloadAgain (
  data: Ref<Record<string, any>>,
  result: Record<'from' | 'exists' | 'baseUrl' | 'resourceFrom' | 'resourceTo', any>,
  page: string
) {
  data.value.progress = 0.0
  await messages.close(data)
  await window.api.invoke('krux:change:page', { page: page })
}

export default function (data: Ref<Record<string, any>>): Function {
  return async function (
    _: Event,
    result: Record<'from' | 'exists' | 'baseUrl' | 'resourceFrom' | 'resourceTo', any>
  ): Promise<void> {
    data.value.baseUrl = result.baseUrl
    data.value.resourceFrom = result.resourceFrom
    data.value.resourceTo = result.resourceTo

    // When user decides between official
    // or test releaases
    if (result.from === 'SelectVersion' ) { 
      if (result.exists) {
        await onResourceExist(data, result)
      } else {
        if (result.baseUrl.match(/selfcustody/g)) {
          await onResourceNotExist(data, result, 'DownloadOfficialReleaseZip')
        }
        if (result.resourceFrom.match(/odudex\/krux_binaries/g)){
          await onResourceNotExist(data, result, 'DownloadTestFirmware')
        }
      }
    }


    // When user decides for official release
    // and checked zip file to redirect to sha256.txt file
    if (
      result.from === 'DownloadOfficialReleaseZip' ||
      result.from.match(/^WarningDownload::.*.zip$/)
    ) {
      if (result.exists) {
        await onResourceExist(data, result)
      } else {
        await onResourceNotExist(data, result, 'DownloadOfficialReleaseSha256')
      }
    }

    // When user decides for official release
    // and checked zip.sha256.txt file to redirect to zip.sig file
    if (
      result.from === 'DownloadOfficialReleaseSha256' ||
      result.from.match(/^WarningDownload::.*.zip.sha256.txt$/)
    ) {
      if (result.exists) {
        await onResourceExist(data, result)
      } else {
        await onResourceNotExist(data, result, 'DownloadOfficialReleaseSig')
      }
    }

    // When user decides for official release
    // and checked zip.sig file to redirect to .pem file
    if (
      result.from === 'DownloadOfficialReleaseSig' ||
      result.from.match(/^WarningDownload::.*.zip.sig$/)
    ) {
      if (result.exists) {
        await onResourceExist(data, result)
      } else {
        await onResourceNotExist(data, result, 'DownloadOfficialReleasePem')
      }
    }

    if (result.from === 'CheckVerifyOfficialRelease') {
      data.value = {}
    }

    if (
      result.from === 'DownloadTestFirmware' ||
      result.from.match(/^WarningDownload::.*firmware.bin$/)
    ) {
      if (result.exists) {
        await onResourceExist(data, result)
      } else {
        await onResourceNotExist(data, result, 'DownloadTestKboot')
      }
    }

    if (
      result.from === 'DownloadTestKboot' ||
      result.from.match(/^WarningDownload::.*kboot.kfpkg$/)
    ) {
      if (result.exists) {
        await onResourceExist(data, result)
      } else {
        await onResourceNotExist(data, result, 'DownloadTestKtool')
      }
    }

    if (
      result.from === 'DownloadTestKtool' ||
      result.from.match(/^WarningDownload::.*ktool-(linux|win.exe|mac|mac-10)$/)
    ) {
      if (result.exists) {
        await onResourceExist(data, result)
      } else {
        await onResourceNotExist(data, result, 'Main')
      }
    }

    // ====================================================
    // Warning Cycle: when user decide to re-download files
    // ====================================================

    if (result.from.match(/^Again::WarningDownload::.*.zip$$/)) {
      await onDownloadAgain(data, result, 'DownloadOfficialReleaseZip')
    }

    if (result.from.match(/^Again::WarningDownload::.*.zip.sha256.txt$/)) {
      await onDownloadAgain(data, result, 'DownloadOfficialReleaseSha256')
    }

    if (result.from.match(/^Again::WarningDownload::.*.zip.sig$/)) {
      await onDownloadAgain(data, result, 'DownloadOfficialReleaseSig')
    }

    if (result.from.match(/^Again::WarningDownload::.*.pem$/)) {
      await onDownloadAgain(data, result, 'DownloadOfficialReleasePem')
    }

    if (result.from.match(/^Again::WarningDownload::.*firmware.bin$/)) {
      await onDownloadAgain(data, result, 'DownloadTestFirmware')
    }

    if (result.from.match(/^Again::WarningDownload::.*kboot.kfpkg$/)) {
      await onDownloadAgain(data, result, 'DownloadTestKboot')
    }

    if (result.from.match(/^Again::WarningDownload::.*ktool-(linux|win.exe|mac|mac-10)$/)) {
      await onDownloadAgain(data, result, 'DownloadTestKtool')
    }
  }
}