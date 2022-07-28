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
      await window.kruxAPI.download_kboot(this.device)
      window.kruxAPI.onDownloadedKbootStatus(async (_event, value) => {
        this.model = value
        if (value === '100.00') {
          await this.$emit('onDownloadedKboot')
        }
      })
    }
  }
}
</script>