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
  <div>
    <form class="space-y-4" @submit.prevent="handleSubmit">
      <div>
        <label class="text-sm font-semibold text-slate-700" for="username">账号</label>
        <input
          id="username"
          v-model="username"
          class="mt-2 w-full rounded-2xl border border-slate-200 bg-white/80 px-4 py-3 text-slate-800 shadow-inner shadow-slate-100 focus:border-slate-400 focus:outline-none"
          placeholder="admin"
          autocomplete="username"
          required
        />
      </div>
      <div>
        <label class="text-sm font-semibold text-slate-700" for="password">密码</label>
        <input
          id="password"
          v-model="password"
          type="password"
          class="mt-2 w-full rounded-2xl border border-slate-200 bg-white/80 px-4 py-3 text-slate-800 shadow-inner shadow-slate-100 focus:border-slate-400 focus:outline-none"
          placeholder="admin"
          autocomplete="current-password"
          required
        />
      </div>
      <button
        class="flex w-full items-center justify-center gap-2 rounded-2xl bg-slate-900 px-4 py-3 text-base font-semibold text-white transition hover:translate-y-[-1px] hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-70"
        type="submit"
        :disabled="state.isLoading"
      >
        <span>{{ state.isLoading ? '登录中...' : '开始登录' }}</span>
      </button>
    </form>

    <div
      v-if="state.status.message"
      class="mt-4 rounded-2xl border px-4 py-3 text-sm"
      :class="
        state.status.type === 'error'
          ? 'border-rose-200 bg-rose-50 text-rose-700'
          : state.status.type === 'success'
            ? 'border-emerald-200 bg-emerald-50 text-emerald-700'
            : 'border-slate-200 bg-slate-50 text-slate-600'
      "
    >
      {{ state.status.message }}
    </div>
  </div>
</template>
