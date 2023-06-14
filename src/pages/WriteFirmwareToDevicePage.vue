<template>
  <v-layout
    row
    wrap
    id="write-firmware-to-device-page"
  >
    <v-flex xs12 sm12>
      <v-card
        v-if="!isWritten"
        class="ma-5 pa-5"
      >
        <v-card-title id="write-firmware-to-device-page-card-title">Flashing...</v-card-title>
        <v-card-subtitle id="write-firmware-to-device-page-card-subtitle">
          <b v-if="!done">Do not unplug device or shutdown computer!</b>
          <b v-if="done">Output (toogle developer tools to see all of them).</b>
        </v-card-subtitle>
        <v-card-content id="write-firmware-to-device-page-card-content">
          <v-card-text>
            <div id="write-firmware-to-device-page-console" class="console" v-html="html" ref="console" />
          </v-card-text>
        </v-card-content>
        <v-card-actions>
          <v-progress-linear 
            v-if="!done"
            :indeterminate="true"
            color="red"
          />
          <v-btn 
            v-if="done"
            @click="onBack"
          >
            Back
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
import AnsiUp from 'ansi_up'

let tmpHtml = ''

export default {
  name: 'WriteFirmwareToDevicePage', 
  data () {
    return {
      done: false,
      html: ''
    }
  },
  beforeMount () {
    this.$data.html = ''
  },
  created () {
    setTimeout(async function () {
      await window.KruxInstaller.flash.firmware()
    }, 1000)

    // eslint-disable-next-line no-unused-vars
    window.KruxInstaller.flash.onData((_event, value) => { 
      this.$nextTick(() => {
        const output = this.parse(value)
        tmpHtml += output
        this.html = output
      })
    })

    // eslint-disable-next-line no-unused-vars
    window.KruxInstaller.flash.onSuccess((_event, value) => {
      this.$nextTick(() => {
        this.html = tmpHtml
        this.done = true
      })
    })

    // eslint-disable-next-line no-unused-vars
    window.KruxInstaller.flash.onError((_event, value) => {
      this.done = false
      this.$emit('onError', value)
    })
  },
  methods: {
    // see 
    // https://www.appsloveworld.com/vuejs/100/8/stream-shell-output-to-web-front-end
    parse (msg) { 
      msg = msg.replace(/%\s/, "\n")
      msg = msg.replace(/kiB\/s/g, "kiB/s\n")
      
      const ansi = new AnsiUp()
      return ansi.ansi_to_html(msg).replace(/\n/gm, '<br>')
    },
    onBack () {
      this.$nextTick(() => {
        this.$emit('onSuccess', { page: 'MainPage' })
      })
    }
  }
}
</script>

<style>
.console {
  font-family: monospace;
  font-size: 10px;
  text-align: left;
  background-color: black;
  color: #fff;
  overflow-y: auto;
  width: 390px;
  height: 360px;
}
</style>
