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
          <b>{{ currentFile }}</b>...
        </v-card-title>
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
      <v-card flat>
        <v-card-title>Files</v-card-title>
        <v-card-text>
          <v-chip
            v-for="(file, i) in files"
            :key="i"
            class="ma-2"
            color="primary"
            text-color="white"
          >
            {{ file }}
          </v-chip>
        </v-card-text>
      </v-card>
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
  name: 'UnzipOfficialReleasePage',
  data () {
    return {
      progress: 0,
      version: '',
      unzipped: false,
      currentFile: '',
      files: [],
    }
  },
  async created () {
    window.kruxAPI.get_version()

    // eslint-disable-next-line no-unused-vars
    window.kruxAPI.onGetVersion(async (_event, value) => {
      this.version = value
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
