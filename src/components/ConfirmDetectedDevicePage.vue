<template>
  <v-container>
    <v-row align="justify">
      <v-col
        cols="32"
        sm12
      >
        <v-layout column wrap>
          <v-flex> 
            <p> With your aid, we detected <b>{{ device }}</b>. But it's good that you confim.</p>
            <br/>
            <div 
              v-if="device === 'maixpy_amigo/maixy_bit'"
            >
              <p>
                Both <b>Sipeed Amigo</b> (IPS and TFT), <b>Sipeed Bit</b> use the same chip for serial communication and have the same Vendor and Product IDs.
              </p>
              <br/>
              <v-btn
                v-for="(d, i) in sharedDevices()"
                :key="i"
                color="primary"
                @click.prevent="$emit('onSuccess', { device: d.name, page: 'DownloadKbootPage' })"
              >
                I'm using {{ d.label }}
              </v-btn>
              <br/>
            </div>
            <div
              v-else
            >
              <v-btn
                v-for="(d, i) in uniqueDevices(device)"
                :key="i"
                color="primary"
                @click.prevent="$emit('onSuccess', { device: d.name, page: 'DownloadKbootPage' })"
              >
                I'm using {{ d.label }}
              </v-btn>
            </div>
            <div>
              <v-btn
                color="red"
                @click.prevent="$emit('onError', { page: 'DetectDevicePage' })"
              >
                Wait! My device is incorrect!
              </v-btn>
            </div>
          </v-flex>
        </v-layout>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { filter } from 'lodash'

export default {
  name: 'ConfirmDetectedDevicePage',
  props: {
    device: {
      type: String,
      required: true
    }
  },
  data () {
    return {
      devices_list: [
        {
          label: 'M5StickV',
          name: 'maixpy_m5stickv',
          vidpid: 'unique'
        },
        {
          label: 'Dock',
          name: 'maixpy_dock',
          vidpid: 'unique'
        },
        {
          label: 'Amigo IPS',
          name: 'maixpy_amigo_ips',
          vidpid: 'shared'
        },
        {
          label: 'Amigo TFT',
          name: 'maixpy_amigo_tft',
          vidpid: 'shared'
        },
        {
          label: 'Bit',
          name: 'maixpy_bit',
          vidpid: 'shared'
        }
      ]
    }
  },
  methods: {
    uniqueDevices (name) {
      return filter(this.devices_list, { name: name, vidpid: 'unique' })    
    },
    sharedDevices () {
      return filter(this.devices_list, { vidpid: 'shared' })
    }
  }
} 
</script>
