<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from './store/auth'

const route = useRoute()
const router = useRouter()
const { state, isAuthed, logout } = useAuthStore()

const statusTone = computed(() => {
  if (state.status.type === 'error') return 'bg-rose-500'
  if (state.status.type === 'success') return 'bg-emerald-500'
  if (state.status.type === 'info') return 'bg-sky-500'
  return 'bg-slate-500'
})

const navigateTo = () => {
  if (isAuthed.value) {
    router.push('/me')
  } else {
    router.push('/login')
  }
}
</script>

<template>
  <div class="page">
    <div class="orb orb-orange"></div>
    <div class="orb orb-teal"></div>

    <header class="mx-auto w-full max-w-6xl px-6 pt-12">
      <div class="reveal">
        <p class="text-sm uppercase tracking-[0.3em] text-slate-500">Person RAG</p>
        <h1 class="mt-4 font-display text-4xl font-semibold text-slate-900 md:text-5xl">
          个人知识库的最小化 Web 入口
        </h1>
        <p class="mt-4 max-w-2xl text-lg text-slate-600">
          用清爽的界面完成登录与身份验证，快速确认 API 工作状态，之后再扩展你的知识库体验。
        </p>
        <div class="mt-6 flex flex-wrap items-center gap-3">
          <button
            class="rounded-full border border-slate-200 px-4 py-2 text-sm font-semibold text-slate-600 hover:border-slate-300 hover:text-slate-900"
            type="button"
            @click="navigateTo"
          >
            {{ isAuthed ? '前往个人信息' : '去登录' }}
          </button>
          <span v-if="isAuthed" class="text-sm text-slate-500">
            当前路由：{{ route.path }}
          </span>
        </div>
      </div>
    </header>

    <main class="mx-auto grid w-full max-w-6xl gap-8 px-6 pb-16 pt-10 lg:grid-cols-[1.1fr,0.9fr]">
      <section class="space-y-6">
        <div
          class="reveal reveal-delay-1 rounded-3xl border border-white/50 bg-white/70 p-6 shadow-xl shadow-slate-200/60 backdrop-blur"
        >
          <h2 class="font-display text-xl font-semibold text-slate-900">当前能力</h2>
          <ul class="mt-4 space-y-3 text-slate-600">
            <li class="flex items-start gap-3">
              <span class="mt-1 h-2 w-2 rounded-full bg-amber-500"></span>
              登录后自动保存 JWT，刷新页面也能保持会话。
            </li>
            <li class="flex items-start gap-3">
              <span class="mt-1 h-2 w-2 rounded-full bg-emerald-500"></span>
              支持登录页与个人信息页路由切换。
            </li>
            <li class="flex items-start gap-3">
              <span class="mt-1 h-2 w-2 rounded-full bg-sky-500"></span>
              支持设置 `VITE_API_BASE` 自定义后端地址。
            </li>
          </ul>
        </div>

        <div class="reveal reveal-delay-2 rounded-3xl border border-slate-200 bg-slate-900 px-6 py-5 text-slate-100 shadow-lg">
          <p class="text-sm uppercase tracking-[0.35em] text-slate-400">状态</p>
          <p class="mt-3 text-lg font-semibold">
            {{ isAuthed ? '已登录' : '未登录' }}
          </p>
          <p class="mt-2 flex items-center gap-2 text-sm text-slate-300">
            <span class="h-2 w-2 rounded-full" :class="statusTone"></span>
            {{ state.status.message || '准备就绪，等待你的操作。' }}
          </p>
        </div>
      </section>

      <section
        class="reveal reveal-delay-3 rounded-3xl border border-white/60 bg-white/80 p-6 shadow-2xl shadow-slate-200/70 backdrop-blur"
      >
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm uppercase tracking-[0.3em] text-slate-400">Access</p>
            <h2 class="mt-2 font-display text-2xl font-semibold text-slate-900">
              {{ isAuthed ? '账户信息' : '登录' }}
            </h2>
          </div>
          <button
            v-if="isAuthed"
            class="rounded-full border border-slate-200 px-4 py-2 text-sm font-semibold text-slate-600 hover:border-slate-300 hover:text-slate-900"
            type="button"
            @click="logout"
          >
            退出
          </button>
        </div>

        <router-view class="mt-6" />
      </section>
    </main>
  </div>
</template>

<style scoped lang="less">
.page {
  position: relative;
  min-height: 100vh;
  overflow: hidden;
}

.orb {
  position: absolute;
  width: 420px;
  height: 420px;
  border-radius: 999px;
  filter: blur(0px);
  opacity: 0.35;
  z-index: 0;
}

.orb-orange {
  top: -120px;
  left: -80px;
  background: radial-gradient(circle at 30% 30%, #ffcf9f, #f18f63 60%, transparent 70%);
  animation: float 12s ease-in-out infinite;
}

.orb-teal {
  bottom: -140px;
  right: -120px;
  background: radial-gradient(circle at 30% 30%, #9ee6df, #2bb3a3 60%, transparent 70%);
  animation: float 14s ease-in-out infinite;
}

@keyframes float {
  0%,
  100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(18px);
  }
}
</style>
