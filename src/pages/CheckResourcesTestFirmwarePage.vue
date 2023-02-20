<template>
  <v-layout
    align-start
    justify-start
    row
    fill-height
    id="check-resources-test-firmware-page"
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
            <v-flex xs8 sm12 id="check-resources-page-card-title-checking">
              Checking for {{ device }} binaries...
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
        <v-card-title class="odudex" id="check-resources-page-card-title-checked"> 
          <v-icon>mdi-folder-alert-outline</v-icon>&ensp;{{ title }}
        </v-card-title>
        <v-card-subtitle id="check-resources-page-card-subtitle-checked">
          Already downloaded
        </v-card-subtitle>
        <v-card-content>
          <v-card-text id="check-resources-page-card-content-checked">
            Click "Proceed" to proceed with the downloaded version or "Download the file again".
          </v-card-text>
        </v-card-content>
        <v-card-actions>
          <v-btn
            @click.prevent="$emit('onSuccess', { page: 'DownloadTestFirmwarePage' })"
            id="check-resources-page-button-proceed-checked"
          >
            Proceed
          </v-btn>
          <v-btn
            @click.prevent="$emit('onSuccess', { page: 'CheckResourcesTestKbootPage' })"
            id="check-resources-page-button-download-checked"
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
  name: 'CheckResourcesTestFirmwarePage',
  data () {
    return {
      checked: false,
      device: '',
      title: ''
    }
  },
  watch: {
    title (value) {
      if (value !== '') {
        setTimeout(async function () {
          await window.KruxInstaller.check.resource(value)
        }, 1000)
      }
    }
  },
  async created () {
    await window.KruxInstaller.device.get()

    // eslint-disable-next-line no-unused-vars
    window.KruxInstaller.device.onGet((_event, value) => {
      this.$nextTick(() => {
        this.device = value
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
      setTimeout(() => {
        this.$emit('onSuccess', { page: 'DownloadTestFirmwarePage' })
      }, 1000)
    })
  }
}
</script>
<style>
.odudex {
  font-size: 16px;
}
</style>
