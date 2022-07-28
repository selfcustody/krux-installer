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
    <v-row>
      <v-btn
        color="primary"
        @click.prevent="$emit('changePage', device)"
      >
        Go
      </v-btn>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'InstallToDevicePage',
  data () {
    return {
      device: '',
      devices: [
        'maixpy_m5stickv',
        'maixpy_amigo_ips',
        'maixpy_bit',
        'maixpy_bit_ov5642',
        'maixpy_dock'
      ],
    }
  }
}
</script>