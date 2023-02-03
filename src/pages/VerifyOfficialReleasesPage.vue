<template>
  <v-layout
    align-start
    justify-start
    row
    fill-height
    id="verify-official-release-page"
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
            <v-flex
              xs8
              sm12
              id="verify-official-release-page-card-title-checking"
            >
              Verifying release {{ version.split('tag/')[1] }}...
            </v-flex>
          </v-layout>
        </v-card-title>
      </v-card>
    </v-flex>
    <v-flex
      xs12
      sm12
      v-if="verifiedHash"
    >
      <v-card>
        <v-card-title>
          <v-icon>mdi-eye-outline</v-icon>&ensp;<b id="verify-official-release-page-card-title-checked">Verified</b>
        </v-card-title>
        <v-card-subtitle>
          <v-icon>mdi-folder-pound-outline</v-icon>&ensp; <b id="verify-official-release-page-card-subtitle-sha256sum-checked">sha256sum results:</b>
        </v-card-subtitle>
        <v-card-content
          id="verify-official-release-page-card-content"
        >
          <v-card-text
            v-for="hash in hashes"
            :key="hash.name"
          >
            <b>Filename: {{ hash.name }}</b> <br/>
            <v-chip class="ma-2" color="primary" text-color="white">
              {{ hash.value }}
            </v-chip>
          </v-card-text>
        </v-card-content>
        <v-card-subtitle v-id="verifiedSign">
          <v-icon>mdi-draw-pen</v-icon>&ensp;<b id="verify-official-release-page-card-subtitle-sig-checked">Openssl signature check:</b>
        </v-card-subtitle>
        <v-card-content>
          <v-flex v-if="!verifiedSign">
            <v-progress-circular
              color="green"
              indeterminate
            />
          </v-flex>
          <v-flex v-else>
            <v-card-text>
              Command: 
              <div
                class="console-openssl"
                id="verify-official-release-page-console-command"
              >
                $> {{ sign_cmd }}
              </div>
            </v-card-text>
            <v-card-text>
              Result:
                <v-chip
                  class="ma-2"
                  color="primary"
                  text-color="white"
                  id="verify-official-release-page-chip-sig-result"
                >
                  {{ signed }}
                </v-chip>
            </v-card-text>
          </v-flex>
        </v-card-content>
        <v-card-actions>
          <v-card-text>
            <b>WARN: You will need to unzip this release before flash.</b>
          </v-card-text>
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

        // TODO fix this ugly hack
        // in windows, if user already downloaded .zip binary
        // the `value` can be an Array with length > 2
        // and we need that the `value` to be an Array with length === 2
        this.hashes = [value[0], value[1]]
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
        setTimeout(async () => {
          const v = value.split('tag/')[1]
          await window.KruxInstaller.hash.verify(
            `${v}/krux-${v}.zip`,
            `${v}/krux-${v}.zip.sha256.txt`
          ) 
        }, 1000)
      }
    },
    async hashes (value) {
      if (value.length == 2) { 
        setTimeout(async () => {
          const v = this.version.split('tag/')[1]
          await window.KruxInstaller.signature.verify({ 
            bin: `${v}/krux-${v}.zip`,
            pem: `main/selfcustody.pem`,
            sig: `${v}/krux-${v}.zip.sig`,
          })
        }, 1000)
      }
    },
    async signed (value) {
      if (value !== '') {
        setTimeout(async () => {
          await window.KruxInstaller.signature_command.get()
        }, 1000)
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
