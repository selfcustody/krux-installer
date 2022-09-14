<template>
  <v-layout row wrap>
    <v-flex xs12 sm12>
      <v-container>
        <v-row>
          <v-col cols="12">
            <v-card
              v-if="!isWritten && isAmigo"
              class="ma-5 pa-5"
            >
              <v-card-title>Choose amigo version</v-card-title>
              <v-card-content>
                <v-select
                  v-model="amigo"
                  :items="['tft', 'ips']"
                  label="Amigo type"
                />
              </v-card-content>
              <v-card-actions>
                <v-btn @click.prevent="setAmigo">
                  Select
                </v-btn>
              </v-card-actions>
            </v-card>
            <v-card
              v-if="!isWritten && !isAmigo"
              class="ma-5 pa-5"
            >
              <v-card-title>Flashing results</v-card-title>
              <v-card-content>
                <v-card-text>
                  <p v-for="(text, i) in response" :key="i">
                    {{ text }}
                  </p>
                </v-card-text>
              </v-card-content>
              <v-card-actions>
                <v-btn @click.prevent="flash">
                  Flash
                </v-btn>
              </v-card-actions>
            </v-card>
            <v-card
              v-if="isWritten"
              class="ma-5 pa-5"
            >
              <v-card-content>
                <v-card-text>
                  Now you can poweroff your device!
                </v-card-text>
              </v-card-content>
              <v-card-actions>
                <v-btn @click.prevent="$emit('onSuccess', { page: 'MainPage' })">
                  Go to initial page
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
  name: 'WriteFirmwareToDevicePage',
  async created () {
    await window.kruxAPI.get_device()

    // eslint-disable-next-line no-unused-vars
    window.kruxAPI.onGetDevice(async (_event, value) => {
      if (value.vendorId === '0403' && value.vendorId === '6010') {
        this.isAmigo = true
      }
      this.device = value
    })
  },
  data () {
    return {
      device: null,
      isWritten: false,
      isAmigo: false,
      amigo: '',
      ready: false,
      response: ['Waiting...']
    }
  },
  methods: {
    async setAmigo () {
      this.device.type = this.amigo
      await window.kruxAPI.set_device(this.device)
    },
    async flash () {
      await window.kruxAPI.write_firmware_to_device()
    
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
    }
  }
}
</script>

<style>
  .v-card-text >>> p {
    font-size: 0.5em;
  }
</style>
