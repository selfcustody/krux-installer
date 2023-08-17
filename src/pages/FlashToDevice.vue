<template>
  <v-item-group>
    <v-container>
      <v-row>
        <v-col>
          <v-item>
            <v-card
              variant="outlined"
            >
              <v-card-title > {{ !done ? 'Flashing...' : 'Done' }} </v-card-title>
              <v-card-subtitle> {{ !done ? 'Do not unplug device or shutdown computer!' : '' }} </v-card-subtitle>
              <v-card-text>
                <div class="console" v-html="allOutput" />
              </v-card-text>  
            </v-card>
          </v-item>
        </v-col>
        <v-col v-if="done">
          <v-item>
            <v-card
              variant="outlined"
              @click="backToFn"
            >
              Back
            </v-card>
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
