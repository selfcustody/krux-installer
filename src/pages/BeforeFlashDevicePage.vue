<template>
  <v-layout
    row wrap
    id="before-flash-device-page"
  >
    <v-flex xs12>
      <v-card class="ma-5 pa-5">
        <v-card-title id="before-flash-device-page-card-title">
          Flash to device
        </v-card-title>
        <v-card-subtitle
          id="before-flash-device-page-card-subtitle-version"
        >
          <b>version</b>: {{ version }}
        </v-card-subtitle> 
        <v-card-subtitle
          id="before-flash-device-page-card-subtitle-device"
        >
          <b>device</b>: {{ device }}
        </v-card-subtitle>
        <v-card-content>
          <v-card-text v-for="(text, i) in texts" :key="i">
            {{ text }}
          </v-card-text>
        </v-card-content>
        <v-card-actions>
          <v-btn
            id="before-flash-device-page-flash-button"
            @click="$emit('onSuccess', { page: 'WriteFirmwareToDevicePage' })"
          >
            Flash
          </v-btn>
          <v-btn
            id="before-flash-device-page-back-button"
            @click="$emit('onSuccess', { page: 'MainPage' })"
          >
            Back
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>

export default {
  name: 'BeforeFlashDevicePage',
  data () {
    return {
      version: '',
      device: '',
      texts: [
        'Flash to device is required when you intend to install krux for the first time on your device (or for development and testing purposes).',
        'Once you plugged an powered it, click on "flash" button',
      ]
    }
  },
  watch: {
    async version (value) {
      if (value !== '') {
        await window.KruxInstaller.device.get()
      }
    }
  },
  async created () {
    await window.KruxInstaller.version.get()

    // eslint-disable-next-line no-unused-vars
    window.KruxInstaller.version.onGet((_event, value) => {
      this.version = value
    })

    // eslint-disable-next-line no-unused-vars
    window.KruxInstaller.device.onGet((_event, value) => {
      this.device = value
    })
  }
}
</script>
