<template>
  <v-layout row wrap>
    <v-flex xs12>
      <v-container>
        <v-row>
          <v-col cols="12">
            <v-card v-if="devices.length === 0">
              <v-card-content>
                <v-alert
                  model="true"
                  border="left"
                  close-text="Close Alert"
                  type="info"
                  dismissible
                  outlined
                >
                  <p v-for="(text, i) in texts" :key="i">
                    {{ text }}
                  </p>
                </v-alert>
              </v-card-content>
              <v-card-actions>
                <v-btn @click.prevent="detect">
                  Detect
                </v-btn>
                <v-btn @click.prevent="$emit('onSuccess', { page: 'MainPage' })">
                  Back
                </v-btn>
              </v-card-actions>
            </v-card>
            <div v-if="devices.length > 0">
              <v-card
                v-for="(device, i) in devices"
                :key="i"
                class="ma-5 pa-5"
              >
                <v-card-title>{{ device.manufacturer }}</v-card-title>
                <v-card-subtitle>{{ device.message }}</v-card-subtitle>
                <v-card-content>
                  <v-card-text
                    v-for="(p, j) in ['path', 'vendorId', 'productId']"
                    :key="j"
                  >
                    <b>{{ p }}</b> {{ device[p] }}
                  </v-card-text>
                </v-card-content>
                <v-card-actions>
                  <v-btn @click.prevent="select(device)">
                    Select
                  </v-btn>
                  <v-btn @click="$emit('onSuccess', { page: 'MainPage' })">
                    Back
                  </v-btn>
                </v-card-actions>
              </v-card>
            </div>
          </v-col>
        </v-row>
      </v-container>
    </v-flex>
  </v-layout>
</template>

<script>

export default {
  name: 'DetectDevicePage',
  data () {
    return {
      texts: [
        'Flash to device is required when you intend to install krux for the first time on your device (or for development and testing purposes).',
        'It\'s supposed that you already selected a krux version.',
        'Once you plugged an powered it, click on "detect" button',
        'WARNING: some devices share the same vendorIDs and productIDs; maybe is possible to confirm which device you are using, so we can flash the properly selected version\'s firmware.'
      ],
      devices: [],
      krux_device: null
    }
  },
  methods: {
    async detect () {
      window.kruxAPI.list_serialport()
    
      // eslint-disable-next-line no-unused-vars
      window.kruxAPI.onListSerialport((_event, value) => {
        this.devices = value
      })
    },
    async select (device) {
      const d = JSON.parse(JSON.stringify(device))
      await window.kruxAPI.set_device(d)
      this.$emit('onSuccess', { page: 'WriteFirmwareToDevicePage' })
    }
  }
}
</script>
