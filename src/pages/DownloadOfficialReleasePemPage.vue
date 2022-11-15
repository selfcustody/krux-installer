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
          <b>main/selfcustody.pem</b>...
        </v-card-subtitle>
        <v-card-actions>
          <v-progress-linear
            v-model="progress"
            height="25"
            color="blue-grey"
          >
            <strong>{{ progress }}%</strong>
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
      this.$emit('onSuccess', { page: 'VerifyOfficialReleasesPage' })
    })

    // eslint-disable-next-line no-unused-vars
    window.KruxInstaller.download.onError((_event, value) => {
      this.$emit('onError', value.error)
    })
  }
}
</script>
