<template>
  <v-container>
    <v-row align="justify">
      <v-col
        cols="32"
        sm12
      >
        <v-layout column wrap>
          <v-flex> 
            <p> With your aid, we detected a <b>{{ sdcard.state }} {{ sdcard.size }} {{ sdcard.type}} card at {{ sdcard.path }}</b></p>
            <br/>
            <p
              v-if="sdcard.state === 'unmounted'"
            >
              We need to mount it. Click in the button below to mount it
            </p>
            <br/>
            <v-btn
              v-if="sdcard.state === 'unmounted'"
              color="primary"
              @click.prevent="mountSDCard"
            >
              Mount the {{ sdcard.size }} {{ sdcard.type }} card at {{ sdcard.path }}
            </v-btn>
          </v-flex>
        </v-layout>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'ConfirmDetectedSDCardPage',
  props: {
    sdcard: {
      type: String,
      required: true
    }
  },
  methods: {
    mountSDCard () {
      console.log('Not implemented')
    }
  }
} 
</script>
