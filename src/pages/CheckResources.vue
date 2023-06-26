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

/**
 * Props
 */
const props = defineProps<{
  message: string
}>()

/**
 * Variables
 */
const timeout: Ref<number> = ref(30)
const canvas: Ref<{ x: number, y: number }> = ref({ x: 16, y: 16})
const fontSize: Ref<string> = ref('12px')
const index: Ref<number> = ref(0)
const list: Ref<string[][]> = ref([
  [' '],
  ['Checking between selfcustody or odudex releases...'],
  [' ']
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
  await delay(4000)
  index.value += 1
  await window.api.invoke('krux:store:get', { from: 'CheckResources', keys: ['version'] })
})

</script>