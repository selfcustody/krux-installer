<template>
  <v-app>
    <v-main>
      <v-layout column wrap>
        <v-flex xs2 sm2 class="mx-auto my-auto">
          <KruxLogo />
        </v-flex>
        <v-flex xs10 sm10 class="mx-auto my-auto">
          <component
            :is="page"
            @onSuccess="handleSuccess"
            @onError="handleError"
          />
        </v-flex>
      </v-layout>
    </v-main>
  </v-app>
</template>

<script>
import KruxLogo from './components/KruxLogo.vue'
import MainPage from './pages/MainPage.vue'
import SelectVersionPage from './pages/SelectVersionPage.vue'
import SelectDevicePage from './pages/SelectDevicePage.vue'
import BeforeFlashDevicePage from './pages/BeforeFlashDevicePage.vue'
import DetectSDCardPage from './pages/DetectSDCardPage.vue'
import CheckResourcesPage from './pages/CheckResourcesPage.vue'
import CheckResourcesOfficialReleasePage from './pages/CheckResourcesOfficialReleasePage.vue'
import CheckResourcesOfficialReleaseSHA256Page from './pages/CheckResourcesOfficialReleaseSHA256Page.vue'
import CheckResourcesOfficialReleaseSigPage from './pages/CheckResourcesOfficialReleaseSigPage.vue'
import CheckResourcesOfficialReleasePemPage from './pages/CheckResourcesOfficialReleasePemPage.vue'
import CheckResourcesTestFirmwarePage from './pages/CheckResourcesTestFirmwarePage.vue'
import CheckResourcesTestKbootPage from './pages/CheckResourcesTestKbootPage.vue'
import CheckResourcesTestKtoolPage from './pages/CheckResourcesTestKtoolPage.vue'
import DownloadOfficialReleasePage from './pages/DownloadOfficialReleasePage.vue'
import DownloadOfficialReleaseSHA256Page from './pages/DownloadOfficialReleaseSHA256Page.vue'
import DownloadOfficialReleaseSigPage from './pages/DownloadOfficialReleaseSigPage.vue'
import DownloadOfficialReleasePemPage from './pages/DownloadOfficialReleasePemPage.vue'
import DownloadTestFirmwarePage from './pages/DownloadTestFirmwarePage.vue'
import DownloadTestKtoolPage from './pages/DownloadTestKtoolPage.vue'
import DownloadTestKbootPage from './pages/DownloadTestKbootPage.vue'
import VerifyOfficialReleasesPage from './pages/VerifyOfficialReleasesPage.vue'
import UnzipOfficialReleasesPage from './pages/UnzipOfficialReleasesPage.vue'
import ConfirmDetectedDevicePage from './pages/ConfirmDetectedDevicePage.vue'
import ConfirmDetectedSDCardPage from './pages/ConfirmDetectedSDCardPage.vue'
import WriteFirmwareToSDCardPage from './pages/WriteFirmwareToSDCardPage.vue'
import WriteFirmwareToDevicePage from './pages/WriteFirmwareToDevicePage.vue'
import VerifyOpensslErrorPage from './pages/VerifyOpensslErrorPage.vue'

export default {
  name: 'App',
  components: {
    KruxLogo,
    MainPage,
    SelectVersionPage,
    SelectDevicePage,
    BeforeFlashDevicePage,  
    DetectSDCardPage,
    CheckResourcesPage,
    CheckResourcesOfficialReleasePage,
    CheckResourcesOfficialReleaseSHA256Page, 
    CheckResourcesOfficialReleaseSigPage,
    CheckResourcesOfficialReleasePemPage,
    CheckResourcesTestFirmwarePage,
    CheckResourcesTestKbootPage,
    CheckResourcesTestKtoolPage,
    DownloadOfficialReleasePage,
    DownloadOfficialReleaseSHA256Page,
    DownloadOfficialReleaseSigPage,
    DownloadOfficialReleasePemPage, 
    DownloadTestKtoolPage,
    DownloadTestFirmwarePage,
    DownloadTestKbootPage,  
    VerifyOfficialReleasesPage,
    UnzipOfficialReleasesPage,
    ConfirmDetectedDevicePage,
    ConfirmDetectedSDCardPage,
    WriteFirmwareToSDCardPage,
    WriteFirmwareToDevicePage,
    VerifyOpensslErrorPage 
  },
  data: () => ({
    page: 'MainPage'
  }),
  created () {
    window.KruxInstaller.client.started()

    // eslint-disable-next-line no-unused-vars
    window.KruxInstaller.client.onLog(function(_event, value) {
      // eslint-disable-next-line
      console.log(`[ INFO ] ${value}`)
    })
  },
  watch: {
    page (value) {
      // eslint-disable-next-line
      console.log(`[ INFO ] page: ${value}`)
    }
  },
  methods: {
    handleSuccess (value) {
      this.page = value.page
    },
    handleError (value) {
      alert(value.error)
      this.page = 'MainPage'
    },
  }
}
</script>
