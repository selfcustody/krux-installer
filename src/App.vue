<template>
  <v-app>
    <v-main>
      <v-layout column wrap>
        <v-flex
          class="mx-auto my-auto"
        >
          <v-container>
            <v-row>
              <v-col>
                <AsciiMorph :ascii="krux" x=10 y=10 /> 
              </v-col>
            </v-row>
            <v-row class="text-center">
              <v-col class="mb-4">
                <h1 class="display-2 font-weight-bold mb-3">
                  {{ title }}
                </h1>
              </v-col>
            </v-row>
          </v-container>
        </v-flex>
        <v-flex
          v-if="page === 'main'"
          class="mx-auto"
        >
          <v-container>
            <v-row
              v-for="(desc,i) in descriptions"
              :key="i"
              class="text-justify"
            >
              <v-col> 
                <p class="subheading font-weight-regular">
                  {{ desc }} 
                </p>
              </v-col>
            </v-row>
            <br/>
            <v-row class="text-center">
              <v-col class="mb-4">
                <v-btn
                  color="primary"
                  @click.prevent="go_to_install_to_device"
                >
                  Install to device
                </v-btn>
              </v-col>
            </v-row>
            <v-row class="text-center">
              <v-col class="mb-4">
                <v-btn color="primary">
                  Flash to device
                </v-btn>
              </v-col>
            </v-row>
            <v-row class="text-center">
              <v-col class="mb-4">
                <v-btn color="primary">
                  Build from source
                </v-btn>
              </v-col>
            </v-row>
          </v-container>
        </v-flex>
        <v-flex
          v-if="page === 'install_to_device'"
          class="ma-auto"
        >
          <v-container fluid>
            <v-row align="justify">
              <v-col
                cols="12"
                sm="6"
              >
                <v-subheader>
                  <p>Select the device you want install to</p>
                </v-subheader>
              </v-col>
              <v-col
                cols="12"
                sm="6"
              >
                <v-select
                  v-model="device"
                  :items="devices"
                  label="device"
                />
              </v-col>
            </v-row>
            <v-row>
              <v-btn color="primary" @click.prevent="go_to_download_ktool">
                Go
              </v-btn>
            </v-row>
          </v-container>
        </v-flex>
        <v-flex
          v-if="page === 'download_ktool'"
          class="ma-auto"
        >
          <v-container fluid>
            <v-row align="justify">
              <v-col
                cols="12"
                sm="6"
              >
                {{ download_ktool.message }}
              </v-col>
              <v-col
                cols="12"
                sm="6"
              >
                <v-progress-linear
                  v-model="download_ktool.model"
                  height="25"
                  color="blue-grey"
                >
                  <strong>{{ download_ktool.model }}%</strong>
                </v-progress-linear>
              </v-col>
            </v-row>
          </v-container>
        </v-flex>
        <v-flex
          v-if="page === 'download_firmware'"
          class="ma-auto"
        >
          <v-container fluid>
            <v-row align="justify">
              <v-col
                cols="12"
                sm="6"
              >
                {{ download_firmware.message }}
              </v-col>
              <v-col
                cols="12"
                sm="6"
              >
                <v-progress-linear
                  v-model="download_firmware.model"
                  height="25"
                  color="blue-grey"
                >
                  <strong>{{ download_firmware.model }}%</strong>
                </v-progress-linear>
              </v-col>
            </v-row>
          </v-container>
        </v-flex>
        <v-flex
          v-if="page === 'download_kboot'"
          class="ma-auto"
        >
          <v-container fluid>
            <v-row align="justify">
              <v-col
                cols="12"
                sm="6"
              >
                {{ download_kboot.message }}
              </v-col>
              <v-col
                cols="12"
                sm="6"
              >
                <v-progress-linear
                  v-model="download_kboot.model"
                  height="25"
                  color="blue-grey"
                >
                  <strong>{{ download_kboot.model }}%</strong>
                </v-progress-linear>
              </v-col>
            </v-row>
          </v-container>
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
export default {
  name: 'App',

  data: () => ({
    title: 'Krux Installer',
    page: 'main',
    descriptions: [
      'Krux is an open-source DIY hardware signer for Bitcoin that can sign for multisignature and single-key wallets.',
      'It is a low-cost airgapped device built from off-the-shelf parts that communicates with wallet software via QR codes and wipes its memory after every session.',
    ],
    krux: [ 
      "           ██              ",
      "           ██              ",
      "           ██              ",
      "         ██████            ", 
      "           ██              ",
      "           ██  ██          ",
      "           ██ ██           ", 
      "           ████            ",
      "           ██ ██           ",
      "           ██  ██          ",
      "           ██   ██         ", 
    ],
    x: 50,
    y: 50,
    device: '',
    devices: [
      'maixpy_m5stickv',
      'maixpy_amigo_ips',
      'maixpy_bit',
      'maixpy_bit_ov5642',
      'maixpy_dock'
    ],
    download_ktool: {
      model: 0,
      message: ''
    },
    download_firmware: {
      model: 0,
      message: ''
    },
    download_kboot: {
      model: 0,
      message: ''
    }
  }),
  methods: {
    go_to_install_to_device () {
      this.page = 'install_to_device'
    },
    async go_to_download_ktool () {
      const os = 'linux'
      this.page = 'download_ktool'
      this.download_ktool.message = `Download ktool-${os}...`
      await window.kruxAPI.download_ktool(os)
      // eslint-disable-next-line no-unused-vars
      window.kruxAPI.onDownloadedKtoolStatus(async (_event, value) => {
        this.download_ktool.model = value
        if (value === '100.00') {
          await this.go_to_download_firmware()
        }
      })
    },
    async go_to_download_firmware () {
      this.page = 'download_firmware'
      this.download_firmware.message = `Download firmware.bin for ${this.device}...`
      await window.kruxAPI.download_firmware(this.device)
      window.kruxAPI.onDownloadedFirmwareStatus(async (_event, value) => {
        this.download_firmware.model = value
        if (value === '100.00') {
          await this.go_to_download_kboot()
        }
      })
    },
    async go_to_download_kboot () {
      this.page = 'download_kboot'
      this.download_kboot.message = `Download kboot.kpkg for ${this.device}...`
      await window.kruxAPI.download_kboot(this.device)
      window.kruxAPI.onDownloadedKbootStatus(async (_event, value) => {
        this.download_kboot.model = value
        if (value === '100.00') {
          await this.go_to_burn_mircoSD()
        }
      })
    },
    async go_to_burn_mircoSD () {
      this.page = 'burn_microSD'
    }
  }
}
</script>
