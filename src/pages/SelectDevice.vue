<template>
  <v-item-group>
    <v-container>
      <v-row v-for="(device, i) in devices" :key="i">
        <v-col>
          <v-item v-slot="{ selectedClass }">
            <v-card
              variant="outlined"
              :class="[selectedClass]"
              @click.prevent="selectDevice(device)"
              :id="`select-device-${device}-button`"
            >
              <v-card-title
                :id="`select-device-${device}-title`"
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
              id="select-device-back-button"
            >
              <v-card-title
                id="select-device-back-title"
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
  'maixpy_amigo_ips',
  'maixpy_amigo_tft',
  'maixpy_bit',
  'maixpy_dock'
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