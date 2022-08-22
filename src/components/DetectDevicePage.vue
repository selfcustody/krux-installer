<template>
  <v-container grid-list-md text-xs-center>
    <v-layout
      row
      wrap
    >
      <v-flex
        xs12
        v-if="devices.length === 0"
      >
        <v-card
          v-for="(text, i) in texts"
          :key="i"
          flat
        >
          <v-card-text>{{ text }} </v-card-text>
        </v-card>
        <br/>
        <v-card
          flat
        >
          <v-btn
            color="green"
            @click.prevent="detect"
          >
            Detect
          </v-btn>
        </v-card>
        <br/>
        <v-card
          flat
        >
          <v-btn  
            color="primary"
            @click.prevent="$emit('onSuccess', { page: 'MainPage' })"
          >
            Back
          </v-btn>
        </v-card>
      </v-flex>
      <v-flex
        xs12
        v-if="devices.length > 0"
      >
        <v-card
          v-for="(device, i) in devices"
          :key="i"
        >
          <v-card-title> {{ device.pnpId }} </v-card-title>
          <v-card-text>
            <p><b>path</b>: {{ device.path }} </p>
            <p><b>manufacturer</b>: {{ device.manufacturer }} </p>
            <p><b>vendorId</b>: {{ device.vendorId }} </p>
            <p><b>productId</b>: {{ device.productId }} </p>
          </v-card-text>
          <v-card-actions>
            <v-chip
              color="primary"
            >
              {{ device.message }}
            </v-chip>
          </v-card-actions>
          <v-card-actions>
            <v-btn
              v-for="(d,i) in device.devices"
              :key="i"
              dark
              color="success"
              @click.prevent="select({ path: device.path, alias: d})"
            >
              Select {{ d }}
            </v-btn>
          </v-card-actions>
        </v-card>
        <v-card>
          <v-btn
            color="primary"
            @click="$emit('onSuccess', { page: 'MainPage' })"
          >
            Back
          </v-btn>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
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
      devices: []
    }
  },
  methods: {
    async detect () {
      await window.kruxAPI.serialport({
        action: 'list'
      })
    
      // eslint-disable-next-line no-unused-vars
      window.kruxAPI.onSerialportList((_event, value) => {
        this.devices = value
      })
    },
    async select(device) {
      await window.kruxAPI.serialport({
        action: 'select',
        device: device
      })

      // eslint-disable-next-line no-unused-vars
      window.kruxAPI.onSerialportSelected((_event, value) => {
        this.$emit('onSuccess', { page: 'FlashDevice' })
      })
    }
  }
}
</script>
