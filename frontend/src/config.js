let runtimeConfig = {}

export const loadRuntimeConfig = async () => {
  try {
    const response = await fetch('/app-config.json', { cache: 'no-store' })
    if (response.ok) {
      runtimeConfig = await response.json()
    }
  } catch (error) {
    runtimeConfig = {}
  }
  return runtimeConfig
}

export const getApiBase = () => {
  return runtimeConfig.apiBase || import.meta.env.VITE_API_BASE || ''
}
