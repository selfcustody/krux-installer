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
          Downloading...
        </v-card-title>
        <v-card-subtitle>
          <b>kboot.kfpkg</b>: {{ device }}
        </v-card-subtitle>
        <v-card-actions>
          <v-progress-linear
            v-model="model"
            height="25"
            color="blue-grey"
          >
            <strong>{{ model }}%</strong>
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
      model: 0,
      device: ''
    }
  },
  async created () {
    await window.kruxAPI.get_device()

    window.kruxAPI.onGetDevice((_event, value) => {
      this.device = value
      this.$nextTick(() => {
        this.download()
      })
    })
  },
  methods: {
    async download () {
      await window.kruxAPI.download_resource({
        baseUrl: 'https://github.com',
        resource: `odudex/krux_binaries/raw/main/${this.device}`,
        filename: 'kboot.kfpkg'
      })

      // eslint-disable-next-line no-unused-vars
      window.kruxAPI.onDownloadStatus((_event, value) => {
        this.model = value
      })

      // eslint-disable-next-line no-unused-vars
      window.kruxAPI.onDownloadDone((_event, value) => {
        this.$emit('onSuccess', { page: 'DownloadTestKtoolPage' })
      })

      // eslint-disable-next-line no-unused-vars
      window.kruxAPI.onDownloadError((_event, value) => {
        alert(value)
        this.$emit('onSuccess', { page: 'MainPage' })
      })
    }
  }
}
</script>
