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
    window.kruxAPI.get_resources_path()

    // eslint-disable-next-line no-unused-vars
    window.kruxAPI.onGetResourcesPath(async (_event, value) => {
      this.resourcesPath = value
    })

    window.kruxAPI.get_version()

    // eslint-disable-next-line no-unused-vars
    window.kruxAPI.onGetVersion(async (_event, value) => {
      this.version = value
    })

    window.kruxAPI.get_action()

    // eslint-disable-next-line no-unused-vars
    window.kruxAPI.onGetAction(async (_event, value) => {
      this.action = value
    })
  },
  watch: {
    async version (value) {
      if (value !== '') {
        const resource = value.split('tag/')[1]
        this.currentFile = `krux-${resource}.zip`
        window.kruxAPI.unzip({
          resource: resource,
          file: this.currentFile
        })

        // eslint-disable-next-line no-unused-vars
        window.kruxAPI.onUnzipProgress((_event, value) => {
          if (this.currentFile !== value.file) {
            this.currentFile = value.file
          }
          this.progress = value.progress
        })

        // eslint-disable-next-line no-unused-vars
        window.kruxAPI.onUnzipped((_event, value) => { 
          this.unzipped = value.length > 0
          this.files = value  
        })
    
        // eslint-disable-next-line no-unused-vars
        window.kruxAPI.onUnzipError((_event, value) => {
          this.$emit('onError', value)
        })
      }
    }
  }
}
</script>
