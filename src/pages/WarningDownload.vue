<template>
  <v-card flat variant="plain">
    <v-card-subtitle>
      {{ resourceTo }}
    </v-card-subtitle>
    <v-card-subtitle> Already downloaded </v-card-subtitle>
    <v-card-text>
      Click <span style="color: green;">Proceed</span>
      to continue with the downloaded version or 
      <span style="color: yellow;">Download the file again.</span>
    </v-card-text>
    <v-card-actions class="justify-center">
      <v-btn
        variant="text"
        color="green"
        @click="proceedToFn"
      >
        Proceed
      </v-btn>
      <v-btn
        variant="text"
        color="yellow"
        @click="downloadToFn"
      >
        Download the file again
      </v-btn>
      <v-btn
        variant="text"
        color="red"
        @click="backToFn"
      >
        Back
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script setup lang="ts">
import { toRefs } from 'vue'

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
const { baseUrl, resourceFrom, resourceTo, proceedTo, backTo} = toRefs(props)

/**
 * Methods
 */
async function proceedToFn () {
  await window.api.invoke('krux:change:page', { page: proceedTo.value })
}

async function downloadToFn () {
  await window.api.invoke('krux:check:resource', {
    from: 'WarningDownload',
    baseUrl: baseUrl.value,
    resource: resourceFrom.value
  })
}

async function backToFn () {
  await window.api.invoke('krux:change:page', { page: backTo.value })
}
</script>