<template>
  <v-layout
    align-start
    justify-start
    row
    fill-height
  >
    <v-flex xs12 sm4>
      <v-card
        class="pa-5"
      >
        <v-card-title
          v-if="isChecking"
        >
          Checking...
        </v-card-title>
        <v-card-title
          v-if="!isChecking"
        >
          Choose between official or test release
        </v-card-title>
        <v-card-content
          v-if="!isChecking"
        >
          <v-select
            v-model="version"
            :items="versions"
            label="Versions"
          />
        </v-card-content>
        <v-card-actions>
          <v-btn
            v-if="version !== ''"
            @click.prevent="select"
          >
            Select
          </v-btn>
          <br/>
          <v-btn
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
  name: 'SelectVersionPage',
  data () {
    return {
      isChecking: true,
      version: '',
      versions: [],
    }
  },
  created () {
    window.kruxAPI.verify_official_releases()

    // eslint-disable-next-line no-unused-vars
    window.kruxAPI.onVerifyOfficialReleases((_event, value) => {
      value.releases.forEach((release) => {
        this.versions.push(release)
      })
      this.isChecking = this.versions.length === 0
    })
  },
  methods: {
    async select () {
      await window.kruxAPI.set_version(this.version)

      // eslint-disable-next-line no-unused-vars
      window.kruxAPI.onSetVersion((_event, data) => {
        this.$emit('onSuccess', { page: 'CheckResourcesPage' })
      })
    }
  }
}
</script>
