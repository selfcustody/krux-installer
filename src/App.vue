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
              :device="device"
              :sdcard="sdcard"
              :resource="resource"
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
    page: 'MainPage',
    device: '',
    resource: '',
    sdcard: {}
  }),
  created () {
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
      if (this.page === 'MainPage') {
        this.page = value.page
      }
      if (this.page === 'DetectDevicePage') {
        this.device = value.device
        this.page = value.page
      }
      if (this.page === 'ConfirmDetectedDevicePage') {
        this.device = value.device
        this.page = value.page
      }
      if (this.page === 'DetectSDCardPage') {
        this.sdcard = value.sdcard
        this.page = value.page
      }
      if (this.page === 'ConfirmDetectedSDCardPage' ){
        this.sdcard = value.sdcard
        this.page = value.page
      }
      if (this.page === 'SelectFirmwarePage'){
        this.device = value.device
        this.sdcard = value.sdcard
        this.page = value.page
      }
      if (this.page === 'DownloadFirmwarePage') {
        this.resource = value.resource
        this.page = value.page
      }
      if (this.page === 'WriteFirmwareToSDCardPage') {
        this.page = value.page
      }
    },
    handleError (value) {
      this.page = value.page
    },
    onWrongDetectedSDCard (){
      this.goTo('main')
    },
    onDownloadedFirmware () {
      this.goTo('mount_sdcard')
    },
    onMountedSDCard () {
      this.goTO('write_firmware_to_sdcard')
    },
    onSelectedDevice (value) {
      this.device = value
      this.goTo('download_firmware')
    },
    onDownloadedKtool () {
      this.goTo('download_firmware')
    },
    onDownloadedKboot () {
      this.goTo('burn_microSD')
    }
  }
}
</script>
