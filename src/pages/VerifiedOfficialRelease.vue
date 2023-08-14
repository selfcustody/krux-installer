<template>
  <v-container>
    <v-item-group>
      <v-row>
        <v-col>
          <v-card variant="text">
            <v-card-title>
              Sha256sum integrity
            </v-card-title>
          </v-card>
        </v-col>
      </v-row>
      <v-row
         v-for="(h, i) in hash"
         :key="i"
      >
        <v-col>
          <v-card variant="text">
            <v-card-text v-html="getSubtitleNameWithHash(h)" />
          </v-card>
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <v-card
            variant="text"
          >
            <v-card-title>
              Signature authenticity
            </v-card-title>
            <v-card-text class="text-justify">
              <span style="font-size: 13px; color: yellowgreen">$> {{ command }}</span>
              <br/>
              <br/>
              <span style="font-size: 13px; color: red">{{ sign }}</span> 
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <v-card
            pa-2
            variant="outlined"
            @click="backToFn"
          >
            Back
          </v-card>
        </v-col>
      </v-row>
    </v-item-group>
  </v-container>
</template>

<style>
.console {
  font-family: monospace;
  font-size: 12px;
  text-align: left;
  background-color: black;
  color: yellowgreen;
  height: 90px;
}
</style>

<script setup lang="ts">
import { onMounted,toRefs } from 'vue';


const props = defineProps<{
  hash: Record<string, string>[],
  sign: string
  command: string
}>()

const { hash, sign, command } = toRefs(props)

/**
 * Split string for groups of 2 chars
 * to facilitate manual verification
 * https://stackoverflow.com/questions/18407260/split-a-string-to-groups-of-2-chars-using-split#18419843
 */
function getSubtitleNameWithHash(toBeHash: Record<string, string>) {
  const splited = (toBeHash.value.split(/(?=(?:..)*$)/)).join(' ')
  let wrapped = ''
  if (/^.*sha256.txt$/g.test(toBeHash.name)) {
    wrapped = `Expected result from file <span style="color: yellowgreen;"> ${toBeHash.name} </span>`
  } else {
    wrapped = `Summed result of file <span style="color: yellowgreen;"> ${toBeHash.name} </span>`
  }
  return `<div style="color: white;">${wrapped}</div><div style="color: red;">${splited}</div>`
}

async function backToFn () {
  await window.api.invoke('krux:store:get', { from: 'VerifiedOfficialRelease', keys: ['device', 'version', 'os'] })
  await window.api.invoke('krux:change:page', { page: 'Main' })
}

onMounted(async () => {
  await window.api.invoke('krux:verify:releases:hash')
  await window.api.invoke('krux:store:get', { from: 'VerifiedOfficialRelease', keys: ['signature-command'] })
})
</script>