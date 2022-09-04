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
      <p>Verifying <b>{{ version }}.zip</b>...</p>
    </v-flex>
    <v-flex
      xs12
      sm12
      v-if="verifiedHash"
    >
      <v-container>
        <v-row>
          <v-col cols="12">
            <v-card class="ma-5 pa-5">
              <v-card-title>
                Verify Sha256sum and signature results
              </v-card-title>
              <v-card-content>
                <v-card-text
                  v-for="hash in hashes"
                  :key="hash.name"
                >
                  Filename: {{ hash.name }}
                  <v-chip
                    class="ma-2"
                    color="primary"
                    text-color="white"
                  >
                    {{ hash.value }}
                  </v-chip>
                </v-card-text>
                <v-card-text
                  v-if="verifiedSign"
                >
                  Signature check
                  <v-chip
                    class="ma-2"
                    color="primary"
                    text-color="white"
                  >
                    {{ signed }}
                  </v-chip>
                </v-card-text>
              </v-card-content>
              <v-card-actions>
                <v-btn
                  v-if="verifiedHash && verifiedSign"
                  @click.prevent="$emit('onSuccess', { page: 'UnzipOfficialReleasesPage' })"
                >
                  It's Ok. Unzip it!
                </v-btn>
                <v-btn
                  v-if="verifiedHash && verifiedSign"
                  @click.prevent="$emit('onSuccess', { page: 'SelectVersionPage' })"
                >
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
  name: 'VerifyOfficialReleasePage',
  data () {
    return {
      version: '',
      verifiedHash: false,
      verifiedSign: false,
      hashes: [],
      signed: ''
    }
  },
  async created () {
    await window.kruxAPI.get_version()
    
    // eslint-disable-next-line no-unused-vars
    window.kruxAPI.onGetVersion(async (_event, value) => { 
      this.version = value
    })
  },
  watch: {
    async version (value) {
      if (value !== '') {
        const resource = value.split('tag/')[1]
        window.kruxAPI.verify_hash(
          `${resource}/krux-${resource}.zip`,
          `${resource}/krux-${resource}.zip.sha256.txt`
        )

        // eslint-disable-next-line no-unused-vars
        window.kruxAPI.onVerifiedHash((_event, value) => { 
          this.verifiedHash = value.length > 0
          this.hashes = value
        })
    
        // eslint-disable-next-line no-unused-vars
        window.kruxAPI.onVerifiedHashError((_event, value) => {
          this.$emit('onError', value.error)
        })
      }
    },
    async hashes (value) {
      if (value.length == 2) { 
        const resource = this.version.split('tag/')[1]
        window.kruxAPI.verify_signature({ 
          bin: `${resource}/krux-${resource}.zip`,
          pem: `main/selfcustody.pem`,
          sig: `${resource}/krux-${resource}.zip.sig`,
        })

        // eslint-disable-next-line no-unused-vars
        window.kruxAPI.onVerifiedSign((_event, value) => {
          console.log(value)
          this.verifiedSign = value.match(new RegExp('Signature Verified Successfully')) ? true : false
          this.signed = value
        })
    
        // eslint-disable-next-line no-unused-vars
        window.kruxAPI.onVerifiedSignError((_event, value) => {
          this.$emit('onError', value.error)
        })
      }
    }
  }
}
</script>
