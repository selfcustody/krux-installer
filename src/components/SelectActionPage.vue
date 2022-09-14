<template>
  <v-layout
    align-start
    justify-start
    row
    fill-height
  >
    <v-flex xs12 sm4>
      <v-card class="ma-5 pa-5">
        <v-card-title>
          Choose an action
        </v-card-title>
        <v-card-content>
          <v-select
            v-model="action"
            :items="actions"
            label="Action"
          />
        </v-card-content>
        <v-card-actions>
          <v-btn
            v-if="version !== ''"
            @click.prevent="select"
          >
            Select
          </v-btn>
          <br/>
          <v-btn
            @click.prevent="$emit('onSuccess', { page: 'MainPage' })"
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
  name: 'SelectActionPage',
  data () {
    return {
      action: '',
      actions: [
        'Flash firmware onto device',
        'Write firmware onto microSD'
      ],
    }
  },
  methods: {
    select () {
      window.kruxAPI.set_action(this.action)

      // eslint-disable-next-line no-unused-vars
      window.kruxAPI.onSetAction((_event, data) => {
        this.$emit('onSuccess', { page: 'MainPage' })
      })
    }
  }
}
</script>
