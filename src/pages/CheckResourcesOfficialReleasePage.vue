<template>
  <v-layout
    align-start
    justify-start
    row
    fill-height
    id="check-resources-official-release-page"
  > 
    <v-flex
      v-if="!checked"
      xs12
    >
      <v-card flat>
        <v-card-title>
          <v-layout row wrap>
            <v-flex xs4 sm12>
              <v-progress-circular
                indeterminate
                color="green"
              />
            </v-flex>
            <v-flex
              xs8
              sm12
              id="check-resources-official-releases-page-card-title-checking">
              Checking official release...
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
        <v-card-title>
          <v-icon>mdi-folder-alert-outline</v-icon>&ensp;{{ title }}
        </v-card-title>
        <v-card-subtitle>
          Already downloaded
        </v-card-subtitle>
        <v-card-content>
          <v-card-text>
            Click "OK" to dowload again or "Cancel" to proceed with the downloaded version.
          </v-card-text>
        </v-card-content>
        <v-card-actions>
          <v-btn @click.prevent="$emit('onSuccess', { page: 'DownloadOfficialReleasePage' })">
            OK
          </v-btn>
          <v-btn @click.prevent="$emit('onSuccess', { page: 'CheckResourcesOfficialReleaseSHA256Page' })">
            Cancel
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
export default {
  name: 'CheckResourcesOfficialReleasePage',
  data () {
    return {
      checked: false,
      title: ''
    }
  },
  watch: {
    async title (value) {
      if (value !== '') {
        await window.KruxInstaller.check.resource(value)
      }
    }
  },
  async created () {
    await window.KruxInstaller.version.get()

    // eslint-disable-next-line no-unused-vars
    window.KruxInstaller.version.onGet((_event, value) => {
      this.$nextTick(() => {
        // https://github.com/selfcustody/krux/releases/download/v22.08.2/krux-v22.08.2.zip
        const regex = /tag/g
        let baseUrl = value.replace(regex, 'download')
        const version = baseUrl.split('download/')[1]
        this.title = `${version}/krux-${version}.zip`
      })
    })

    // eslint-disable-next-line no-unused-vars
    window.KruxInstaller.check.onSuccess((_event, value) => {
      this.$nextTick(() => {
        this.checked = true
      })
    })

    // eslint-disable-next-line no-unused-vars
    window.KruxInstaller.check.onError((_event, value) => {
      this.$emit('onSuccess', { page: 'DownloadOfficialReleasePage' })
    })
  }
}
</script>
