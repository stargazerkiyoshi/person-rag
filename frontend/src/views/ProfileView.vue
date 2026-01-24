<script setup>
import { computed } from 'vue'
import { useAuthStore } from '../store/auth'

const { state, loadProfile } = useAuthStore()

const tokenPreview = computed(() => {
  if (!state.token) {
    return ''
  }
  if (state.token.length < 12) {
    return state.token
  }
  return `${state.token.slice(0, 24)}...${state.token.slice(-6)}`
})
</script>

<template>
  <div class="space-y-4">
    <div class="rounded-2xl border border-slate-200 bg-white px-4 py-3">
      <p class="text-xs uppercase tracking-[0.3em] text-slate-400">User</p>
      <p class="mt-2 text-lg font-semibold text-slate-900">
        <span v-if="state.profile">{{ state.profile.user }}</span>
        <span v-else-if="state.isLoading">加载中...</span>
        <span v-else>未获取</span>
      </p>
    </div>
    <div class="rounded-2xl border border-slate-200 bg-white px-4 py-3">
      <p class="text-xs uppercase tracking-[0.3em] text-slate-400">Token</p>
      <p class="mt-2 text-sm text-slate-600">
        {{ tokenPreview || '未保存' }}
      </p>
    </div>

    <button
      class="flex w-full items-center justify-center gap-2 rounded-2xl border border-slate-900 px-4 py-3 text-base font-semibold text-slate-900 transition hover:bg-slate-900 hover:text-white disabled:cursor-not-allowed disabled:opacity-70"
      type="button"
      @click="loadProfile"
      :disabled="state.isLoading"
    >
      {{ state.isLoading ? '刷新中...' : '刷新个人信息' }}
    </button>

    <div
      v-if="state.status.message"
      class="rounded-2xl border px-4 py-3 text-sm"
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
