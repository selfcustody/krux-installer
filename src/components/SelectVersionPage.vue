<template>
  <v-layout
    align-start
    justify-start
    row
    fill-height
  >
    <v-flex v-if="isChecking">
      Checking...
    </v-flex>
    <v-flex
      v-if="!isChecking"
      xs12
      align="justify"
    >
      <p>Choose between oficial realeases (selfcustody/krux) and test binaries (odudex/krux_binaries).</p>
      <br/>
      <v-select
        v-model="version"
        :items="versions"
        label="versions"
      />
      <br/>
      <v-btn
        v-if="version !== ''"
        color="green"
        @click.prevent="select"
      >
        Download krux {{ version }}
      </v-btn>
      <br/>
      <v-btn
        color="primary"
        @click.prevent="$emit('onSuccess', { page: 'MainPage' })"
      >
        Back
      </v-btn>
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
    select () {
      window.kruxAPI.set_version(this.version)

      // eslint-disable-next-line no-unused-vars
      window.kruxAPI.onSetVersion((_event, value) => {
        if (this.version === 'odudex/krux_binaries') {
          this.$emit('onSuccess', { page: 'DownloadTestBinariesPage' })
        } else {
          this.$emit('onSuccess', { page: 'DownloadOfficialReleasePage' })
        }
      })
    }
  }
}
</script>
