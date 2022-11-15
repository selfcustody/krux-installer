<template>
  <v-layout row wrap>
    <v-flex xs12 sm12>
      <v-card class="ma-5 pa-5">
        <v-card-content>
          <v-card-text>
            <p>Update firmware to SDCard is required when you intend to update a newly krux firmware.</p>
            <br/>
            <p><b>It's imperative that SDCard is formatted to FAT32 filesystem. If it's not formatted, close this program and format it to FAT32</b></p>
            <br/>
            <p>Then put it on computer,  and we will mount it (administrator privileges will be required).</p>
          </v-card-text>
        </v-card-content>
        <v-card-actions>
          <v-btn @click.prevent="$emit('onSuccess', { page: 'ConfirmDetectedSDCardPage' })">
            Start
          </v-btn>
          <v-btn @click.prevent="$emit('onSuccess', { page: 'MainPage' })">
            Back
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
export default {
  name: 'DetectSDCardPage',
  data () {
    return {
      alert: true
    }
  }
}
</script>
