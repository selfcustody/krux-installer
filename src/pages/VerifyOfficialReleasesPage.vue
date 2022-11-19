<template>
  <v-layout
    align-start
    justify-start
    row
    fill-height
  >
    <v-flex
      xs12
      sm12
      v-if="!verifiedHash && !verifiedSign"
    >
      <v-card>
        <v-card-title> 
          <v-layout column wrap>
            <v-flex xs4 sm12>
              <v-progress-circular
                indeterminate
                color="green"
              />
            </v-flex>
            <v-flex xs8 sm12>
              Verifying...
            </v-flex>
          </v-layout>
        </v-card-title>
        <v-card-subtitle>
          <b>file:</b> {{ version }}.zip
        </v-card-subtitle>
      </v-card>
    </v-flex>
    <v-flex
      xs12
      sm12
      v-if="verifiedHash"
    >
      <v-card>
        <v-card-title>
          <v-icon>mdi-eye-outline</v-icon>&ensp;Verified
        </v-card-title>
        <v-card-subtitle>
          <v-icon>mdi-folder-pound-outline</v-icon>&ensp;Sha256 Sum results:
        </v-card-subtitle>
        <v-card-content>
          <v-card-text v-for="hash in hashes" :key="hash.name">
            Filename: {{ hash.name }} <br/>
            <v-chip class="ma-2" color="primary" text-color="white">
              {{ hash.value }}
            </v-chip>
          </v-card-text>
        </v-card-content>
        <v-card-subtitle v-id="verifiedSign">
          <v-icon>mdi-draw-pen</v-icon>&ensp;Openssl signature check:
        </v-card-subtitle>
        <v-card-content> 
          <v-card-text>
            Command: 
            <div class="console-openssl">
              $> {{ sign_cmd }}
            </div>
          </v-card-text>
          <v-card-text>
            Result:
              <v-chip class="ma-2" color="primary" text-color="white">
                {{ signed }}
              </v-chip>
          </v-card-text>
        </v-card-content>
        <v-card-actions>
          <v-btn
            v-if="verifiedHash && verifiedSign"
            @click.prevent="$emit('onSuccess', { page: 'UnzipOfficialReleasesPage' })"
          >
            Unzip
          </v-btn>
          <v-btn
            v-if="verifiedHash && verifiedSign"
            @click.prevent="$emit('onSuccess', { page: 'MainPage' })"
          >
            Back
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
export default {
  name: 'VerifyOfficialReleasePage',
  data () {
    return {
      version: '',
      verifiedHash: false,
      verifiedSign: false,
      hashes: [],
      signed: '',
      sign_cmd: ''
    }
  },
  async created () {
    await window.KruxInstaller.version.get()
    
    // eslint-disable-next-line no-unused-vars
    window.KruxInstaller.version.onGet(async (_event, value) => { 
      this.$nextTick(() => {
        this.version = value
      })
    })

    // eslint-disable-next-line no-unused-vars
    window.KruxInstaller.hash.onSuccess((_event, value) => { 
      this.$nextTick(() => {
        this.verifiedHash = value.length > 0
        this.hashes = value
      })
    })

    // eslint-disable-next-line no-unused-vars
    window.KruxInstaller.hash.onError((_event, value) => {
      alert(value)
      this.$emit('onSuccess', { page: 'MainPage' })
    })

    // eslint-disable-next-line no-unused-vars
    window.KruxInstaller.signature.onSuccess((_event, value) => {
      this.$nextTick(() => {
        this.verifiedSign = value.match(new RegExp('Signature Verified Successfully')) ? true : false
        this.signed = value
      })
    })

    // eslint-disable-next-line no-unused-vars
    window.KruxInstaller.signature.onError((_event, value) => {
      alert(value)
      this.$emit('onSuccess', { page: 'MainPage' })
    })

    // eslint-disable-next-line no-unused-vars
    window.KruxInstaller.signature_command.onGet((_event, value) => {
      this.$nextTick(() => {
        this.sign_cmd = value.join(' ')
      })
    })
  },
  watch: {
    async version (value) {
      if (value !== '') {
        const v = value.split('tag/')[1]
        await window.KruxInstaller.hash.verify(
          `${v}/krux-${v}.zip`,
          `${v}/krux-${v}.zip.sha256.txt`
        ) 
      }
    },
    async hashes (value) {
      if (value.length == 2) { 
        const v = this.version.split('tag/')[1]
        await window.KruxInstaller.signature.verify({ 
          bin: `${v}/krux-${v}.zip`,
          pem: `main/selfcustody.pem`,
          sig: `${v}/krux-${v}.zip.sig`,
        }) 
      }
    },
    async signed (value) {
      if (value !== '') {
        await window.KruxInstaller.signature_command.get()
      }
    }
  }
}
</script>

<style>
.console-openssl {
  font-family: monospace;
  font-size: 10px;
  text-align: left;
  background-color: black;
  color: green;
  width: 540px;
  height: 90px;
}
</style>
