<template>
  <v-layout
    align-start
    justify-start
    row
    fill-height
    id="download-test-ktool-page"
  >
    <v-flex xs12 sm8>
      <v-card flat>
        <v-card-title id="download-test-ktool-page-card-title">
          <v-icon>mdi-monitor-arrow-down</v-icon>
          Downloading {{ tool }}...
        </v-card-title>
        <v-card-subtitle id="download-test-ktool-page-card-subtitle">
          <b>device</b>: {{ device }}
        </v-card-subtitle>
        <v-card-actions>
          <v-progress-linear
            v-model="progress"
            height="25"
            color="blue-grey"
          >
            <strong id="download-test-ktool-page-card-progress-linear-test">{{ progress }}%</strong>
          </v-progress-linear>
        </v-card-actions>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
export default {
  name: 'DownloadKtoolPage',
  data () {
    return {
      progress: 0,
      device: '',
      tool: ''
    }
  },
  async created () {

    await window.KruxInstaller.os.get()

    // eslint-disable-next-line no-unused-vars
    window.KruxInstaller.os.onGet((_event, value) => {
      this.$nextTick(async () => {
        if (value === 'linux') {
          this.tool = 'ktool-linux'
        }
        if (value === 'darwin') {
          await window.KruxInstaller.isMac10.get()
        }
        if (value === 'win32') {
          this.tool = 'ktool-win.exe'
        }
      })
    })

    // eslint-disable-next-line no-unused-vars
    window.KruxInstaller.isMac10.onGet((_event, value) => {
      if (value === true) {
        this.tool = 'ktool-mac-10'
      } else {
        this.tool = 'ktool-mac'
      }
    })

    // eslint-disable-next-line no-unused-vars
    window.KruxInstaller.device.onGet((_event, _value) => {
      this.$nextTick(() => {
        this.device = _value
      })
    })

    // eslint-disable-next-line no-unused-vars
    window.KruxInstaller.download.onData((_event, value) => {
      this.progress = value
    })

    // eslint-disable-next-line no-unused-vars
    window.KruxInstaller.download.onSuccess((_event, value) => {
      this.$emit('onSuccess', { page: 'MainPage' })
    })

    // eslint-disable-next-line no-unused-vars
    window.KruxInstaller.download.onError((_event, value) => {
      alert(value)
      this.$emit('onSuccess', { page: 'MainPage' })
    })
  },
  watch: {
    tool (value) {
      if (value !== '') {
        setTimeout(async () => {
          await window.KruxInstaller.device.get()
        }, 1000)
      }
    },
    async device (value) {
      if (value !== '') {
        await window.KruxInstaller.download.resource({
          baseUrl: 'https://github.com',
          resource: 'odudex/krux_binaries/raw/main',
          filename: this.tool
        })
      }
    }
  }
}
</script>
