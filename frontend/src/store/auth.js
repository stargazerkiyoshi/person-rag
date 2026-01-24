import { computed, reactive } from 'vue'

const state = reactive({
  token: localStorage.getItem('auth_token') || '',
  profile: null,
  status: { type: '', message: '' },
  isLoading: false,
})

const apiBase = import.meta.env.VITE_API_BASE || ''

const buildUrl = (path) => {
  if (!apiBase) {
    return path
  }
  return `${apiBase.replace(/\/$/, '')}${path}`
}

const isAuthed = computed(() => state.token.length > 0)

const setStatus = (type, message) => {
  state.status = { type, message }
}

const clearStatus = () => {
  state.status = { type: '', message: '' }
}

const login = async (username, password) => {
  clearStatus()
  state.isLoading = true
  try {
    const response = await fetch(buildUrl('/auth/login'), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password }),
    })

    if (!response.ok) {
      setStatus('error', '登录失败，请检查账号或密码。')
      return false
    }

    const data = await response.json()
    state.token = data.access_token || ''
    if (!state.token) {
      setStatus('error', '未获取到访问令牌。')
      return false
    }

    localStorage.setItem('auth_token', state.token)
    await loadProfile()
    return true
  } catch (error) {
    setStatus('error', '网络连接失败，请稍后重试。')
    return false
  } finally {
    state.isLoading = false
  }
}

const loadProfile = async () => {
  if (!state.token) {
    return false
  }
  state.isLoading = true
  try {
    const response = await fetch(buildUrl('/protected/me'), {
      headers: {
        Authorization: `Bearer ${state.token}`,
      },
    })

    if (!response.ok) {
      state.token = ''
      localStorage.removeItem('auth_token')
      state.profile = null
      setStatus('error', '认证失效，请重新登录。')
      return false
    }

    state.profile = await response.json()
    setStatus('success', '已获取个人信息。')
    return true
  } catch (error) {
    setStatus('error', '无法获取个人信息，请稍后重试。')
    return false
  } finally {
    state.isLoading = false
  }
}

const logout = () => {
  state.token = ''
  state.profile = null
  localStorage.removeItem('auth_token')
  setStatus('info', '已退出登录。')
}

export const useAuthStore = () => ({
  state,
  isAuthed,
  login,
  loadProfile,
  logout,
  setStatus,
  clearStatus,
})
