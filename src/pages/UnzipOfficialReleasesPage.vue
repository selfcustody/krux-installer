<template>
  <v-layout
    align-start
    justify-start
    row
    fill-height
  >
    <v-flex
      xs12
      v-if="!unzipped"
    >
      <v-card flat>
        <v-card-title>
          Unzipping...
        </v-card-title>
        <v-card-subtitle>
          <b>file:</b> {{ currentFile }}
        </v-card-subtitle>
        <v-card-actions>
          <v-progress-linear
            v-model="progress"
            height="25"
            color="blue-grey"
          >
            <strong>{{ progress }}%</strong>
          </v-progress-linear>
        </v-card-actions>
      </v-card>
    </v-flex>
    <v-flex
      xs12
      v-if="unzipped"
    >
      <v-card flat class="ma-2 pa-2">
        <v-card-title>
          Extracted files
        </v-card-title>
        <v-card-subtitle>
          Relative to: {{ resourcesPath }}
        </v-card-subtitle>
        <v-card-content>
          <v-card-text>
            <div
              v-for="(file, i) in files"
              :key="i"
              class="text--primary"
            >
              {{ file }}
            </div>
          </v-card-text>
        </v-card-content>
        <v-card-actions>
          <v-btn @click.prevent="$emit('onSuccess', { page: 'MainPage' })">
            Done
          </v-btn>
          <v-btn @click.prevent="$emit('onSuccess', { page: 'SelectVersionPage' })">
            Back.
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
export default {
  name: 'UnzipOfficialReleasePage',
  data () {
    return {
      resourcesPath: '',
      progress: 0,
      version: '',
      action: '',
      unzipped: false,
      currentFile: '',
      files: [],
    }
  },
  async created () {
    window.KruxInstaller.resourcesPath.get()

    // eslint-disable-next-line no-unused-vars
    window.KruxInstaller.resourcesPath.onGet((_event, value) => {
      this.$nextTick(() => {
        this.resourcesPath = value
      })
    })

    // eslint-disable-next-line no-unused-vars
    window.KruxInstaller.version.onGet((_event, value) => {
      this.$nextTick(() => {
        this.version = value
      })
    })

    // eslint-disable-next-line no-unused-vars
    window.KruxInstaller.unzip.onData((_event, value) => {
      this.$nextTick(() => {
        if (this.currentFile !== value.file) {
          this.currentFile = value.file
        }
        this.progress = value.progress
      })
    })

    // eslint-disable-next-line no-unused-vars
    window.KruxInstaller.unzip.onSuccess((_event, value) => { 
      this.$nextTick(() => {
        this.unzipped = value.length > 0
        this.files = value  
      })
    })

    // eslint-disable-next-line no-unused-vars
    window.KruxInstaller.unzip.onError((_event, value) => {
      this.$emit('onError', value)
    })
  },
  watch: {
    async resourcesPath (value) {
      if (value !== '') {
        await window.KruxInstaller.version.get()
      }
    },
    async version (value) {
      if (value !== '') {
        const v = value.split('tag/')[1]
        this.currentFile = `krux-${v}.zip`
        await window.KruxInstaller.unzip.resource({
          resource: v,
          file: this.currentFile
        })
      }
    }
  }
}
</script>
