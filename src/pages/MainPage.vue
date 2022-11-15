<template>
  <v-layout row>
    <v-flex xs12 sm12>
      <v-container>
        <v-row dense>
          <v-col cols="12"> 
            <v-card class="ma-5 pa-5">
              <v-card-subtitle>
                Select Device
              </v-card-subtitle>
              <v-card-actions>
                <v-btn @click.prevent="$emit('onSuccess', { page: 'SelectDevicePage' })">
                  <v-icon>mdi-devices</v-icon> {{ device }}
                </v-btn>
              </v-card-actions>
            </v-card>
            <v-card class="ma-5 pa-5">
              <v-card-subtitle>
                Select between <b>selfcustody</b> or <b>odudex</b> releases
              </v-card-subtitle>
              <v-card-actions>
                <v-btn @click.prevent="$emit('onSuccess', { page: 'SelectVersionPage' })">
                   <v-icon>mdi-cube-outline</v-icon> {{ version }}
                </v-btn>
              </v-card-actions>
            </v-card>
            <v-card class="ma-5 pa-5">
              <v-card-actions> 
                <v-btn @click.prevent="$emit('onSuccess', { page: 'BeforeFlashDevicePage' })">
                  <v-icon>mdi-lightning-bolt-outline</v-icon> Flash to device
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
  data () {
    return {
      version: '',
      device: ''
    }
  },
  async created () {
    await window.KruxInstaller.version.get()

    // eslint-disable-next-line no-unused-vars
    window.KruxInstaller.version.onGet((_event, value) => {
      this.$nextTick(() => {
        this.version = value
      })
    })
  },
  watch: {
    async version (v) {
      if (v !== '') { 
        await window.KruxInstaller.device.get()

        // eslint-disable-next-line no-unused-vars
        window.KruxInstaller.device.onGet((_event, value) => {
          this.$nextTick(() => {
            this.device = value
          })
        })
      }
    }
  }
}
</script>

<style>
.v-main{
  background: rgba(0, 0, 0);
} 
.v-btn{
  background:  rgba(0, 0, 0);
  color: rgba(255, 255, 255) !important;
}
.logo {
  color: rgba(255,255,255);
}
</style>
