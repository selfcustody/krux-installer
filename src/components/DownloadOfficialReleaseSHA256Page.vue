<template>
  <v-layout
    align-start
    justify-start
    row
    fill-height
  >
    <v-flex>
      <p>Downloading <b>{{ version }}.sha256.txt</b>...</p>
      <br/>
      <v-progress-linear
        v-model="model"
        height="25"
        color="blue-grey"
      >
        <strong>{{ model }}%</strong>
      </v-progress-linear>
    </v-flex>
  </v-layout>
</template>

<script>
export default {
  name: 'DownloadOfficialReleaseSHA256Page',
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
        this.version = `${baseUrl}/${version}/krux-${version}.zip.sha256.txt`
        window.kruxAPI.download_resource({
          baseUrl: `https://github.com/${baseUrl}`,
          resource: version,
          filename: `krux-${version}.zip.sha256.txt`
        })
      })
      
      // eslint-disable-next-line no-unused-vars
      window.kruxAPI.onDownloadStatus((_event, value) => {
        this.model = value
      })
        
      // eslint-disable-next-line no-unused-vars
      window.kruxAPI.onDownloadDone((_event, value) => {
        if (!value.error) {
          this.$emit('onSuccess', { page: 'DownloadOfficialReleaseSigPage' })
        } else {
          this.$emit('onError', value.error)
        }
      })
    }
  }
}
</script>
