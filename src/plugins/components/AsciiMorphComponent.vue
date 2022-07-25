<template>
  <pre class="__asciimorph__" :data-uuid="id"> </pre>
</template>

<script>
import AsciiMorph from './asciiMorph.js'
import { uuid } from 'vue-uuid'

export default {
  name: 'AsciiMorph',
  props: ['ascii', 'x', 'y'],
  data: function () {
    return {
      id: uuid.v1(),
      art: null
    }
  },
  mounted () {
    const el = document.querySelector(`pre.__asciimorph__[data-uuid='${this.id}']`)
    AsciiMorph(el, { x: this.x, y: this.y })
    AsciiMorph.render(this.ascii)
  }
}
</script>
