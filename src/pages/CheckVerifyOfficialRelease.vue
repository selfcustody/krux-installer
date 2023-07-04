<template>
  <v-container>
    <v-row>
      <v-col>
        <AsciiMorph
          :list="list"
          :index="index"
          :canvas="canvas"
          :timeout="timeout"
          :fontSize="fontSize"
        />
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { onMounted, Ref, ref } from 'vue'
import { AsciiMorph  } from 'vue-asciimorph'

/**
 * Variables
 */
const index: Ref<number> = ref(0)
const timeout: Ref<number> = ref(30)
const canvas: Ref<{ x: number, y: number }> = ref({ x: 16, y: 16})
const fontSize: Ref<string> = ref('12px')

// https://gist.github.com/lxynox/05850487e633c51fc863a9ff1bd022a3
const list: Ref<string[][]> = ref([
  [ " " ],
  [ 
    "        :.:'' ,,xiW,\"4x, ''       ",
    "        :  ,dWWWXXXXi,4WX,         ",
    "        ' dWWWXXX7\"     `X,       ",
    "        lWWWXX7   __   _ X         ",
    "        :WWWXX7 ,xXX7' \"^^X       ",
    "        lWWWX7, _.+,, _.+.,        ",
    "        :WWW7,. `^\"-\" ,^-'       ",
    "        WW\",X:        X,          ",
    "        \"7^^Xl.    _(_x7'         ",
    "        l ( :X:       __ _         ",
    "        `. \" XX  ,xxWWWWX7        ",
    "          )X- \"\" 4X\" .___.      ",
    "        ,W X     :Xi  _,,_         ",
    "        WW X      4XiyXWWXd        ",
    "        \"\" ,,      4XWWWWXX      ",
    "        , R7X,       \"^447^       ",
    "        R, \"4RXk,      _, ,       ",
    "        TWk  \"4RXXi,   X',x       ",
    "        lTWk,  \"4RRR7' 4 XH       ",
    "        :lWWWk,  ^\"     `4        ",
    "        ::TTXWWi,_  Xll :..        ",
    "                                   ",
    " verifying sha256sum and signature " 
  ],
  [ " " ]
])

/**
 * Methods
 */
 async function delay (t: number) {
  await new Promise(function (resolve) {
    setTimeout(resolve, t)
  })
}

onMounted(async function() {
  index.value += 1
  await delay(1000)
  await window.api.invoke('krux:store:get', {
    from: 'CheckVerifyOfficialRelease',
    keys: ['version']
  })
  await delay(4000)
  index.value += 1
})
</script>