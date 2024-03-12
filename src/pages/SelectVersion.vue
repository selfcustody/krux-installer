<template>
  <v-item-group id="select-version-page">
    <v-container>
      <v-row v-for="(version, i) in versions" :key="i">
        <v-col>
          <v-item v-slot="{ selectedClass }">
            <v-card
              variant="outlined"
              :class="[selectedClass]"
              @click="select(version)"
              :id="`select-version-page-${ transformVersion(version) }-button`"
            >
              <v-card-title :id="`select-version-page-${ transformVersion(version) }-text`"> {{ version }}</v-card-title>
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
              <v-card-title id="select-version-page-back-text">
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
import { toRefs } from 'vue'

const props = defineProps<{
  versions: string[]
}>()

const { versions } = toRefs(props)

/**
 * Functions
 */
async function back() {
  await window.api.invoke('krux:store:get', { from: 'Back::SelectVersion', keys: ['device', 'version', 'os', 'isMac10'] })
}

async function select(version: string) {
  await window.api.invoke('krux:store:set', { from: 'SelectVersion', key: 'version', value: version })
}

function transformVersion (version: string): string {
  return version.replace(/[\/\_\.]/g, '-')
}

</script>
