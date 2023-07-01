<template>
  <v-layout>
    <v-main>
      <component :is="pages[page]" v-bind="data" />
    </v-main>
  </v-layout>
</template>

<script setup lang="ts">
import { Ref, ref, shallowRef, onMounted } from 'vue';

/**
 * Pages: this components will be injected
 * in dynamic manner, see `pages` and `page` variable
 * for more information
 */
import KruxInstallerLogo from './pages/KruxInstallerLogo.vue';
import ConsoleLoad from './pages/ConsoleLoad.vue';
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
import CheckResourcesTestFirmware from './pages/CheckResourcesTestFirmware.vue';
import DownloadTestFirmware from './pages/DownloadTestFirmware.vue';
import CheckResourcesTestKboot from './pages/CheckResourcesTestKboot.vue';
import DownloadTestKboot from './pages/DownloadTestKboot.vue'
import CheckResourcesTestKtool from './pages/CheckResourcesTestKtool.vue';
import DownloadTestKtool from './pages/DownloadTestKtool.vue'

/**
 * Methods: These function will
 * manipulate `page` and `data` variables
 */
import onError from './utils/onError'
import onKruxVerifyOpenssl from './utils/onKruxVerifyOpenssl';
import onKruxChangePage from './utils/onKruxChangePage';
import onKruxStoreGet from './utils/onKruxStoreGet';
import onKruxStoreSet from './utils/onKruxStoreSet';
import onKruxVerifyReleasesFetch from './utils/onKruxVerifyReleasesFetch';
import onKruxCheckResources from './utils/onKruxCheckResources';
import onKruxDownloadResources from './utils/onKruxDownloadResources';
import onKruxVerifyReleasesHash from './utils/onKruxVerifyReleasesHash';
import onKruxVerifyReleaseSign from './utils/onKruxVerifyReleaseSign';
import onKruxDownloadResourcesData from './utils/onKruxDownloadResourcesData';
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
 * ```js
 * export default defineComponent({
 *  components: { ... }
 * })
 * ```
 * @see https://stackoverflow.com/questions/71627355/dynamic-components-doesnt-work-in-script-setup
 */
const pages: Ref<Record<string, any>> = shallowRef({
  'KruxInstallerLogo': KruxInstallerLogo,
  'ConsoleLoad': ConsoleLoad,
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
  'VerifiedOfficialRelease': VerifiedOfficialRelease,
  'CheckResourcesTestFirmware': CheckResourcesTestFirmware,
  'DownloadTestFirmware': DownloadTestFirmware,
  'CheckResourcesTestKboot': CheckResourcesTestKboot,
  'DownloadTestKboot': DownloadTestKboot,
  'CheckResourcesTestKtool': CheckResourcesTestKtool,
  'DownloadTestKtool': DownloadTestKtool
})

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
window.api.onSuccess('krux:change:page', onKruxChangePage(page));
window.api.onSuccess('krux:verify:openssl',onKruxVerifyOpenssl(data))
window.api.onSuccess('krux:store:get', onKruxStoreGet(data));
window.api.onSuccess('krux:store:set', onKruxStoreSet(data));
window.api.onSuccess('krux:verify:releases:fetch', onKruxVerifyReleasesFetch(data));
window.api.onSuccess('krux:check:resource', onKruxCheckResources(data));
window.api.onSuccess('krux:download:resources', onKruxDownloadResources(data));
window.api.onSuccess('krux:verify:releases:hash', onKruxVerifyReleasesHash(data));
window.api.onSuccess('krux:verify:releases:sign', onKruxVerifyReleaseSign(data));
window.api.onData('krux:download:resources', onKruxDownloadResourcesData(data));
window.api.onError('krux:change:page', onError(data));
window.api.onError('krux:store:get', onError(data));
window.api.onError('krux:store:set', onError(data));
window.api.onError('krux:verify:openssl', onError(data));
window.api.onError('krux:verify:releases:fetch', onError(data));
window.api.onError('krux:check:resource',onError(data));
window.api.onError('krux:download:resources', onError(data));

/**
 * Mounted: when app starts,
 * first show the krux logo to 
 * fit the style in devices
 */
onMounted(async function () {
  await window.api.invoke('krux:change:page', { page: 'KruxInstallerLogo' })
})
</script>