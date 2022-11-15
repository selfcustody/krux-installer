<template>
  <v-layout
    align-start
    justify-start
    row
    fill-height
  >
    <v-flex xs12 sm4>
      <v-card flat class="ma-5 pa-5">
        <v-card-title>
          <v-icon>mdi-monitor-arrow-down</v-icon>
          Downloading...
        </v-card-title>
        <v-card-subtitle>
          <b>kboot.kfpkg</b>: {{ device }}
        </v-card-subtitle>
        <v-card-actions>
          <v-progress-linear
            v-model="progress"
            height="25"
            color="blue-grey"
          >
            <strong>{{ progress }}%</strong>
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
        this.download()
      })
    })
  },
  methods: {
    async download () {
      await window.KruxInstaller.download.resource({
        baseUrl: 'https://github.com',
        resource: `odudex/krux_binaries/raw/main/${this.device}`,
        filename: 'kboot.kfpkg'
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
}
</script>
