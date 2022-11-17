<template>
  <pre class="__asciimorph__"> </pre>
</template>

<script>
import AsciiMorph from './asciiMorph.js'

export default {
  name: 'AsciiMorph',
  props: ['ascii', 'x', 'y'],
  data: function () {
    return {
      art: null
    }
  },
  mounted () {
    const el = document.querySelector('pre.__asciimorph__')
    AsciiMorph(el, { x: this.x, y: this.y })
    AsciiMorph.render(this.ascii)
  }
}
</script>
