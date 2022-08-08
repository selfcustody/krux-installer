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
              <b>Update firmware to SDCard</b> is required when you intend to update a newly krux firmware.
            </p>
            <br/>
            <p>
                We will first <b>detect</b> your SDcard.
            </p>
            <br/>
            <p>
              <b>It's imperative that SDCard is formatted to FAT32 filesystem</b>.
            </p>
            <br/>
            <p>
              If not, close this program and format it.
            </p>
            <br/>
            <p>
              Then we will mount it and ask which firmware you want update to, so that we can download appropriate <b>firmware.bin</b> and <b>firmware.bin.sig</b> files.
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
              @click.prevent="$emit('onError', { page: 'MainPage' })"
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
  name: 'DetectSDCardPage',
  methods: {
    async detectSDCard () {
      await window.kruxAPI.start_detect_sdcard()
    
      // eslint-disable-next-line no-unused-vars
      window.kruxAPI.onDetectedSDCardFound((_event, value) => {
        this.$emit('onSuccess', { sdcard: value, page: 'ConfirmDetectedSDCardPage' })
      })
    }
  }
}
</script>
