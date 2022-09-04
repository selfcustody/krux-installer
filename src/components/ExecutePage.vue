<template>
  <v-layout>
    Proxy page... 
  </v-layout>
</template>

<script>
export default {
  name: 'ExecutePage',
  /**
   * If user selected:
   * - a version: change the button 'version' with the selected string
   * - a device: change the button 'flash' with the selected string
   * - a firmware: change the button 'firmware' with the selected string
   */
  async created () {
    await window.kruxAPI.get_action()
    
    // eslint-disable-next-line no-unused-vars
    window.kruxAPI.onGetAction((_event, value) => {
      if (value === 'Flash firmware onto device') {
        this.$emit('onSuccess', {
          page: 'DetectDevicePage'
        })
      }
      else if (value === 'Write firmware onto microSD') {
        this.$emit('onSuccess', {
          page: 'DetectSDCardPage'
        })
      } else {
        this.$emit('onError', {
          error: new Error(`Invalid action '${value}'`)
        })
      }
    })
  }
}
</script>
