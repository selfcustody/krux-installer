<template>
  <v-layout
    align-start
    justify-start
    row
    fill-height
    id="download-official-release-pem-page"
  >
    <v-flex xs12>
      <v-card flat>
        <v-card-title
          id="download-official-release-pem-page-card-title"
        >
          Downloading...
        </v-card-title>
        <v-card-subtitle
          id="download-official-release-pem-page-card-subtitle"
        >
          <b>main/selfcustody.pem</b>...
        </v-card-subtitle>
        <v-card-actions>
          <v-progress-linear
            v-model="progress"
            height="25"
            color="blue-grey"
          >
            <strong id="download-official-release-pem-page-card-progress-linear-text">{{ progress }}%</strong>
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
      progress: 0
    }
  },
  async created () {
    await window.KruxInstaller.download.resource({
      baseUrl: 'https://raw.githubusercontent.com/selfcustody/krux',
      resource: 'main',
      filename: 'selfcustody.pem'
    })
      
    // eslint-disable-next-line no-unused-vars
    window.KruxInstaller.download.onData((_event, value) => {
      this.progress = value
    })
        
    // eslint-disable-next-line no-unused-vars
    window.KruxInstaller.download.onSuccess((_event, value) => {
      this.$nextTick(() => {
        setTimeout(() => {
          this.$emit('onSuccess', { page: 'VerifyOfficialReleasesPage' })
        }, 1000)
      })
    })

    // eslint-disable-next-line no-unused-vars
    window.KruxInstaller.download.onError((_event, value) => {
      this.$emit('onError', value.error)
    })
  }
}
</script>
