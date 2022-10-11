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
  name: 'DownloadOfficialReleaseSigPage',
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
      window.kruxAPI.get_version('version')
       
      // eslint-disable-next-line no-unused-vars
      window.kruxAPI.onGetVersion((_event, value) => { 
        const regex = /tag/g
        let baseUrl = value.replace(regex, 'download') 
        const version = baseUrl.split('download/')[1]
        baseUrl = baseUrl.split(`/${version}`)[0]
        this.version = `${baseUrl}/${version}/krux-${version}.zip.sig`
        window.kruxAPI.download_resource({
          baseUrl: `https://github.com/${baseUrl}`,
          resource: version,
          filename: `krux-${version}.zip.sig`
        })
      })
      
      // eslint-disable-next-line no-unused-vars
      window.kruxAPI.onDownloadStatus((_event, value) => {
        this.model = value
      })
        
      // eslint-disable-next-line no-unused-vars
      window.kruxAPI.onDownloadDone((_event, value) => {
        if (!value.error) {
          this.$emit('onSuccess', { page: 'DownloadOfficialReleasePemPage' })
        } else {
          this.$emit('onError', value.error)
        }
      })
    }
  }
}
</script>
