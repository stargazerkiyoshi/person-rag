import { createRouter, createWebHistory } from 'vue-router'
import LoginView from './views/LoginView.vue'
import ProfileView from './views/ProfileView.vue'
import AgentView from './views/AgentView.vue'
import { useAuthStore } from './store/auth'

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: LoginView, meta: { guestOnly: true } },
  { path: '/me', component: ProfileView, meta: { requiresAuth: true } },
  { path: '/agent', component: AgentView, meta: { requiresAuth: true } },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach(async (to) => {
  const { isAuthed, loadProfile } = useAuthStore()

  if (to.meta.requiresAuth && !isAuthed.value) {
    return '/login'
  }

  if (to.meta.guestOnly && isAuthed.value) {
    return '/me'
  }

  if (to.meta.requiresAuth) {
    await loadProfile()
  }

  return true
})

export default router
