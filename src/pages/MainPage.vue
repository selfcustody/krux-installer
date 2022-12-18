<template>
  <v-layout row>
    <v-flex xs12 sm12>
      <v-container>
        <v-row dense>
          <v-col cols="12"> 
            <v-card class="ma-5 pa-5">
              <v-card-subtitle>
                Select between available devices (m5stickV, amigo, bit, dock)
              </v-card-subtitle>
              <v-card-actions>
                <v-btn @click.prevent="$emit('onSuccess', { page: 'SelectDevicePage' })">
                  <v-icon>mdi-devices</v-icon>&ensp;{{ device }}
                </v-btn>
              </v-card-actions>
            </v-card>
            <v-card class="ma-5 pa-5">
              <v-card-subtitle>
                Select between <b>selfcustody</b> (official) or <b>odudex</b> (test) releases
              </v-card-subtitle>
              <v-card-actions>
                <v-btn @click.prevent="$emit('onSuccess', { page: 'SelectVersionPage' })">
                   <v-icon>mdi-cube-outline</v-icon>&ensp;{{ version }}
                </v-btn>
              </v-card-actions>
            </v-card>
            <v-card class="ma-5 pa-5">
              <v-card-subtitle>
                Flash to device with <b>{{ ktool }}</b>
              </v-card-subtitle>
              <v-card-actions> 
                <v-btn @click.prevent="$emit('onSuccess', { page: 'BeforeFlashDevicePage' })">
                  <v-icon>mdi-lightning-bolt-outline</v-icon>&ensp;Flash
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-flex>
  </v-layout>
</template>

<script>
export default {
  name: 'MainPage',
  data () {
    return {
      version: '',
      device: '',
      ktool: ''
    }
  },
  async created () {
    await window.KruxInstaller.version.get()

    // eslint-disable-next-line no-unused-vars
    window.KruxInstaller.version.onGet((_event, value) => {
      this.$nextTick(() => {
        this.version = value
      })
    })


    // eslint-disable-next-line no-unused-vars
    window.KruxInstaller.device.onGet((_event, value) => {
      this.$nextTick(() => {
        this.device = value
      })
    })

    // eslint-disable-next-line no-unused-vars
    window.KruxInstaller.os.onGet((_event, value) => {
      this.$nextTick(() => {
        if (value === 'linux') this.ktool = 'ktool-linux'
        if (value === 'win32') this.ktool = 'ktool-win.exe'
        if (value === 'darwin') this.ktool = 'ktool-mac'
      })
    })

    // eslint-disable-next-line no-unused-vars
    window.KruxInstaller.isMac10.onGet((_event, value) => {
      this.$nextTick(() => {
        if (value) this.ktool += '-10'
      })
    })

    // eslint-disable-next-line no-unused-vars
    window.KruxInstaller.openssl.onError((_event, value) => {
      this.$nextTick(() => {
        this.$emit('onSuccess', { page: 'VerifyOpensslErrorPage' })
      })
    })
  },
  watch: {
    async version (v) {
      if (v !== '') { 
        await window.KruxInstaller.device.get()
      }
    },
    async device (v) {
      if (v !== '') {
        await window.KruxInstaller.os.get()
      } 
    },
    async ktool (v) {
      if (v === 'ktool-win.exe') {
        await window.KruxInstaller.openssl.check()
      }
      if (v === 'ktool-mac') {
        await window.KruxInstaller.isMac10.get()
      }
    }
  }
}
</script>

<style>
.v-main{
  background: rgba(0, 0, 0);
} 
.v-btn{
  background:  rgba(0, 0, 0);
  color: rgba(255, 255, 255) !important;
}
.logo {
  color: rgba(255,255,255);
}
</style>
