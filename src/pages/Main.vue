<template>
  <v-item-group>
    <v-container>
      <v-row>
        <v-col>
          <v-item v-slot="{ selectedClass }">
            <v-card
              variant="outlined"
              :class="selectedClass"
              @click.prevent="selectDevice"
            >
              <v-card-title>
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
              :class="selectedClass"
              @click.prevent="selectVersion"
            >
              <v-card-title>
                {{ version }}
              </v-card-title>
            </v-card>
          </v-item>
        </v-col>
      </v-row>
      <v-row v-if="showFlash">
        <v-col>
          <v-item v-slot="{ selectedClass }">
            <v-card
              variant="outlined"
              :class="selectedClass"
              @click.prevent="flashDevice"
            >
              <v-card-title>
                {{ flash }}
              </v-card-title>
            </v-card>
          </v-item>
        </v-col>
      </v-row>
    </v-container>
  </v-item-group>
</template>

<script setup lang="ts">
import { onMounted, computed, toRefs } from 'vue';

const props = defineProps<{
  version: string,
  device: string,
  os: string,
  isMac10: boolean,
  showFlash: boolean
}>()


/**
 * Computed variables 
 */
const device = computed(() => {
  return props.device === 'Select device' ? props.device : `Device: ${props.device}`
})

const version = computed(() => {
  return props.version === 'Select version' ? props.version : `Version: ${props.version}`
})

const flash = computed(() => {
  if (props.os === 'linux') {
    return 'Flash with ktool-linux'
  }
  else if (props.os === 'win32') {
    return 'Flash with ktool-win.exe'
  }
  else if (props.os === 'darwin' && !props.isMac10) {
    return 'Flash with ktool-mac'
  }
  else if (props.os === 'darwin' && props.isMac10) {
    return 'Flash with ktool-mac-10'
  }
  else {
    return 'Flash'
  }
})

/**
 *Variables
 */
const { showFlash } = toRefs(props)

/**
 * Methods
 */
async function selectDevice () {
  await window.api.invoke('krux:change:page', { page: 'SelectDevice' })
} 

async function selectVersion () {
  await window.api.invoke('krux:change:page', { page: 'GithubChecker' })
}

async function flashDevice () {
  await window.api.invoke('krux:change:page', { page: 'BeforeFlashDevice' })
}

onMounted(async function () {
// set data.value.showFlash
  if (props.device.match(/maixpy_(m5stickv|amigo_ips|amigo_tft|bit|dock)/g)) {
    if (props.version.match(/selfcustody\/.*/g)) {
      const __version__ = props.version.split('tag/')[1]
      await window.api.invoke('krux:check:resource', {
        from: `CheckShowFlash::Main`,
        baseUrl: '',
        resource: `${__version__}/krux-${__version__}.zip`
      })
    } else if (props.version.match(/odudex\/krux_binaries/g)) {
      await window.api.invoke('krux:check:resource', {
        from: `CheckShowFlash::Main`,
        baseUrl: '',
        resource: `${props.version}/main/${props.device}/firmware.bin`
      })
    }
  }
})
</script>