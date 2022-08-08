<template>
  <v-container fluid>
    <v-row align="justify">
      <v-col
        cols="12"
        sm="6"
      >
        <v-subheader>
          <p>Select the device you want install to</p>
        </v-subheader>
      </v-col>
      <v-col
        cols="12"
        sm="6"
      >
        <v-select
          v-model="device"
          :items="devices"
          label="device"
        />
      </v-col>
    </v-row>
    <br />
    <v-row align="justify">
      <v-col
        cols="12"
        sm="6"
      >
        <v-btn
          color="green"
          @click.prevent="$emit('onSuccess', { sdcard: this.sdcard, device: device, page: 'DownloadFirmwarePage' })"
        >
          Download firmware
        </v-btn>
        <br/>
        <v-btn
          color="primary"
          @click.prevent="$emit('onError', { page: 'ConfirmDetectedSDCardPage' })"
        >
          Back
        </v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'SelectFirmwarePage', 
  props: {
    sdcard: {
      type: String,
      required: true
    }
  },
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
  }
}
</script>
