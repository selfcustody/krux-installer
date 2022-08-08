<template>
  <v-container fluid>
    <v-row align="justify">
      <v-col
        cols="12"
        sm="6"
      >
        Downloading firmware for {{ device }}...
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
  name: 'DownloadFirmwarePage',
  props: {
    device: {
      type: String,
      required: true
    },
    sdcard: {
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
      try { 
        await window.kruxAPI.download_firmware(this.device)
        window.kruxAPI.onDownloadedFirmwareStatus((_event, value) => {
          this.model = value
        })
        window.kruxAPI.onDownloadFirmwareDone((_event, value) => {
          console.log(value)
          this.$emit('onSuccess', { sdcard: this.sdcard, resource: value, page: 'WriteFirmwareToSDCardPage' })
        })
      } catch (error) {
        this.$emit('onError', { page: 'SelectFirmwarePage' })
      }
    }
  }
}
</script>
