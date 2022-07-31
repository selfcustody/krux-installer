<template>
  <v-container fluid>
    <v-row align="justify">
      <v-col
        cols="32"
        sm12
      >
        <v-layout column wrap>
          <v-flex>
            <p>
              <b>Flash to device</b> is required when you intend to install krux for the first time on your device (or for development and testing purposes).
            </p>
            <br/>
            <p> We will first <b>detect</b> your <a href="https://selfcustody.github.io/krux/getting-started/installing/#hardware">device</a> so that we can download and verify the appropriate <b>kbook.kfpkg</b> file. </p>
            <br/>
            <p> Then we will <a href="https://selfcustody.github.io/krux/getting-started/installing/#flash-the-firmware-onto-the-m5stickv">flash</a> the <b>kboot.kfpkg</b> into device.</p>
            <br/>
            <p> Connect your device, power on it, and then click in button below </p>
            <br/>
            <v-btn  
              color="primary"
              @click.prevent="detectDevice"
            >
              Start detection
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
      device: ''
    }
  },
  methods: {
    async detectDevice () {
      await window.kruxAPI.start_detect_device()
    
      // eslint-disable-next-line no-unused-vars
      window.kruxAPI.onDetectedDeviceFoundUsb((_event, value) => {
        console.log(value)
        this.$emit('onDetectedDevice', value)
      })
    }
  }
}
</script>
