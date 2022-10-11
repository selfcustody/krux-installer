<template>
  <v-layout
    align-start
    justify-start
    row
    fill-height
  >
    <v-flex xs12>
      <v-card flat>
        <v-card-title>
          Downloading...
        </v-card-title>
        <v-card-subtitle>
          <b>{{ version }}.zip.sig</b>...
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
  name: 'DownloadOfficialReleasePemPage',
  data () {
    return {
      version: '',
      model: 0
    }
  },
  async created () {
    await this.download()
  },
  methods: {
    async download () {
      // const version = value.split('tag/')[1]
      this.version = 'selfcustody/krux/main/selfcustody.pem'
      window.kruxAPI.download_resource({
        baseUrl: 'https://raw.githubusercontent.com/selfcustody/krux',
        resource: 'main',
        filename: 'selfcustody.pem'
      })
      
      // eslint-disable-next-line no-unused-vars
      window.kruxAPI.onDownloadStatus((_event, value) => {
        this.model = value
      })
        
      // eslint-disable-next-line no-unused-vars
      window.kruxAPI.onDownloadDone((_event, value) => {
        if (!value.error) {
          this.$emit('onSuccess', { page: 'VerifyOfficialReleasesPage' })
        } else {
          this.$emit('onError', value.error)
        }
      })
    }
  }
}
</script>
