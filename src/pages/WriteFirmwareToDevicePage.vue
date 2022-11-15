<template>
  <v-layout row wrap>
    <v-flex xs12 sm12>
      <v-card
        v-if="!isWritten"
        class="ma-5 pa-5"
      >
        <v-card-title>Flashing...</v-card-title>
        <v-card-subtitle>
          <b v-if="!done">Do not unpulg device or shutdown computer!</b>
          <b v-if="done">Output </b>
          <b v-if="done">(toogle developer tools to see all outputs).</b>
        </v-card-subtitle>
        <v-card-content>
          <v-card-text>
            <div class="console" v-html="html" />
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
            @click.prevent="$emit('onSuccess', { page: 'MainPage' })"
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
  async created () {  

    await window.KruxInstaller.flash.firmware()
 
    // eslint-disable-next-line no-unused-vars
    window.KruxInstaller.flash.onData((_event, value) => { 
      const output = this.parse(value)
      tmpHtml += output
      this.html = output
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
    }
  }
}
</script>

<style>
.console {
  font-family: monospace;
  text-align: left;
  background-color: black;
  color: #fff;
  overflow-y: auto;
  width: 390px;
  height: 360px;
}
</style>
