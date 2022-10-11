<template>
  <v-layout row>
    <v-flex xs12 sm12>
      <v-container>
        <v-row dense>
          <v-col cols="12"> 
            <v-card class="ma-5 pa-5">
              <v-card-subtitle>
                Select device firmware
              </v-card-subtitle>
              <v-card-actions>
                <v-btn @click.prevent="$emit('onSuccess', { page: 'SelectFirmwarePage' })">
                  {{ device }}
                </v-btn>
              </v-card-actions>
            </v-card> 
            <v-card class="ma-5 pa-5">
              <v-card-subtitle>
                Select betweeen "Flash firmware onto device" or "Write firmware to microSD"
              </v-card-subtitle>
              <v-card-actions>
                <v-btn @click.prevent="$emit('onSuccess', { page: 'SelectActionPage' })">
                  {{ action }}
                </v-btn>
              </v-card-actions>
            </v-card>
            <v-card class="ma-5 pa-5">
              <v-card-subtitle>
                Select between available official (selfcustody) or test (odudex) releases,
              </v-card-subtitle>
              <v-card-actions>
                <v-btn @click.prevent="$emit('onSuccess', { page: 'SelectVersionPage' })">
                  {{ version }}
                </v-btn>
              </v-card-actions>
            </v-card>
            <v-card class="ma-5 pa-5">
              <v-card-subtitle>
                Execute the selected action combined with the select firmware's version
              </v-card-subtitle>
              <v-card-actions>
                <v-btn @click.prevent="$emit('onSuccess', { page: 'ExecutePage' })">
                  Execute
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
  name: 'MainPage',
  /**
   * If user selected:
   * - a version: change the button 'version' with the selected string
   * - a device: change the button 'flash' with the selected string
   * - a firmware: change the button 'firmware' with the selected string
   */
  async created () {
    await window.kruxAPI.get_version()

    // eslint-disable-next-line no-unused-vars
    window.kruxAPI.onGetVersion((_event, value) => {
      this.$nextTick(() => {
        this.version = value
      })
    })

    await window.kruxAPI.get_action()
    
    // eslint-disable-next-line no-unused-vars
    window.kruxAPI.onGetAction((_event, value) => {
      this.$nextTick(() => {
        this.action = value
      })
    })

    await window.kruxAPI.get_device()

    // eslint-disable-next-line no-unused-vars
    window.kruxAPI.onGetDevice((_event, value) => {
      this.$nextTick(() => {
        this.device = value
      })
    })
  },
  data () {
    return {
      version: '',
      action: '',
      device: ''
    }
  }
}
</script>

<style>
.v-main{
  background: rgba(242, 169, 0);
} 
.v-btn{
  background:  rgba(0, 150, 255);
  color:       rgba(255, 255, 255);
}
</style>
