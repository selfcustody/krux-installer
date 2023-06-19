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
import onCheckVerifyReleaseHash from './utils/onCheckVerifyReleaseHash';
import onSelectPage from './utils/onSelectPage';
import onGithubCheck from './utils/onGithubCheck';
import onCameFromCheckResourcesOfficialRelease from './utils/onCameFromCheckResourcesOfficialRelease';
import onCameFromCheckVerifyOfficialRelease from './utils/onCameFromCheckVerifyOfficialRelease';
import onCameFromWarningDownload from './utils/onCameFromWarningDownload';
import onDownloadOfficialRelease from './utils/onDownloadOfficialRelease';
import onVerifyReleaseHash from './utils/onVerifyReleaseHash'
import onVerifyReleaseSign from './utils/onVerifyReleaseSign'
import onErrorMsg from './utils/onErrorMsg'

/**
 * Reference for which component will be used as showing page
 */
const page: Ref<string> = ref('')

/**
 * Arbitrary data to dynamic component for page
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
 * Generalized Rprocedure to redirects to ErrorMsg page
 * @param _ 
 * @param result 
 */
function onError (_: Event, result: Record<'name' | 'message' | 'stack', any>): void  {
  onErrorMsg(data, result)
}

function onKruxChangePage (_: Event, result: Record<'page', string>) {
  page.value = result.page
}

/**
 * Setup `data` and/or redirects to a `page`, or invoke another api call
 */
async function onKruxStoreGet (_: Event, result: Record<'from' | 'key' | 'values', any>) {
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
  await onCheckVerifyReleaseHash(result)
}

/**
 * Setup `data` for SelectDevice and SelectVersion Pages
 */
function onKruxStoreSet (_: Event, result: Record<'from' | 'key' | 'value', any>) {
  onSelectPage(data, result, { page: 'SelectDevice' })
  onSelectPage(data, result, { page: 'SelectVersion' })
}

async function onKruxVerifyReleasesFetch (_event: Event, result: Record<'from' | 'key' | 'value', any>) {
  await onGithubCheck(data, result)
}

async function onKruxCheckResource (_: Event, result: Record<'from' | 'exists' | 'baseUrl' | 'resourceFrom' | 'resourceTo', any>) {
  await onCameFromCheckResourcesOfficialRelease(data, result, { from: 'Zip',    proceedTo: 'Sha256', abbreviated: true })
  await onCameFromCheckResourcesOfficialRelease(data, result, { from: 'Sha256', proceedTo: 'Sig',    abbreviated: true })
  await onCameFromCheckResourcesOfficialRelease(data, result, { from: 'Sig',    proceedTo: 'Pem',    abbreviated: true })
  await onCameFromCheckResourcesOfficialRelease(data, result, { from: 'Pem',    proceedTo: 'CheckVerifyOfficialRelease', abbreviated: false })
  await onCameFromCheckVerifyOfficialRelease(data, result)
  await onCameFromWarningDownload(data, result)
}

/**
 * When download finishes, redirect it:
 * - DownloadOfficialReleaseZip --> CheckResourcesOfficialReleaseSha256
 * - DownloadOfficialReleaseSha256 --> CheckResourcesOfficialReleaseSig
 * - DownloadOfficialReleaseSig --> CheckResourcesOfficialReleasePem
 * - DownloadOfficialReleasePem --> VerifyOfficialRelease
 */
async function onKruxDownloadResources (_: Event, result: Record<'from', string>) {
  onDownloadOfficialRelease(result, { from: 'DownloadOfficialReleaseZip',    to: 'CheckResourcesOfficialReleaseSha256' })
  onDownloadOfficialRelease(result, { from: 'DownloadOfficialReleaseSha256', to: 'CheckResourcesOfficialReleaseSig' })
  onDownloadOfficialRelease(result, { from: 'DownloadOfficialReleaseSig',    to: 'CheckResourcesOfficialReleasePem' })
  onDownloadOfficialRelease(result, { from: 'DownloadOfficialReleasePem',    to: 'CheckVerifyOfficialRelease'})
}

async function onKruxVerifyReleasesHash (_: Event, result: any) {
  onVerifyReleaseHash(data, result)
}

async function onKruxVerifyReleaseSign (_: Event, result: any) {
  onVerifyReleaseSign(data, result)
}

/**
 * Stream progress when download resources
 */
function onKruxDownloadResourcesData (_: Event, result: any) {
  data.value.progress = result
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

window.api.onSuccess('krux:change:page', onKruxChangePage);
window.api.onSuccess('krux:store:get', onKruxStoreGet);
window.api.onSuccess('krux:store:set', onKruxStoreSet);
window.api.onSuccess('krux:verify:releases:fetch', onKruxVerifyReleasesFetch)
window.api.onSuccess('krux:check:resource', onKruxCheckResource)
window.api.onSuccess('krux:download:resources', onKruxDownloadResources)
window.api.onSuccess('krux:verify:releases:hash', onKruxVerifyReleasesHash)
window.api.onSuccess('krux:verify:releases:sign', onKruxVerifyReleaseSign)
window.api.onData('krux:download:resources', onKruxDownloadResourcesData)
window.api.onError('krux:change:page', onError)
window.api.onError('krux:store:get', onError)
window.api.onError('krux:store:set', onError)
window.api.onError('krux:verify:openssl', onError)
window.api.onError('krux:verify:releases:fetch', onError)
window.api.onError('krux:check:resource',onError)
window.api.onError('krux:download:resources', onError)

/**
 * Mounted
 */
onMounted(async function () {
  await window.api.invoke('krux:change:page', { page: 'KruxInstallerLogo' })
})
</script>