<template>
  <v-layout
    align-start
    justify-start
    row
    fill-height
    id="select-device-page"
  >
    <v-flex xs12 sm4>
      <v-card class="ma-5 pa-5">
        <v-card-title
          id="select-device-page-card-title"
        >
          <v-icon>mdi-devices</v-icon>
          Choose the firmware's device that you want install
        </v-card-title>
        <v-card-content
          id="select-device-page-card-content"
        >
          <v-select
            v-model="device"
            :items="devices"
            label="Device"
            id="select-device-page-form-select"
          />
        </v-card-content>
        <v-card-actions>
          <v-btn
            @click.prevent="select"
            id="select-device-page-form-select-button"
          >
            Select
          </v-btn>
          <v-btn 
            @click.prevent="$emit('onSuccess', { page: 'MainPage' })"
            id="select-device-page-form-back-button"
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
  name: 'SelectDevicePage', 
  data () {
    return {
      device: '',
      devices: [
        'maixpy_m5stickv',
        'maixpy_amigo_ips',
        'maixpy_amigo_tft',
        'maixpy_bit',
        'maixpy_dock'
      ],
    }
  },
  methods: {
    async select () {
      await window.KruxInstaller.device.set(this.device)

      // eslint-disable-next-line no-unused-vars
      window.KruxInstaller.device.onSet((_event, value) => {
        this.$nextTick(() => {
          this.$emit('onSuccess', { page: 'MainPage' })
        })
      })
    }
  }
}
</script>
