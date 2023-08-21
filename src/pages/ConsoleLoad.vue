<template>
  <v-container>
    <div v-for="(msg, i) in list_msg" :key="i">
      <AsciiMorph 
        :list="msg"
        :canvas="canvas"
        :index="indexes[i]"
        :timeout="timeout"
        :fontSize="fontSize"
        :id="toDashes(messages[i])"
      />
    </div>
  </v-container>
</template>

<script setup lang="ts">
import { AsciiMorph } from 'vue-asciimorph';
import { Ref, ref, toRefs, computed} from 'vue';

const timeout: Ref<number> = ref(10)
const canvas: Ref<{ x: number, y: number }> = ref({ x: 64, y: 5})
const fontSize: Ref<string> = ref('12px')
  
const props = defineProps<{
  messages: string[],
  indexes: number[]
}>()

const { messages, indexes } = toRefs(props)

const list_msg = computed(function () {
  if (messages === undefined) {
    return [
      [[' '], ['wait...'], [' ']]
    ]
  } else {
    return messages.value.map(function (val) {
      return [[' '], [val], [' ']]
    })
  }
})

function toDashes(msg: string) {
  let tag = msg.split(' ').map(function(str) {
    return str.toLowerCase()
  }).join('-')
  
  // unix need to replace / to -
  tag = tag.replace(/\//g, '-')
  
  // general replace of . to -
  tag = tag.replace(/\./g, '-')
  
  // windows need to replace \ to -
  tag = tag.replace(/\\/g, '-')
  
  console.log(tag)
  return tag
}
</script>