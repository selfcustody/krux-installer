<template>
  <v-app>
    <v-main>
      <v-layout column wrap>
        <v-flex class="mx-auto my-auto">
          <KruxLogo />
        </v-flex>
        <v-flex class="mx-auto my-auto">
          <keep-alive>
            <component
              :is="page"
              @onSuccess="handleSuccess"
              @onError="handleError"
            />
          </keep-alive>
        </v-flex>
      </v-layout>
    </v-main>
  </v-app>
</template>

<script>
import KruxLogo from './components/KruxLogo.vue'
import MainPage from './components/MainPage.vue'
import SelectVersionPage from './components/SelectVersionPage.vue'
import DownloadOfficialReleasePage from './components/DownloadOfficialReleasePage.vue'
import DownloadOfficialReleaseSHA256Page from './components/DownloadOfficialReleaseSHA256Page.vue'
import DownloadOfficialReleaseSigPage from './components/DownloadOfficialReleaseSigPage.vue'
import DetectDevicePage from './components/DetectDevicePage.vue'
import ConfirmDetectedDevicePage from './components/ConfirmDetectedDevicePage.vue'
import DetectSDCardPage from './components/DetectSDCardPage.vue'
import ConfirmDetectedSDCardPage from './components/ConfirmDetectedSDCardPage.vue'
import SelectFirmwarePage from './components/SelectFirmwarePage.vue'
import WriteFirmwareToSDCardPage from './components/WriteFirmwareToSDCardPage.vue'
import DownloadKtoolPage from './components/DownloadKtoolPage.vue'
import DownloadFirmwarePage from './components/DownloadFirmwarePage.vue'
import DownloadKbootPage from './components/DownloadKbootPage.vue'

export default {
  name: 'App',
  components: {
    KruxLogo,
    MainPage,
    SelectVersionPage,
    DownloadOfficialReleasePage,
    DownloadOfficialReleaseSHA256Page,
    DownloadOfficialReleaseSigPage,
    DetectDevicePage, 
    ConfirmDetectedDevicePage,
    DetectSDCardPage,
    ConfirmDetectedSDCardPage,
    SelectFirmwarePage,
    WriteFirmwareToSDCardPage,
    DownloadKtoolPage  ,
    DownloadFirmwarePage,
    DownloadKbootPage  
  },
  data: () => ({
    page: 'MainPage'
  }),
  created () {
    window.kruxAPI.window_started()
    window.kruxAPI.onLogLevelInfo(function(_event, value) {
      console.log(`[ INFO ] ${value}`)
    })
  },
  watch: {
    page (value) {
      console.log(`[ INFO ] page: ${value}`)
    }
  },
  methods: {
    handleSuccess (value) {
      this.page = value.page
    },
    handleError (value) {
      alert(value.error)
    },
  }
}
</script>
