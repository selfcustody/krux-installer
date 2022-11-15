<template>
  <v-layout column wrap>
    <v-flex
      v-if="error"
      xs12 sm12
    >
      <v-card class="ma-5 pa-5">
        <v-card-title>
          {{ error.message }}
        </v-card-title>
      </v-card>
    </v-flex>
    <v-flex
      v-if="!error && info.state === 'mounting'"
      xs12 sm12
    >
      <v-card class="ma-5 pa-5">
        <v-card-title>
          Waiting for administrator permissions...
        </v-card-title>
      </v-card>
    </v-flex>
    <v-flex
      v-if="!error && info.state !== 'mounting'"
      xs12
      sm12
    >
      <v-card class="ma-5 pa-5">
        <v-card-title>
          {{ action }}
        </v-card-title>
        <v-card-subtitle>
          {{ version }}
        </v-card-subtitle>
        <v-card-content>
          <v-card-text
            v-for="(val, key) in info"
            :key="key"
          >
            <b>microSD {{ key }}</b>: {{ val }}
          </v-card-text>
        </v-card-content>
        <v-card-actions>
          <v-btn
            v-if="info.state === 'umounted'"
            @click.prevent="mountSDCard"
          >
            Mount it!
          </v-btn>
          <v-btn
            v-if="info.state === 'mounted'"
            @click.prevent="set_sdcard"
          >
            Download and write
          </v-btn>
          <br/>
          <v-btn
            @click.prevent="$emit('onSuccess', { page: 'DetectSDCardPage' })"
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
  name: 'ConfirmDetectedSDCardPage',
  data () {
    return {
      action: '',
      version: '',
      infos: ['state', 'pttype', 'size', 'device', 'description', 'mountpoint'],
      info: {},
      error: null
    }
  },
  async created () {
    await window.kruxAPI.get_action()

    // eslint-disable-next-line no-unused-vars
    window.kruxAPI.onGetAction((_event, value) => {
      this.action = value
    })

    await window.kruxAPI.get_version()

    // eslint-disable-next-line no-unused-vars
    window.kruxAPI.onGetVersion((_event, value) => {
      this.version = value
    })

    await window.kruxAPI.sdcard_action({ action: 'detect' })

    // eslint-disable-next-line no-unused-vars
    window.kruxAPI.onDetectedSDCardSuccess((_event, value) => {
      this.error = null
      this.infos.forEach((e) => {
        if (value[e]) this.info[e] = value[e]
      })
    })

    // eslint-disable-next-line no-unused-vars
    window.kruxAPI.onDetectedSDCardError((_event, value) => {
      this.error = value
    })

  },
  methods: {
    async mountSDCard () {
      this.info.state = 'mounting'
      await window.kruxAPI.sdcard_action({ action: 'mount' })
        
      // eslint-disable-next-line no-unused-vars
      window.kruxAPI.onMountAction((_event, value) => {
        this.infos.forEach((e) => {
          if (value[e]) this.info[e] = value[e]
        })
      })

      // eslint-disable-next-line no-unused-vars
      window.kruxAPI.onMountActionError((_event, value) => {
        this.$emit('onError', { error: value })
      })
    },
    async set_sdcard () {
      let sdcard = ''
      if (this.info.mountpoint !== '') {
        sdcard = this.info.mountpoint
      }
      if (this.info.description !== '') {
        sdcard = this.info.description.split('(')[1]
        sdcard = sdcard.split(')')[0]
      }

      await window.kruxAPI.set_sdcard(sdcard)

      // eslint-disable-next-line no-unused-vars
      window.kruxAPI.onSetSdcard((_event, value) => {
        this.$emit('onSuccess', { page: 'DownloadPage' })
      })
    }
  }
} 
</script>
