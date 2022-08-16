<template>
  <v-layout
    align-start
    justify-start
    row
    fill-height
  >
    <v-flex>
      <p>Downloading <b>{{ version }}</b>...</p>
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
  name: 'DownloadOfficialReleasePage',
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
      await window.kruxAPI.get_version()
       
      // eslint-disable-next-line no-unused-vars
      window.kruxAPI.onGetVersion(async (_event, value) => { 
        const regex = /tag/g
        let baseUrl = value.replace(regex, 'download') 
        const version = baseUrl.split('download/')[1]
        baseUrl = baseUrl.split(`/${version}`)[0]
        this.version = `${baseUrl}/${version}/krux-${version}.zip`
        await window.kruxAPI.download_resource({
          baseUrl: `https://github.com/${baseUrl}`,
          resource: version,
          filename: `krux-${version}.zip`
        })
      })
      
      // eslint-disable-next-line no-unused-vars
      window.kruxAPI.onDownloadStatus((_event, value) => {
        this.model = value
      })
        
      // eslint-disable-next-line no-unused-vars
      window.kruxAPI.onDownloadDone((_event, value) => {
        this.$emit('onSuccess', { page: 'DownloadOfficialReleaseSHA256Page' })
      })

      // eslint-disable-next-line no-unused-vars
      window.kruxAPI.onDownloadError((_event, value) => {
        this.$emit('onError', value)
      })
    }
  }
}
</script>
