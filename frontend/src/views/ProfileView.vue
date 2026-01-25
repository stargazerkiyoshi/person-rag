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
    <a-card :bordered="false">
      <p class="text-xs uppercase tracking-[0.3em] text-slate-400">用户</p>
      <p class="mt-2 text-lg font-semibold text-slate-900">
        <span v-if="state.profile">{{ state.profile.user }}</span>
        <span v-else-if="state.isLoading">加载中...</span>
        <span v-else>未获取</span>
      </p>
    </a-card>

    <a-card :bordered="false">
      <p class="text-xs uppercase tracking-[0.3em] text-slate-400">Token</p>
      <p class="mt-2 text-sm text-slate-600">
        {{ tokenPreview || '未保存' }}
      </p>
    </a-card>

    <a-button type="primary" long size="large" :loading="state.isLoading" @click="loadProfile">
      {{ state.isLoading ? '刷新中...' : '刷新个人信息' }}
    </a-button>

    <a-alert v-if="state.status.message" :type="state.status.type || 'info'" show-icon :closable="false">
      {{ state.status.message }}
    </a-alert>
  </div>
</template>
