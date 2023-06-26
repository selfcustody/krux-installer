<template>
  <v-container >
    <v-row>
      <v-col>
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

interface ErrorMessage {
  name: string;
  message: string;
  stack: string[];
}

/**
 * Variables
 */
const index: Ref<number> = ref(0)
const timeout: Ref<number> = ref(30)
const canvas: Ref<{ x: number, y: number }> = ref({ x: 16, y: 16})
const fontSize: Ref<string> = ref('12px')

// https://gist.github.com/lxynox/05850487e633c51fc863a9ff1bd022a3
let list: Ref<string[][]> = ref([
  [
    "                                  "
  ],
  [ 
    "       MMM.           .MMM        ",
    "       MMMMMMMMMMMMMMMMMMM        ",
    "       MMMMMMMMMMMMMMMMMMM        ",  
    "      MMMMMMMMMMMMMMMMMMMMM       ",
    "     MMMMMMMMMMMMMMMMMMMMMMM      ",
    "    MMMMMMMMMMMMMMMMMMMMMMMMM     ",
    "    MMMM::- -:::::::- -::MMMM     ",
    "     MM~:~ 00~:::::~ 00~:~MM      ",
    ".. MMMMM::.00:::+:::.00::MMMMM .. ",
    "      .MM::::: ._. :::::MM.       ",
    "         MMMM;:::::;MMMM          ",
    "  -MM        MMMMMMM              ",
    "  ^  M+     MMMMMMMMM             ",
    "      MMMMMMM MM MM MM            ",
    "           MM MM MM MM            ",
    "           MM MM MM MM            ",
    "        .~~MM~MM~MM~MM~~.         ",
    "     ~~~~MM:~MM~~~MM~:MM~~~~      ",
    "    ~~~~~~==~==~~~==~==~~~~~~     ",
    "     ~~~~~~==~==~==~==~~~~~~      ",
    "         :~==~==~==~==~~          ",
    " Checking latest release on github"
  ],
  [
    "                                  "
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
  await delay(4000)
  await window.api.invoke('krux:verify:releases:fetch', { from: 'GithubChecker' })
  index.value += 1
  await delay(4000)
})
</script>