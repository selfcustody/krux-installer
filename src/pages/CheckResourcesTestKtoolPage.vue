<template>
  <v-layout
    align-start
    justify-start
    row
    fill-height
  > 
    <v-flex
      v-if="!checked && checking_mac === -1"
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
      v-if="!checking && checking_mac === 0"
      xs12
    > 
      <v-card flat class="ma-5 pa-5">
        <v-card-title>
          <v-icon>mdi-apple</v-icon>&ensp;Choose ktool-mac flavor
        </v-card-title>
        <v-card-content>
          <v-select
            v-model="ktool"
            :items="['ktool-mac', 'ktool-mac-10']"
            label="Mac Flavour"
          />
        </v-card-content>
        <v-card-actions>
          <v-btn @click.prevent="ktool !== '' ? (checking_mac = 1) : checking_mac = 0">
            Choose
          </v-btn>
        </v-card-actions>
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
          <v-btn @click.prevent="$emit('onSuccess', { page: 'DownloadTestKtoolPage' })">
            OK
          </v-btn>
          <v-btn @click.prevent="$emit('onSuccess', { page: 'MainPage' })">
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
      checking_mac: -1,
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
    checking_mac (value) {
      if (value === 1) {
        this.checked = true
      }
    },
    async title (value) {
      if (value !== '') {
        await window.KruxInstaller.check.resource(value)
      }
    }
  },
  async created () {
    await window.KruxInstaller.os.get()

    // eslint-disable-next-line no-unused-vars
    window.KruxInstaller.os.onGet((_event, value) => {
      this.$nextTick(() => {
        if (value === 'linux') {
          this.ktool = 'ktool-linux'
          this.checked = true
        } else if (value === 'darwin') {
          this.checking_mac = 0
        } else if (value === 'win32') {
          this.ktool = 'ktool-win.exe'
          this.checked = true
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
