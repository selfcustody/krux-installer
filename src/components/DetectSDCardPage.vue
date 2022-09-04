<template>
  <v-layout row wrap>
    <v-flex xs12 sm12>
      <v-container fluid>
        <v-row>
          <v-col
            cols="12"
          >
            <v-alert
              v-model="alert"
              border="left"
              close-text="Close Alert"
              type="info"
              dismissible
              outlined
            >
              <p>Update firmware to SDCard is required when you intend to update a newly krux firmware.</p>
              <p><b>It's imperative that SDCard is formatted to FAT32 filesystem.</b></p>
              <p>If it's not formatted, close this program and format it to FAT32</p>
              <p>Then we will mount it (administrator privileges will be required), and we will use the selected version of firmware.</p>
            </v-alert>
            <v-card xs12 sm12>
              <v-card-actions>
                <v-btn @click.prevent="$emit('onSuccess', { page: 'ConfirmDetectedSDCardPage' })">
                  Start
                </v-btn>
                <v-btn @click.prevent="$emit('onSuccess', { page: 'MainPage' })">
                  Back
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
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
