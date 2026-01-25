<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../store/auth'

const { state, login } = useAuthStore()
const router = useRouter()

const username = ref('')
const password = ref('')

const handleSubmit = async () => {
  const ok = await login(username.value, password.value)
  if (ok) {
    password.value = ''
    router.push('/me')
  }
}
</script>

<template>
  <div class="space-y-4">
    <div>
      <label class="text-sm font-semibold text-slate-700" for="username">账号</label>
      <a-input
        id="username"
        v-model="username"
        placeholder="admin"
        allow-clear
        size="large"
        class="mt-2"
      />
    </div>
    <div>
      <label class="text-sm font-semibold text-slate-700" for="password">密码</label>
      <a-input-password
        id="password"
        v-model="password"
        placeholder="admin"
        allow-clear
        size="large"
        class="mt-2"
      />
    </div>
    <a-button type="primary" long size="large" :loading="state.isLoading" @click="handleSubmit">
      {{ state.isLoading ? '登录中...' : '开始登录' }}
    </a-button>

    <a-alert v-if="state.status.message" :type="state.status.type || 'info'" show-icon :closable="false">
      {{ state.status.message }}
    </a-alert>
  </div>
</template>
