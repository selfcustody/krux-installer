<template>
  <v-layout
    align-start
    justify-start
    row
    fill-height
    id="download-test-firmware-page"
  >
    <v-flex xs12>
      <v-card flat>
        <v-card-title
          id="download-test-firmware-page-card-title"
        >
          <v-icon>mdi-monitor-arrow-down</v-icon>
          Downloading <b>firmware.bin</b>...
        </v-card-title>
        <v-card-subtitle
          id="download-test-firmware-page-card-subtitle"
        >
          device: {{ device }}
        </v-card-subtitle>
        <v-card-actions>
          <v-progress-linear
            v-model="progress"
            height="25"
            color="blue-grey"
          >
            <strong id="download-test-firmware-page-card-progress-linear-test">{{ progress }}%</strong>
          </v-progress-linear>
        </v-card-actions>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
export default {
  name: 'DownloadTestFirmwarePage',
  data () {
    return {
      progress: 0,
      device: '',
      download: false
    }
  },
  async created () {
    await window.KruxInstaller.device.get()

    window.KruxInstaller.device.onGet((_event, value) => {
      this.$nextTick(() => {
        this.device = value
      })
    })
  },
  watch: {
    async device (value) {
      if (value !== '') {
        await this.download_resource({
          baseUrl: 'https://github.com',
          resource: `odudex/krux_binaries/raw/main/${value}`, 
          filename: 'firmware.bin'
        })
      }
    }
  },
  methods: {
    async download_resource (options) {
      await window.KruxInstaller.download.resource(options)

      // eslint-disable-next-line no-unused-vars
      window.KruxInstaller.download.onData((_event, value) => {
        this.progress = value
      })
        
      // eslint-disable-next-line no-unused-vars
      window.KruxInstaller.download.onSuccess((_event, value) => {
        this.$emit('onSuccess', { page: 'CheckResourcesTestKbootPage' })
      })

      // eslint-disable-next-line no-unused-vars
      window.KruxInstaller.download.onError((_event, value) => {
        alert(value)
        this.$emit('onSuccess', { page: 'MainPage' })
      })
    }
  }
}
</script>
