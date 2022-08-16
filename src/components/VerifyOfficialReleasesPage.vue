<template>
  <v-layout
    align-start
    justify-start
    row
    fill-height
  >
    <v-flex
      v-if="!verified"
    >
      <p>Verifying <b>{{ version }}.zip</b> sha256sum...</p>
    </v-flex>
    <v-flex
      v-if="verified"
    >
      <v-toolbar color="indigo" dark>
        <v-toolbar-title>{{ version }}</v-toolbar-title>
      </v-toolbar>
      <v-list>
        <v-list-tile
          v-for="hash in hashes"
          :key="hash.name"
          class="pa-5"
        >
          <v-list-tile-content class="my-2">
            <h4>
              Filename
            </h4>
            <p>{{ hash.name }}</p>
            <br />
            <h4>Hash</h4>
            <v-chip
              class="ma-2"
              color="orange"
              text-color="white"
            >
              {{ hash.value }}
            </v-chip>
            <v-divider></v-divider>
          </v-list-tile-content>
        </v-list-tile>
      </v-list>
      <v-btn
        color="green"
        @click.prevent="$emit('onSuccess', { page: 'MainPage' })"
      >
        It's Ok.
      </v-btn>
      <br/>
      <v-btn
        color="primary"
        @click.prevent="$emit('onSuccess', { page: 'SelectVersionPage' })"
      >
        Back.
      </v-btn>
    </v-flex>
  </v-layout>
</template>

<script>
export default {
  name: 'VerifyOfficialReleasePage',
  data () {
    return {
      version: '',
      verified: false,
      hashes: []
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
        await window.kruxAPI.verify_hash(
          `${resource}/krux-${resource}.zip`,
          `${resource}/krux-${resource}.zip.sha256.txt`
        )

        // eslint-disable-next-line no-unused-vars
        window.kruxAPI.onVerifiedHash((_event, value) => { 
          this.verified = value.length > 0
          this.hashes = value
        })
    
        // eslint-disable-next-line no-unused-vars
        window.kruxAPI.onVerifiedHashError((_event, value) => {
          this.$emit('onError', value.error)
        })
      }
    }
  }
}
</script>
