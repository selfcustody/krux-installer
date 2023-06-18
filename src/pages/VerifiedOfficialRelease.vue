<template>
  <v-card flat variant="plain">
    <v-card-title>Succesfully Verified</v-card-title>
    <v-card-actions>
      <v-item-group>
        <v-card-subtitle>Sha256 sum verification hash</v-card-subtitle>
        <v-container>
          <v-row>
            <v-col v-for="(h, i) in hash">
              <v-card-item>
                <div class="console"> {{ h.name }} </div>
                <div class="console-result"> {{ split2chars(h.value) }}</div>
              </v-card-item>
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              <v-card-subtitle>Openssl verification command </v-card-subtitle>
              <v-card-item>
                <div class="console"> $> {{ command }} </div>
                <div class="console-result"> {{ sign }} </div>
                <v-btn
                  variant="text"
                  color="red"
                  @click="backToFn"
                >
                  Back to main menu
                </v-btn>
              </v-card-item>
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              
            </v-col>
          </v-row>
        </v-container>
      </v-item-group>
    </v-card-actions>
  </v-card>
</template>

<style>
.console {
  font-family: monospace;
  font-size: 12px;
  text-align: left;
  background-color: black;
  color: green;
  height: 90px;
}
.console-result {
  font-family: monospace;
  font-size: 12px;
  text-align: left;
  background-color: black;
  color: white;
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