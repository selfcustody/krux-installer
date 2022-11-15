<template>
  <v-layout
    align-start
    justify-start
    row
    fill-height
  >
    <v-flex 
      v-if="checking == 0"
      xs12
      sm4
    >
      <v-card flat class="ma-5 pa-5">
        <v-card-title>
          Choose ktool-mac flavor
        </v-card-title>
        <v-card-content>
          <v-select
            v-model="tool"
            :items="['ktool-mac', 'ktool-mac-10']"
            label="Mac Flavour"
          />
        </v-card-content>
        <v-card-actions>
          <v-btn @click.prevent="tool !== '' ? (checking = 1) : (checking = 0)">
            Choose
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-flex>
    <v-flex
      v-if="checking == 1"
      xs12
    >
      <v-card flat>
        <v-card-title>
          <v-icon>mdi-monitor-arrow-down</v-icon>
          Downloading...
        </v-card-title>
        <v-card-subtitle>
          <b>ktool</b>: {{ tool }}
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
  name: 'DownloadKtoolPage',
  data () {
    return {
      progress: 0,
      device: '',
      checking: -1,
      tool: ''
    }
  },
  async created () {

    await window.KruxInstaller.os.get()

    // eslint-disable-next-line no-unused-vars
    window.KruxInstaller.os.onGet((_event, value) => {
      if (value === 'linux') {
        this.$nextTick(() => { 
          this.tool = 'ktool-linux'
          this.checking = 1
        })
      }
      if (value === 'darwin') {
        this.$nextTick(() => {
          this.checking = 0
        })
      }
      if (value === 'win32') {
        this.$nextTick(() => { 
          this.tool = 'ktool-win.exe'
          this.checking = 1
        })
      }
    })
  },
  watch: {
    async checking (value) {
      if (value === 1) {
        await window.KruxInstaller.device.get()

        window.KruxInstaller.device.onGet((_event, _value) => {
          this.$nextTick(() => {
            this.device = _value
          })
        })
      }
    },
    async device (value) {
      if (value !== '') {
        await this.download()
      }
    }
  },
  methods: {
    async download () {
      await window.KruxInstaller.download.resource({
        baseUrl: 'https://github.com',
        resource: 'odudex/krux_binaries/raw/main',
        filename: this.tool
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
    }
  }
}
</script>
