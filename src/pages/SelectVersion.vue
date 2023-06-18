<template>
  <v-item-group>
    <v-container>
      <v-row v-for="(version, i) in versions" :key="i">
        <v-col>
          <v-item v-slot="{ selectedClass }">
            <v-card
              variant="outlined"
              :class="[selectedClass]"
              @click="select(version)"
            >
              <v-card-title> {{ version }}</v-card-title>
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
            >
              <v-card-title>
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
import { onMounted, toRefs } from 'vue'

const props = defineProps<{
  versions: string[]
}>()

const { versions } = toRefs(props)
/**
 * Functions
 */
async function back() {
  await window.api.invoke('krux:store:get', { from: 'SelectVersion', keys: ['device', 'version', 'os', 'isMac10'] })
  await window.api.invoke('krux:change:page', { page: 'Main' })
}

async function select(version: string) {
  await window.api.invoke('krux:store:set', { key: 'version', value: version })
  await window.api.invoke('krux:change:page', { page: 'CheckResources' })
}

</script>