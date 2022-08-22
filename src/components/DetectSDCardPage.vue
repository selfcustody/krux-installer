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
              <b>It's imperative that SDCard is formatted to FAT32 filesystem</b>. If it's not formatted, close this program and format it.
            </p>
            <br/>
            <p>
              Then we will mount it (administrator privileges will be required), and we will use the selected version of firmware. If a version was not selected, press <b>Back</b> and the <b>Select version</b> page. If you selected an <b>official release</b> the <b>firmware.bin</b> and <b>firmware.bin.sig</b> will be written to the SDCard. If you selected a <b>test release</b>, only the <b>firmware.bin</b> will be written to SDCard.
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
              @click.prevent="$emit('onSuccess', { page: 'MainPage' })"
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
      await window.kruxAPI.sdcard_action({ action: 'detect' })
    
      // eslint-disable-next-line no-unused-vars
      window.kruxAPI.onDetectedSDCardFound((_event, value) => {
        this.$emit('onSuccess', { page: 'ConfirmDetectedSDCardPage' })
      })
    }
  }
}
</script>
