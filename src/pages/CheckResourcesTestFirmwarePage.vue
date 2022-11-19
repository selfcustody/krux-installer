<template>
  <v-layout
    align-start
    justify-start
    row
    fill-height
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
            <v-flex xs8 sm12>
              Checking...
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
        <v-card-title class="odudex"> 
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
          <v-btn @click.prevent="$emit('onSuccess', { page: 'DownloadTestFirmwarePage' })">
            OK
          </v-btn>
          <v-btn @click.prevent="$emit('onSuccess', { page: 'CheckResourcesTestKbootPage' })">
            Cancel
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
export default {
  name: 'CheckResourcesTestFirmwarePage',
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
    await window.KruxInstaller.device.get()

    // eslint-disable-next-line no-unused-vars
    window.KruxInstaller.device.onGet((_event, value) => {
      this.$nextTick(() => {
        this.title = `odudex/krux_binaries/raw/main/${value}/firmware.bin`
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
      this.$emit('onSuccess', { page: 'DownloadTestFirmwarePage' })
    })
  }
}
</script>
<style>
.odudex {
  font-size: 16px;
}
</style>
