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
    <v-row
      v-for="(action, i) in actions"
      :key="i"
      class="text-center"
    >
      <v-col class="mb-4">
        <v-btn
          color="primary"
          @click.prevent="$emit('onSuccess', { page: action.page })"
        >
          {{ action.label }}
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
        ],
      actions: [
        {
          label: 'Flash to device',
          page: 'DetectDevicePage' 
        },
        {
          label: 'Update firmware to SDCard',
          page: 'DetectSDCardPage'
        }
      ]
    }
  }
}
</script>
