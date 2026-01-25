import axios from 'axios'
import { getApiBase } from '../config'

const client = axios.create({
  timeout: 15000,
})

client.interceptors.request.use((config) => {
  const apiBase = getApiBase()
  if (apiBase) {
    const trimmed = apiBase.replace(/\/$/, '')
    if (config.url && config.url.startsWith('/')) {
      config.url = `${trimmed}${config.url}`
    } else {
      config.baseURL = trimmed
    }
  }
  return config
})

export default client
