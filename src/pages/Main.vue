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
      <v-row>
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
import { computed } from 'vue'

const props = defineProps<{
  version: string,
  device: string,
  ktool: string
}>()


/**
 * Computed variables 
 */
const device = computed(() => {
  return props.device === 'Select device' ? props.device : `Device: ${props.device}`
})

const myVersion = computed(() => {
  return props.version === 'Select version' ? props.version : `Version: ${props.version}`
})


const flash = computed(() => {
  return props.device === 'Select device' ? 'Flash' : `Flash with ${props.ktool}`
})

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
</script>