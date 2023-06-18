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
        />
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { Ref, ref, onMounted } from 'vue'
import { AsciiMorph  } from 'vue-asciimorph'

const index: Ref<number> = ref(0)
const timeout: Ref<number> = ref(30)
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
    "   LOADING DATA     "
  ],
  [
    "  VERIFYING OPENSSL "
  ],
  [
    "                    "
  ]
])

async function delay (t: number) {
  await new Promise(function (resolve) {
    setTimeout(resolve, t)
  })
}

onMounted(async function () {
  await delay(1000)
  index.value += 1
  await delay(3000)
  index.value += 1
  await delay(100)
  await window.api.invoke('krux:store:get', { from: 'KruxInstallerLogo', keys: ['device', 'version', 'os', 'isMac10'] })
  await delay(1000)
  index.value += 1
  await window.api.invoke('krux:verify:openssl', { from: 'KruxInstallerLogo' })
  await delay(1000)
  index.value += 1
  await delay(100)
  await window.api.invoke('krux:change:page', { page: 'Main' })
})
</script>