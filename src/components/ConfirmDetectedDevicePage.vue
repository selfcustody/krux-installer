<template>
  <v-container>
    <v-row align="justify">
      <v-col
        cols="32"
        sm12
      >
        <v-layout column wrap>
          <v-flex> 
            <p> With your aid, we detected <b>{{ device }}</b></p>
            <br/>
            <p
              v-if="device === 'maixpy_amigo_ips/maixpy_bit/maixy_bit_ov5642'"
            >
              Both <b>Sipeed Amigo IPS</b>,  <b>Sipeed Bit</b> and <b>Sipeed Bit ov5642</b> use the same chip for serial communication and have the same Vendor and Product IDs.
            </p>
            <br/>
            <p> It will be necessary to confirm which of these devices you are using.</p>
            <br/>
            <v-btn
              v-if="device === 'maixpy_amigo_ips/maixpy_bit/maixy_bit_ov5642'"
              color="primary"
              @click.prevent="$emit('onConfirmDetectedDevice', 'maixpy_amigo_ips')"
            >
              I'm using Amigo IPS
            </v-btn>
            <br/>
            <v-btn 
              v-if="device === 'maixpy_amigo_ips/maixpy_bit/maixy_bit_ov5642'"
              color="primary"
              @click.prevent="$emit('onConfirmDetectedDevice', 'maixpy_bit')"
            >
              I'm using Bit
            </v-btn>
            <br/>
            <v-btn
              v-if="device === 'maixpy_amigo_ips/maixpy_bit/maixy_bit_ov5642'"
              color="primary"
              @click.prevent="$emit('onConfirmDetectedDevice', 'maixpy_bit_ov5642')"
            >
              I'm using Bit ov5642
            </v-btn>
            <v-btn
              v-if="device === 'maixpy_m5stickv'"
              color="primary"
              @click.prevent="$emit('onConfirmDetectedDevice', 'maixpy_m5stickv')"
            >
              I'm using M5StickV
            </v-btn>
            <br/>
            <v-btn
              v-if="device === 'maixpy_dock'"
              color="primary"
              @click.prevent="$emit('onConfirmDetectedDevice', 'maixpy_dock')"
            >
              I'm using Dock
            </v-btn>
            <v-btn
              color="red"
              @click.prevent="$emit('onWrongConfirmDetectedDevice')"
            >
              Wait! None of these are my device!
            </v-btn>
          </v-flex>
        </v-layout>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'ConfirmDetectedDevicePage',
  props: {
    device: {
      type: String,
      required: true
    }
  }
} 
</script>
