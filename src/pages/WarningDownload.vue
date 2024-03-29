<template>
  <v-item-group id="warning-download-page">
    <v-container>
      <v-row>
        <v-col>
          <v-overlay
            v-model="details"
            contained
            width="100%" 
            height="100%"
            id="warning-already-downloaded-overlay"
          >
            <!-- 'text' | 'flat' | 'elevated' | 'tonal' | 'outlined' | 'plain'-->
            <v-card color="black">
              <v-card-title color="white" id="warning-already-downloaded-overlay-title">Resource details</v-card-title>
              <v-card-subtitle id="warning-already-downloaded-overlay-subtitle">{{ resourceFrom }} </v-card-subtitle>
              <v-card-text color="white" id="warning-already-downloaded-overlay-text-remote"><b>Remote:</b><br/> {{ baseUrl}}/{{ resourceFrom }}</v-card-text>
              <v-card-text color="white" id="warning-already-downloaded-overlay-text-local"><b>Local:</b><br/> {{ resourceTo }}</v-card-text>
              <v-card-text color="white" id="warning-already-downloaded-overlay-text-whatdo"><b>Description:</b><br/> {{ whatDo }}</v-card-text>
              <v-card-actions color="white" class="align-center justify-center">
                <v-item v-slot="{ selectedClass }">
                  <v-card
                    variant="outlined"
                    :class="[selectedClass]"
                    @click="closeDetails"
                    id="warning-already-downloaded-overlay-button-close"
                  >
                    <v-card-title>Close</v-card-title>
                  </v-card>
                </v-item>
              </v-card-actions>
            </v-card>
          </v-overlay>
        </v-col>
      </v-row>
      <v-row>
        <v-col id="warning-already-downloaded-text">
          <span style="color: yellowgreen;">{{ resourceName }} </span> already downloaded 
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <v-item v-slot="{ selectedClass }">
            <v-card
              variant="outlined"
              :class="[selectedClass]"
              @click="proceedToFn"
              id="warning-download-proceed-button"
            >
              <v-card-title id="warning-download-proceed-button-text">Proceed with current file</v-card-title>
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
              @click="downloadToFn"
              id="warning-download-again-button"
            >
              <v-card-title id="warning-download-again-button-text">Download it again</v-card-title>
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
              @click="showDetails"
              id="warning-download-show-details-button"
            >
              <v-card-title id="warning-download-show-details-button-text">Show details</v-card-title>
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
              @click="backToFn"
              id="warning-download-back-button"
            >
              <v-card-title id="warning-download-back-button-text">Back</v-card-title>
            </v-card>
          </v-item>
        </v-col>
      </v-row>
    </v-container>
  </v-item-group>
</template>

<script setup lang="ts">
import { Ref, ref, toRefs, computed } from 'vue'

/**
 * Allowed props
 */
const props = defineProps<{
  baseUrl: string,
  resourceFrom: string,
  resourceTo: string,
  proceedTo: string,
  backTo:string
}>()

/**
 * Variables
 */
const details: Ref<boolean> = ref(false)
const { baseUrl, resourceFrom, resourceTo, proceedTo} = toRefs(props)

const resourceName = computed(function () {
  let __resourceName__ = ''
  if (resourceTo.value.match(/^.*(zip|sha256.txt|sig|pem)$/g)){
    __resourceName__ = resourceTo.value.split('krux-installer/')[1]
    
    // If fails, maybe we are in windows
    if (__resourceName__ === undefined) {
      __resourceName__ = resourceTo.value.split('krux-installer\\')[1]
    }
  } else if (resourceTo.value.match(/^.*(firmware|kboot|ktool).*$/g)) {
    __resourceName__ = resourceTo.value.split('/main/')[1]
    
    // If fails, maybe we are in windows
    if (__resourceName__ === undefined) {
      __resourceName__ = resourceTo.value.split('\\main\\')[1]
    }
  }
  return __resourceName__ 
})

const whatDo = computed(function (){
  if (resourceTo.value.match(/^.*zip$/g)){
    return 'This file is the official release with all necessary contents to flash or update krux firmware on your Kendryte K210 device, including the firmware signature that prove the firmware\'s authenticity'
  } else if (resourceTo.value.match(/^.*sha256.txt$/g)){
    return 'This file proves the integrity of previous file. It uses the sha256 algorithm to check if zip file has not be changed during download.'
  } else if (resourceTo.value.match(/^.*sig$/g)){
    return 'This file, with the public key certificate, proves the authenticity of zip file, checking if the zip file was signed by its creator.'
  } else if (resourceTo.value.match(/^.*pem$/g)){
    return 'This file, with the signature, proves the authenticity of zip file, checking if the zip file was signed by its creator.'
  } else if (resourceTo.value.match(/^.*firmware.bin$/g)) {
    return 'This file is the unsigned krux firmware used for tests.'
  } else if (resourceTo.value.match(/^.*kboot.kfpkg$/g)) {
    return 'This file is the unsigned krux kendryte bootloader used for tests.'
  } else if (resourceTo.value.match(/^.*ktool-.*$/g)) {
    return 'This file is the OS\'s specific kendryte tool to write firmware and the bootloader onto device.'
  } else {
    throw new Error(`${resourceTo} not recognized`)
  }
})

/**
 * Methods
 */
async function proceedToFn () {
  await window.api.invoke('krux:store:get', {
    from: `WarningDownload::${resourceTo.value}`,
    keys: ['device', 'version', 'os', 'isMac10']
  })
  await window.api.invoke('krux:change:page', { page: proceedTo.value })
}

async function downloadToFn () {
  await window.api.invoke('krux:check:resource', {
    from: `Again::WarningDownload::${resourceTo.value}`,
    baseUrl: baseUrl.value,
    resource: resourceFrom.value
  })
}

function showDetails () {
  details.value = true
}

function closeDetails () {
  details.value = false
}

async function backToFn () {
  await window.api.invoke('krux:store:get', {
    from: 'Back::WarningDownload',
    keys: ['device', 'version', 'os', 'isMac10']
  })
}
</script>
