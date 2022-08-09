<template>
  <v-container fluid>
    <v-row align="justify">
      <v-col
        cols="32"
        sm12
      >
        <v-layout column wrap>
          <v-flex v-if="!sdcard_file">
            <p>
              Now let's write <b>{{ resource }} </b> to <b>{{ sdcard }}</b>. 
            </p>
            <v-btn  
              color="green"
              @click.prevent="writeFirmwareToSDCard"
            >
              Write it!
            </v-btn>
            <br/>
            <v-btn
              color="primary"
              @click.prevent="$emit('onError', { page: 'SelectFirmwarePage' })"
            >
              Back
            </v-btn>
          </v-flex>
          <v-flex v-else>
            <p> <b>{{ resource }}</b> was copied to <b>{{ firmware_file }}</b>.</p>
            <br/> 
            <p> Now you can umount sdcard, and put it on your device!</p>
            <br/>
            <v-btn
              color="primary"
              @click.prevent="umountSDCard"
            >
              Umount Sdcard
            </v-btn>
          </v-flex>
        </v-layout>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'WriteFirmwareToSDCardPage',
  props: {
    resource: {
      type: String,
      required: true
    },
    sdcard: {
      type: String,
      require: true
    }
  },
  data () {
    return {
      sdcard_file: null
    }
  },
  methods: {
    async writeFirmwareToSDCard () {
      try {
        await window.kruxAPI.sdcard_action({
          action: 'copyto',
          origin: this.resource,
          destination: `${this.sdcard}/firmware.bin`
        })
    
        // eslint-disable-next-line no-unused-vars
        window.kruxAPI.onFirmwareWritedOnSDCard((_event, value) => {
          if (value !== '') {
            this.wrote = true
            this.firmware_file = value
            this.$emit('onSuccess', { resource: value, page: 'ConfirmFirmwareWritedOnSDCardPage' })
          } else {
            this.$emit('onError', { page: 'ConfirmDetectedSDCardPage' })
          }
        })
      } catch (error) {
        this.$emit('onError', { page: 'ConfirmDetectedSDCardPage' }) 
      }
    },
    async umountSDCard () {
      try {
        await window.kruxAPI.stop_mount_sdcard();

        // eslint-disable-next-line no-unused-vars
        window.kruxAPI.onUmountedSDCard((_event, value) => {
          this.$emit('onSuccess', { sdcard: '', page: 'MainPage' })
        });
      } catch (error) {
        console.log(error)
        this.$emit('onError', { page: 'ConfirmDetectedSDCardPage' })
      }
    }
  }
}
</script>
