import { createApp } from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import asciimorph from './plugins/asciimorph'
import { loadFonts } from './plugins/webfontloader'

loadFonts()

const app = createApp(App)

app.use(vuetify)
app.use(asciimorph)
app.mount('#app')
