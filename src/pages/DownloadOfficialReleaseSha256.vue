<template>
  <v-item-group>
    <v-container id="download-official-release-zip-sha256-txt-page">
      <v-row>
        <v-col>
          <v-item>
            <v-card
              variant="plain"
            >
              <v-card-title id="download-official-release-zip-sha256-txt-page-title">
                Downloading
              </v-card-title>
              <v-card-subtitle id="download-official-release-zip-sha256-txt-page-subtitle">
                {{ downloadUrl }}
              </v-card-subtitle>
              <v-card-text class="downloading" id="download-official-release-zip-sha256-txt-page-progress">
                <strong> {{ downloadProgress }} </strong>
              </v-card-text>
            </v-card>
          </v-item>
        </v-col>
      </v-row>
    </v-container>
  </v-item-group>
</template>

<script setup lang="ts">
import { computed, toRefs, onMounted } from 'vue'

const props = defineProps<{
  baseUrl: string,
  resourceFrom: string,
  resourceTo: string,
  progress: string
}>()

const { baseUrl, resourceFrom, resourceTo, progress } = toRefs(props)

const downloadUrl = computed(() => {
  return `${baseUrl.value}/${resourceFrom.value}`
})

const downloadProgress = computed(() => {
  return `${progress.value} %`
})

onMounted(async () => {
  await window.api.invoke('krux:download:resources', {
    from: 'DownloadOfficialReleaseSha256',
    baseUrl: baseUrl.value,
    resourceFrom: resourceFrom.value,
    resourceTo: resourceTo.value
  })
})
</script>