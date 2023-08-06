<template>
  <v-container>
    <v-row>
      <v-col
        class="pa-4 mx-auto my-auto"
        color="white"
      >
        <AsciiMorph
          :list="list"
          :canvas="canvas"
          :index="index"
          :timeout="timeout"
          :fontSize="fontSize"
          id="krux-installer-logo"
        />
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { Ref, ref, onMounted, toRefs } from 'vue'
import { AsciiMorph  } from 'vue-asciimorph'
import delay from '../utils/delay'

const index: Ref<number> = ref(0)
const timeout: Ref<number> = ref(25)
const canvas: Ref<{ x: number, y: number }> = ref({ x: 16, y: 16})
const fontSize: Ref<string> = ref('18px')
const list: Ref<string[][]> = ref([
  [
    "                    "
  ],
  [ 
    "       ██           ",
    "       ██           ",
    "       ██           ",
    "     ██████         ",
    "       ██           ",
    "       ██  ██       ",
    "       ██ ██        ",
    "       ████         ",
    "       ██ ██        ",
    "       ██  ██       ",
    "       ██   ██      ",
    "                    ",
    "   KRUX INSTALLER   "
  ],
  [
    " "
  ]
])

onMounted(async function () {
  await delay(500)
  index.value += 1
  await delay(2000)
  index.value += 1
  await window.api.invoke('krux:store:get', { from: 'KruxInstallerLogo', keys: ['device', 'version', 'os', 'isMac10'] })
})
</script>
