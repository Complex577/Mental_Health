// admin/main.js

import './assets/main.css'
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { createPinia } from 'pinia'
import { initCsrf } from './services/initCsrf'

initCsrf().then(() => {
  const app = createApp(App)
  app.use(router)
  app.use(createPinia())
  app.mount('#app')
})
