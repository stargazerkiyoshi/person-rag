<script setup>
import { computed, ref } from 'vue'
import { useAgentStore } from '../store/agent'

const { state, sendTask, clearConversation } = useAgentStore()
const input = ref('')

const canSend = computed(() => input.value.trim().length > 0 && !state.isLoading)

const handleSend = async () => {
  const task = input.value.trim()
  if (!task || state.isLoading) {
    return
  }
  input.value = ''
  await sendTask(task)
}
</script>

<template>
  <section class="space-y-6">
    <header class="flex flex-wrap items-center justify-between gap-3">
      <div>
        <p class="text-sm uppercase tracking-[0.3em] text-slate-400">Agent</p>
        <h2 class="mt-2 font-display text-2xl font-semibold text-slate-900">智能体多轮对话</h2>
      </div>
      <a-button type="outline" shape="round" @click="clearConversation">清空会话</a-button>
    </header>

    <div class="space-y-4">
      <a-card
        v-for="message in state.messages"
        :key="message.id"
        :bordered="false"
        class="shadow-sm"
      >
        <a-space class="text-xs uppercase tracking-[0.24em] text-slate-400" align="center">
          <span>{{ message.role === 'user' ? '用户' : '智能体' }}</span>
          <span>{{ new Date(message.createdAt).toLocaleString() }}</span>
        </a-space>
        <a-typography-paragraph class="mt-3" :type="message.isError ? 'danger' : 'secondary'">
          {{ message.content }}
        </a-typography-paragraph>

        <a-card v-if="message.sources?.length" class="mt-4" :bordered="false">
          <p class="font-semibold text-slate-800">来源</p>
          <ul class="mt-2 space-y-1 text-sm text-slate-600">
            <li v-for="(source, index) in message.sources" :key="`${message.id}-source-${index}`">
              {{ source }}
            </li>
          </ul>
        </a-card>

        <a-card v-if="message.trace?.length" class="mt-4" :bordered="false">
          <p class="font-semibold text-slate-800">执行轨迹</p>
          <ul class="mt-2 space-y-2 text-sm text-slate-600">
            <li v-for="(step, index) in message.trace" :key="`${message.id}-trace-${index}`">
              <a-space>
                <span class="font-semibold text-slate-700">{{ step.step }}</span>
                <a-tag size="small" color="gray">{{ step.status }}</a-tag>
              </a-space>
              <div class="mt-1 text-slate-500">{{ step.detail }}</div>
            </li>
          </ul>
        </a-card>

        <a-card v-if="message.actions?.length" class="mt-4" :bordered="false">
          <p class="font-semibold text-slate-800">动作结果</p>
          <ul class="mt-2 space-y-2 text-sm text-slate-600">
            <li v-for="(action, index) in message.actions" :key="`${message.id}-action-${index}`">
              <a-space>
                <span class="font-semibold text-slate-700">{{ action.name }}</span>
                <a-tag size="small" color="gray">{{ action.status }}</a-tag>
              </a-space>
              <div class="mt-1 text-slate-500">{{ action.detail }}</div>
            </li>
          </ul>
        </a-card>
      </a-card>

      <a-empty v-if="!state.messages.length" description="还没有对话记录，输入任务开始和智能体沟通吧。" />
    </div>

    <form class="space-y-3" @submit.prevent="handleSend">
      <label class="block text-sm font-semibold text-slate-700">任务输入</label>
      <a-textarea
        v-model="input"
        :auto-size="{ minRows: 4, maxRows: 8 }"
        placeholder="例如：帮我整理最近的资料要点，并给出下一步行动建议。"
      />
      <div class="flex flex-wrap items-center gap-3">
        <a-button type="primary" :loading="state.isLoading" :disabled="!canSend" html-type="submit">
          {{ state.isLoading ? '处理中...' : '发送任务' }}
        </a-button>
        <a-alert v-if="state.status.message" :type="state.status.type || 'error'" show-icon>
          {{ state.status.message }}
        </a-alert>
      </div>
    </form>
  </section>
</template>
