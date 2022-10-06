<template>
  <v-container fluid>
    <v-row align="justify">
      <v-col
        cols="12"
        sm="6"
      >
        Downloading ktool-{{ os }}...
      </v-col>
      <v-col
        cols="12"
        sm="6"
      >
        <v-progress-linear
          v-model="model"
          height="25"
          color="blue-grey"
        >
          <strong>{{ model }}%</strong>
        </v-progress-linear>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'DownloadKtoolPage',
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
    })
    
    await window.kruxAPI.download_resource({
      baseUrl: 'https://github.com/odudex/krux_binaries/raw/main/',
      resource: '',
      filename: 'ktool-linux'
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
</script>
