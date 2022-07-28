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
  props: {
    os: {
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
      await window.kruxAPI.download_ktool(this.os)
      // eslint-disable-next-line no-unused-vars
      window.kruxAPI.onDownloadedKtoolStatus(async (_event, value) => {
        this.model = value
        if (value === '100.00') {
          this.$emit('onDownloadedKtool')
        }
      })
    }
  }
}
</script>