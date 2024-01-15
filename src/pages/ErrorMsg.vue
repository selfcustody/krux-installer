<template>
  <v-layout>
    <v-flex xs12 sm6 offset-sm3>
      <v-card
        variant="plain"
        flat
      >
        <v-card-text w>
          <AsciiMorph
            :list="list"
            :canvas="{ x: 6, y: 6 }"
            :index="index"
            :timeout="30"
            fontSize="10px"
          />
        </v-card-text>
        <v-card-actions class="justify-center">
          <v-btn
            variant="outlined"
            color="green"
            @click="backToFn"
          >
            Back
          </v-btn>
          <v-btn
            variant="outlined"
            color="red"
            @click="exitAppFn"
          >
            Quit
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script setup lang="ts">
import { toRefs, ref, type Ref, onMounted } from 'vue'
import { AsciiMorph } from 'vue-asciimorph'

/**
 * Allowed props
 */
const props = defineProps<{
  name: string,
  message: string,
  stack: string,
  backTo: string
}>()

/**
 * Variables
 */
const { name, message, stack, backTo } = toRefs(props)
const index: Ref<number> = ref(0)
const list: Ref<string[][]> = ref([
  [" "],
  [`${stack.value}`],
  [" "]
])

/**
 * Methods
 */
async function backToFn () {
  index.value += 1
  await delay(50)
  await window.api.invoke('krux:store:get', { from: 'ErrorMsg', keys: ['device', 'version', 'os', 'isMac10'] })
  await window.api.invoke('krux:change:page', { page: backTo.value })
}


async function exitAppFn () {
  await window.api.invoke('krux:quit')
}

/**
 * Methods
 */
async function delay (t: number) {
  await new Promise(function (resolve) {
    setTimeout(resolve, t)
  })
}

onMounted(async function (){
  delay(50)
  index.value += 1
})
</script>
