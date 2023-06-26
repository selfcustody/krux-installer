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
import { Ref, ref, onMounted, toRefs } from 'vue'
import { AsciiMorph  } from 'vue-asciimorph'

const props = defineProps<{
  opensslMsg: string
}>()

const { opensslMsg } = toRefs(props)

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
    "Checking if\nopenssl exists\on the system..."
  ],
  [
    opensslMsg.value
  ],
  [
    " "
  ]
])

async function delay (t: number) {
  await new Promise(function (resolve) {
    setTimeout(resolve, t)
  })
}

onMounted(async function () {
  await delay(500)
  index.value += 1
  await delay(2000)
  index.value += 1
  await delay(3000)
  index.value += 1
  await delay(5000)
  index.value += 1
  await window.api.invoke('krux:store:get', { from: 'KruxInstallerLogo', keys: ['device', 'version', 'os', 'isMac10'] })
  await window.api.invoke('krux:change:page', { page: 'Main' })
})
</script>