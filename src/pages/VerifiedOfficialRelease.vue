<template>
  <v-container>
    <v-item-group>
      <v-row>
        <v-col>
          <v-card
            variant="plain"
          >
            <v-card-title>
              Succesfully Verified
            </v-card-title>
          </v-card>
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <v-card
            variant="plain"
          >
            <v-card-subtitle>
              Sha256 sum verification hash
            </v-card-subtitle>
          </v-card>
        </v-col>
      </v-row>
      <v-row
         v-for="(h, i) in hash"
         :key="i"
      >
        <v-col>
          <v-card
            variant="plain"
          >
            <v-card-subtitle>
              {{ h.name }} 
            </v-card-subtitle>
            <v-card-text style="color: yellowgreen;">
              {{ split2chars(h.value) }}
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <v-card
            variant="plain"
          >
            <v-card-subtitle>
              Openssl verification command
            </v-card-subtitle>
            <v-card-text style="color: yellowgreen;">
              $> {{ command }} 
            </v-card-text>
            <v-card-text style="color: yellowgreen;">
              Output: {{ sign }} 
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <v-card
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
function split2chars(str: string): string {
  return (str.split(/(?=(?:..)*$)/)).join(' ')
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