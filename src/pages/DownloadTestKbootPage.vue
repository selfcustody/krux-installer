<template>
  <v-layout
    align-start
    justify-start
    row
    fill-height
    id="download-test-kboot-page"
  >
    <v-flex xs12 sm4>
      <v-card flat class="ma-5 pa-5">
        <v-card-title
          id="download-test-kboot-page-card-title"
        >
          <v-icon>mdi-monitor-arrow-down</v-icon>
          Downloading <b>kboot.kfpkg</b>...
        </v-card-title>
        <v-card-subtitle
          id="download-test-kboot-page-card-subtitle"
        >
          <b>device</b>: {{ device }}
        </v-card-subtitle>
        <v-card-actions>
          <v-progress-linear
            v-model="progress"
            height="25"
            color="blue-grey"
          >
            <strong id="download-test-kboot-page-card-progress-linear-test">{{ progress }}%</strong>
          </v-progress-linear>
        </v-card-actions>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
export default {
  name: 'DownloadTestKbootPage',
  data () {
    return {
      progress: 0,
      device: ''
    }
  },
  async created () {
    await window.KruxInstaller.device.get()

    window.KruxInstaller.device.onGet((_event, value) => {
      this.device = value
      this.$nextTick(() => {
        setTimeout(async () => {
          await window.KruxInstaller.download.resource({
            baseUrl: 'https://github.com',
            resource: `odudex/krux_binaries/raw/main/${this.device}`,
            filename: 'kboot.kfpkg'
          })
        }, 1000)
      })
    })

    // eslint-disable-next-line no-unused-vars
    window.KruxInstaller.download.onData((_event, value) => {
      this.progress = value
    })

    // eslint-disable-next-line no-unused-vars
    window.KruxInstaller.download.onSuccess((_event, value) => {
      this.$emit('onSuccess', { page: 'CheckResourcesTestKtoolPage' })
    })

    // eslint-disable-next-line no-unused-vars
    window.KruxInstaller.download.onError((_event, value) => {
      alert(value)
      this.$emit('onSuccess', { page: 'MainPage' })
    })
  }
}
</script>
