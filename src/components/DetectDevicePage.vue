<template>
  <v-container fluid>
    <v-row align="justify">
      <v-col
        cols="12"
        sm="6"
      >
        <v-layout
          row
          wrap
        >
          <v-flex>
            <p> {{ status }} </p>
          </v-flex>
          <v-flex
            v-if="device !== ''"
          >
            <p> It's OK? </p>
          </v-flex>
        </v-layout>   
      </v-col>
    </v-row>
    <br />
    <v-row>
      <v-col
        cols="12"
        sm="6"
      >
        <v-layout column wrap>
          <v-flex
            v-if="device === ''"
          >
            <v-btn
              color="primary"
              @click.prevent="detectDevice"
            >
              Start detection
            </v-btn>
          </v-flex>
          <v-flex
            v-if="device !== ''"
          >
            <v-btn
              color="primary"
              @click.prevent="$emit('onDetectedDevice', device)"
            >
              It's OK
            </v-btn>
          </v-flex>
          <v-flex
            v-if="device !== ''"
          >
            <v-btn
              color="primary"
              @click.prevent="$emit('onWrongDetectedDevice')"
            >
              It's wrong
            </v-btn>
          </v-flex>
        </v-layout>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'DetectDevicePage',
  data () {
    return {
      status: 'Connect your device, power on it, and then click in button below',
      device: '',
    }
  },
  methods: {
    async detectDevice () {
      await window.kruxAPI.start_detect_device()
      // eslint-disable-next-line no-unused-vars
      window.kruxAPI.onDetectedDeviceFoundUsb(async (_event, value) => {
        this.status = `Device ${value} detected.`
        this.device = value
        console.log(`[ INFO ] ${this.status}`)

        // this will be moved in another commit
        await window.kruxAPI.stop_detect_device()
      })

      // eslint-disable-next-line no-unused-vars
      window.kruxAPI.onStopMonitoringDeviceUsb(async (_event, value) => {
        const msg = `Stopped monitoring ${this.device}`
        console.warn(msg)
        window.alert(msg)
      })
    }
  }
}
</script>
