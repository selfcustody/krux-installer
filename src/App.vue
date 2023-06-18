<template>
  <v-layout>
    <v-main>
      <component :is="pages[page]" v-bind="data" />
    </v-main>
  </v-layout>
</template>

<script setup lang="ts">
import { Ref, ref, shallowRef, onMounted } from 'vue';

// pages
import KruxInstallerLogo from './pages/KruxInstallerLogo.vue';
import ErrorMsg from './pages/ErrorMsg.vue';
import Main from './pages/Main.vue';
import SelectDevice from './pages/SelectDevice.vue';
import SelectVersion from './pages/SelectVersion.vue';
import GithubChecker from './pages/GithubChecker.vue';
import CheckResources from './pages/CheckResources.vue';
import WarningDownload from './pages/WarningDownload.vue';
import CheckResourcesOfficialReleaseZip from './pages/CheckResourcesOfficialReleaseZip.vue';
import DownloadOfficialReleaseZip from './pages/DownloadOfficialReleaseZip.vue';
import CheckResourcesOfficialReleaseSha256 from './pages/CheckResourcesOfficialReleaseSha256.vue';
import DownloadOfficialReleaseSha256 from './pages/DownloadOfficialReleaseSha256.vue';
import CheckResourcesOfficialReleaseSig from './pages/CheckResourcesOfficialReleaseSig.vue';
import DownloadOfficialReleaseSig from './pages/DownloadOfficialReleaseSig.vue';
import CheckResourcesOfficialReleasePem from './pages/CheckResourcesOfficialReleasePem.vue';
import DownloadOfficialReleasePem from './pages/DownloadOfficialReleasePem.vue';
import CheckVerifyOfficialRelease from './pages/CheckVerifyOfficialRelease.vue';
import VerifiedOfficialRelease from './pages/VerifiedOfficialRelease.vue';

// methods
import setupDataToMainPage from './utils/setupDataToMainPage';
import onCheckResources from './utils/onCheckResources';
import onCheckResourcesOfficial from './utils/onCheckResourcesOfficial';
import onVerifyHash from './utils/onVerifyHash';
import onSelectPage from './utils/onSelectPage';
import onGithubCheck from './utils/onGithubCheck';
import onCameFromCheckResourcesOfficialRelease from './utils/onCameFromCheckResourcesOfficialRelease';
import onCameFromCheckVerifyOfficialRelease from './utils/onCameFromCheckVerifyOfficialRelease';
import onCameFromWarningDownload from './utils/onCameFromWarningDownload';
import onDownloadOfficialRelease from './utils/onDownloadOfficialRelease';

/**
 * Reference for which page will be shown
 */
const page: Ref<string> = ref('')

/**
 * Arbitrary data to dynamic component
 */
const data: Ref<Record<string, any>> = ref({})

/**
 * Register individual components, as pages, for dynamic tagging.
 * 
 * This works like the legacy approach:
 * 
 * @example
 * ```js
 * export default defineComponent({
 *  components: { ... }
 * })
 * ```
 * @see https://stackoverflow.com/questions/71627355/dynamic-components-doesnt-work-in-script-setup
 */
const pages: Ref<Record<string, any>> = shallowRef({
  'KruxInstallerLogo': KruxInstallerLogo,
  'ErrorMsg': ErrorMsg,
  'Main': Main,
  'SelectDevice': SelectDevice,
  'GithubChecker': GithubChecker,
  'SelectVersion': SelectVersion,
  'CheckResources': CheckResources,
  'WarningDownload': WarningDownload,
  'CheckResourcesOfficialReleaseZip': CheckResourcesOfficialReleaseZip,
  'DownloadOfficialReleaseZip': DownloadOfficialReleaseZip,
  'CheckResourcesOfficialReleaseSha256': CheckResourcesOfficialReleaseSha256,
  'DownloadOfficialReleaseSha256': DownloadOfficialReleaseSha256,
  'CheckResourcesOfficialReleaseSig': CheckResourcesOfficialReleaseSig,
  'DownloadOfficialReleaseSig': DownloadOfficialReleaseSig,
  'CheckResourcesOfficialReleasePem': CheckResourcesOfficialReleasePem,
  'DownloadOfficialReleasePem': DownloadOfficialReleasePem,
  'CheckVerifyOfficialRelease': CheckVerifyOfficialRelease,
  'VerifiedOfficialRelease': VerifiedOfficialRelease
}) 

/**
 * Redirects to ErrorMsg page
 * @param _ 
 * @param result 
 */
function onError (_: Event, result: Record<'name' | 'message' | 'data' | 'stack', any>): void  {
  page.value = 'ErrorMsg'
  data.value = result.data
}

async function onVerifyReleaseHash (result: Record<'name' | 'value', string>[]): Promise<void> {
  data.value = {
    hash: result
  }
  await window.api.invoke('krux:verify:releases:sign')
}

async function onVerifyOpensslError(result: Record<'name' | 'message' | 'stack', any>): Promise<void> {
  data.value = {
    ...result,
    backTo: 'Main'
  }
  await window.api.invoke('krux:change:page', { page: 'ErrorMsg' })
}

async function onVerifyReleaseSign (result: Record<'command' | 'sign', any>): Promise<void> {
  data.value.command = result.command
  data.value.sign = result.sign
  await window.api.invoke('krux:change:page', { page: 'VerifiedOfficialRelease' })
}

/**
 * ================================================
 * API EVENT LISTENERS (IPC RENDERER)
 * All application events should be configured here
 * to avoid multiple calls of registered events
 * ================================================
 * * onSuccess: Channels that have the post-fixed word 'success' in `lib/*.ts` finished calls
 * * onError: Channels that have the post-fixed word 'error' in `lib/*.ts` finished calls
 * * onData: Channels that have the post-fixed word 'data' in `lib/*.ts` streaming calls 
 */

window.api.onSuccess('krux:change:page', (_: Event, result: Record<'page', string>) => {
  page.value = result.page as string
})

/**
 * Setup `data` and/or redirects to a `page`, or invoke another api call
 */
window.api.onSuccess('krux:store:get', async function (_: Event, result: Record<'from' | 'key' | 'values', any>) {
  setupDataToMainPage(data, result, {
    when: [
      'KruxInstallerLogo',
      'SelectVersion',
      'VerifiedOfficialRelease',
      'ErrorMsg'
    ]
  })
  await onCheckResources(result, [
    { match: /selfcustody\/.*/g, goto: 'CheckResourcesOfficialReleaseZip' } ,
    { match: /odudex\/.*/g,      goto: 'CheckResourcesTestFirmware' }
  ])
  await onCheckResourcesOfficial(result)
  await onVerifyHash(result)
})

window.api.onSuccess('krux:store:set', (_: Event, result: Record<'from' | 'key' | 'value', any>) => {
  onSelectPage(data, result, { page: 'SelectDevice' })
  onSelectPage(data, result, { page: 'SelectVersion' })
})


window.api.onSuccess('krux:verify:releases:fetch', async (_event: Event, result: Record<'from' | 'key' | 'value', any>) => {
  await onGithubCheck(data, result)
})

window.api.onSuccess('krux:check:resource', async (_: Event, result: Record<'from' | 'exists' | 'baseUrl' | 'resourceFrom' | 'resourceTo', any>) => {
  await onCameFromCheckResourcesOfficialRelease(data, result, { from: 'Zip',    proceedTo: 'Sha256', abbreviated: true })
  await onCameFromCheckResourcesOfficialRelease(data, result, { from: 'Sha256', proceedTo: 'Sig',    abbreviated: true })
  await onCameFromCheckResourcesOfficialRelease(data, result, { from: 'Sig',    proceedTo: 'Pem',    abbreviated: true })
  await onCameFromCheckResourcesOfficialRelease(data, result, { from: 'Pem',    proceedTo: 'CheckVerifyOfficialRelease', abbreviated: false })
  await onCameFromCheckVerifyOfficialRelease(data, result)
  await onCameFromWarningDownload(data, result)
})

/**
 * When download finishes, redirect it:
 * - DownloadOfficialReleaseZip --> CheckResourcesOfficialReleaseSha256
 * - DownloadOfficialReleaseSha256 --> CheckResourcesOfficialReleaseSig
 * - DownloadOfficialReleaseSig --> CheckResourcesOfficialReleasePem
 * - DownloadOfficialReleasePem --> VerifyOfficialRelease
 */
window.api.onSuccess('krux:download:resources', async (_: Event, result: Record<'from', string>) => {
  onDownloadOfficialRelease(result, { from: 'DownloadOfficialReleaseZip',    to: 'CheckResourcesOfficialReleaseSha256' })
  onDownloadOfficialRelease(result, { from: 'DownloadOfficialReleaseSha256', to: 'CheckResourcesOfficialReleaseSig' })
  onDownloadOfficialRelease(result, { from: 'DownloadOfficialReleaseSig',    to: 'CheckResourcesOfficialReleasePem' })
  onDownloadOfficialRelease(result, { from: 'DownloadOfficialReleasePem',    to: 'CheckVerifyOfficialRelease'})
})

/**
 * Verification (sha256sum)
 */
window.api.onSuccess('krux:verify:releases:hash', async (_: Event, result: any) => {
  onVerifyReleaseHash(result)
})

/**
 * Verification (signature)
 */
window.api.onSuccess('krux:verify:releases:sign', async (_: Event, result: any) => {
  onVerifyReleaseSign(result)
})

/**
 * 
 */
window.api.onData('krux:download:resources', (_: Event, result: any) => {
  data.value.progress = result
})

/**
 * onError listeners
 * 
 * Channels that have the post-fixed word 'error' 
 */
window.api.onError('krux:change:page', onError)
window.api.onError('krux:store:get', onError)
window.api.onError('krux:store:set', onError)
window.api.onError('krux:verify:openssl', async (_: Event, result: Record<'name' | 'message' | 'stack', any>) => {
  onVerifyOpensslError(result)
})

window.api.onError('krux:verify:releases:fetch', async (_: Event, result: any) => {
  data.value = {
    ...result,
    backTo: 'Main'
  }
  await window.api.invoke('krux:change:page', {
    page: 'ErrorMsg'
  })
})

window.api.onError('krux:check:resource', async (_: Event, result: any) => {
  data.value = {
    ...result,
    backTo: 'Main'
  }
  await window.api.invoke('krux:change:page', {
    page: 'ErrorMsg',
  })
})

window.api.onError('krux:download:resources', async (_: Event, result: any) => {
  data.value = {
    ...result,
    backTo: 'Main'
  }
  await window.api.invoke('krux:change:page', {
    page: 'ErrorMsg'
  })
})

/**
 * Mounted
 */
onMounted(async function () {
  await window.api.invoke('krux:change:page', { page: 'KruxInstallerLogo' })
})
</script>