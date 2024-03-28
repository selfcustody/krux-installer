<template>
  <v-item-group id="main-page">
    <v-container>
      <v-row v-if="clickMessage !== ''">
        <v-col
          id="main-page-click-message-text"
        >
          {{ clickMessage }}
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <v-item v-slot="{ selectedClass }">
            <v-card
              variant="outlined"
              :class="selectedClass"
              @click.prevent="selectDevice"
              id="main-page-select-device-button"
            >
              <v-card-title
                id="main-page-select-device-text"
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
              :class="selectedClass"
              @click.prevent="selectVersion"
              id="main-page-select-version-button"
            >
              <v-card-title
                id="main-page-select-version-text"
              >
                {{ version }}
              </v-card-title>
            </v-card>
          </v-item>
        </v-col>
      </v-row>
      <v-row v-if="showWipe">
        <v-col>
          <v-item v-slot="{ selectedClass }">
            <v-card
              variant="outlined"
              :class="selectedClass"
              @click.prevent="wipeDevice"
              id="main-page-wipe-button"
            >
              <v-card-title
                id="main-page-wipe-text"
              >
                {{ wipe }}
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
              id="main-page-flash-button"
            >
              <v-card-title
                id="main-page-flash-text"
              >
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
  showFlash: boolean,
  showWipe: boolean,
  clickMessage: string
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

const wipe = computed(() => {
  if (props.os === 'linux') {
    return 'Wipe with ktool-linux'
  }
  else if (props.os === 'win32') {
    return 'Wipe with ktool-win.exe'
  }
  else if (props.os === 'darwin' && !props.isMac10) {
    return 'Wipe with ktool-mac'
  }
  else if (props.os === 'darwin' && props.isMac10) {
    return 'Wipe with ktool-mac-10'
  }
  else {
    return 'Wipe'
  }
})

/**
 *Variables
 */
const { showFlash, showWipe } = toRefs(props)


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
  await window.api.invoke('krux:change:page', { page: 'FlashToDevice' })
}

async function wipeDevice () {
  const message = [
    "\t\t\t\t\tWARNING: CRITICAL OPERATION",
    "",
    "You are about to initiate a FULL WIPE of this device. This operation will:",
    "",
    "- Permanently erase all saved data.",
    "- Remove the existing firmware.",
    "- Render the device non-functional until new firmware is re-flashed."
  ].join("\n")
  
  const confirmed = confirm(message)
  if (confirmed) {
    await window.api.invoke('krux:change:page', { page: 'WipeDevice' })
  }
}

onMounted(async function () {
  await window.api.invoke('krux:check:will:wipe')
  await window.api.invoke('krux:check:will:flash')
})
</script>
