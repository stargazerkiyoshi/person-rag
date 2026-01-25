import { reactive } from 'vue'
import client from '../api/client'

const state = reactive({
  messages: [],
  status: { type: '', message: '' },
  isLoading: false,
  sessionId: '',
})

const setStatus = (type, message) => {
  state.status = { type, message }
}

const clearStatus = () => {
  state.status = { type: '', message: '' }
}

const _pushMessage = (message) => {
  state.messages.push({
    id: `${Date.now()}-${Math.random().toString(16).slice(2)}`,
    createdAt: new Date().toISOString(),
    ...message,
  })
}

const sendTask = async (task) => {
  clearStatus()
  _pushMessage({ role: 'user', content: task })
  state.isLoading = true
  try {
    const response = await client.post('/agent', {
      task,
      session_id: state.sessionId || null,
    })

    if (response.status !== 200) {
      let errorMessage = '智能体请求失败，请稍后重试。'
      if (response.data?.detail) {
        errorMessage = response.data.detail
      }
      setStatus('error', errorMessage)
      _pushMessage({ role: 'agent', content: errorMessage, isError: true })
      return false
    }

    const data = response.data
    if (data.session_id) {
      state.sessionId = data.session_id
    }
    _pushMessage({
      role: 'agent',
      content: data.result,
      sources: data.sources || [],
      trace: data.trace || [],
      actions: data.actions || [],
    })
    return true
  } catch (error) {
    let message = '网络连接失败，请稍后重试。'
    if (error?.response) {
      message = `请求失败（状态码 ${error.response.status}）。`
      if (error.response.data?.detail) {
        message = error.response.data.detail
      }
    }
    setStatus('error', message)
    _pushMessage({ role: 'agent', content: message, isError: true })
    return false
  } finally {
    state.isLoading = false
  }
}

const clearConversation = () => {
  state.messages = []
  state.sessionId = ''
  clearStatus()
}

export const useAgentStore = () => ({
  state,
  sendTask,
  clearConversation,
})
