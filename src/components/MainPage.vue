<template>
  <v-container>
    <v-row
      v-for="(description,i) in descriptions"
      :key="i"
      class="text-justify"
    >
      <v-col> 
        <p class="subheading font-weight-regular">
          {{ description }} 
        </p>
      </v-col>
    </v-row>
    <br/>
    <v-row class="text-center">
      <v-col class="mb-4">
        <v-btn
          color="primary"
          @click.prevent="$emit('changePage', 'detect_device')"
        >
          Flash to device
        </v-btn>
      </v-col>
    </v-row>
    <v-row class="text-center">
      <v-col class="mb-4">
        <v-btn
          color="primary"
          @click.prevent="$emit('changePage', 'detect_sdcard')"
        >
          Update firmware to SDCard
        </v-btn>
      </v-col>
    </v-row>
    <v-row class="text-center">
      <v-col class="mb-4">
        <v-btn
          color="primary"
          @click.prevent="$emit('changePage', 'build_from_source')"
        >
          Build from source
        </v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'MainPage',
  data () {
    return {
      descriptions: [
        'Krux is an open-source DIY hardware signer for Bitcoin that can sign for multisignature and single-key wallets.',
        'It is a low-cost airgapped device built from off-the-shelf parts that communicates with wallet software via QR codes and wipes its memory after every session.',
        'Krux Installer is a GUI tool to simplify the flash, installation or build process that a user would be do in command line interfaces.'
        ]
    }
  }
}
</script>
