<template>
  <v-item-group id="select-device-page">
    <v-container>
      <v-row v-for="(device, i) in devices" :key="i">
        <v-col>
          <v-item v-slot="{ selectedClass }">
            <v-card
              variant="outlined"
              :class="[selectedClass]"
              @click.prevent="selectDevice(device)"
              :id="`select-device-page-${device}-button`"
            >
              <v-card-title
                :id="`select-device-page-${device}-text`"
              >
                {{ device }}
              </v-card-title>
            </v-card>
          </v-item>
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <v-item v-slot="{ selectedClass }">
            <v-card
              variant="outlined"
              :class="[selectedClass]"
              @click.prevent="back()"
              id="select-device-page-back-button"
            >
              <v-card-title
                id="select-device-page-back-text"
              >
                Back
              </v-card-title>
            </v-card>
          </v-item>
        </v-col>
      </v-row>
    </v-container>
  </v-item-group>
</template>

<script setup lang="ts">
import { Ref, ref } from 'vue'

const devices: Ref<string[]> = ref([
  'maixpy_m5stickv',
  'maixpy_amigo',
  'maixpy_amigo_ips',
  'maixpy_amigo_tft',
  'maixpy_bit',
  'maixpy_dock',
  'maixpy_yahboom',
  'maixpy_cube'
])

async function selectDevice (device: string) {
  await window.api.invoke('krux:store:set', {
    from: 'SelectDevice', 
    key: 'device',
    value: device
  })
  await back()
}

async function back () {
  await window.api.invoke('krux:change:page', { page: 'Main' })
}
</script>
