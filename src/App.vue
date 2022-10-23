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
import MainPage from './components/MainPage.vue'
import SelectVersionPage from './components/SelectVersionPage.vue'
import SelectActionPage from './components/SelectActionPage.vue'
import SelectFirmwarePage from './components/SelectFirmwarePage.vue'
import ExecutePage from './components/ExecutePage.vue'
import BeforeFlashDevicePage from './components/BeforeFlashDevicePage.vue'
import DetectSDCardPage from './components/DetectSDCardPage.vue'
import CheckResourcesPage from './components/CheckResourcesPage.vue'
import DownloadOfficialReleasePage from './components/DownloadOfficialReleasePage.vue'
import DownloadOfficialReleaseSHA256Page from './components/DownloadOfficialReleaseSHA256Page.vue'
import DownloadOfficialReleaseSigPage from './components/DownloadOfficialReleaseSigPage.vue'
import DownloadOfficialReleasePemPage from './components/DownloadOfficialReleasePemPage.vue'
import DownloadTestFirmwarePage from './components/DownloadTestFirmwarePage.vue'
import DownloadTestKtoolPage from './components/DownloadTestKtoolPage.vue'
import DownloadTestKbootPage from './components/DownloadTestKbootPage.vue'
import VerifyOfficialReleasesPage from './components/VerifyOfficialReleasesPage.vue'
import UnzipOfficialReleasesPage from './components/UnzipOfficialReleasesPage.vue'
import ConfirmDetectedDevicePage from './components/ConfirmDetectedDevicePage.vue'
import ConfirmDetectedSDCardPage from './components/ConfirmDetectedSDCardPage.vue'
import WriteFirmwareToSDCardPage from './components/WriteFirmwareToSDCardPage.vue'
import WriteFirmwareToDevicePage from './components/WriteFirmwareToDevicePage.vue'

export default {
  name: 'App',
  components: {
    KruxLogo,
    MainPage,
    SelectVersionPage,
    SelectActionPage, 
    SelectFirmwarePage,
    ExecutePage, 
    BeforeFlashDevicePage,  
    DetectSDCardPage,
    CheckResourcesPage,
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
  },
  data: () => ({
    page: 'MainPage'
  }),
  created () {
    window.kruxAPI.window_started()

    // eslint-disable-next-line no-unused-vars
    window.kruxAPI.onLogLevelInfo(function(_event, value) {
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
