<template>
  <v-app>
    <v-main>
      <v-layout column wrap>
        <v-flex class="mx-auto my-auto">
          <KruxLogo />
        </v-flex>
        <v-flex
          v-if="page === 'main'"
          class="mx-auto my-auto"
        >
          <MainPage
            @changePage.once="onMainPageClicked"
          />
        </v-flex>
        <v-flex
          v-if="page === 'detect_device'"
          class="mx-auto my-auto"
        >
          <DetectDevicePage
            @onDetectedDevice="onDetectedDevice"
          />
        </v-flex>
        <v-flex
          v-if="page === 'confirm_detected_device'"
          class="mx-auto my-auto"
        >
          <ConfirmDetectedDevicePage
            :device="device"
            @onConfirmDetectedDevice="onConfirmDetectedDevice"
            @onWrongConfirmDetectedDevice="onWrongDetectedDevice"
          />
        </v-flex>
        <v-flex
          v-if="page === 'install_to_device'"
          class="ma-auto"
        >
          <InstallToDevicePage
            @changePage.once="onSelectedDevice"
          />
        </v-flex>
        <v-flex
          v-if="page === 'download_ktool'"
          class="ma-auto"
        >
          <DownloadKtoolPage
            :os="'linux'"
            @onDownloadedKtool="onDownloadedKtool"
          />
        </v-flex>
        <v-flex
          v-if="page === 'download_firmware'"
          class="ma-auto"
        >
          <DownloadFirmwarePage
            :device="device"
            @onDownloadedFirmware="onDownloadedFirmware"
          />
        </v-flex>
        <v-flex
          v-if="page === 'download_kboot'"
          class="ma-auto"
        >
          <DownloadKbootPage
            :device="device"
            @onDownloadedKboot="onDownloadedKboot"
          />
        </v-flex>
        <v-flex
          v-if="page === 'burn_microSD'"
          class="ma-auto"
        >
          <v-container fluid>
            <v-row align="justify">
              <v-col
                cols="12"
                sm="6"
              >
                BURNING TO MICROSD (TODO)
              </v-col>
            </v-row>
          </v-container>
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
import InstallToDevicePage from './components/InstallToDevicePage.vue'
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
    InstallToDevicePage,
    DownloadKtoolPage  ,
    DownloadFirmwarePage,
    DownloadKbootPage  
  },
  data: () => ({
    page: 'main',
    device: ''
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
    onMainPageClicked (value) {
      this.goTo(value)
    },
    onDetectedDevice (value) {
      this.device = value
      console.log(value)
      this.goTo('confirm_detected_device')
    },
    onConfirmDetectedDevice (value) {
      this.device = value
      this.goTo('download_kboot')
    },
    onWrongDetectedDevice (){
      this.goTo('main')
    },
    onSelectedDevice (value) {
      this.device = value
      this.goTo('download_ktool')
    },
    onDownloadedKtool () {
      this.goTo('download_firmware')
    },
    onDownloadedFirmware () {
      this.goTo('download_kboot')
    },
    onDownloadedKboot () {
      this.goTo('burn_microSD')
    },
    goTo (page) {
      this.page = page
    }
  }
}
</script>
