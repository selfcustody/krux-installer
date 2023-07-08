<template>
  <v-item-group>
    <v-container>
      <v-row>
        <v-col>
          <span style="color: yellowgreen;">{{  resourceName }} </span> already downloaded 
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <v-item v-slot="{ selectedClass }">
            <v-card
              variant="outlined"
              :class="[selectedClass]"
              @click="proceedToFn"
              >
              <v-card-title>Proceed with current file</v-card-title>
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
              >
              <v-card-title> Download it again</v-card-title>
            </v-card>
          </v-item>
        </v-col>
      </v-row>
    </v-container>
  </v-item-group>
</template>

<script setup lang="ts">
import { toRefs, computed } from 'vue'

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
const { baseUrl, resourceFrom, resourceTo, proceedTo} = toRefs(props)

const resourceName = computed(function () {
  if (resourceTo.value.match(/^.*(zip|sha256.txt|sig|pem)$/g)){
    return resourceTo.value.split('krux-installer/')[1]
  } else if (resourceTo.value.match(/^.*(firmware|kboot|ktool).*$/g)) {
    return resourceTo.value.split('/main/')[1]
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

async function backToFn () {
  await window.api.invoke('krux:store:get', {
    from: 'Back::WarningDownload',
    keys: ['device', 'version', 'os', 'isMac10']
  })
}
</script>