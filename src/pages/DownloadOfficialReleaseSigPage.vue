<template>
  <v-layout
    align-start
    justify-start
    row
    fill-height
    id="download-official-release-sig-page"
  >
    <v-flex xs12>
      <v-card flat>
        <v-card-title
          id="download-official-release-sig-page-card-title"
        >
          Downloading...
        </v-card-title>
        <v-card-subtitle
          id="download-official-release-sig-page-card-subtitle"
        >
          <b>{{ baseUrl }}/{{ version }}/krux-{{ version }}.zip.sig</b>...
        </v-card-subtitle>
        <v-card-actions>
          <v-progress-linear
            v-model="progress"
            height="25"
            color="blue-grey"
          >
            <strong id="download-official-release-sig-page-card-progress-linear-text">{{ progress }}%</strong>
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
      baseUrl: '',
      version: '',
      progress: 0
    }
  },
  async created () {
    await  window.KruxInstaller.version.get()

    // eslint-disable-next-line no-unused-vars
    window.KruxInstaller.version.onGet((_event, value) => { 
      const regex = /tag/g
      let baseUrl = value.replace(regex, 'download') 
      const version = baseUrl.split('download/')[1]
      this.baseUrl = baseUrl.split(`/${version}`)[0]
      this.version = version
    })

    // eslint-disable-next-line no-unused-vars
    window.KruxInstaller.download.onData((_event, value) => {
      this.progress = value
    })
        
    // eslint-disable-next-line no-unused-vars
    window.KruxInstaller.download.onSuccess((_event, value) => {
      this.$nextTick(() => {
        setTimeout(() => {
          this.$emit('onSuccess', { page: 'CheckResourcesOfficialReleasePemPage' })
        }, 1000)
      })
    })

    // eslint-disable-next-line no-unused-vars
    window.KruxInstaller.download.onError((_event, value) => {
      this.$emit('onError', value.error)
    })
  }, 
  watch: {
    async version (value) {
      if (value !== '') {
        await window.KruxInstaller.download.resource({
          baseUrl: `https://github.com/${this.baseUrl}`,
          resource: value,
          filename: `krux-${value}.zip.sig`
        })
      }
    }
  }
}
</script>
