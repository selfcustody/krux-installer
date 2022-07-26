<template>
  <v-app>
    <v-main>
      <v-layout column wrap>
        <v-flex
          class="mx-auto my-auto"
        >
          <v-container>
            <v-row>
              <v-col>
                <AsciiMorph :ascii="krux" x=10 y=10 /> 
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
        </v-flex>
        <v-flex
          class="mx-auto"
          color="white"
        >
          <v-container>
            <v-row
              v-for="(desc,i) in descriptions"
              :key="i"
              class="text-justify"
            >
              <v-col> 
                <p class="subheading font-weight-regular">
                  {{ desc }} 
                </p>
              </v-col>
            </v-row>
            <br/>
            <v-row class="text-center">
              <v-col class="mb-4">
                <v-btn
                  color="primary"
                  @click.prevent='install2device'
                >
                  Install to device
                </v-btn>
              </v-col>
            </v-row>
            <v-row class="text-center">
              <v-col class="mb-4">
                <v-btn color="primary">
                  Flash to device
                </v-btn>
              </v-col>
            </v-row>
            <v-row class="text-center">
              <v-col class="mb-4">
                <v-btn color="primary">
                  Build from source
                </v-btn>
              </v-col>
            </v-row>
          </v-container>
        </v-flex>
      </v-layout>
    </v-main>
  </v-app>
</template>

<script>
export default {
  name: 'App',

  data: () => ({
    title: 'Krux Installer',
    descriptions: [
      'Krux is an open-source DIY hardware signer for Bitcoin that can sign for multisignature and single-key wallets.',
      'It is a low-cost airgapped device built from off-the-shelf parts that communicates with wallet software via QR codes and wipes its memory after every session.',
    ],
    krux: [ 
      "           ██              ",
      "           ██              ",
      "           ██              ",
      "         ██████            ", 
      "           ██              ",
      "           ██  ██          ",
      "           ██ ██           ", 
      "           ████            ",
      "           ██ ██           ",
      "           ██  ██          ",
      "           ██   ██         ", 
    ],
    x: 50,
    y: 50
  }),
  methods: {
    async install2device () {
      await window.kruxAPI.download_ktool_linux()
    }
  }
}
</script>
