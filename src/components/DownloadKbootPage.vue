<template>
  <v-container fluid>
    <v-row align="justify">
      <v-col
        cols="12"
        sm="6"
      >
        Downloading kboot.kfpkg for {{ device }}...
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
  name: 'DownloadKbootPage',
  props: {
    device: {
      type: String,
      required: true
    }
  },
  data () {
    return {
      model: 0
    }
  },
  async created () {
    await this.onDownload()
  },
  methods: {
    async onDownload () {
      await window.kruxAPI.download_resource(`${this.device}/kboot.kfpkg`)
      
      // eslint-disable-next-line no-unused-vars
      window.kruxAPI.onDownloadStatus((_event, value) => {
        this.model = value
      })
      
      // eslint-disable-next-line no-unused-vars
      window.kruxAPI.onDownloadDone((_event, value) => {
        this.$emit('onSuccess', { device: this.device, page: 'DownloadKtoolPage' })
      })
    }
  }
}
</script>
