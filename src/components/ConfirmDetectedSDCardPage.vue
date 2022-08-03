<template>
  <v-container>
    <v-row align="justify">
      <v-col
        cols="32"
        sm12
      >
        <v-layout column wrap>
          <v-flex> 
            <p> With your aid, we detected a <b>{{ sdcard.state }} {{ sdcard.size }} card at {{ sdcard.device }}</b></p>
            <br/>
            <div v-if="sdcard.state === 'unmounted'">
              <p>
                We need to mount it. Click in the button below to mount it
              </p>
              <br/>
              <v-btn
                color="primary"
                @click.prevent="mountSDCard"
              >
                Mount it!
              </v-btn>
            </div>
            <div v-if="sdcard.state === 'mounted'">
              <p>
                SDCard already mounted. Let's proceed with download
              </p>
              <br/>
              <v-btn
                color="primary"
                @click.prevent="$emit('onConfirmDetectedSDCard', sdcard)"
              >
                Download firmware!
              </v-btn>
            </div>
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
