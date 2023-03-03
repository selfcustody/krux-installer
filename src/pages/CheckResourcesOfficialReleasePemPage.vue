<template>
  <v-layout
    align-start
    justify-start
    row
    fill-height
    id="check-resources-official-release-pem-page"
  > 
    <v-flex
      v-if="!checked"
      xs12
    >
      <v-card flat>
        <v-card-title> 
          <v-layout column wrap>
            <v-flex xs4 sm12>
              <v-progress-circular
                indeterminate
                color="green"
              />
            </v-flex>
            <v-flex xs8 sm12 id="check-resources-official-release-pem-page-card-title-checking">
              Checking selfcustody public key certificate...
            </v-flex>
          </v-layout>
        </v-card-title>
      </v-card>
    </v-flex>
    <v-flex
      v-if="checked"
      xs12
    >
      <v-card flat>
        <v-card-title
          id="check-resources-official-release-pem-page-card-title-checked"
        > 
          <v-icon>mdi-folder-alert-outline</v-icon>&ensp;{{ title }}
        </v-card-title>
        <v-card-subtitle
          id="check-resources-official-release-pem-page-card-subtitle-checked"
        >
          Already downloaded
        </v-card-subtitle>
        <v-card-content>
          <v-card-text
            id="check-resources-official-release-pem-page-card-content-checked"
          >
            Click "Proceed" to proceed with the downloaded version or "Download the file again".
          </v-card-text>
        </v-card-content>
        <v-card-actions> 
          <v-btn
            @click="$emit('onSuccess', { page: 'VerifyOfficialReleasesPage' })"
            id="check-resources-official-release-pem-page-button-proceed-checked"
          >
            Proceed
          </v-btn>
          <v-btn
            @click="$emit('onSuccess', { page: 'DownloadOfficialReleasePemPage' })"
            id="check-resources-official-release-pem-page-button-download-checked"
          >
            Download the file again
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
export default {
  name: 'CheckResourcesOfficialReleasePemPage',
  data () {
    return {
      checked: false,
      title: ''
    }
  },
  watch: {
    async title (value) {
      if (value !== '') {
        setTimeout(async () => {
          await window.KruxInstaller.check.resource(value)
        }, 1000)
      }
    }
  },
  async created () {
    this.title = `main/selfcustody.pem`

    // eslint-disable-next-line no-unused-vars
    window.KruxInstaller.check.onSuccess((_event, value) => {
      this.$nextTick(() => {
        this.checked = true
      })
    })

    // eslint-disable-next-line no-unused-vars
    window.KruxInstaller.check.onError((_event, value) => {
      this.$nextTick(() => {
        this.$emit('onSuccess', { page: 'DownloadOfficialReleasePemPage' })
      })
    })
  }
}
</script>
