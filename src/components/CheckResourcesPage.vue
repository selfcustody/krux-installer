<template>
  <v-layout>
    Proxy page... 
  </v-layout>
</template>

<script>
export default {
  name: 'CheckResourcesPage',
  /**
   * If user selected:
   * - a version: change the button 'version' with the selected string
   * - a device: change the button 'flash' with the selected string
   * - a firmware: change the button 'firmware' with the selected string
   */
  async created () {
    await window.kruxAPI.get_version()
    
    // eslint-disable-next-line no-unused-vars
    window.kruxAPI.onGetVersion((_event, value) => {
      const regexp_selfcustody = /selfcustody\/.*/g
      const regexp_odudex = /odudex\/.*/g

      if (value.match(regexp_selfcustody)) {
        this.$emit('onSuccess', { page: 'DownloadOfficialReleasePage' })
      } else if (value.match(regexp_odudex)) {
        this.$emit('onSuccess', { page: 'DownloadTestFirmwarePage' })
      } else {
        this.$emit('onError', { error: new Error(`Invalid action '${value}'`) })
      }
    })
  }
}
</script>
