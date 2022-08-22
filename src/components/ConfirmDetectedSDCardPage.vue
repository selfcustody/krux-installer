<template>
  <v-container>
    <v-row align="justify">
      <v-col
        cols="32"
        sm12
      >
        <v-layout column wrap>
          <v-flex v-if="sdcard.error">
            <p>No SDCard detected.</p>
            <br/>
            <p>Click in the button below, insert your SDCard and try again</p>
            <br/>
            <v-btn
              color="green"
              @click.prevent="mountSDCard"
            >
              Try again
            </v-btn>
            <br/>
            <v-btn
              color="primary"
              @click.prevent="umountSDCard"
            >
              Back
            </v-btn>
          </v-flex>
          <v-flex v-if="!sdcard.error"> 
            <div v-if="state === 'umounted'">
              <p> We detected an <b>{{ state }} {{ sdcard.fstype }} {{ sdcard.size }} card at {{ sdcard.device }}</b></p>
              <p>
                Click in the button below to mount it
              </p>
              <br/>
              <v-btn
                color="green"
                @click.prevent="mountSDCard"
              >
                Mount it!
              </v-btn>
              <br/>
              <v-btn
                color="primary"
                @click.prevent="umountSDCard"
              >
                Back
              </v-btn>
            </div>
            <div v-if="state === 'mounting' || state === 'umounting'">
              <p> Waiting for administrator permissions... </p>
            </div>
            <div v-if="state === 'mounted'"> 
              <p> We detected an <b>{{ state }} {{ sdcard.fstype }} {{ sdcard.size }} card at {{ mountpoint }}</b></p>
              <p>
                SDCard mounted. Let's proceed with download
              </p>
              <br/>
              <v-btn
                color="green"
                @click.prevent="select_firmware"
              >
                Select firmware!
              </v-btn>
              <br/>
              <v-btn
                color="primary"
                @click.prevent="umountSDCard"
              >
                back
              </v-btn>
            </div>
          </v-flex>
        </v-layout>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>

export default {
  name: 'ConfirmDetectedSDCardPage',
  data () {
    return {
      device: '',
      size: 0,
      description: '',
      isFAT32: false,
      state: 'umounted'
    }
  },
  methods: {
    async mountSDCard () {
      this.state = 'mounting'
      await window.kruxAPI.sdcard_action({ action: 'mount' });

      // eslint-disable-next-line no-unused-vars
      window.kruxAPI.onMountAction((_event, value) => {
        this.state = value.state
        this.mountpoint = value.mountpoint
      });
    },
    async umountSDCard () {
      if (this.state === 'mounted') {
        this.state = 'umounting'
        await window.kruxAPI.sdcard_action({ action: 'umount' });

        // eslint-disable-next-line no-unused-vars
        window.kruxAPI.onMountAction((_event, value) => {
          this.state = value.state
          this.$emit('onError', { sdcard: this.mountpoint, page: 'DetectSDCardPage' })
        });

      } else {
        this.$emit('onError', { sdcard: this.mountpoint, page: 'DetectSDCardPage' })
      }
    },
    select_firmware () {
      this.$emit('onSuccess', { sdcard: this.mountpoint, page: 'SelectFirmwarePage' })
    }
  }
} 
</script>
