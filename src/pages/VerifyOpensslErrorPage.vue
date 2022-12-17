<template>
  <v-layout
    align-start
    justify-start
    row
    fill-height
  >
    <v-flex xs12 sm4>
      <v-card flat class="ma-5 pa-5">
        <v-card-title>
          <v-icon>mdi-alert-remove-outline</v-icon>
           WARNING
        </v-card-title>
        <v-card-subtitle>
          <b>OpenSSL</b> not found on System
        </v-card-subtitle>
        <v-card-content>
          <v-card-text>
            We require that an external OpenSSL tool to be installed in your system. We support these ones delivered by:
          </v-card-text>
          <v-card-text>
            <ul>
              <li>Git-SCM GUI at <b>https://git-scm.com/download/win.</b> (RECOMENDED FOR DEVELOPERS);</li>
              <li>OpenSSL for windows at <b>https://wiki.openssl.org/index.php/Binaries</b>. Tested versions:
                <ul>
                  <li>Shining Light Productions Win64 OpenSSL v3.0.7 Light at <b>https://slproweb.com/products/Win32OpenSSL.html</b>.</li>
                </ul>
              </li>
            </ul>
          </v-card-text>
          <v-card-text>
            So, you must follow these steps:
          </v-card-text>
          <v-card-text>
            <ol>
              <li>Copy the desired link;</li>
              <li>close KruxInstaller;</li>
              <li>download OpenSSL;</li>
              <li>install OpenSSL;</li>
              <li>re-open Krux-Installer.</li>
            </ol>
          </v-card-text>
        </v-card-content>
      </v-card>
    </v-flex>
  </v-layout>
</template>