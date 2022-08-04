<template>
  <v-container>
    <v-row align="justify">
      <v-col
        cols="32"
        sm12
      >
        <v-layout column wrap>
          <v-flex v-if="sdcard.error">
            <p>No SDCard detected.</p>
            <br/>
            <p>Click in the button below, insert your SDCard and try again</p>
            <br/>
            <v-btn
              color="green"
              @click.prevent="mountSDCard"
            >
              Try again
            </v-btn>
            <br/>
            <v-btn
              color="primary"
              @click.prevent="$emit('onBack', 'detect_sdcard')"
            >
              Back
            </v-btn>
          </v-flex>
          <v-flex v-if="!sdcard.error"> 
            <p> We detected a{{ sdcard.state === 'unmounted' ? 'n' : '' }}  <b>{{ sdcard.state }} {{ sdcard.fstype }} {{ sdcard.size }} card at {{ sdcard.device }}</b></p>
            <br/>
            <div v-if="sdcard.state === 'unmounted'">
              <p>
                Click in the button below to mount it
              </p>
              <br/>
              <v-btn
                color="green"
                @click.prevent="mountSDCard"
              >
                Mount it!
              </v-btn>
              <br/>
              <v-btn
                color="primary"
                @click.prevent="$emit('onBack', 'detect_sdcard')"
              >
                Back
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
