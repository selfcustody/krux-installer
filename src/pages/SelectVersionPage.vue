<template>
  <v-layout
    align-start
    justify-start
    row
    fill-height
    id="select-version-page"
  >
    <v-flex
      xs12
      sm4
    >
      <v-card
        class="pa-5"
      >
        <v-card-title
          v-if="isChecking"
          id="select-version-page-card-title-checking"
        >
          <v-layout
            column
            wrap
          >
            <v-flex xs4 sm12>
              <v-progress-circular
                indeterminate
                color="green"
              />
            </v-flex>
            <v-flex xs8 sm12>
              Checking...
            </v-flex>
          </v-layout>
        </v-card-title>
        <v-card-title
          v-if="!isChecking"
          id="select-version-page-card-title-checked"
        >
          <v-icon>mdi-cube-outline</v-icon>
          Select between <b>selfcustody</b> or <b>odudex</b> releases
        </v-card-title>
        <v-card-subtitle
          id="select-version-page-card-subtitle-official"
        >
          <b>Official</b>: selfcustody/krux/releases/tag/v*
        </v-card-subtitle>
        <v-card-subtitle
          id="select-version-page-card-subtitle-test"
        >
          <b>Test</b>: odudex/krux_binaries
        </v-card-subtitle>
        <v-card-content
          class="ma-2 pa-2"
          v-if="!isChecking"
          id='select-version-page-card-content' 
        >
          <v-select
            v-model="version"
            :items="versions"
            label="Versions"
            id="select-version-page-form-select-versions"
          />
        </v-card-content>
        <v-card-actions>
          <v-btn
            v-if="version !== ''"
            @click.prevent="select"
            id="select-version-page-form-select-versions-button"
          >
            Select
          </v-btn>
          <br/>
          <v-btn
            @click.prevent="$emit('onSuccess', { page: 'MainPage' })"
            id="select-device-page-form-select-versions-back-button"
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
    window.KruxInstaller.official_releases.fetch()

    // eslint-disable-next-line no-unused-vars
    window.KruxInstaller.official_releases.onSuccess((_event, value) => {
      value.releases.forEach((release) => {
        this.versions.push(release)
      })
      this.isChecking = this.versions.length === 0
    })

    // eslint-disable-next-line no-unused-vars
    window.KruxInstaller.official_releases.onError((_event, value) => {
      alert(value)
      this.$emit('onSuccess', { page: 'MainPage' })
    })
  },
  methods: {
    async select () {
      await window.KruxInstaller.version.set(this.version)

      // eslint-disable-next-line no-unused-vars
      window.KruxInstaller.version.onSet((_event, data) => {
        this.$emit('onSuccess', { page: 'CheckResourcesPage' })
      })
    }
  }
}
</script>
