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
              <b>Update firmware to SDCard</b> is required when you intend to update a newly krux firmware krux.
            </p>
            <br/>
            <p>
                We will first <b>detect</b> your SDcard; and, if necessary, format it to <b>FAT32</b> filesystem.
            </p>
            <br/>
            <p>
                Then we will ask which device you want update to, so that we can download appropriate <b>firmware.bin</b> and <b>firmware.bin.sig</b> files.
            </p>
            <br/>
            <p>
                Next, these files will be written to the SDCard, which will be unmounted, so you can use it on your device.
            </p>
            <br/>
            <v-btn  
              color="green"
              @click.prevent="detectSDCard"
            >
              Start
            </v-btn>
            <br/>
            <v-btn
              color="primary"
              @click.prevent="$emit('onBack', 'main')"
            >
              Back
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
    async detectSDCard () {
      await window.kruxAPI.start_detect_sdcard()
    
      // eslint-disable-next-line no-unused-vars
      window.kruxAPI.onDetectedSDCardFound((_event, value) => {
        this.$emit('onDetectedSDCard', value)
      })
    }
  }
}
</script>
