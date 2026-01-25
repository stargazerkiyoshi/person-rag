import { createApp } from 'vue'
import ArcoVue from '@arco-design/web-vue'
import '@arco-design/web-vue/dist/arco.css'
import App from './App.vue'
import router from './router'
import { loadRuntimeConfig } from './config'
import './style.css'

const bootstrap = async () => {
  await loadRuntimeConfig()
  createApp(App).use(router).use(ArcoVue).mount('#app')
}

bootstrap()
