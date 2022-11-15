<template>
  <v-layout row wrap>
    <v-flex xs12 sm12>
      <v-container>
        <v-row>
          <v-col cols="12">
            <v-card
              v-if="!isWritten"
              class="ma-5 pa-5"
            >
              <v-card-title>
                Waiting for Firmware to be copied...
              </v-card-title>
            </v-card>
            <v-card
              v-if="isWritten"
              class="ma-5 pa-5"
            >
              <v-card-content>
                <v-card-text>
                  Now you can umount sdcard, and put it on your device!
                </v-card-text>
              </v-card-content>
              <v-card-actions>
                <v-btn @click.prevent="umountSDCard">
                  Umount Sdcard
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-flex>
  </v-layout>
</template>

<script>
export default {
  name: 'WriteFirmwareToSDCardPage',
  async created () {
    await window.kruxAPI.get_version()
    
    // eslint-disable-next-line no-unused-vars
    window.kruxAPI.onGetVersion((_event, value) => {
      this.version = value
    })
  },
  watch: {
    async version (value) {
      if (value !== '') {
        await window.kruxAPI.get_device()

        // eslint-disable-next-line no-unused-vars
        window.kruxAPI.onGetDevice((_event, value) => {
          this.device = value
        })
      }
    },
    async device (value) {
      if (value !== '') { 
        await window.kruxAPI.sdcard_action({ action: 'copy_firmware_bin' })

        // eslint-disable-next-line no-unused-vars
        window.kruxAPI.onFirmwareCopied((_event, val) => {
          if (val !== '') {
            this.isWritten = true
          } else {
            this.$emit('onError', { page: 'ConfirmDetectedSDCardPage' })
          }
        })
      }
    }
  },
  data () {
    return {
      isWritten: false,
      version: '',
      device: ''
    }
  },
  methods: {
    async umountSDCard () {
      await window.kruxAPI.sdcard_action({ action: 'umount' });

      // eslint-disable-next-line no-unused-vars
      window.kruxAPI.onMountAction((_event, value) => {
        this.$emit('onSuccess', { sdcard: '', page: 'MainPage' })
      });

      // eslint-disable-next-line no-unused-vars
      window.kruxAPI.onMountActionError((_event, value) => {
        this.$emit('onError', { error: value })
      });
    }
  }
}
</script>
