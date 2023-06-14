<template>
  <v-layout
    align-start
    justify-start
    row
    fill-height
    id="check-resources-test-ktool-page"
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
            <v-flex
              xs8
              sm12
              id="check-resources-test-ktool-page-card-title-checking"
            >
              Checking for {{ ktool }}...
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
        <v-card-title id="check-resources-test-ktool-page-card-title-checked"> 
          <v-icon>mdi-folder-alert-outline</v-icon>&ensp;{{ title }}
        </v-card-title>
        <v-card-subtitle id="check-resources-test-ktool-page-card-subtitle-checked">
          Already downloaded
        </v-card-subtitle>
        <v-card-content>
          <v-card-text id="check-resources-test-ktool-page-card-content-checked">
            Click "Proceed" to proceed with the downloaded version or "Download the file again".
          </v-card-text>
        </v-card-content>
        <v-card-actions> 
          <v-btn
            @click="$emit('onSuccess', { page: 'MainPage' })"
            id="check-resources-test-ktool-page-button-proceed-checked"
          >
            Proceed
          </v-btn>
          <v-btn
            @click="$emit('onSuccess', { page: 'DownloadTestKtoolPage' })"
            id="check-resources-test-ktool-page-button-download-checked"
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
  name: 'CheckResourcesTestKtoolPage',
  data () {
    return {
      checked: false,
      ktool: '',
      title: ''
    }
  },
  watch: {
    ktool (value) {
      if (value !== '') {
        this.title = `odudex/krux_binaries/raw/main/${value}`
      }
    },
    title (value) {
      if (value !== '') {
        setTimeout(async () => {
          await window.KruxInstaller.check.resource(value)
        }, 1000)
      }
    }
  },
  async created () {
    await window.KruxInstaller.os.get()

    // eslint-disable-next-line no-unused-vars
    window.KruxInstaller.os.onGet((_event, value) => {
      this.$nextTick(async () => {
        if (value === 'linux') {
          this.ktool = 'ktool-linux'
        } else if (value === 'darwin') {
          await window.KruxInstaller.isMac10.get()
        } else if (value === 'win32') {
          this.ktool = 'ktool-win.exe'
        }
      })
    })

    // eslint-disable-next-line no-unused-vars
    window.KruxInstaller.isMac10.onGet((_event, value) => {
      this.$nextTick(() => {
        if (value === true) {
          this.ktool = 'ktool-mac-10'
        } else {
          this.ktool = 'ktool-mac'
        }
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
      this.$emit('onSuccess', { page: 'DownloadTestKtoolPage' })
    })
  }
}
</script>
