<template>
  <v-item-group>
    <v-container>
      <v-row>
        <v-col>
          <v-item>
            <AsciiMorph
              :list="list"
              :index="index"
              :canvas="canvas"
              :timeout="timeout"
              :fontSize="fontSize"
            />
          </v-item>
        </v-col>
      </v-row>
    </v-container>
  </v-item-group>
</template>

<script setup lang="ts">
import { Ref, onMounted, ref } from 'vue'
import { AsciiMorph } from 'vue-asciimorph';

const index: Ref<number> = ref(0)
const timeout: Ref<number> = ref(30)
const canvas: Ref<{ x: number, y: number }> = ref({ x: 16, y: 16})
const fontSize: Ref<string> = ref('12px')
const list: Ref<string[][]> = ref([
  [
    " "
  ],
  [
    "Checking if public key certificate file is already downloaded..."
  ],
  [
    " "
  ]
])

/**
 * Methods
 */
async function delay (t: number) {
  await new Promise(function (resolve) {
    setTimeout(resolve, t)
  })
}

onMounted(async () => {
  index.value += 1
  await delay(1000)
  await window.api.invoke('krux:store:get', { from: 'CheckResourcesOfficialReleasePem', keys: ['version'] })
})
</script>