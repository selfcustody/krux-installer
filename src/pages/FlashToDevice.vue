<template>
  <v-item-group>
    <v-container>
      <v-row>
        <v-col>
          <v-item>
            <v-card
              variant="outlined"
            >
              <v-card-title > {{ !done ? 'Flashing...' : 'Do not trust, verify! ' }} </v-card-title>
              <v-card-subtitle> {{ !done ? 'Do not unplug device or shutdown computer!' : 'Before quit:' }} </v-card-subtitle>
              <v-card-subtitle> {{ !done ? '' : '(1) Scroll down the output to check what happened to your device;' }} </v-card-subtitle>
              <v-card-subtitle> {{ !done ? '' : '(2) shutdown your device and unplug it' }} </v-card-subtitle>
              <v-card-text>
                <div class="console" v-html="!done ? output : allOutput" />
              </v-card-text>  
            </v-card>
          </v-item>
        </v-col>
        <v-col v-if="done">
          <v-item>
            <v-btn
              variant="outlined"
              color="green"
              @click="backToFn"
            >
              Back
            </v-btn>
          </v-item>
          <v-item>
            <v-btn
              variant="outlined"
              color="red"
              @click="exitAppFn"
            >
              Quit
            </v-btn>
          </v-item>
        </v-col>
      </v-row>
    </v-container>
  </v-item-group>
</template>

<script setup lang="ts">

import { onMounted, toRefs, ref, Ref, watch } from 'vue';

const props = defineProps<{
  output: string,
  done: boolean
}>()

const { output, done } = toRefs(props)

const allOutput: Ref<string> = ref('')

/**
  Methods
 */
async function backToFn () {
  output.value = output.value.split(' ').splice(0).join('')
  await window.api.invoke('krux:store:get', { from: 'FlashToDevice', keys: ['device', 'version', 'os', 'isMac10', 'showFlash'] })
}

async function exitAppFn () {
  await window.api.invoke('krux:quit')
}

onMounted(async function () {
  allOutput.value = allOutput.value.split(' ').splice(0).join('')
  await window.api.invoke('krux:unzip')
})

watch(output, function(newValue) {
  allOutput.value += newValue
})
</script>

<style>
.console {
  font-family: monospace;
  font-size: 10px;
  text-align: left;
  background-color: black;
  /*color: #fff;*/
  overflow-y: auto;
  width: 720px;
  height: 360px;
}
</style>
