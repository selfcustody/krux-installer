<template>
  <v-layout row wrap>
    <v-flex xs12 sm12>
      <v-container>
        <v-row>
          <v-col cols="12">
            <v-card class="ma-5 pa-5">
              <v-card-title>
                Select the device you want install
              </v-card-title>
              <v-card-subtitle>
                {{ version }}
              </v-card-subtitle>
              <v-card-content>
                <v-card-text>
                  <v-select
                    v-model="device"
                    :items="devices"
                    label="Device"
                  />
                </v-card-text>
              </v-card-content>
              <v-card-actions>
                <v-btn @click.prevent="select">
                  Proceed
                </v-btn>
                <v-btn @click.prevent="$emit('onSuccess', { page: 'ConfirmDetectedSDCardPage' })">
                  Back
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
  name: 'SelectFirmwarePage', 
  async created () { 
    await window.kruxAPI.get_version()

    // eslint-disable-next-line no-unused-vars
    window.kruxAPI.onGetVersion((_event, value) => {
      this.version = value
    })
  }, 
  data () {
    return {
      version: '',
      device: '',
      devices: [
        'maixpy_m5stickv',
        'maixpy_amigo_ips',
        'maixpy_amigo_tft',
        'maixpy_bit',
        'maixpy_dock'
      ],
    }
  },
  methods: {
    async select () {
      await window.kruxAPI.set_device(this.device)

      // eslint-disable-next-line no-unused-vars
      window.kruxAPI.onSetDevice((_event, value) => {
        const regexp_official = /selfcustody.*/g
        const regexp_test = /odudex.*/g
        if (this.version.match(regexp_official)) {
          this.$emit('onSuccess', { page: 'DownloadOfficialReleasePage' })
        } else if (this.version.match(regexp_test)) { 
          this.$emit('onSuccess', { page: 'DownloadTestReleasePage' })
        } else {
          this.$emit('onError', { error: new Error(`Invalid version '${this.version}'`)})
        }
      })
    }
  }
}
</script>
