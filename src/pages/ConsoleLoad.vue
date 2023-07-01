<template>
  <v-container>
    <div v-for="(msg, i) in list_msg" :key="i">
      <AsciiMorph 
        :list="msg"
        :canvas="canvas"
        :index="indexes[i]"
        :timeout="timeout"
        :fontSize="fontSize"
      />
    </div>
  </v-container>
</template>

<script setup lang="ts">
import { AsciiMorph  } from 'vue-asciimorph';
import { Ref, ref, toRefs, computed} from 'vue';

const timeout: Ref<number> = ref(10)
const canvas: Ref<{ x: number, y: number }> = ref({ x: 32, y: 6})
const fontSize: Ref<string> = ref('12px')
  
const props = defineProps<{
  messages: string[],
  indexes: number[]
}>()

const { messages, indexes } = toRefs(props)

const list_msg = computed(function () {
  return messages.value.map(function (val) {
    return [[' '], [val]]
  })
})

</script>

<!--
<style>
.console {
  font-family: monospace;
  font-size: 10px;
  text-align: left;
  background-color: black;
  color: #fff;
  overflow-y: auto;
  width: 600px;
  height: 600px;
}
</style>
-->