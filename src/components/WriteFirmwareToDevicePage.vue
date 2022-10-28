<template>
  <v-layout row wrap>
    <v-flex xs12 sm12>
      <v-card
        v-if="!isWritten"
        class="ma-5 pa-5"
      >
        <v-card-title>Flashing...</v-card-title>
        <v-card-subtitle>
          <b>Wait a moment</b>
        </v-card-subtitle>
        <v-card-content>
          <v-card-text>
            DO NOT UNPLUG DEVICE OR SHUTDOWN COMPUTER!
          </v-card-text>
        </v-card-content>
      </v-card>
      <v-card
        v-if="isWritten"
        class="ma-5 pa-5"
      >
        <v-card-title>Flashing done</v-card-title>
        <v-card-subtitle>
          Now your device should be rebooting! Enjoy!
        </v-card-subtitle>
        <v-card-content>
          <v-card-text>
            <div class="console" v-html="html" />
          </v-card-text>
        </v-card-content>
        <v-card-actions>
          <v-btn @click.prevent="$emit('onSuccess', { page: 'MainPage' })">
            Back
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
import AnsiUp from 'ansi_up'

export default {
  name: 'WriteFirmwareToDevicePage',
  async created () {  
    await window.kruxAPI.test_sipeed_device()

    await window.kruxAPI.flash_firmware_to_device()
  
    // eslint-disable-next-line no-unused-vars
    window.kruxAPI.onFlashingDone((_event, value) => {
      this.$nextTick(() => {
        // see 
        // https://www.appsloveworld.com/vuejs/100/8/stream-shell-output-to-web-front-end
        const ansi = new AnsiUp()
        value = value.replace(/%\s/, "\n")
        value = value.replace(/kiB\/s/g, "kiB/s\n")
        this.html = ansi.ansi_to_html(value).replace(/\n/gm, '<br>')
        this.isWritten = true
      })
    })

    // eslint-disable-next-line no-unused-vars
    window.kruxAPI.onFlashingError((_event, value) => { 
      this.$emit('onError', { error: value })
    })
  },
  data () {
    return {
      isWritten: false,
      html: ''
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
