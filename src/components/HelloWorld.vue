<template>
  <v-container>
    <v-row class="text-center">
      <v-col cols="12">
        <v-img
          :src="require('../assets/logo.png')"
          class="my-3"
          contain
          height="200"
        />
      </v-col>

      <v-col class="mb-4">
        <h1 class="display-2 font-weight-bold mb-3">
          {{ title }}
        </h1>


        <p class="subheading font-weight-regular">
          {{ description }} 
        </p>
      </v-col>

      <v-col
        class="mb-5"
        cols="12"
      >
        <h2 class="headline font-weight-bold mb-5">
          Important Links
        </h2>

        <v-row justify="center">
          <a
            v-for="(link, i) in importantLinks"
            :key="i"
            :href="link.href"
            class="subheading mx-3"
            target="_blank"
          >
            {{ link.text }}
          </a>
        </v-row>
      </v-col>

      <v-col
        class="mb-5"
        cols="12"
      >
        <h2 class="headline font-weight-bold mb-5">
          Ecosystem
        </h2>

        <v-row justify="center">
          <a
            v-for="(eco, i) in ecosystem"
            :key="i"
            :href="eco.href"
            class="subheading mx-3"
            target="_blank"
          >
            {{ eco.text }}
          </a>
        </v-row>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>

export default {
  name: 'HelloWorld',

  data: () => ({
    title: 'Krux Installer',
    description: 'Krux is an open-source DIY hardware signer for Bitcoin that can sign for multisignature and single-key wallets. It is a low-cost airgapped device built from off-the-shelf parts that communicates with wallet software via QR codes and wipes its memory after every session.',
    ecosystem: [
      {
        text: 'krux online documentation',
        href: 'https://selfcustody.github.io/krux/'
      },
      {
        text: 'krux source code',
        href: 'https://github.com/selfcustody/krux',
      },
      {
        text: 'krux installer source code',
        href: 'https://github.com/qlrd/krux-installer',
      },
    ],
    importantLinks: [
      {
        text: 'Discussions',
        href: 'https://github.com/selfcustody/krux/discussions',
      },
      {
        text: 'Telegram Group',
        href: 'https://t.me/SC_Krux',
      }
    ],
  }),
}
</script>
