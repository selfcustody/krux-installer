<template>
  <v-item-group>
    <v-container>
      <v-row>
        <v-col>
          <v-item>
            <v-card
              variant="outlined"
            >
              <v-card-title v-if="!done">Flashing...</v-card-title>
              <v-card-title v-if="done && !error">Flashed</v-card-title> 
              <v-card-title v-if="done && error">Error</v-card-title>
              <v-card-subtitle v-if="!done">Do not unplug device or shutdown computer!</v-card-subtitle>
              <v-card-subtitle v-if="done && !error">Done</v-card-subtitle>
              <v-card-subtitle v-if="done && error">Something wrong occured</v-card-subtitle>
              <v-card-text>
                <div class="console" v-html="output" />
              </v-card-text>  
              <v-card-actions
                @click="backToFn"
              >
                Back
              </v-card-actions>
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
  done: boolean,
  error: boolean
}>()

const tmpOutput: Ref<string> = ref('');
const { output, done, error } = toRefs(props)


/**
  Methods
 */
async function backToFn () {
  await window.api.invoke('krux:store:get', { from: 'FlashToDevice', keys: ['device', 'version', 'os', 'isMac10', 'showFlash'] })
}

onMounted(async function () {
  await window.api.invoke('krux:flash') 
})

watch(output, function(newValue) {
  if (!done) {
    tmpOutput.value += newValue
  }
})
</script>

<style>
.console {
  font-family: monospace;
  font-size: 10px;
  text-align: left;
  background-color: black;
  color: #fff;
  overflow-y: auto;
  width: 390px;
  height: 360px;
}
</style>
