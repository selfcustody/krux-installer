<template>
  <v-layout
    align-start
    justify-start
    row
    fill-height
  >
    <v-flex xs12>
      <v-card flat>
        <v-card-title>
          Checking...
        </v-card-title>
      </v-card>
    </v-flex>
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
    await window.KruxInstaller.version.get()
    
    // eslint-disable-next-line no-unused-vars
    window.KruxInstaller.version.onGet(async (_event, value) => {
      const regexp_selfcustody = /selfcustody\/.*/g
      const regexp_odudex = /odudex\/.*/g

      if (value.match(regexp_selfcustody)) {
        this.$emit('onSuccess', { page: 'CheckResourcesOfficialReleasePage' })
      } else if (value.match(regexp_odudex)) {
        this.$emit('onSuccess', { page: 'CheckResourcesTestFirmwarePage' })
      } else {
        this.$emit('onError', { error: new Error(`Invalid action '${value}'`) })
      }
    })
  }
}
</script>
