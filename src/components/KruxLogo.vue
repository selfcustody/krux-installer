<template>
  <v-container>
    <v-row>
      <v-col
        class="pa-4 mx-auto my-auto"
      >
        <AsciiMorph :ascii="krux" x=16 y=16 />
      </v-col>
    </v-row>
    <v-row class="text-center">
      <v-col class="mb-4">
        <h1 class="display-2 font-weight-bold mb-3">
          {{ title }}
        </h1>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'KruxLogo',
  data () {
    return {
      title: 'Krux Installer',
      krux: [ 
        "     ██        ",
        "     ██        ",
        "     ██        ",
        "   ██████      ", 
        "     ██        ",
        "     ██  ██    ",
        "     ██ ██     ", 
        "     ████      ",
        "     ██ ██     ",
        "     ██  ██    ",
        "     ██   ██   "
      ]
    }
  }
}
</script>
