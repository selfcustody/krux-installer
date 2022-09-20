<template>
  <v-layout row wrap>
    <v-flex xs12 sm12>
      <v-card
        v-if="!isWritten"
        class="ma-5 pa-5"
      >
        <v-card-title>Flashing...</v-card-title>
        <v-card-content>
          <v-card-text
            v-for="(text, i) in response"
            :key="i"
          >
            {{ text }}
          </v-card-text>
        </v-card-content>
      </v-card>
      <v-card
        v-if="isWritten"
        class="ma-5 pa-5"
      >
        <v-card-title>Flashing done</v-card-title>
        <v-card-content>
          <v-card-text>
            Now you can poweroff your device!
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
export default {
  name: 'WriteFirmwareToDevicePage',
  async created () {  
    await window.kruxAPI.flash_firmware_to_device()
    
    // eslint-disable-next-line no-unused-vars
    window.kruxAPI.onFlashing((_event, value) => {
      this.response.push(value)
    })

    // eslint-disable-next-line no-unused-vars
    window.kruxAPI.onFlashingError((_event, value) => { 
      this.$emit('onError', { error: value })
    })

    // eslint-disable-next-line no-unused-vars
    window.kruxAPI.onFlashingDone((_event, value) => {
      this.isWritten = true
    })
  },
  data () {
    return {
      isWritten: false,
      response: []
    }
  }
}
</script>

<style>
  .v-card-text >>> p {
    font-size: 0.5em;
  }
</style>
